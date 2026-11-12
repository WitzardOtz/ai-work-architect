# Claude environment profile

[English](claude.md) | [Italiano](../docs/it/environments/claude.md)

Last reviewed: 2026-11-12. These are dated notes to verify in the session, not guarantees.

Treat Claude as several different environments, not one capability set.

## Claude chat / Project

Potentially cloud-only. Verify connectors actually available in the session. No assumption of local filesystem or local Python.

If the shared Google Drive AWA Vault is reachable through a verified connector, use the cloud adapter pattern. Otherwise persistence is `DEGRADED` for that session.

## Claude Cowork

- A Cowork session may run in a cloud workspace rather than on the user's device. Anthropic's support documentation describes cloud as the default for new sessions since October 2026, while sessions started locally before then stay local. Do not assume a local VM; check where the shell runs.
- In a cloud session, Python and the shell belong to the cloud workspace. The user's folders are reached only through the desktop app, only while it is running, and only for connected folders; access may need approval.
- A connected folder on a virtual drive, such as Google Drive for Desktop, may be readable and writable file by file yet not mountable in a shell. Observed once (2026-11): the bundled CLI could not then run against the Vault.
- In that case treat file-level access as a cloud adapter: read `index/` first, create new immutable event files, and leave shared indexes to an environment that can run `compact`. A verified Google Drive connector is an alternative. If neither can create event files, persistence is `DEGRADED`.
- Synced-folder SQLite was fragile in earlier testing, which is why the Vault uses immutable files. Any cache in the session workspace is disposable.

## Claude Code

When running locally, prefer `scripts/awa_cli.py` and a locally synced Google Drive Vault.

## Independent review

Where Claude supports subagents or isolated workers, map them to `ISOLATE` / `PARALLEL` only after verifying the feature is available in the current mode.

## Skills

Installed/user-specific Skills are environment-local. Probe or inspect the actual inventory; do not assume a Skill exists merely because it was available in a past Claude session.

An installation may contain only `SKILL.md` (observed once, 2026-11). Check that `references/`, `templates/` and `scripts/` are present before relying on them.
