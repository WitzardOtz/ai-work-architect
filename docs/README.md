# Documentation index

[English](README.md) | [Italiano](it/README.md)

All human-readable AWA documentation is available in English and Italian. English files retain their existing locations; Italian reference translations mirror them under `docs/it/`. README and practical guides have explicit root-level language variants.

| Document | English | Italiano |
|---|---|---|
| README.md | [English](../README.md) | [Italiano](../README_IT.md) |
| USER_GUIDE_EN.md | [English](../USER_GUIDE_EN.md) | [Italiano](../USER_GUIDE_IT.md) |
| SKILL.md | [English](../SKILL.md) | [Italiano](it/SKILL.md) |
| SOURCES.md | [English](../SOURCES.md) | [Italiano](it/SOURCES.md) |
| CHANGELOG.md | [English](../CHANGELOG.md) | [Italiano](it/CHANGELOG.md) |
| docs/LICENSE_EN.md | [English](LICENSE_EN.md) | [Italiano](it/LICENSE.md) |
| references/cloud-adapters.md | [English](../references/cloud-adapters.md) | [Italiano](it/references/cloud-adapters.md) |
| references/controlled-improvement.md | [English](../references/controlled-improvement.md) | [Italiano](it/references/controlled-improvement.md) |
| references/decomposition.md | [English](../references/decomposition.md) | [Italiano](it/references/decomposition.md) |
| references/environment-capabilities.md | [English](../references/environment-capabilities.md) | [Italiano](it/references/environment-capabilities.md) |
| references/first-run-setup.md | [English](../references/first-run-setup.md) | [Italiano](it/references/first-run-setup.md) |
| references/logging-learning.md | [English](../references/logging-learning.md) | [Italiano](it/references/logging-learning.md) |
| references/organization-context-setup.md | [English](../references/organization-context-setup.md) | [Italiano](it/references/organization-context-setup.md) |
| references/persistence.md | [English](../references/persistence.md) | [Italiano](it/references/persistence.md) |
| references/routing.md | [English](../references/routing.md) | [Italiano](it/references/routing.md) |
| references/signatures.md | [English](../references/signatures.md) | [Italiano](it/references/signatures.md) |
| references/testing.md | [English](../references/testing.md) | [Italiano](it/references/testing.md) |
| templates/handoff-pack.md | [English](../templates/handoff-pack.md) | [Italiano](it/templates/handoff-pack.md) |
| templates/improvement-experiment.md | [English](../templates/improvement-experiment.md) | [Italiano](it/templates/improvement-experiment.md) |
| templates/machine-examples.md | [English](../templates/machine-examples.md) | [Italiano](it/templates/machine-examples.md) |
| templates/organization-profile.md | [English](../templates/organization-profile.md) | [Italiano](it/templates/organization-profile.md) |
| templates/organization-sources.md | [English](../templates/organization-sources.md) | [Italiano](it/templates/organization-sources.md) |
| templates/project-brief.md | [English](../templates/project-brief.md) | [Italiano](it/templates/project-brief.md) |
| templates/project-work.md | [English](../templates/project-work.md) | [Italiano](it/templates/project-work.md) |
| templates/task-contract.md | [English](../templates/task-contract.md) | [Italiano](it/templates/task-contract.md) |
| environments/antigravity.md | [English](../environments/antigravity.md) | [Italiano](it/environments/antigravity.md) |
| environments/chatgpt.md | [English](../environments/chatgpt.md) | [Italiano](it/environments/chatgpt.md) |
| environments/claude.md | [English](../environments/claude.md) | [Italiano](it/environments/claude.md) |
| environments/codex.md | [English](../environments/codex.md) | [Italiano](it/environments/codex.md) |
| environments/generic.md | [English](../environments/generic.md) | [Italiano](it/environments/generic.md) |
| AGENTS.md | [English](../AGENTS.md) | [Italiano](it/AGENTS.md) |

## Language and maintenance rules

Read one language version, not both by default. The host responds in the user's language. The installed skill entrypoint remains the root `SKILL.md`; the Italian skill document is its reference translation, not a second installation.

Update a document and its counterpart together when changing behavior, constraints or user instructions. Preserve commands, API/JSON keys, enum values, identifiers and file paths. The paired inventory in [languages.json](languages.json) records coverage; it is documentation metadata, not company or runtime configuration.

Machine-readable JSON examples and executable scripts remain language-neutral interfaces. Their fields and use are explained in both language versions of the machine-example guide. The full Apache legal text remains unchanged in [LICENSE](../LICENSE); explanatory pages in both languages do not replace it.

Translations preserve the same limitations: the company setup is conversational, profile bindings are agent-managed, sharing does not grant permissions, and company onboarding efficacy is not established by structural checks.
