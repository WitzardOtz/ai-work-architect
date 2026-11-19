# AI Work Architect v0.6.1

[English](README.md) | [Italiano](README_IT.md)

AWA helps decide **how to structure AI-assisted work** before choosing a model. It decomposes complex work, derives execution steps, matches those steps to tools/models/effort available in the current environment, generates handoffs when another workspace/device is better suited, and learns from run outcomes without loading its whole history into the model context.

## Start here

**[Practical guide in English](USER_GUIDE_EN.md)** — installation, first use, company setup, colleague reuse, access, project continuity and limitations.

**[Bilingual documentation index](docs/README.md)** — paired English and Italian versions of all human-readable documentation.

| Your situation | Start with |
|---|---|
| First use | Ask AWA to guide your initial setup; choose local or shared memory. |
| First person configuring a company | Ask AWA to configure company context and provide selected sources. Review the profile, confirm its scope, and receive a message to copy to colleagues. |
| Joining an existing company setup | Give AWA the shared profile reference. It checks your access and current version, then asks only for missing role/project details. |
| Returning to a project | Reuse its checkpoint and scoped profile reference; clarify relevant changes without recreating the setup. |

The company wizard is conversational guidance followed by the host agent, not a hosted application. The detailed workflow is in [organization context setup](references/organization-context-setup.md).

## Guided first use

At first use, AWA checks for existing configuration and guides you through local or shared persistence when needed. Google Drive is optional. The agent verifies the available storage adapter, reports any access limitations, and resumes your task. Existing healthy profiles are reused without repeating setup. See [guided setup](references/first-run-setup.md).

## Latest release — v0.6.1, 19 November 2026

