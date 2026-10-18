# Machine-readable examples

[English](machine-examples.md) | [Italiano](../docs/it/templates/machine-examples.md)

JSON keys, command names, enum values, file paths and version identifiers stay the same in both languages so the examples remain compatible with the software. These are illustrative templates, not your configured environment. Do not copy example availability claims or identities as verified facts.

## Persistence configuration

[config.example.json](config.example.json) contains `schema_version`, `mode`, `vault_root`, `device_id`, `environment_id` and `shared_provider`. Replace the example path and identifiers with verified values chosen during setup. `LOCAL` stores the Vault on one device; `SHARED_GOOGLE_DRIVE` requires the selected Drive location. Prefer the setup CLI to hand-editing configuration; init can overwrite an existing selected profile.

## Environment profile

[environment-profile.example.json](environment-profile.example.json) identifies the `device_id × environment_id` pair through `environment_key`. `last_verified` records when capabilities were checked. Each entry in `capabilities` has a status and may include a version. `AVAILABLE` requires actual evidence; `UNKNOWN` does not authorize use. Do not treat the example's date or installed capabilities as current facts.

## Event

[event.example.json](event.example.json) illustrates an event header and payload. `event_id` and `run_id` must be fresh valid identifiers, not the literal example strings. `occurred_at` records the UTC timestamp; `event_type` identifies the transition. Version fields identify the schema and architect. Environment/device/project/task fields scope the record; `summary` and `payload.description` are compact metadata. Keep sensitive raw inputs out of them. Events are immutable; use the existing CLI or a verified adapter.

## Organization-context binding

[context-bindings.example.json](context-bindings.example.json) is a private, agent-managed companion format, not a configuration read by `awa_cli.py`. `bindings` scopes choices through `scope_ref` and `mode`. An organization uses its ID, profile and source-index references, observed revision/hash and confirmation time. The example has personal mode, null organization fields and `unconfigured` status; it activates no company. Preserve other scope entries when changing one. Sharing a profile does not share user permissions.

## Package metadata

[MANIFEST.json](../MANIFEST.json) describes the distributed skill: name, version, entrypoint, persistence architecture/profiles, Python dependency approach and license. It is package metadata, not a place for user/company configuration or credentials.
