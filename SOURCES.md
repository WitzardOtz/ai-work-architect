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
