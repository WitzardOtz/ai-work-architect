# Codex environment profile

[English](codex.md) | [Italiano](../docs/it/environments/codex.md)

Last reviewed: 2026-11-12.

When Codex runs locally with shell/filesystem access, prefer the local AWA CLI and a Google Drive for Desktop-synced Vault. A Codex session that does not run on the user's device is a cloud environment for AWA; follow the cloud adapter pattern there.

Verify rather than assume:

- Python runtime;
- repository/filesystem access;
- Google Drive mount path;
- installed Skills/tools;
- subagent or multi-agent availability;
- models offered and whether reasoning effort can be set or changed in the session;
- test/build runtimes.

Coding and test execution are separate capabilities from generic reasoning. Route deterministic tests to the environment that can actually execute them.
