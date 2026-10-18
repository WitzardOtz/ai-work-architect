#!/usr/bin/env python3
"""AI Work Architect v0.4 persistent event vault.

Stdlib only. The canonical state is an immutable event store. A local SQLite
cache/index is disposable and can always be rebuilt from event files.

Modes:
- LOCAL: canonical event vault on this device.
- SHARED_GOOGLE_DRIVE: canonical event vault in a Google Drive-synced folder.

The same event schema can also be written by a cloud Drive adapter. Cloud
connectors should create final immutable JSON event files and never edit an
existing event.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import secrets
import shutil
import sqlite3
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

VERSION = "0.4.0"
SCHEMA_VERSION = "1.0"
CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
ALLOWED_OUTCOMES = {
    "FIRST_PASS_ACCEPTED",
    "MINOR_CORRECTION",
    "MAJOR_CORRECTION",
    "REROUTED",
    "FAILED",
    "ABANDONED",
    "OUTCOME_UNKNOWN",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def _encode_crockford(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        chars.append(CROCKFORD[value & 31])
        value >>= 5
    return "".join(reversed(chars))


def new_ulid() -> str:
    """Generate a sortable ULID-compatible 26-char identifier using stdlib only."""
    ts_ms = int(time.time() * 1000) & ((1 << 48) - 1)
    rnd = secrets.randbits(80)
    return _encode_crockford(ts_ms, 10) + _encode_crockford(rnd, 16)


def safe_slug(value: Optional[str], fallback: str = "na", max_len: int = 48) -> str:
    s = (value or "").strip()
    if not s:
        s = fallback
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-._")
    return (s or fallback)[:max_len]


def normalize_token(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip().lower()
    s = re.sub(r"[\s\-]+", "_", s)
    return re.sub(r"_+", "_", s)


def atomic_write_json(path: Path, data: Any, *, replace_existing: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / f".tmp-{new_ulid()}-{path.name}"
    raw = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with open(tmp, "x", encoding="utf-8", newline="\n") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    # Same-directory rename is atomic on normal local filesystems. Readers skip .tmp-*.
    if replace_existing:
        os.replace(tmp, path)
    else:
        os.rename(tmp, path)


def default_config_path() -> Path:
    return Path(os.path.expanduser(os.environ.get("AWA_CONFIG_PATH", "~/.ai-work-architect/config.json")))


def default_local_vault() -> Path:
    return Path(os.path.expanduser("~/.ai-work-architect/vault"))


def _cache_path_for(vault_root: Path) -> Path:
    key = hashlib.sha256(str(vault_root.resolve()).encode("utf-8")).hexdigest()[:16]
    return Path(os.path.expanduser(f"~/.ai-work-architect/cache/{key}.db"))


@dataclass
class AWAConfig:
    mode: str
    vault_root: str
    device_id: str
    environment_id: str
    config_path: Path
    cache_db: Optional[str] = None
    shared_provider: Optional[str] = None

    @property
    def environment_key(self) -> str:
        return f"{safe_slug(self.device_id)}__{safe_slug(self.environment_id)}"

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "AWAConfig":
        p = Path(path or default_config_path())
        if not p.exists():
            raise FileNotFoundError(f"AWA is not initialized. Missing config: {p}")
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls(
            mode=data["mode"],
            vault_root=data["vault_root"],
            device_id=data["device_id"],
            environment_id=data["environment_id"],
            config_path=p,
            cache_db=data.get("cache_db"),
            shared_provider=data.get("shared_provider"),
        )

    def save(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "schema_version": "0.4",
            "mode": self.mode,
            "vault_root": self.vault_root,
            "device_id": self.device_id,
            "environment_id": self.environment_id,
            "cache_db": self.cache_db,
            "shared_provider": self.shared_provider,
            "updated_at": now_iso(),
        }
        atomic_write_json(self.config_path, data, replace_existing=True)


CACHE_SCHEMA = r"""
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS seen_files (
  relpath TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  size INTEGER,
  mtime_ns INTEGER,
  ingested_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
  event_id TEXT PRIMARY KEY,
  schema_version TEXT NOT NULL,
  event_type TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  run_id TEXT,
  project_id TEXT,
  task_family TEXT,
  environment TEXT,
  device_id TEXT,
  summary TEXT,
  payload_json TEXT,
  source_relpath TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_run ON events(run_id);
CREATE INDEX IF NOT EXISTS idx_events_project ON events(project_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_time ON events(occurred_at);

CREATE TABLE IF NOT EXISTS run_state (
  run_id TEXT PRIMARY KEY,
  project_id TEXT,
  task_family TEXT,
  description TEXT,
  environment TEXT,
  device_id TEXT,
  architect_version TEXT,
  status TEXT NOT NULL DEFAULT 'OPEN',
  outcome TEXT NOT NULL DEFAULT 'PENDING',
  started_at TEXT,
  ended_at TEXT,
  recommended_json TEXT,
  actual_json TEXT,
  failure_mode TEXT,
  notes TEXT,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_run_state_status ON run_state(status);
CREATE INDEX IF NOT EXISTS idx_run_state_project ON run_state(project_id);
CREATE INDEX IF NOT EXISTS idx_run_state_family ON run_state(task_family);

CREATE TABLE IF NOT EXISTS environment_profiles (
  environment_key TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  environment_id TEXT NOT NULL,
  session_id TEXT,
  capabilities_json TEXT NOT NULL,
  last_verified TEXT NOT NULL,
  source_event_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resource_observations (
  observation_id TEXT PRIMARY KEY,
  resource_id TEXT NOT NULL,
  environment_key TEXT,
  task_family TEXT,
  capability TEXT,
  assessment TEXT,
  confidence TEXT,
  evidence_type TEXT,
  configuration_json TEXT,
  metrics_json TEXT,
  notes TEXT,
  observed_at TEXT NOT NULL,
  source_event_id TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_resource_obs_task ON resource_observations(task_family);
CREATE INDEX IF NOT EXISTS idx_resource_obs_resource ON resource_observations(resource_id);

CREATE TABLE IF NOT EXISTS generic_observations (
  observation_id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  object_id TEXT,
  environment_key TEXT,
  task_family TEXT,
  outcome TEXT,
  payload_json TEXT,
  observed_at TEXT NOT NULL,
  source_event_id TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_generic_kind ON generic_observations(kind);
"""


class AWAVault:
    def __init__(self, config: AWAConfig):
        self.config = config
        self.root = Path(os.path.expanduser(config.vault_root))
        self.events_root = self.root / "events"
        self.index_root = self.root / "index"
        self.meta_root = self.root / "meta"
        self.root.mkdir(parents=True, exist_ok=True)
        self.events_root.mkdir(parents=True, exist_ok=True)
        self.index_root.mkdir(parents=True, exist_ok=True)
        self.meta_root.mkdir(parents=True, exist_ok=True)
        cache_path = Path(os.path.expanduser(config.cache_db)) if config.cache_db else _cache_path_for(self.root)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path = cache_path
        self.conn = sqlite3.connect(str(cache_path), timeout=30)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA busy_timeout=30000")
        self.conn.executescript(CACHE_SCHEMA)
        self.conn.execute("INSERT INTO meta(key,value) VALUES('cache_schema','0.4') ON CONFLICT(key) DO UPDATE SET value=excluded.value")
        self.conn.execute("INSERT INTO meta(key,value) VALUES('vault_root',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(self.root),))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # ---------- event store ----------
    def _event_path(self, event: Dict[str, Any]) -> Path:
        dt = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
        etype = safe_slug(event["event_type"], max_len=40)
        rid = safe_slug(event.get("run_id"), "no-run", max_len=34)
        project = safe_slug(event.get("project_id"), "no-project", max_len=32)
        env = safe_slug(event.get("environment"), "unknown", max_len=28)
        filename = f"{event['event_id']}__{etype}__{rid}__{project}__{env}.json"
        return self.events_root / f"{dt.year:04d}" / f"{dt.month:02d}" / filename

    def write_event(
        self,
        event_type: str,
        *,
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
        task_family: Optional[str] = None,
        summary: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None,
        occurred_at: Optional[str] = None,
        environment: Optional[str] = None,
        device_id: Optional[str] = None,
        architect_version: str = VERSION,
    ) -> Dict[str, Any]:
        eid = event_id or new_ulid()
        event = {
            "schema_version": SCHEMA_VERSION,
            "event_id": eid,
            "occurred_at": occurred_at or now_iso(),
            "event_type": event_type,
            "architect_version": architect_version,
            "environment": environment or self.config.environment_id,
            "device_id": device_id or self.config.device_id,
            "run_id": run_id,
            "project_id": project_id,
            "task_family": normalize_token(task_family),
            "summary": (summary or "").strip()[:500],
            "payload": payload or {},
        }
        path = self._event_path(event)
        atomic_write_json(path, event)
        self._ingest_file(path)
        return event

    def _ingest_file(self, path: Path) -> Optional[Dict[str, Any]]:
        if path.name.startswith(".tmp-") or path.suffix.lower() != ".json":
            return None
        rel = str(path.relative_to(self.root)).replace("\\", "/")
        if self.conn.execute("SELECT 1 FROM seen_files WHERE relpath=?", (rel,)).fetchone():
            return None
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
        required = {"event_id", "event_type", "occurred_at", "schema_version", "payload"}
        if not required.issubset(event):
            return None
        # Drive may permit duplicate filenames/objects. event_id is the semantic dedupe key.
        if self.conn.execute("SELECT 1 FROM events WHERE event_id=?", (event["event_id"],)).fetchone():
            stat = path.stat()
            self.conn.execute(
                "INSERT OR IGNORE INTO seen_files(relpath,event_id,size,mtime_ns,ingested_at) VALUES(?,?,?,?,?)",
                (rel, event["event_id"], stat.st_size, stat.st_mtime_ns, now_iso()),
            )
            self.conn.commit()
            return event
        self.conn.execute(
            """INSERT INTO events(event_id,schema_version,event_type,occurred_at,run_id,project_id,task_family,
               environment,device_id,summary,payload_json,source_relpath) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                event["event_id"], event.get("schema_version", "1.0"), event["event_type"], event["occurred_at"],
                event.get("run_id"), event.get("project_id"), normalize_token(event.get("task_family")),
                event.get("environment"), event.get("device_id"), event.get("summary", ""),
                json.dumps(event.get("payload", {}), ensure_ascii=False, separators=(",", ":")), rel,
            ),
        )
        stat = path.stat()
        self.conn.execute(
            "INSERT INTO seen_files(relpath,event_id,size,mtime_ns,ingested_at) VALUES(?,?,?,?,?)",
            (rel, event["event_id"], stat.st_size, stat.st_mtime_ns, now_iso()),
        )
        self._project_event(event)
        self.conn.commit()
        return event

    def scan_new_events(self) -> int:
        count = 0
        if not self.events_root.exists():
            return 0
        for path in self.events_root.rglob("*.json"):
            if path.name.startswith(".tmp-"):
                continue
            before = self.conn.total_changes
            self._ingest_file(path)
            if self.conn.total_changes > before:
                count += 1
        return count

    def rebuild_cache(self) -> int:
        self.conn.close()
        try:
            self.cache_path.unlink()
        except FileNotFoundError:
            pass
        self.conn = sqlite3.connect(str(self.cache_path), timeout=30)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.executescript(CACHE_SCHEMA)
        self.conn.commit()
        return self.scan_new_events()

    def _project_event(self, event: Dict[str, Any]) -> None:
        etype = event["event_type"]
        payload = event.get("payload") or {}
        rid = event.get("run_id")
        ts = event["occurred_at"]
        if etype == "run.started" and rid:
            desc = (event.get("summary") or payload.get("description") or event.get("task_family") or event.get("project_id") or "run").strip()
            self.conn.execute(
                """INSERT INTO run_state(run_id,project_id,task_family,description,environment,device_id,architect_version,
                   status,outcome,started_at,updated_at) VALUES(?,?,?,?,?,?,?,'OPEN','PENDING',?,?)
                   ON CONFLICT(run_id) DO UPDATE SET project_id=excluded.project_id,task_family=excluded.task_family,
                   description=excluded.description,environment=excluded.environment,device_id=excluded.device_id,
                   architect_version=excluded.architect_version,updated_at=excluded.updated_at""",
                (rid, event.get("project_id"), normalize_token(event.get("task_family")), desc, event.get("environment"),
                 event.get("device_id"), event.get("architect_version"), ts, ts),
            )
        elif etype == "run.recommended" and rid:
            self.conn.execute("UPDATE run_state SET recommended_json=?,updated_at=? WHERE run_id=?", (json.dumps(payload, ensure_ascii=False, separators=(",", ":")), ts, rid))
        elif etype in {"run.execution", "run.rerouted"} and rid:
            self.conn.execute("UPDATE run_state SET actual_json=?,updated_at=? WHERE run_id=?", (json.dumps(payload, ensure_ascii=False, separators=(",", ":")), ts, rid))
        elif etype == "run.closed" and rid:
            outcome = str(payload.get("outcome", "OUTCOME_UNKNOWN")).upper()
            if outcome not in ALLOWED_OUTCOMES:
                outcome = "OUTCOME_UNKNOWN"
            self.conn.execute(
                "UPDATE run_state SET status='CLOSED',outcome=?,ended_at=?,failure_mode=?,notes=?,updated_at=? WHERE run_id=?",
                (outcome, ts, payload.get("failure_mode"), payload.get("notes"), ts, rid),
            )
        elif etype == "environment.profile_published":
            env_id = str(payload.get("environment_id") or event.get("environment") or "unknown")
            dev_id = str(payload.get("device_id") or event.get("device_id") or "unknown")
            env_key = str(payload.get("environment_key") or f"{safe_slug(dev_id)}__{safe_slug(env_id)}")
            caps = payload.get("capabilities") or {}
            self.conn.execute(
                """INSERT INTO environment_profiles(environment_key,device_id,environment_id,session_id,capabilities_json,last_verified,source_event_id)
                   VALUES(?,?,?,?,?,?,?) ON CONFLICT(environment_key) DO UPDATE SET device_id=excluded.device_id,
                   environment_id=excluded.environment_id,session_id=excluded.session_id,capabilities_json=excluded.capabilities_json,
                   last_verified=excluded.last_verified,source_event_id=excluded.source_event_id""",
                (env_key, dev_id, env_id, payload.get("session_id"), json.dumps(caps, ensure_ascii=False, separators=(",", ":")),
                 payload.get("last_verified") or ts, event["event_id"]),
            )
        elif etype == "capability.observed":
            oid = str(payload.get("observation_id") or event["event_id"])
            self.conn.execute(
                """INSERT OR REPLACE INTO resource_observations(observation_id,resource_id,environment_key,task_family,capability,
                   assessment,confidence,evidence_type,configuration_json,metrics_json,notes,observed_at,source_event_id)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (oid, payload.get("resource_id") or "unknown", payload.get("environment_key"), normalize_token(payload.get("task_family") or event.get("task_family")),
                 normalize_token(payload.get("capability")), payload.get("assessment"), payload.get("confidence"), payload.get("evidence_type"),
                 json.dumps(payload.get("configuration") or {}, ensure_ascii=False, separators=(",", ":")),
                 json.dumps(payload.get("metrics") or {}, ensure_ascii=False, separators=(",", ":")), payload.get("notes"),
                 payload.get("observed_at") or ts, event["event_id"]),
            )
        elif etype in {"skill.observed", "pattern.observed"}:
            oid = str(payload.get("observation_id") or event["event_id"])
            kind = "skill" if etype.startswith("skill") else "pattern"
            object_id = payload.get("skill_id") if kind == "skill" else payload.get("pattern_id")
            self.conn.execute(
                """INSERT OR REPLACE INTO generic_observations(observation_id,kind,object_id,environment_key,task_family,outcome,payload_json,observed_at,source_event_id)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (oid, kind, object_id, payload.get("environment_key"), normalize_token(payload.get("task_family") or event.get("task_family")),
                 payload.get("outcome"), json.dumps(payload, ensure_ascii=False, separators=(",", ":")), payload.get("observed_at") or ts, event["event_id"]),
            )

    # ---------- high-level run API ----------
    def start_run(self, *, project_id: Optional[str], task_family: Optional[str], description: str,
                  parent_run_id: Optional[str] = None) -> Dict[str, Any]:
        description = (description or "").strip()
        if not description:
            raise ValueError("description is required")
        rid = f"R_{new_ulid()}"
        payload = {"description": description}
        if parent_run_id:
            payload["parent_run_id"] = parent_run_id
        event = self.write_event("run.started", run_id=rid, project_id=project_id, task_family=task_family,
                                 summary=description, payload=payload)
        return {"run_id": rid, "event_id": event["event_id"], "status": "OPEN", "outcome": "PENDING"}

    def recommend(self, run_id: str, recommendation: Dict[str, Any], summary: str = "routing recommendation") -> Dict[str, Any]:
        return self.write_event("run.recommended", run_id=run_id, summary=summary, payload=recommendation)

    def record_execution(self, run_id: str, actual: Dict[str, Any], summary: str = "actual execution") -> Dict[str, Any]:
        return self.write_event("run.execution", run_id=run_id, summary=summary, payload=actual)

    def reroute(self, run_id: str, details: Dict[str, Any], summary: str = "run rerouted") -> Dict[str, Any]:
        return self.write_event("run.rerouted", run_id=run_id, summary=summary, payload=details)

    def close_run(self, run_id: str, *, outcome: str, failure_mode: Optional[str] = None,
                  notes: Optional[str] = None, summary: str = "run closed") -> Dict[str, Any]:
        outcome = str(outcome).upper()
        if outcome not in ALLOWED_OUTCOMES:
            raise ValueError(f"invalid outcome: {outcome}; allowed={sorted(ALLOWED_OUTCOMES)}")
        return self.write_event("run.closed", run_id=run_id, summary=summary,
                                payload={"outcome": outcome, "failure_mode": failure_mode, "notes": notes})

    def pending(self, *, project_id: Optional[str] = None, task_family: Optional[str] = None,
                environment: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        self.scan_new_events()
        clauses = ["status='OPEN'"]
        params: List[Any] = []
        if project_id:
            clauses.append("lower(project_id)=lower(?)"); params.append(project_id)
        if task_family:
            clauses.append("lower(task_family)=lower(?)"); params.append(normalize_token(task_family))
        if environment:
            clauses.append("lower(environment)=lower(?)"); params.append(environment)
        sql = f"SELECT run_id,started_at,project_id,task_family,environment,device_id,description FROM run_state WHERE {' AND '.join(clauses)} ORDER BY started_at DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def close_latest(self, *, outcome: str, project_id: Optional[str] = None, task_family: Optional[str] = None,
                     environment: Optional[str] = None, failure_mode: Optional[str] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        rows = self.pending(project_id=project_id, task_family=task_family, environment=environment, limit=1)
        if not rows:
            raise ValueError("no pending run matches the requested scope")
        rid = rows[0]["run_id"]
        self.close_run(rid, outcome=outcome, failure_mode=failure_mode, notes=notes)
        return {**rows[0], "status": "CLOSED", "outcome": outcome.upper()}

    # ---------- environment capability profiles ----------
    def publish_environment_profile(self, capabilities: Dict[str, Any], *, session_id: Optional[str] = None,
                                    last_verified: Optional[str] = None, summary: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "environment_key": self.config.environment_key,
            "device_id": self.config.device_id,
            "environment_id": self.config.environment_id,
            "session_id": session_id,
            "last_verified": last_verified or now_iso(),
            "capabilities": capabilities,
        }
        return self.write_event("environment.profile_published", summary=summary or f"capability profile {self.config.environment_key}", payload=payload)

    def environment_profiles(self) -> List[Dict[str, Any]]:
        self.scan_new_events()
        rows = self.conn.execute("SELECT * FROM environment_profiles ORDER BY last_verified DESC").fetchall()
        out = []
        for r in rows:
            d = dict(r); d["capabilities"] = json.loads(d.pop("capabilities_json"))
            out.append(d)
        return out

    # ---------- learning observations ----------
    def observe_capability(self, *, resource_id: str, task_family: Optional[str], capability: str,
                           assessment: str, confidence: str, evidence_type: str,
                           configuration: Optional[Dict[str, Any]] = None,
                           metrics: Optional[Dict[str, Any]] = None,
                           notes: Optional[str] = None,
                           environment_key: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "observation_id": f"O_{new_ulid()}",
            "resource_id": resource_id,
            "environment_key": environment_key or self.config.environment_key,
            "task_family": normalize_token(task_family),
            "capability": normalize_token(capability),
            "assessment": assessment,
            "confidence": confidence,
            "evidence_type": evidence_type,
            "configuration": configuration or {},
            "metrics": metrics or {},
            "notes": notes,
            "observed_at": now_iso(),
        }
        return self.write_event("capability.observed", task_family=task_family,
                                summary=f"{resource_id}: {capability}={assessment}", payload=payload)

    def observe_skill(self, *, skill_id: str, version: str, task_family: Optional[str], outcome: str,
                      metrics: Optional[Dict[str, Any]] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        payload = {"observation_id": f"SO_{new_ulid()}", "skill_id": skill_id, "version": version,
                   "environment_key": self.config.environment_key, "task_family": normalize_token(task_family),
                   "outcome": outcome, "metrics": metrics or {}, "notes": notes, "observed_at": now_iso()}
        return self.write_event("skill.observed", task_family=task_family, summary=f"skill {skill_id} {outcome}", payload=payload)

    def observe_pattern(self, *, pattern_id: str, version: str, task_family: Optional[str], outcome: str,
                        metrics: Optional[Dict[str, Any]] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        payload = {"observation_id": f"PO_{new_ulid()}", "pattern_id": pattern_id, "version": version,
                   "environment_key": self.config.environment_key, "task_family": normalize_token(task_family),
                   "outcome": outcome, "metrics": metrics or {}, "notes": notes, "observed_at": now_iso()}
        return self.write_event("pattern.observed", task_family=task_family, summary=f"pattern {pattern_id} {outcome}", payload=payload)

    # ---------- compact views ----------
    def _atomic_index(self, name: str, data: Any) -> Path:
        path = self.index_root / name
        atomic_write_json(path, data, replace_existing=True)
        return path

    def compact(self, recent_limit: int = 100) -> Dict[str, Any]:
        new_count = self.scan_new_events()
        pending = self.pending(limit=1000)
        recent = [dict(r) for r in self.conn.execute(
            "SELECT run_id,project_id,task_family,environment,device_id,description,status,outcome,started_at,ended_at,updated_at FROM run_state ORDER BY updated_at DESC LIMIT ?",
            (recent_limit,)).fetchall()]
        envs = self.environment_profiles()
        # Compact capability view: latest 200 observations, deliberately not a giant registry dump.
        caps = [dict(r) for r in self.conn.execute(
            "SELECT resource_id,environment_key,task_family,capability,assessment,confidence,evidence_type,observed_at FROM resource_observations ORDER BY observed_at DESC LIMIT 200"
        ).fetchall()]
        paths = {
            "pending": str(self._atomic_index("pending.json", pending)),
            "recent_runs": str(self._atomic_index("recent-runs.json", recent)),
            "environments": str(self._atomic_index("environments.json", envs)),
            "capabilities": str(self._atomic_index("capability-view.json", caps)),
        }
        meta = {"schema_version": "0.4", "generated_at": now_iso(), "new_events_ingested": new_count,
                "event_count": self.conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
                "run_count": self.conn.execute("SELECT COUNT(*) FROM run_state").fetchone()[0]}
        self._atomic_index("manifest.json", meta)
        return {"ok": True, "meta": meta, "paths": paths}

    def query_context(self, *, task_family: Optional[str] = None, capability: Optional[str] = None,
                      current_environment_only: bool = False, limit: int = 5) -> Dict[str, Any]:
        self.scan_new_events()
        tf = normalize_token(task_family)
        cap = normalize_token(capability)
        run_clauses = ["1=1"]; run_params: List[Any] = []
        if tf:
            run_clauses.append("task_family=?"); run_params.append(tf)
        if current_environment_only:
            run_clauses.append("lower(environment)=lower(?)"); run_params.append(self.config.environment_id)
        runs = [dict(r) for r in self.conn.execute(
            f"SELECT run_id,project_id,task_family,environment,device_id,description,outcome,updated_at FROM run_state WHERE {' AND '.join(run_clauses)} ORDER BY updated_at DESC LIMIT ?",
            (*run_params, limit)).fetchall()]
        obs_clauses = ["1=1"]; obs_params: List[Any] = []
        if tf:
            obs_clauses.append("task_family=?"); obs_params.append(tf)
        if cap:
            obs_clauses.append("capability=?"); obs_params.append(cap)
        observations = [dict(r) for r in self.conn.execute(
            f"SELECT resource_id,environment_key,task_family,capability,assessment,confidence,evidence_type,observed_at FROM resource_observations WHERE {' AND '.join(obs_clauses)} ORDER BY observed_at DESC LIMIT ?",
            (*obs_params, limit)).fetchall()]
        current_key = self.config.environment_key
        row = self.conn.execute("SELECT * FROM environment_profiles WHERE environment_key=?", (current_key,)).fetchone()
        current_profile = None
        if row:
            current_profile = dict(row); current_profile["capabilities"] = json.loads(current_profile.pop("capabilities_json"))
        alternates = []
        for e in self.environment_profiles():
            if e["environment_key"] != current_key:
                alternates.append(e)
            if len(alternates) >= limit:
                break
        return {
            "current_environment": current_profile,
            "relevant_runs": runs,
            "resource_observations": observations,
            "known_alternate_environments": alternates,
        }

    def status(self) -> Dict[str, Any]:
        self.scan_new_events()
        return {
            "version": VERSION,
            "mode": self.config.mode,
            "shared_provider": self.config.shared_provider,
            "vault_root": str(self.root),
            "cache_db": str(self.cache_path),
            "device_id": self.config.device_id,
            "environment_id": self.config.environment_id,
            "environment_key": self.config.environment_key,
            "events": self.conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "runs": self.conn.execute("SELECT COUNT(*) FROM run_state").fetchone()[0],
            "pending": self.conn.execute("SELECT COUNT(*) FROM run_state WHERE status='OPEN'").fetchone()[0],
        }


def detect_local_capabilities() -> Dict[str, Any]:
    def cmd_version(cmd: str, args: List[str]) -> Optional[str]:
        exe = shutil.which(cmd)
        if not exe:
            return None
        try:
            p = subprocess.run([exe, *args], capture_output=True, text=True, timeout=4)
            out = (p.stdout or p.stderr).strip().splitlines()
            return out[0][:180] if out else "available"
        except Exception:
            return "available"

    caps: Dict[str, Any] = {
        "os": {"status": "AVAILABLE", "value": platform.platform()},
        "python": {"status": "AVAILABLE", "value": platform.python_version()},
        "shell": {"status": "AVAILABLE"},
        "git": {"status": "AVAILABLE" if shutil.which("git") else "UNAVAILABLE", "value": cmd_version("git", ["--version"])},
    }
    return caps
