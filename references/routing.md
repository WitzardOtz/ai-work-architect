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

## Resource knowledge currency

Names, prices, limits and features of models and tools are perishable and are deliberately kept out of this skill. Evidence for a concrete choice, in order of preference:

1. what the current environment verifiably offers now (model picker, tool inventory, provider documentation consulted in the session);
2. dated observations in the Vault (`query-context`), read with their environment and date;
3. the host model's built-in knowledge, treated as possibly outdated.

Treat an observation as stale when a newer generation of that resource exists, or as a rule of thumb when it is older than about three months, and re-verify before a decision depends on it. If no current evidence is available, recommend the resource class and effort level, name a specific model only as an unverified suggestion, and say what would confirm it. After a run closes, record what was learned (see [logging-learning.md](logging-learning.md)). An empty registry means no evidence, not a neutral default.

## Organizational context

For a bound organization, use [organization-context-setup.md](organization-context-setup.md). Read the compact profile and verify its scope/revision before resource selection. Intersect task requirements with both verified capabilities and applicable permissions. An available tool is not automatically allowed. Retrieve only relevant sources; preserve unknowns, surface conflicts and stop only the affected action when required permission cannot be established. Keep preferences subordinate to applicable mandatory constraints and governing host instructions.
