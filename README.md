# AI Work Architect v0.4.0

AWA helps decide **how to structure AI-assisted work** before choosing a model. It decomposes complex work, derives execution steps, matches those steps to tools/models/effort available in the current environment, generates handoffs when another workspace/device is better suited, and learns from run outcomes without loading its whole history into the model context.

## Start here / Inizia da qui

**[Guida pratica in italiano](USER_GUIDE_IT.md)** — installazione, primo utilizzo, configurazione aziendale, messaggio per i colleghi, accessi, continuita e limiti.

| Your situation | Start with |
|---|---|
| First use | Ask AWA to guide your initial setup; choose local or shared memory. |
| First person configuring a company | Ask AWA to configure company context and provide selected sources. Review the profile, confirm its scope, and receive a message to copy to colleagues. |
| Joining an existing company setup | Give AWA the shared profile reference. It checks your access and current version, then asks only for missing role/project details. |
| Returning to a project | Reuse its checkpoint and scoped profile reference; clarify relevant changes without recreating the setup. |

The company wizard is conversational guidance followed by the host agent, not a hosted application. The detailed workflow is in [organization context setup](references/organization-context-setup.md).

## Guided first use

At first use, AWA checks for existing configuration and guides you through local or shared persistence when needed. Google Drive is optional. The agent verifies the available storage adapter, reports any access limitations, and resumes your task. Existing healthy profiles are reused without repeating setup. See [guided setup](references/first-run-setup.md).

## Latest skill updates — 18 October 2026

- Short, verifiable tasks with project-owned plans, checkpoints and work logs let another agent resume without reconstructing chat history or requiring a formal handoff. See [the project work template](templates/project-work.md).
- Optional [controlled improvement](references/controlled-improvement.md) compares a recoverable baseline with bounded candidates, uses separate validation cases, and records explicit decisions and stopping criteria. See [the experiment template](templates/improvement-experiment.md).
- The runtime remains v0.4.0. These instruction changes are recorded under Unreleased in [CHANGELOG.md](CHANGELOG.md). Structural checks and runtime tests pass; comparative behavioral efficacy has not yet been established.

## Get the skill

Clone this repository, or download its ZIP and place the extracted folder under the name `ai-work-architect` in the skills location supported by your AI environment. The repository root contains `SKILL.md`.

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

The installed folder must be named `ai-work-architect`, matching the `name:` in `SKILL.md`. GitHub source ZIPs may extract as `ai-work-architect-main`; rename that folder when installing.

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
```

Expected:

```text
AWA v0.4.0 smoke test: PASS
AWA v0.4.0 regression test: PASS
```

## Design status

v0.4 freezes the main architecture for real-world testing. Further changes should be driven primarily by closed runs and actual environment failures rather than additional speculative design.

## License

Copyright 2026 WitzardOtz.

AI Work Architect instructions, scripts, references and templates in this repository are licensed under the [Apache License 2.0](LICENSE).

The license applies to the distributed AWA package; it does not license users' private configuration, Vault contents, company documents or other user-provided materials. Third-party materials retain their own terms.
