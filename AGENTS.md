# Repository instructions

[English](AGENTS.md) | [Italiano](docs/it/AGENTS.md)

## Bilingual documentation

Maintain all human-readable documentation in English and Italian. Update both language versions together when changing behavior, constraints, setup or usage. Keep reciprocal language links and register every pair in `docs/languages.json` and both documentation indexes. English files keep their existing paths; Italian reference translations mirror them under `docs/it/`, with `README_IT.md` and `USER_GUIDE_IT.md` at the root.

Preserve executable commands, API/JSON keys, enum values, identifiers and paths across translations. Machine-readable examples and code remain shared interfaces; explain their use in both languages. Keep the official Apache legal text in `LICENSE` unchanged and clearly separate explanatory pages from that text. The installed entrypoint is root `SKILL.md`; its Italian counterpart is documentation, not a second installable skill.

Before publishing documentation, check paired coverage, local links and command/JSON example consistency. Check the skill frontmatter if changing `SKILL.md`. Structural checks do not establish behavioral efficacy. Keep personal configuration, company documents, Vault events, caches and private run artifacts out of this repository.
