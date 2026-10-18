#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

from awa_vault import AWAConfig, AWAVault, VERSION, default_config_path, default_local_vault, detect_local_capabilities


def emit(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True))


def parse_json_arg(value: str | None) -> Dict[str, Any]:
    if not value:
        return {}
    p = Path(value)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return json.loads(value)


def load_config(path: str | None) -> AWAConfig:
    return AWAConfig.load(Path(path) if path else None)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=f"AI Work Architect CLI v{VERSION}")
    p.add_argument("--config", help="Path to AWA config.json")
    sub = p.add_subparsers(dest="cmd", required=True)

    x = sub.add_parser("init-local", help="Initialize single-device local persistence")
    x.add_argument("--device-id", required=True)
    x.add_argument("--environment-id", required=True)
    x.add_argument("--vault", default=str(default_local_vault()))

    x = sub.add_parser("init-shared", help="Initialize a shared Google Drive-backed AWA Vault")
    x.add_argument("--device-id", required=True)
    x.add_argument("--environment-id", required=True)
    x.add_argument("--vault", required=True, help="Local path to the Google Drive-synced AWA folder")
    x.add_argument("--provider", default="GOOGLE_DRIVE")

    sub.add_parser("status")
    sub.add_parser("compact")
    x = sub.add_parser("rebuild-cache")

    x = sub.add_parser("probe", help="Publish current local environment capability profile")
    x.add_argument("--extra", help="JSON object or JSON file merged into detected capabilities")
    x.add_argument("--session-id")

    x = sub.add_parser("env-list")

    x = sub.add_parser("run-start")
    x.add_argument("--project-id")
    x.add_argument("--task-family")
    x.add_argument("--description", required=True)
    x.add_argument("--parent-run-id")

    x = sub.add_parser("run-recommend")
    x.add_argument("run_id")
    x.add_argument("--json", required=True, help="JSON object or file")
    x.add_argument("--summary", default="routing recommendation")

    x = sub.add_parser("run-execution")
    x.add_argument("run_id")
    x.add_argument("--json", required=True)
    x.add_argument("--summary", default="actual execution")

    x = sub.add_parser("run-reroute")
    x.add_argument("run_id")
    x.add_argument("--json", required=True)
    x.add_argument("--summary", default="run rerouted")

    x = sub.add_parser("run-close")
    x.add_argument("run_id")
    x.add_argument("--outcome", required=True)
    x.add_argument("--failure-mode")
    x.add_argument("--notes")

    x = sub.add_parser("pending")
    x.add_argument("--project-id")
    x.add_argument("--task-family")
    x.add_argument("--environment")
    x.add_argument("--limit", type=int, default=20)

    x = sub.add_parser("close-latest")
    x.add_argument("--outcome", required=True)
    x.add_argument("--project-id")
    x.add_argument("--task-family")
    x.add_argument("--environment")
    x.add_argument("--failure-mode")
    x.add_argument("--notes")

    x = sub.add_parser("observe-capability")
    x.add_argument("--resource-id", required=True)
    x.add_argument("--task-family")
    x.add_argument("--capability", required=True)
    x.add_argument("--assessment", required=True)
    x.add_argument("--confidence", required=True)
    x.add_argument("--evidence-type", required=True)
    x.add_argument("--configuration")
    x.add_argument("--metrics")
    x.add_argument("--notes")
    x.add_argument("--environment-key")

    x = sub.add_parser("observe-skill")
    x.add_argument("--skill-id", required=True)
    x.add_argument("--version", required=True)
    x.add_argument("--task-family")
    x.add_argument("--outcome", required=True)
    x.add_argument("--metrics")
    x.add_argument("--notes")

    x = sub.add_parser("observe-pattern")
    x.add_argument("--pattern-id", required=True)
    x.add_argument("--version", required=True)
    x.add_argument("--task-family")
    x.add_argument("--outcome", required=True)
    x.add_argument("--metrics")
    x.add_argument("--notes")

    x = sub.add_parser("query-context")
    x.add_argument("--task-family")
    x.add_argument("--capability")
    x.add_argument("--current-environment-only", action="store_true")
    x.add_argument("--limit", type=int, default=5)
    return p


