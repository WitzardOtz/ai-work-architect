# Logging and learning

[English](logging-learning.md) | [Italiano](../docs/it/references/logging-learning.md)

## Observability

A substantive AWA invocation should create a compact persistent run trace when canonical storage is reachable.

The event Vault is the evidence base. Aggregate registries are derived views.

## Recommendation vs actual

Always preserve the distinction between:

- what AWA recommended ex ante;
- what was actually executed;
- any user/environment override.

## Run outcomes

- FIRST_PASS_ACCEPTED
- MINOR_CORRECTION
- MAJOR_CORRECTION
- REROUTED
- FAILED
- ABANDONED
- OUTCOME_UNKNOWN

A run with `run.started` and no `run.closed` is projected as `PENDING`.

## Failure classes

Useful categories include factual, reasoning, coverage, instruction, context, tool, format, hallucination, style, efficiency, architecture and routing.

## Recording observations

Run events alone do not populate the resource registry. When a closed run gives usable evidence about a model, tool, Skill or execution pattern, record it as a separate observation and query it later:

```text
python scripts/awa_cli.py observe-capability --resource-id <model-or-tool> --task-family <family> --capability <capability> --assessment <STRONG|ADEQUATE|WEAK> --confidence <LOW|MEDIUM|HIGH> --evidence-type <run|comparison|documentation>
python scripts/awa_cli.py observe-skill --skill-id <skill> --version <version> --outcome <outcome>
python scripts/awa_cli.py observe-pattern --pattern-id <pattern> --version <version> --outcome <outcome>
python scripts/awa_cli.py query-context --task-family <family> --capability <capability>
```

The current CLI stores `assessment`, `confidence`, `evidence-type` and `outcome` as free text; the values shown are a suggested vocabulary, not an enforced one. Use the resource's exact identifier, put effort and context strategy in `--configuration` (JSON), and keep notes compact and free of sensitive content. Each observation carries its environment and date; read both before reusing it.

## Learning governance

```text
observation -> repeated pattern -> policy candidate -> policy update
```

Do not alter default routing from one isolated run. Preserve evidence provenance, environment and date.

## Controlled comparisons

For requested experiments or recurring problems, use [controlled-improvement.md](controlled-improvement.md). Link baseline/candidate versions, comparison evidence, decision scope and rollback reference through existing run events. Experiment decisions (`ADOPT`, `REVISE`, `REJECT`, `KEEP_BASE`) are payload metadata, not new run outcomes. Keep structural checks, behavioral evidence and user acceptance distinct. Findings remain scoped observations until repeated evidence supports broader use.

## Token discipline

Logging itself should be deterministic and compact. The model should never reread full logs merely to continue a task. Use compact indexes / targeted queries.
