# Istruzioni del repository

[English](../../AGENTS.md) | [Italiano](AGENTS.md)

## Documentazione bilingue

Mantenere tutta la documentazione destinata alla lettura in inglese e italiano. Aggiornare entrambe le versioni quando cambiano comportamento, vincoli, setup o utilizzo. Conservare collegamenti reciproci e registrare ogni coppia in `docs/languages.json` e nei due indici documentali. I file inglesi mantengono i percorsi esistenti; le traduzioni dei riferimenti rispecchiano la struttura sotto `docs/it/`, con `README_IT.md` e `USER_GUIDE_IT.md` nella radice.

Preservare comandi eseguibili, chiavi API/JSON, valori degli stati, identificatori e percorsi tra le lingue. Esempi leggibili dal software e codice restano interfacce condivise; spiegarne l'utilizzo in entrambe le lingue. Conservare invariato il testo legale ufficiale Apache in `LICENSE`, distinguendo le pagine esplicative. Il punto di ingresso installato è `SKILL.md` nella radice; la controparte italiana è documentazione, non una seconda skill installabile, e si chiama `docs/it/SKILL_IT.md` perché gli host che installano tramite caricamento rifiutano un pacchetto con due file chiamati `SKILL.md`.

Prima di pubblicare, verificare copertura delle coppie, link locali e coerenza di comandi/esempi JSON. Controllare i metadati iniziali della skill se cambia `SKILL.md`. Le verifiche strutturali non dimostrano efficacia comportamentale. Escludere dal repository configurazione personale, documenti aziendali, eventi Vault, cache e artefatti privati delle esecuzioni.

## Controlli prima del rilascio

Eseguire `python tests/smoke_test.py`, `python tests/regression_test.py` e `python tests/package_check.py` prima di pubblicare. La versione è `VERSION` in `scripts/awa_vault.py`; `MANIFEST.json`, `SKILL.md`, `docs/it/SKILL_IT.md`, i titoli dei due README e gli esempi di evento devono coincidere con essa, e l'autoverifica del pacchetto fallisce se divergono. Tenere nomi di modelli, prezzi e risultati di benchmark fuori dalla skill; le note datate sugli ambienti vanno in `environments/` con data di revisione.
