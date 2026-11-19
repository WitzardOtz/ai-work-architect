#!/usr/bin/env python3
"""Build the two installable AWA packages attached to each GitHub release.

Stdlib only. Run from anywhere:

    python scripts/build_release.py [output-folder]

It writes, by default into ``dist/``:

- ``ai-work-architect-skill.zip``: the skill folder ``ai-work-architect/`` with
  ``SKILL.md`` at its root, for Claude, Claude Code, Antigravity and any agent
  that reads a skills folder or accepts a skill upload.
- ``ai-work-architect-codex-plugin.zip``: the same skill under
  ``skills/ai-work-architect/`` plus ``.codex-plugin/plugin.json``, the manifest
  Codex reads to show the plugin name and version.

Only the files listed in INCLUDE are packaged, so private files placed in the
folder (configuration, Vault data, caches) never end up in a package. Archive
timestamps are fixed so the same sources give the same archives.
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from awa_vault import VERSION  # noqa: E402

NAME = "ai-work-architect"
REPO = "https://github.com/WitzardOtz/ai-work-architect"
SKILL_ZIP = "ai-work-architect-skill.zip"
PLUGIN_ZIP = "ai-work-architect-codex-plugin.zip"
INCLUDE = [
    "SKILL.md", "MANIFEST.json", "LICENSE", "README.md", "README_IT.md", "USER_GUIDE_EN.md",
    "USER_GUIDE_IT.md", "CHANGELOG.md", "SOURCES.md", "AGENTS.md",
    "docs", "environments", "references", "scripts", "templates", "tests",
]
SKIP_PARTS = {"__pycache__", ".git", ".github", "dist"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".db", ".db-shm", ".db-wal", ".zip"}
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def package_files() -> list[Path]:
    files = []
    for entry in INCLUDE:
        path = ROOT / entry
        if not path.exists():
            raise SystemExit(f"missing package entry: {entry}")
        candidates = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file())
        for p in candidates:
            rel = p.relative_to(ROOT)
            if SKIP_PARTS.intersection(rel.parts) or p.suffix in SKIP_SUFFIXES:
                continue
            files.append(rel)
    return files


def plugin_manifest() -> dict:
    return {
        "name": NAME,
        "version": VERSION,
        "description": "Plan AI-assisted work before execution: decompose it, route each step to verified models, tools and effort, and keep project continuity.",
        "author": {"name": "WitzardOtz", "url": "https://github.com/WitzardOtz"},
        "homepage": REPO,
        "repository": REPO,
        "license": "Apache-2.0",
        "keywords": ["planning", "routing", "model-selection", "agents", "skills"],
        "skills": "./skills/",
        "interface": {
            "displayName": "AI Work Architect",
            "shortDescription": "Plan AI-assisted work before execution",
            "developerName": "WitzardOtz",
            "category": "Productivity",
            "websiteURL": REPO,
        },
    }


def _write(zf: zipfile.ZipFile, arcname: str, data: bytes) -> None:
    info = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def build(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    files = package_files()
    skill_path = out_dir / SKILL_ZIP
    plugin_path = out_dir / PLUGIN_ZIP
    with zipfile.ZipFile(skill_path, "w") as skill, zipfile.ZipFile(plugin_path, "w") as plugin:
        _write(plugin, ".codex-plugin/plugin.json",
               (json.dumps(plugin_manifest(), ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        for rel in files:
            data = (ROOT / rel).read_bytes()
            posix = rel.as_posix()
            _write(skill, f"{NAME}/{posix}", data)
            _write(plugin, f"skills/{NAME}/{posix}", data)
    return {"version": VERSION, "files": len(files), "skill": str(skill_path), "plugin": str(plugin_path)}


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    result = build(out_dir)
    print(f"AWA v{result['version']} packages: {result['files']} files")
    print(result["skill"])
    print(result["plugin"])


if __name__ == "__main__":
    main()
