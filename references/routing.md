# Routing

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
2. hard constraints;
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
