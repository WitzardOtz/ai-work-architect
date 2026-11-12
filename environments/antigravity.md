# Antigravity environment profile

[English](antigravity.md) | [Italiano](../docs/it/environments/antigravity.md)

Last reviewed: 2026-11-12.

Prior environment review indicates Antigravity can operate locally on Windows with filesystem/PowerShell command execution and can use Python/SQLite. Treat these as **environment evidence to verify**, not eternal guarantees.

Antigravity can also run remote agents in the cloud; the product changelog describes this rolling out to paid plans in late 2026. Identify whether the current conversation is local or remote before routing: a remote agent has no local filesystem, PowerShell or locally synced Vault unless verified, and is a cloud environment for AWA.

Preferred adapter:

```text
python scripts/awa_cli.py ...
```

Recommended mapping when verified:

- local filesystem / PowerShell -> local execution and Vault access;
- Python -> deterministic compute and AWA CLI/cache;
- Google Drive for Desktop -> shared Vault filesystem adapter;
- subagents -> `PARALLEL` or `ISOLATE` execution;
- Markdown artifacts -> Project Brief / Handoff Pack presentation.

Skills, rules and plugins may be global or project-scoped, and configuration locations have changed between releases (the changelog reports per-project configuration under `<project>/.gemini/config.json` in 2026). Inspect the actual installed inventory for the current workspace rather than relying on a remembered path.

If the Vault sits outside the active workspace and direct editing is restricted, use the AWA Python CLI via command execution rather than writing event JSON manually.
