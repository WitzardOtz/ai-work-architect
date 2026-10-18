# Environment capability model

## Fundamental distinction

**Knowledge is global; availability is local.**

AWA must not equate “resource exists somewhere” with “resource is usable here”.

Use three layers:

1. **Resource Knowledge Base** — global observations about models, tools, Skills and execution patterns.
2. **Environment Capability Profile** — capabilities actually available in a specific `device_id × environment_id` pair.
3. **Session overrides** — temporary grants/mounts/connectors that may differ by session.

## Environment profile

Typical fields:

```json
{
  "environment_key": "MY-PC__antigravity-local",
  "device_id": "MY-PC",
  "environment_id": "antigravity-local",
  "last_verified": "...",
  "capabilities": {
    "python": {"status": "AVAILABLE", "version": "..."},
    "filesystem": {"status": "AVAILABLE"},
    "google_drive_vault": {"status": "AVAILABLE"},
    "subagents": {"status": "AVAILABLE"},
    "skill:foo": {"status": "AVAILABLE"}
  }
}
```

Statuses should be concrete where possible: `AVAILABLE`, `UNAVAILABLE`, `NOT_YET_GRANTED`, `UNKNOWN`, `STALE`.

## Probing

Do not ask the user about capabilities that can be checked deterministically.

Examples:

- `python --version`
- `git --version`
- filesystem path check
- Drive mount check
- installed Skill inventory
- connector health probe

Cache stable facts. Re-probe only what is stale or decision-relevant.

## Routing across environments

Conceptual rule:

```text
Task requirements
∩ global resource knowledge
∩ current environment availability
= feasible local plan
```

If the ideal plan is infeasible locally:

1. check known alternate environments;
2. if a better verified environment exists, recommend `HANDOFF_TO_ENVIRONMENT`; reuse accessible project plan/checkpoint/log files, and produce a Handoff Pack only when the destination needs context or access not provided there;
3. otherwise adapt the execution plan locally.

Do not route to an alternate environment merely because its last known profile says a capability existed long ago. Respect `last_verified` and confidence.
