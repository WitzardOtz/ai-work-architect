# Repository instructions

[English](AGENTS.md) | [Italiano](docs/it/AGENTS.md)

## Bilingual documentation

Maintain all human-readable documentation in English and Italian. Update both language versions together when changing behavior, constraints, setup or usage. Keep reciprocal language links and register every pair in `docs/languages.json` and both documentation indexes. English files keep their existing paths; Italian reference translations mirror them under `docs/it/`, with `README_IT.md` and `USER_GUIDE_IT.md` at the root.

Preserve executable commands, API/JSON keys, enum values, identifiers and paths across translations. Machine-readable examples and code remain shared interfaces; explain their use in both languages. Keep the official Apache legal text in `LICENSE` unchanged and clearly separate explanatory pages from that text. The installed entrypoint is root `SKILL.md`; its Italian counterpart is documentation, not a second installable skill, and is named `docs/it/SKILL_IT.md` because upload-based hosts reject a package containing two files named `SKILL.md`.

Before publishing documentation, check paired coverage, local links and command/JSON example consistency. Check the skill frontmatter if changing `SKILL.md`. Structural checks do not establish behavioral efficacy. Keep personal configuration, company documents, Vault events, caches and private run artifacts out of this repository.

## Release checks

Run `python tests/smoke_test.py`, `python tests/regression_test.py` and `python tests/package_check.py` before publishing. The version is `VERSION` in `scripts/awa_vault.py`; `MANIFEST.json`, `SKILL.md`, `docs/it/SKILL_IT.md`, both README titles and the event examples must match it, and the package check fails when they disagree. Keep model names, prices and benchmark claims out of the skill; dated environment notes belong in `environments/` with a review date.
