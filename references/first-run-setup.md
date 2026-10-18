# Guided first-run setup

Use on first use, an explicit setup/reconfiguration request, or a persistence failure. Keep the conversation brief and in the user's language. Ask only for information that changes the next step; one decision at a time is usually enough. Setup supports the current task rather than replacing it.

## Optional personal or organization context

Context setup is independent of storage setup. On first use in an unknown scope, ask whether AWA is being used personally or for an organization; reuse an explicit existing choice. Organizational use follows [organization-context-setup.md](organization-context-setup.md) to connect sources or build and confirm a private profile. An explicit company-context request enters that path even when persistence is already configured. Personal use skips it. Do not repeat a healthy scoped profile or treat an existing Vault configuration as a company-policy configuration. If a storage failure is being repaired, resolve that failure without forcing unrelated context onboarding.

## 1. Inspect before asking

Verify the current environment's actual shell/Python/filesystem or connector access. Do not assume that a product name implies capabilities. For local clients, inspect the configuration selected by `AWA_CONFIG_PATH`, otherwise `~/.ai-work-architect/config.json`. Do not expose credentials or dump configuration into chat.

- Existing healthy configuration: report the mode briefly and continue. Do not repeat the initial choice or reset settings.
- Existing configuration with unreachable storage: preserve it, explain the failed check, and offer reconnection or a separate local profile. Do not silently create a second canonical Vault or fall back to local while claiming shared persistence.
- Missing configuration: ask the first-run local/shared question in SKILL.md. Explain that local mode is sufficient for one device; shared mode supports continuity across environments that can actually reach the same Vault.

## 2. Configure the chosen path

### Local mode with a verified Python/filesystem adapter

Use the bundled CLI. Select stable device/environment identifiers from verified metadata or ask if ambiguous. Use the CLI's default local Vault unless the user chooses another location. A typical configuration is:

```text
python scripts/awa_cli.py init-local --device-id MY-PC --environment-id local-agent
```

Run from the skill directory or use the script's absolute location. Use actual identifiers, not the example values. Configuration initialization writes files; perform it only within the user's selected setup mode and accessible storage.

### Shared mode with a locally synced Google Drive folder

Check whether Drive for Desktop and the intended synced folder are available. Ask for the actual Vault folder when it cannot be established from configuration or user-provided context. Do not infer a drive letter, search unrelated personal folders, install Drive, or connect an account automatically.

If the user already has an AWA Vault, reuse it; inspect only necessary metadata. Keep the SQLite cache outside synced storage. Configure using the actual path, for example:

```text
python scripts/awa_cli.py init-shared --device-id MY-PC --environment-id local-agent --vault "G:/My Drive/AWA"
```

The CLI's init commands overwrite the selected configuration. Do not invoke them on an existing profile unless the user requests that change. Use a separate `--config` path for an intentionally separate profile; do not treat this as migration of existing events.

### Cloud or connector-only environments

Follow [cloud-adapters.md](cloud-adapters.md). Verify the connector's read/search/create capabilities and the exact user-selected Vault reference. Never invent a local filesystem path or run local initialization where unavailable. If discovery metadata cannot persist, retain the setup reference only for the current session and say future sessions may need it again.

If account connection or missing access requires human action, explain the concrete step and keep independent task work moving. A read-only connector can consult evidence but cannot satisfy persistence. Report `DEGRADED` for writes. Do not claim unsupported connectors or automatic multi-device synchronization.

## 3. Verify the configured adapter

For a new configuration, validate with one minimal metadata-only round trip using a unique setup run:

1. Check `status` and the detected environment profile. Publish a fresh `probe` when availability needs refreshing.
2. Use `run-start --project-id AWA_SETUP --task-family setup-verification` with a short setup description. Retain the returned run ID.
3. Confirm `pending` contains that exact run ID through the selected storage adapter.
4. Close that run by ID with `OUTCOME_UNKNOWN`, noting that the storage check is complete and user acceptance is not yet known. Confirm it is no longer pending. With the local CLI, run `compact` so connector readers have fresh derived indexes.

These commands are under `scripts/awa_cli.py`; use `--help` for their exact arguments. Prefer the existing CLI rather than hand-writing events. A connector-only adapter uses equivalent immutable events and targeted reads from cloud-adapters.md. If a check fails, record what passed and what remains unavailable; never fabricate a successful close. Do not repeatedly create setup runs when the same access failure persists.

Local read/write success proves that adapter only. Cross-device continuity is unverified until a second environment reads the same unique event; do not claim that a locally synced folder alone proves remote synchronization. Existing healthy profiles need a health check only when relevant, not a new test run for every task.

## 4. Explain the result and next step

Give a short result in plain language:

- chosen mode and verified storage location/reference;
- capabilities actually checked, and any remaining access or sync limitation;
- what AWA will retain: compact metadata and references, not raw sensitive material;
- whether setup is ready locally, ready through the connector, or degraded, and the next concrete user action if needed.

Keep technical diagnostics available on request. Do not claim that setup validates AWA's decision quality. Never store credentials in the Vault or publish personal configuration, events or caches with the skill.
