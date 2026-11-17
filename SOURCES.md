# Design evidence for v0.4

[English](SOURCES.md) | [Italiano](docs/it/SOURCES.md)

This version is based primarily on cross-environment validation of v0.3.x rather than external benchmark claims.

Observed constraints incorporated into the design:

- synchronized live SQLite can fail or lock on mounted/synced folders;
- immutable file creation is materially safer for multi-device cloud-sync workflows;
- local AI environments can use Python/PowerShell/filesystem capabilities that cloud sessions may not have;
- cloud sessions need a connector or other verified adapter to reach shared storage;
- large shared registries should be indexed/queried rather than loaded into model context;
- capability availability differs by device, client and sometimes session.

Model-specific performance claims deliberately do not live in the Skill kernel. They belong in AWA observations/registries and should be updated from current evidence.

## Controlled improvement addition — 2026-10-18

The optional protocol draws on [Harness2](https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335), specifically evidence-linked proposals, Propose-Probe-Compose and KEEP_BASE. The reference and template are original AWA adaptations; no upstream runtime code is imported. Upstream benchmark results are not local AWA validation. See `references/controlled-improvement.md` for scope and adoption rules.

## Environment review — 2026-11-12

The Claude, Codex and Antigravity profiles were re-read against vendor documentation and changelogs, plus one observed Cowork session. Recorded changes: Cowork sessions may run in the cloud and reach user folders through the desktop app; a Vault on a virtual drive may be reachable file by file but not by the CLI; Antigravity added remote agents and moved per-project configuration; Codex added multi-agent features. Profiles carry a review date and remain evidence to verify. The review also found the resource registry of a real Vault empty after 17 runs, which motivated the explicit currency rule and the documented observation commands. No model names, prices or benchmark claims were added to the skill.

## Public registry and Fable 5.2 guidance — 2026-11-17

Model facts and benchmark results moved to a separate public repository, the [AWA resource registry](https://github.com/WitzardOtz/awa-resource-registry), updated twice a week from vendor pages and benchmark leaderboards. The skill still contains no model names, prices or scores; it only describes how to read the registry and how to combine it with the Vault. The general guidance added in 0.6.0 comes from Anthropic's [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2) and was kept only where it applies beyond that model. Its effect on AWA has not been measured.
