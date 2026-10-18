# Testing protocol

After installation, test the environment rather than only reviewing the Skill.

Minimum checks:

1. initialize local/shared profile;
2. publish environment profile;
3. open run;
4. `pending` finds it;
5. recommendation/execution events are written;
6. `close-latest` closes it;
7. `compact` generates indexes;
8. delete local cache and `rebuild-cache`; reconstructed state must match;
9. two distinct environments can write different immutable events to the same shared Vault;
10. query-context returns compact evidence, not the whole Vault.

Real validation should include:

- simple task that must not be over-architected;
- hybrid deterministic-compute -> LLM task;
- long project requiring decomposition/handoff.

Prefer 5–10 real runs before redesigning the architecture again, unless a blocking bug appears.

## Optional improvement experiments

When evaluating an AWA change, follow [controlled-improvement.md](controlled-improvement.md). Fix criteria and budget before execution, compare a preserved baseline and candidate, and use separate validation cases. Recheck a composed candidate. Existing runtime tests and the skill validator verify structure/runtime compatibility; they do not establish that routing, decomposition or user outcomes improved. Record behavioral efficacy as not tested until an actual comparison supports it.
