# Changelog

## Unreleased — 2026-10-18

- Give the first company configurator a copyable colleague onboarding message using a verified shared profile reference; later users reuse company context while checking their own scope and access. Local-only references produce an explicit draft, not a false sharing claim.

- Add optional organization-context wizard: connect selected sources or build private profiles, separate constraints/preferences, review and activate per project/workspace, and support updates/disconnection without resetting persistence.
- Add organization profile, source-index and binding templates; integrate scoped constraints into setup, resource routing and project checkpoints. No organization is configured by installation; private content is excluded from the public package and global learning.

- License the distributed AWA package under Apache-2.0; add the full license and package metadata. Private user materials are outside this license grant.

- Fix Windows replacement of mutable configuration and derived Vault indexes; preserve event-write behavior. Add regression coverage for repeated compaction, configuration save and unchanged historical events.

- Add conversational first-run setup: inspect existing profiles, guide local/shared storage choice, verify adapter round trips, and distinguish local access from cross-device sync. Drive remains optional; preserve existing configuration on failures.

- Add optional controlled improvement: bounded baseline/candidate comparisons, separate validation cases, explicit ADOPT/REVISE/REJECT/KEEP_BASE decisions, budget/stop criteria and rollback references.
- Add an experiment record template and integrate comparison metadata with existing Vault run events; preserve runtime schemas, outcome values and no-silent-learning rules.
- Attribute the Harness2 design inspiration without importing its runtime or claiming transferred benchmark gains. Structural validation and behavioral efficacy remain separate.

- Make short, verifiable tasks with project-owned plan/checkpoint/log files the default for work spanning sessions, quotas, models or agents.
- Save partial progress and observed verification results during work so another agent can resume from files.
- Reuse shared project state instead of requiring a formal Handoff Pack for every model or environment switch.
- Preserve authorization, active task ownership, privacy and the immutable AWA Vault; do not imply parallel execution or interrupt work when the user specifies a future preference.

## 0.4.0

- Replaced synchronized live SQLite as canonical shared state with an immutable event Vault.
- Added `LOCAL` and `SHARED_GOOGLE_DRIVE` persistence profiles.
- Added one-time first-run persistence bootstrap.
- Added ULID event IDs and sync-safe filenames.
- Added disposable local SQLite cache/index, rebuildable from events.
- Added compact indexes for cloud/token-efficient retrieval.
- Added explicit separation between global resource knowledge and local Device × Environment capability availability.
- Added Environment Capability Profiles with `last_verified` and optional session metadata.
- Added routing fallback: adapt locally or hand off to a known environment that has the required capability.
- Added local `awa_cli.py` commands for run lifecycle, environment probes, capability/Skill/pattern observations, compaction and targeted context queries.
- Parked the HTTPS Hub as a non-required future option; it is not part of the active v0.4 runtime.
- Preserved Handoff Pack, Task Signature, decomposition, execution-step routing, verification and learning principles from v0.3.x.