def main() -> None:
    args = parser().parse_args()
    cfg_path = Path(args.config) if args.config else default_config_path()

    if args.cmd in {"init-local", "init-shared"}:
        mode = "LOCAL" if args.cmd == "init-local" else "SHARED_GOOGLE_DRIVE"
        cfg = AWAConfig(
            mode=mode,
            vault_root=str(Path(args.vault).expanduser()),
            device_id=args.device_id,
            environment_id=args.environment_id,
            config_path=cfg_path,
            shared_provider=None if mode == "LOCAL" else args.provider,
        )
        cfg.save()
        v = AWAVault(cfg)
        try:
            # Every environment gets an initial local capability profile.
            v.publish_environment_profile(detect_local_capabilities(), summary=f"initial profile {cfg.environment_key}")
            v.compact()
            emit({"initialized": True, **v.status(), "config": str(cfg_path)})
        finally:
            v.close()
        return

    cfg = load_config(str(cfg_path))
    vault = AWAVault(cfg)
    try:
        if args.cmd == "status":
            emit(vault.status())
        elif args.cmd == "compact":
            emit(vault.compact())
        elif args.cmd == "rebuild-cache":
            emit({"events_ingested": vault.rebuild_cache(), **vault.status()})
        elif args.cmd == "probe":
            caps = detect_local_capabilities()
            extra = parse_json_arg(args.extra)
            caps.update(extra)
            event = vault.publish_environment_profile(caps, session_id=args.session_id)
            emit({"event_id": event["event_id"], "environment_key": cfg.environment_key, "capabilities": caps})
        elif args.cmd == "env-list":
            emit(vault.environment_profiles())
        elif args.cmd == "run-start":
            emit(vault.start_run(project_id=args.project_id, task_family=args.task_family, description=args.description, parent_run_id=args.parent_run_id))
        elif args.cmd == "run-recommend":
            emit(vault.recommend(args.run_id, parse_json_arg(args.json), args.summary))
        elif args.cmd == "run-execution":
            emit(vault.record_execution(args.run_id, parse_json_arg(args.json), args.summary))
        elif args.cmd == "run-reroute":
            emit(vault.reroute(args.run_id, parse_json_arg(args.json), args.summary))
        elif args.cmd == "run-close":
            emit(vault.close_run(args.run_id, outcome=args.outcome, failure_mode=args.failure_mode, notes=args.notes))
        elif args.cmd == "pending":
            emit(vault.pending(project_id=args.project_id, task_family=args.task_family, environment=args.environment, limit=args.limit))
        elif args.cmd == "close-latest":
            emit(vault.close_latest(outcome=args.outcome, project_id=args.project_id, task_family=args.task_family,
                                    environment=args.environment, failure_mode=args.failure_mode, notes=args.notes))
        elif args.cmd == "observe-capability":
            emit(vault.observe_capability(resource_id=args.resource_id, task_family=args.task_family, capability=args.capability,
                                           assessment=args.assessment, confidence=args.confidence, evidence_type=args.evidence_type,
                                           configuration=parse_json_arg(args.configuration), metrics=parse_json_arg(args.metrics),
                                           notes=args.notes, environment_key=args.environment_key))
        elif args.cmd == "observe-skill":
            emit(vault.observe_skill(skill_id=args.skill_id, version=args.version, task_family=args.task_family,
                                     outcome=args.outcome, metrics=parse_json_arg(args.metrics), notes=args.notes))
        elif args.cmd == "observe-pattern":
            emit(vault.observe_pattern(pattern_id=args.pattern_id, version=args.version, task_family=args.task_family,
                                       outcome=args.outcome, metrics=parse_json_arg(args.metrics), notes=args.notes))
        elif args.cmd == "query-context":
            emit(vault.query_context(task_family=args.task_family, capability=args.capability,
                                     current_environment_only=args.current_environment_only, limit=args.limit))
        else:
            raise SystemExit(f"unsupported command: {args.cmd}")
    finally:
        vault.close()


if __name__ == "__main__":
    main()
