# Istruzioni del repository

[English](../../AGENTS.md) | [Italiano](AGENTS.md)

## Documentazione bilingue

Mantenere tutta la documentazione destinata alla lettura in inglese e italiano. Aggiornare entrambe le versioni quando cambiano comportamento, vincoli, setup o utilizzo. Conservare collegamenti reciproci e registrare ogni coppia in `docs/languages.json` e nei due indici documentali. I file inglesi mantengono i percorsi esistenti; le traduzioni dei riferimenti rispecchiano la struttura sotto `docs/it/`, con `README_IT.md` e `USER_GUIDE_IT.md` nella radice.

Preservare comandi eseguibili, chiavi API/JSON, valori degli stati, identificatori e percorsi tra le lingue. Esempi leggibili dal software e codice restano interfacce condivise; spiegarne l'utilizzo in entrambe le lingue. Conservare invariato il testo legale ufficiale Apache in `LICENSE`, distinguendo le pagine esplicative. Il punto di ingresso installato è `SKILL.md` nella radice; la controparte italiana è documentazione, non una seconda skill installabile.

Prima di pubblicare, verificare copertura delle coppie, link locali e coerenza di comandi/esempi JSON. Controllare i metadati iniziali della skill se cambia `SKILL.md`. Le verifiche strutturali non dimostrano efficacia comportamentale. Escludere dal repository configurazione personale, documenti aziendali, eventi Vault, cache e artefatti privati delle esecuzioni.
