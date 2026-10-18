# Claude environment profile

[English](claude.md) | [Italiano](../docs/it/environments/claude.md)

Treat Claude as several different environments, not one capability set.

## Claude chat / Project

Potentially cloud-only. Verify connectors actually available in the session. No assumption of local filesystem or local Python.

If the shared Google Drive AWA Vault is reachable through a verified connector, use the cloud adapter pattern. Otherwise persistence is `DEGRADED` for that session.

## Claude Cowork

Observed in prior environment testing:

- Python available in the Cowork VM;
- connected folders can persist across sessions, but folder access may need per-session approval;
- synced-folder SQLite was fragile, which is why v0.4 uses immutable Vault files instead;
- local scratch/cache is disposable per session;
- use the shared Vault as canonical and rebuild local cache as needed.

## Claude Code

When running locally, prefer `scripts/awa_cli.py` and a locally synced Google Drive Vault.

## Independent review

Where Claude supports subagents or isolated workers, map them to `ISOLATE` / `PARALLEL` only after verifying the feature is available in the current mode.

## Skills

Installed/user-specific Skills are environment-local. Probe or inspect the actual inventory; do not assume a Skill exists merely because it was available in a past Claude session.
