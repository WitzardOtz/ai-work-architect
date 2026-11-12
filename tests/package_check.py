#!/usr/bin/env python3
"""Structural self-check of the AWA package. Stdlib only.

Verifies that the package is internally consistent before it is installed or
published. It checks structure, not behavioral efficacy.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from awa_vault import VERSION  # noqa: E402
from awa_cli import parser as cli_parser  # noqa: E402

SKIP_DIRS = {".git", "__pycache__", ".venv"}
PACKAGE_DIRS = ("references", "templates", "scripts", "environments", "tests")
PRIVATE_PATTERNS = [
    re.compile(r"[A-Za-z]:[\\/]+Users[\\/]"),
    re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"),
    re.compile(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}"),
]
errors = []


def err(message):
    errors.append(message)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def files(suffix):
    for path in sorted(ROOT.rglob(f"*{suffix}")):
        if not SKIP_DIRS.intersection(path.relative_to(ROOT).parts):
            yield path


def rel(path):
    return path.relative_to(ROOT).as_posix()


def check_frontmatter():
    text = read("SKILL.md")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return err("SKILL.md: missing frontmatter")
    block = match.group(1)
    name = re.search(r"^name:\s*(\S+)\s*$", block, re.M)
    manifest = json.loads(read("MANIFEST.json"))
    if not name or name.group(1) != manifest["name"]:
        err("SKILL.md: frontmatter name must match MANIFEST.json name")
    if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)):
        err("SKILL.md: name must be lowercase kebab-case")
    desc = re.search(r"^description:\s*(?:>-?\s*\n((?:[ \t]+.*\n?)+)|(.+))$", block, re.M)
    if not desc:
        return err("SKILL.md: missing description")
    value = " ".join((desc.group(1) or desc.group(2)).split())
    if not 1 <= len(value) <= 1024:
        err(f"SKILL.md: description length {len(value)} outside 1..1024")
    if "<" in value or ">" in value:
        err("SKILL.md: description must not contain angle brackets")
    if not (ROOT / manifest["entrypoint"]).is_file():
        err("MANIFEST.json: entrypoint does not exist")
    extra = [rel(p) for p in files(".md") if p.name == "SKILL.md" and p.parent != ROOT]
    if extra:
        err(f"only the root SKILL.md may have that name (upload-based hosts reject a second one): {extra}")


def check_versions():
    manifest = json.loads(read("MANIFEST.json"))
    found = {
        "MANIFEST.json": manifest.get("version"),
        "SKILL.md": (re.search(r"^Version: (\S+)$", read("SKILL.md"), re.M) or [None, None])[1],
        "docs/it/SKILL_IT.md": (re.search(r"^Versione: (\S+)$", read("docs/it/SKILL_IT.md"), re.M) or [None, None])[1],
        "README.md": (re.match(r"# AI Work Architect v(\S+)", read("README.md")) or [None, None])[1],
        "README_IT.md": (re.match(r"# AI Work Architect v(\S+)", read("README_IT.md")) or [None, None])[1],
        "templates/event.example.json": json.loads(read("templates/event.example.json")).get("architect_version"),
    }
    for name, value in found.items():
        if value != VERSION:
            err(f"{name}: version {value!r} differs from scripts/awa_vault.py VERSION {VERSION!r}")
    for name in ("CHANGELOG.md", "docs/it/CHANGELOG.md"):
        if not re.search(rf"^## {re.escape(VERSION)}\b", read(name), re.M):
            err(f"{name}: no section for version {VERSION}")
    for name in ("README.md", "README_IT.md"):
        for stale in set(re.findall(r"AWA v(\d+\.\d+\.\d+) ", read(name))) - {VERSION}:
            err(f"{name}: expected test output mentions v{stale}")


def check_links():
    for path in files(".md"):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
            if re.match(r"[a-z]+:", target):
                continue
            if not (path.parent / target).exists():
                err(f"{rel(path)}: broken link {target}")
        for target in re.findall(r"`((?:%s)/[\w./-]+\.\w+)`" % "|".join(PACKAGE_DIRS), text):
            if not (ROOT / target).exists():
                err(f"{rel(path)}: path {target} does not exist in the package")


def check_languages():
    pairs = json.loads(read("docs/languages.json"))["pairs"]
    registered = set()
    for pair in pairs:
        for lang, other in (("en", "it"), ("it", "en")):
            path = ROOT / pair[lang]
            registered.add(pair[lang])
            if not path.is_file():
                err(f"docs/languages.json: missing {pair[lang]}")
                continue
            targets = re.findall(r"\]\(([^)#\s]+)\)", path.read_text(encoding="utf-8"))
            resolved = {(path.parent / t).resolve() for t in targets if not re.match(r"[a-z]+:", t)}
            if (ROOT / pair[other]).resolve() not in resolved:
                err(f"{pair[lang]}: no link to its counterpart {pair[other]}")
        en, it = (ROOT / pair["en"]), (ROOT / pair["it"])
        if en.is_file() and it.is_file():
            a, b = en.read_text(encoding="utf-8"), it.read_text(encoding="utf-8")
            if len(re.findall(r"^#+ ", a, re.M)) != len(re.findall(r"^#+ ", b, re.M)):
                err(f"{pair['en']}: heading count differs from {pair['it']}")
            if a.count("```") != b.count("```"):
                err(f"{pair['en']}: code block count differs from {pair['it']}")
    for path in files(".md"):
        if rel(path) not in registered:
            err(f"{rel(path)}: not registered in docs/languages.json")


def check_entrypoint_reach():
    skill = read("SKILL.md")
    for path in sorted((ROOT / "references").glob("*.md")):
        if rel(path) not in skill:
            err(f"SKILL.md: does not reference {rel(path)}")
    for needed in ("scripts/awa_cli.py", "environments/", "templates/"):
        if needed not in skill:
            err(f"SKILL.md: does not reference {needed}")


def check_cli_commands():
    sub = next(a for a in cli_parser()._actions if getattr(a, "choices", None) and a.dest == "cmd")
    known = set(sub.choices)
    for path in files(".md"):
        for cmd in re.findall(r"awa_cli\.py\s+(?:--config\s+\S+\s+)?([a-z][a-z-]+)", path.read_text(encoding="utf-8")):
            if cmd not in known:
                err(f"{rel(path)}: documents unknown CLI command {cmd}")


def check_json_and_privacy():
    for path in files(".json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            err(f"{rel(path)}: invalid JSON ({exc})")
    for suffix in (".md", ".json", ".py"):
        for path in files(suffix):
            if path.name == "package_check.py":
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in PRIVATE_PATTERNS:
                hit = pattern.search(text)
                if hit:
                    err(f"{rel(path)}: possible private path or address {hit.group(0)!r}")


def main():
    for check in (check_frontmatter, check_versions, check_links, check_languages,
                  check_entrypoint_reach, check_cli_commands, check_json_and_privacy):
        check()
    if errors:
        for message in errors:
            print(f"FAIL {message}")
        raise SystemExit(1)
    print(f"AWA v{VERSION} package check: PASS")


if __name__ == "__main__":
    main()
