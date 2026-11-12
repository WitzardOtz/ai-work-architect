#!/usr/bin/env python3
import json
import os
import subprocess
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from awa_vault import AWAConfig, AWAVault, VERSION, new_ulid  # noqa


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        vault = base / "shared" / "AWA"

        cfg_a = AWAConfig("SHARED_GOOGLE_DRIVE", str(vault), "PC-A", "antigravity-local", base/"a.json", str(base/"a.db"), "GOOGLE_DRIVE")
        cfg_b = AWAConfig("SHARED_GOOGLE_DRIVE", str(vault), "PC-B", "claude-cowork", base/"b.json", str(base/"b.db"), "GOOGLE_DRIVE")
        cfg_a.save(); cfg_b.save()

        a = AWAVault(cfg_a)
        b = AWAVault(cfg_b)
        try:
            a.publish_environment_profile({"python":{"status":"AVAILABLE"}, "subagents":{"status":"AVAILABLE"}})
            b.publish_environment_profile({"python":{"status":"AVAILABLE"}, "drive_connector":{"status":"AVAILABLE"}})
            r = a.start_run(project_id="P2", task_family="research", description="Cross-environment run")
            b.scan_new_events()
            check(len(b.pending(project_id="P2")) == 1, "second environment sees run")
            b.close_latest(project_id="P2", outcome="MINOR_CORRECTION", notes="closed in another environment")
            a.scan_new_events()
            check(a.pending(project_id="P2") == [], "first environment sees close")

            envs = a.environment_profiles()
            keys = {e["environment_key"] for e in envs}
            check("PC-A__antigravity-local" in keys and "PC-B__claude-cowork" in keys, "local availability profiles stay separate")

            # Duplicate event_id in a different file must not duplicate semantic state.
            event = a.write_event("capability.observed", task_family="research", summary="dup test", payload={
                "observation_id":"OBS1","resource_id":"model-x","environment_key":cfg_a.environment_key,
                "task_family":"research","capability":"reasoning","assessment":"STRONG","confidence":"MEDIUM",
                "evidence_type":"real_task","configuration":{},"metrics":{},"observed_at":"2026-09-26T00:00:00Z"
            })
            original = next(vault.rglob(f"{event['event_id']}__*.json"))
            dup = original.parent / f"DUPLICATE__{original.name}"
            dup.write_bytes(original.read_bytes())
            before = a.conn.execute("SELECT COUNT(*) FROM events WHERE event_id=?", (event["event_id"],)).fetchone()[0]
            a.scan_new_events()
            after = a.conn.execute("SELECT COUNT(*) FROM events WHERE event_id=?", (event["event_id"],)).fetchone()[0]
            check(before == 1 and after == 1, "event_id dedupe")

            # Readers ignore temp files.
            tmp = vault / "events" / "2026" / "09" / ".tmp-bad.json"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text("{broken", encoding="utf-8")
            a.scan_new_events()

            # Invalid close outcome rejected.
            failed = False
            try:
                a.close_run(r["run_id"], outcome="GREAT")
            except ValueError:
                failed = True
            check(failed, "invalid outcome")

            # Rewriting mutable configuration and indexes must work on Windows too.
            cfg_a.save()
            check(json.loads(cfg_a.config_path.read_text(encoding="utf-8"))["device_id"] == "PC-A", "config replacement")
            a.compact()
            event_bytes = {p: p.read_bytes() for p in vault.rglob("*.json") if "events" in p.parts}
            later = a.start_run(project_id="INDEX-REFRESH", task_family="setup-verification", description="Second compaction includes new pending run")
            a.compact()
            pending_index = json.loads((vault / "index" / "pending.json").read_text(encoding="utf-8"))
            check(any(row["run_id"] == later["run_id"] for row in pending_index), "index replacement reflects new run")
            a.close_run(later["run_id"], outcome="OUTCOME_UNKNOWN")
            a.compact()
            pending_index = json.loads((vault / "index" / "pending.json").read_text(encoding="utf-8"))
            check(not any(row["run_id"] == later["run_id"] for row in pending_index), "index replacement reflects close")
            check(all(p.read_bytes() == raw for p, raw in event_bytes.items()), "compaction leaves immutable event files unchanged")

            # New identifiers are filename-safe.
            check(new_ulid().isalnum(), "ULID safe")
        finally:
            a.close(); b.close()

    # Projection must not depend on the order in which event files arrive.
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        vault = base / "vault"
        src = AWAVault(AWAConfig(mode="LOCAL", vault_root=str(vault), device_id="PC-O", environment_id="order-test",
                                 config_path=base / "src.json", cache_db=str(base / "src.db")))
        try:
            src.publish_environment_profile({"python": {"status": "UNKNOWN"}}, last_verified="2026-01-01T00:00:00Z")
            src.publish_environment_profile({"python": {"status": "AVAILABLE"}}, last_verified="2026-02-01T00:00:00Z")
            r = src.start_run(project_id="ORDER", task_family="setup-verification", description="Order independence")
            src.recommend(r["run_id"], {"plan": "a"})
            src.record_execution(r["run_id"], {"tool": "x"})
            src.close_run(r["run_id"], outcome="MINOR_CORRECTION", notes="n")
            still_open = src.start_run(project_id="ORDER", task_family="setup-verification", description="Still open")
            expected = [dict(row) for row in src.conn.execute("SELECT * FROM run_state ORDER BY run_id")]
        finally:
            src.close()
        paths = sorted((vault / "events").rglob("*.json"))
        for label, ordering in (("reverse", list(reversed(paths))), ("closed-first", sorted(paths, key=lambda p: "run.closed" not in p.name))):
            other = AWAVault(AWAConfig(mode="LOCAL", vault_root=str(vault), device_id="PC-O", environment_id="order-test",
                                       config_path=base / f"{label}.json", cache_db=str(base / f"{label}.db")))
            try:
                other.conn.execute("DELETE FROM seen_files"); other.conn.commit()
                for path in ordering:
                    other._ingest_file(path)
                got = [dict(row) for row in other.conn.execute("SELECT * FROM run_state ORDER BY run_id")]
                check(got == expected, f"run state independent of arrival order ({label})")
                check([p["run_id"] for p in other.pending(project_id="ORDER")] == [still_open["run_id"]], f"pending after {label} ingestion")
                profile = other.environment_profiles()[0]
                check(profile["capabilities"]["python"]["status"] == "AVAILABLE", f"latest environment profile wins ({label})")
            finally:
                other.close()

    # CLI reports user errors as one line with exit code 2, never a traceback.
    cli = [sys.executable, str(SCRIPTS / "awa_cli.py")]
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        env = dict(os.environ, AWA_CONFIG_PATH=str(base / "missing" / "config.json"))
        p = subprocess.run(cli + ["status"], capture_output=True, text=True, env=env)
        check(p.returncode == 2 and "Traceback" not in p.stderr and "not initialized" in p.stderr, "uninitialized CLI error")
        p = subprocess.run(cli + ["--version"], capture_output=True, text=True, env=env)
        check(p.returncode == 0 and VERSION in p.stdout, "CLI version")
        cfg = AWAConfig(mode="LOCAL", vault_root=str(base / "vault"), device_id="PC-C", environment_id="cli-test",
                        config_path=base / "config.json", cache_db=str(base / "cache.db"))
        cfg.save()
        with_cfg = cli + ["--config", str(cfg.config_path)]
        p = subprocess.run(with_cfg + ["run-close", "R_NONE", "--outcome", "GREAT"], capture_output=True, text=True, env=env)
        check(p.returncode == 2 and "Traceback" not in p.stderr and "invalid outcome" in p.stderr, "invalid outcome CLI error")
        p = subprocess.run(with_cfg + ["probe", "--extra", "{broken"], capture_output=True, text=True, env=env)
        check(p.returncode == 2 and "Traceback" not in p.stderr and "invalid JSON" in p.stderr, "invalid JSON CLI error")
        events = list((base / "vault").rglob("events/**/*.json")) if (base / "vault").exists() else []
        check(events == [], "rejected CLI commands write no events")

    print(f"AWA v{VERSION} regression test: PASS")


if __name__ == "__main__":
    main()
