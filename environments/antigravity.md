# Antigravity environment profile

Prior environment review indicates Antigravity can operate locally on Windows with filesystem/PowerShell command execution and can use Python/SQLite. Treat these as **environment evidence to verify**, not eternal guarantees.

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

Skills may be global or workspace-scoped; inspect the actual installed inventory for the current workspace.

If the Vault sits outside the active workspace and direct editing is restricted, use the AWA Python CLI via command execution rather than writing event JSON manually.