- Ready-made packages for each environment, attached to every release: one for Codex, with a manifest that shows the right version, and one for Claude, Claude Code, Antigravity and other agents. See [Get the skill](#get-the-skill).

- Paired English/Italian README, practical guides, skill instructions, operational references, environment notes and templates. Machine identifiers remain unchanged; the official Apache legal text is accompanied by explanations in both languages.

- Short, verifiable tasks with project-owned plans, checkpoints and work logs let another agent resume without reconstructing chat history or requiring a formal handoff. See [the project work template](templates/project-work.md).
- Optional [controlled improvement](references/controlled-improvement.md) compares a recoverable baseline with bounded candidates, uses separate validation cases, and records explicit decisions and stopping criteria. See [the experiment template](templates/improvement-experiment.md).
- AWA reads the public [resource registry](https://github.com/WitzardOtz/awa-resource-registry) before naming a model: what exists and what others measured, dated and sourced. Your Vault decides what worked for you; see [how the two combine](references/resource-registry.md).
- Model and tool knowledge is treated as perishable: AWA checks what the current environment offers before naming a resource, and the [observation commands](references/logging-learning.md) that build its evidence are documented.
- Environment profiles for Claude, Codex and Antigravity were reviewed and dated; `SKILL.md` now references the CLI and every supporting file.
- All changes are listed in [CHANGELOG.md](CHANGELOG.md). Structural checks and runtime tests pass; comparative behavioral efficacy has not yet been established.

## Get the skill

Download the ready-made package for your environment from the [latest release](https://github.com/WitzardOtz/ai-work-architect/releases/latest):

| Environment | Package | How to install |
|---|---|---|
| Codex (ChatGPT desktop app) | [`ai-work-architect-codex-plugin.zip`](https://github.com/WitzardOtz/ai-work-architect/releases/latest/download/ai-work-architect-codex-plugin.zip) | In Customize (Personalizza), open Plugins, choose Add and upload the ZIP. Codex shows the AWA version from the plugin manifest. |
| Claude apps (claude.ai, desktop) | [`ai-work-architect-skill.zip`](https://github.com/WitzardOtz/ai-work-architect/releases/latest/download/ai-work-architect-skill.zip) | Upload the ZIP where the app accepts skills. |
| Claude Code, Antigravity and other agents that read a skills folder | [`ai-work-architect-skill.zip`](https://github.com/WitzardOtz/ai-work-architect/releases/latest/download/ai-work-architect-skill.zip) | Extract it into the agent's skills folder, so that you get `.../skills/ai-work-architect/SKILL.md`. Claude Code reads `~/.claude/skills/`. On the Antigravity installations observed, global skills are in `~/.gemini/config/skills/`; check the agent's skill list after a restart. |

Both packages contain the same complete skill: `SKILL.md` refers to files under `references/`, `templates/`, `environments/` and `scripts/`, so do not install `SKILL.md` alone. An installed copy does not update itself: install the new package after each release. The instructions need no runtime; the optional local CLI needs Python 3.9 or later and uses only the standard library.

Developers can also clone the repository. GitHub's automatic "Source code" archives extract as `ai-work-architect-main` and have no Codex manifest, so use the packages above for installation.

```bash
git clone https://github.com/WitzardOtz/ai-work-architect.git
```

The repository contains reusable instructions, scripts, templates and tests. Your personal configuration, Vault events, caches and run artifacts belong outside this package and are not included. Installing the skill does not connect accounts or configure shared persistence; the first-run instructions guide that choice.

## Company context setup

Ask AWA: **"Help me configure our company context"** (or in your preferred language). AWA guides you through selecting an organization and scope, connecting existing documents or building a profile, separating policies from preferences, reviewing gaps, and confirming the profile to use. Existing healthy project bindings are reused.

The [conversational wizard](references/organization-context-setup.md) works with selected local files or supported connected storage; Google Drive is optional. Private profiles and source indexes stay outside this public package. AWA retrieves only relevant material and uses applicable constraints when planning work and selecting tools. The workflow does not implement access control or guarantee compliance, and the current CLI does not automatically load these agent-managed profiles.

After the first reusable company setup, AWA gives the configurator a message to copy to colleagues, including the shared profile reference and an existing-context setup instruction. Each colleague verifies their own access; messages and permissions are not sent or changed automatically.

Reusable templates: [organization profile](templates/organization-profile.md), [source index](templates/organization-sources.md), and [scoped context binding](templates/context-bindings.example.json). No real company data is included.

## What changed in v0.4

The major change is persistence and environment awareness.

### 1. Immutable AWA Vault

AWA no longer treats a synchronized SQLite file as canonical. Canonical state is now a set of **immutable event files**.

- In `LOCAL` mode, the Vault lives on one device.
- In `SHARED_GOOGLE_DRIVE` mode, the Vault lives in a Google Drive folder and can be synchronized locally with Google Drive for Desktop and accessed by cloud environments that have a verified Drive connector.
- SQLite remains a **disposable local cache/index**, rebuildable from events.

### 2. Knowledge is global; availability is local

AWA separates:

- **global resource knowledge** — what has been learned about models/tools/Skills across environments;
- **Environment Capability Profiles** — what is actually available on this device/client/session;
- **resource performance evidence** — how configurations performed, segmented by environment.

A task may therefore be routed locally or handed off to another known environment.

### 3. First-run bootstrap

On first use, AWA asks once whether persistence should be local-only or shared across devices/environments.

Recommended shared architecture:

```text
ChatGPT / Claude / Codex / Antigravity
                  │
                  ▼
           Google Drive /AWA
          immutable event Vault
                  │
        ┌─────────┴─────────┐
        │                   │
 local device cache   cloud selective reads
  disposable SQLite      via connector
```

## Installable package

The installed folder must be named `ai-work-architect`, matching the `name:` in `SKILL.md`. Both release packages are built by:

```bash
python scripts/build_release.py
```

It writes `dist/ai-work-architect-skill.zip` and `dist/ai-work-architect-codex-plugin.zip`. The Codex package adds `.codex-plugin/plugin.json`, whose `version` comes from the code, so Codex shows the right version. Only the package files are included; private configuration, Vault data and caches are never packaged.

## Local CLI

The local adapter is `scripts/awa_cli.py` and uses only the Python standard library.

### Initialize local mode

```bash
python scripts/awa_cli.py init-local \
  --device-id MY-PC \
  --environment-id antigravity-local
```

### Initialize shared Google Drive mode

```bash
python scripts/awa_cli.py init-shared \
  --device-id MY-PC \
  --environment-id antigravity-local \
  --vault "G:/My Drive/AWA"
```

Use the actual local path created by Google Drive for Desktop.

### Open / inspect / close a run

```bash
python scripts/awa_cli.py run-start \
  --project-id EXAMPLE_PROJECT \
  --task-family data-to-insight \
  --description "Interpret network metrics and identify hypotheses"

python scripts/awa_cli.py pending --project-id EXAMPLE_PROJECT

python scripts/awa_cli.py close-latest \
  --project-id EXAMPLE_PROJECT \
  --outcome FIRST_PASS_ACCEPTED
```

### Publish current environment capabilities

```bash
python scripts/awa_cli.py probe
```

Additional verified capabilities can be supplied as JSON:

```bash
python scripts/awa_cli.py probe --extra '{"subagents":{"status":"AVAILABLE"}}'
```

### Compact / publish indexes

```bash
python scripts/awa_cli.py compact
```

This generates rebuildable views under `AWA/index/` such as `pending.json`, `recent-runs.json`, `environments.json` and `capability-view.json`. Event files remain the source of truth.

### Record and query evidence

```bash
python scripts/awa_cli.py observe-capability \
  --resource-id EXAMPLE_MODEL \
  --task-family data-to-insight \
  --capability long-context-synthesis \
  --assessment ADEQUATE --confidence LOW --evidence-type run

python scripts/awa_cli.py query-context --task-family data-to-insight
```

Run events alone do not build resource knowledge; observations do. See [logging and learning](references/logging-learning.md).

### Inspect and repair

```bash
python scripts/awa_cli.py --version
python scripts/awa_cli.py status
python scripts/awa_cli.py env-list
python scripts/awa_cli.py rebuild-cache
```

Every command accepts `--help`. A missing configuration or invalid input produces a one-line error and exit code 2.

## Vault layout

```text
AWA/
├── events/
│   └── YYYY/MM/<ULID>__<event_type>__<run>__<project>__<environment>.json
├── index/
│   ├── pending.json
│   ├── recent-runs.json
│   ├── environments.json
│   ├── capability-view.json
│   └── manifest.json
└── meta/
```

Do not append to shared files and do not modify existing event files. A new fact/state transition creates a new event.

## Cloud environments

A cloud environment does **not** need local SQLite. It should:

1. verify that the shared Google Drive Vault is reachable;
2. read compact indexes/search first;
3. retrieve only the few event files relevant to the current decision;
4. write new immutable event files through its Drive connector if that connector supports file creation;
5. otherwise mark persistence `DEGRADED` rather than pretending a write succeeded.

See `references/cloud-adapters.md`.

## Multi-device safety

The event model is intentionally sync-friendly:

- one new file per event;
- unique ULID event IDs;
- safe filename charset;
- no shared database locks;
- no shared append-only ledger;
- duplicate Drive objects are deduplicated by `event_id` when indexed;
- `.tmp-*` files are ignored by readers.

## Tests

```bash
python tests/smoke_test.py
python tests/regression_test.py
python tests/package_check.py
```

Expected:

```text
AWA v0.6.1 smoke test: PASS
AWA v0.6.1 regression test: PASS
AWA v0.6.1 package check: PASS
```

The first two exercise the runtime in temporary folders. The third checks the package structure: frontmatter, local links, language pairs and version consistency.

## Design status

v0.4 freezes the main architecture for real-world testing. Further changes should be driven primarily by closed runs and actual environment failures rather than additional speculative design.

## License

See the [English explanation](docs/LICENSE_EN.md) or [Italian explanation](docs/it/LICENSE.md); the complete legal license is the unchanged English text in `LICENSE`.

Copyright 2026 WitzardOtz.

AI Work Architect instructions, scripts, references and templates in this repository are licensed under the [Apache License 2.0](LICENSE).

The license applies to the distributed AWA package; it does not license users' private configuration, Vault contents, company documents or other user-provided materials. Third-party materials retain their own terms.
