# Routing

[English](routing.md) | [Italiano](../docs/it/references/routing.md)

## Capability requirements before resource names

Translate the Task Signature into required/important/optional capabilities, then build the Execution Plan.

Execution classes:

- retrieval
- deterministic compute
- semantic transformation
- reasoning
- generation
- validation

## Step-level routing

For each step:

1. resource class;
2. hard constraints, including applicable confirmed organizational policy;
3. current environment feasibility;
4. local adaptation vs handoff;
5. global performance evidence if needed;
6. context strategy;
7. concrete configuration;
8. verification;
9. fallback/escalation.

## Invariants

- deterministic before probabilistic;
- retrieve before loading;
- structure before expensive reasoning;
- verification should match epistemology;
- model × effort × environment matters more than model name alone;
- optimize Total Cost to Accepted Output, not raw call price.

## Organizational context

For a bound organization, use [organization-context-setup.md](organization-context-setup.md). Read the compact profile and verify its scope/revision before resource selection. Intersect task requirements with both verified capabilities and applicable permissions. An available tool is not automatically allowed. Retrieve only relevant sources; preserve unknowns, surface conflicts and stop only the affected action when required permission cannot be established. Keep preferences subordinate to applicable mandatory constraints and governing host instructions.
