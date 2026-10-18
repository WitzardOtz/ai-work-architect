# Persistence architecture

## Principle

Canonical state must survive sessions without being loaded wholesale into the LLM context.

AWA v0.4 uses an **immutable event Vault** as source of truth. SQLite is only a disposable local index/cache.

For guided configuration and adapter checks, read [first-run-setup.md](first-run-setup.md).

## First-run choice

Ask once whether the user wants cross-device / cross-environment continuity.

- **LOCAL**: canonical Vault on this device.
- **SHARED_GOOGLE_DRIVE**: canonical Vault in Google Drive; local clients use the synced filesystem and cloud clients use a verified Drive connector.
- **CUSTOM_SHARED**: future adapter.
- **DEGRADED**: configured canonical storage is not reachable from the current environment.

The user must be able to choose Local mode without being forced to connect a cloud drive.

## Event model

Every state transition is a new file. Never append to a shared file and never update an existing event.

Initial event types:

- `run.started`
- `run.recommended`
- `run.execution`
- `run.rerouted`
- `run.closed`
- `project.updated`
- `artifact.registered`
- `environment.profile_published`
- `capability.observed`
- `skill.observed`
- `pattern.observed`

Event headers should remain compact:

```json
{
  "schema_version": "1.0",
  "event_id": "<ULID>",
  "occurred_at": "<UTC timestamp>",
  "event_type": "run.closed",
  "architect_version": "0.4.0",
  "environment": "claude-cowork",
  "device_id": "MY-PC",
  "run_id": "R_<ULID>",
  "project_id": "EXAMPLE_PROJECT",
  "task_family": "data_to_insight",
  "summary": "Network analysis accepted",
  "payload": {}
}
```

## File naming

Use only `[A-Za-z0-9._-]` in filenames. Never use raw ISO timestamps containing `:`.

Recommended form:

```text
<ULID>__<event_type>__<run_id>__<project_slug>__<environment_slug>.json
```

The semantic de-duplication key is `event_id`, not the filename.

## Local write safety

Local writers should write a `.tmp-*` file, flush/fsync it, then rename it into its unique final filename. Readers skip `.tmp-*` files.

## Indexes are projections

Files under `index/` are rebuildable and never canonical. Useful views include:

- `pending.json`
- `recent-runs.json`
- `environments.json`
- `capability-view.json`
- `manifest.json`

Cloud readers should prefer an index/search first, then targeted event reads.

## SQLite cache

The cache is local, WAL-enabled and rebuildable from Vault events. It must not be placed in the shared/synced canonical folder.

## Privacy

Default to metadata and references. Do not duplicate raw corpora, personal mail, sensitive datasets or full chat histories into the Vault merely for convenience.
