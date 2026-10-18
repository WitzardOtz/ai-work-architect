# Task decomposition

## Task boundary

A Task is the smallest logical unit that stably owns:

- objective;
- input set;
- dominant transformation;
- evaluable output;
- success criterion.

A tool change inside the same objective does not automatically create a new Task.

## Decomposition engine

1. define final output;
2. backward-chain indispensable intermediate outputs;
3. form candidate Tasks;
4. compare execution contracts;
5. split/merge based on routing benefit vs handoff cost;
6. build dependencies;
7. add validation/human gates;
8. detect repeated patterns / Skill opportunities.

## Boundary heuristics

Split more readily when there is a change in:

- independently reusable output;
- quality gate;
- context corpus;
- independence requirement;
- owner/workspace/environment;
- failure propagation risk.

Do not atomize simple operations such as search -> open -> read -> extract when they form one coherent retrieval task.
