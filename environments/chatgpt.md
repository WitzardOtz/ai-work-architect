# ChatGPT environment profile

Treat each ChatGPT surface as a distinct environment.

## Cloud chat

Do not assume local filesystem or local Python. If a Google Drive connector is available and can access the shared AWA Vault, use the cloud adapter protocol: index/search first, targeted reads, immutable event creation if supported.

If Drive is not connected or cannot create/read Vault records, persistence is `DEGRADED` for that session.

## Work / computer-enabled modes

Capabilities can differ materially from ordinary chat. Verify actual browser/computer/file/plugin availability before routing.

## Skills/plugins

Use the actual environment inventory. A Skill or connector available elsewhere does not imply availability in this session.
