# Registro delle modifiche

[English](../../CHANGELOG.md) | [Italiano](CHANGELOG.md)

## Unreleased — 18 ottobre 2026

- Rendere bilingue la documentazione: README, guide pratiche, istruzioni della skill, riferimenti operativi, note sugli ambienti e modelli in inglese e italiano, con collegamenti tra le versioni e indice di copertura. Gli identificatori tecnici restano invariati e il testo legale Apache resta quello ufficiale inglese, con spiegazione italiana separata.
- Fornire al primo configuratore un messaggio copiabile per i colleghi con riferimento condiviso verificato. Gli utenti successivi riusano il contesto aziendale verificando accessi e ambito propri. Riferimenti solo locali producono una bozza esplicita, non una falsa promessa di condivisione.
- Aggiungere il wizard aziendale opzionale: collegare fonti selezionate o creare profili privati, separare vincoli e preferenze, rivedere e attivare per progetto/spazio di lavoro, aggiornare o scollegare senza azzerare la persistenza.
- Aggiungere modelli di profilo aziendale, indice delle fonti e collegamento; integrare i vincoli nel setup, nella scelta delle risorse e nei checkpoint. L'installazione non configura alcuna azienda; i contenuti privati sono esclusi dal pacchetto pubblico e dall'apprendimento globale.
- Distribuire il pacchetto AWA sotto Apache-2.0, aggiungendo licenza completa e metadati. I materiali privati degli utenti non rientrano nella concessione.
- Correggere su Windows la sostituzione di configurazione e indici derivati modificabili, preservando il comportamento di scrittura degli eventi. Aggiungere controlli di regressione per compattazioni ripetute, salvataggio della configurazione ed eventi storici invariati.
- Aggiungere il setup conversazionale iniziale: esaminare profili esistenti, guidare locale/condiviso, verificare ciclo di scrittura/rilettura e distinguere accesso locale e sincronizzazione tra dispositivi. Drive resta opzionale e i problemi non azzerano la configurazione.
- Aggiungere miglioramento controllato opzionale: confronti circoscritti base/candidata, casi separati di validazione, decisioni ADOPT/REVISE/REJECT/KEEP_BASE, budget, condizioni di arresto e riferimenti di ripristino.
- Aggiungere modello di esperimento e metadati comparativi negli eventi Vault esistenti, senza cambiare schemi runtime, esiti e regole contro l'apprendimento silenzioso.
- Attribuire l'ispirazione progettuale a Harness2 senza importarne runtime o rivendicare trasferimenti dei guadagni dei benchmark. Distinguere validità strutturale ed efficacia comportamentale.
- Rendere predefiniti task brevi e verificabili con piano/checkpoint/log nei file del progetto per lavoro distribuito tra sessioni, quote, modelli o agenti.
- Salvare progressi parziali e risultati osservati durante il lavoro affinché un altro agente riprenda dai file.
- Riutilizzare lo stato condiviso del progetto senza un Handoff Pack formale a ogni cambio di modello o ambiente.
- Preservare autorizzazioni, responsabilità attive, privacy e Vault immutabile; non implicare parallelismo o interruzioni quando l'utente esprime una preferenza futura.

## 0.4.0

- Sostituire SQLite vivo sincronizzato come stato canonico con un Vault di eventi immutabili.
- Aggiungere profili di persistenza `LOCAL` e `SHARED_GOOGLE_DRIVE`.
- Aggiungere scelta iniziale una tantum.
- Aggiungere ID ULID e nomi di file sicuri per la sincronizzazione.
- Aggiungere cache/indice SQLite locale eliminabile e ricostruibile dagli eventi.
- Aggiungere indici compatti per recupero efficiente da cloud e in termini di token.
- Separare conoscenza globale delle risorse e disponibilità locale per dispositivo × ambiente.
- Aggiungere profili delle capacità con `last_verified` e metadati di sessione opzionali.
- Aggiungere alternative nella scelta delle risorse: adattamento locale o passaggio a un ambiente noto con la capacità richiesta.
- Aggiungere comandi `awa_cli.py` per ciclo delle esecuzioni, verifiche ambiente, osservazioni su capacità/skill/schemi, compattazione e interrogazioni mirate.
- Rinviare l'Hub HTTPS a opzione futura non obbligatoria, fuori dal runtime v0.4 attivo.
- Preservare Handoff Pack, Task Signature, scomposizione, scelta per passaggio, verifica e apprendimento delle versioni v0.3.x.
