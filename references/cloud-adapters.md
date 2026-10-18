# Cloud adapters

[English](cloud-adapters.md) | [Italiano](../docs/it/references/cloud-adapters.md)

A cloud client may not have local shell/filesystem access. Shared persistence therefore depends on a **verified cloud connector** to the same Google Drive Vault.

## Read pattern

1. retrieve/search `AWA/index/` first;
2. select only the relevant run/project/environment/capability records;
3. read a few targeted immutable event files if more detail is needed;
4. never enumerate/read the entire Vault into context.

## Write pattern

When the connector supports file creation:

1. create one new immutable JSON event file under `events/YYYY/MM/`;
2. use a newly generated unique `event_id`/ULID;
3. do not edit or append to an existing event file;
4. do not update the shared indexes from cloud unless the environment can do so safely; indexes can lag and remain rebuildable.

If the connector cannot create the event file, persistence is `DEGRADED`. Do not claim the run was logged cross-session.

## Connector differences

Connector capabilities vary by product and can change. Verify actual support for create/search/read at runtime instead of hardcoding assumptions.
