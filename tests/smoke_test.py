#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from awa_vault import AWAConfig, AWAVault  # noqa


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        cfg = AWAConfig(
            mode="LOCAL",
            vault_root=str(base / "vault"),
            device_id="TEST-PC",
            environment_id="test-local",
            config_path=base / "config.json",
            cache_db=str(base / "cache.db"),
        )
        cfg.save()
        v = AWAVault(cfg)
        try:
            v.publish_environment_profile({"python":{"status":"AVAILABLE"}, "filesystem":{"status":"AVAILABLE"}})
            run = v.start_run(project_id="P1", task_family="Data-To-Insight", description="Analyze test dataset")
            rid = run["run_id"]
            v.recommend(rid, {"pattern":"data_to_insight", "steps":["python","reasoning"]})
            v.record_execution(rid, {"tool":"python", "result":"ok"})
            pending = v.pending(project_id="P1")
            check(len(pending) == 1 and pending[0]["run_id"] == rid, "pending run")
            v.close_latest(project_id="P1", outcome="FIRST_PASS_ACCEPTED")
            check(v.pending(project_id="P1") == [], "closed run should not be pending")
            v.observe_capability(resource_id="python", task_family="data-to-insight", capability="data_manipulation",
                                 assessment="EXCELLENT", confidence="HIGH", evidence_type="real_task")
            compact = v.compact()
            check(compact["ok"], "compact")
            for name in ["pending.json","recent-runs.json","environments.json","capability-view.json","manifest.json"]:
                check((base / "vault" / "index" / name).exists(), f"index {name}")
            ctx = v.query_context(task_family="DATA TO INSIGHT", capability="data-manipulation")
            check(ctx["resource_observations"], "query context observations")
        finally:
            v.close()

        # Cache must be disposable/rebuildable.
        (base / "cache.db").unlink(missing_ok=True)
        v2 = AWAVault(cfg)
        try:
            n = v2.rebuild_cache()
            check(n >= 5, "rebuild should ingest events")
            check(v2.status()["runs"] == 1, "run reconstructed")
            check(v2.pending(project_id="P1") == [], "closed state reconstructed")
        finally:
            v2.close()

    print("AWA v0.4.0 smoke test: PASS")


if __name__ == "__main__":
    main()
