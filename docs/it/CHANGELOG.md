# Registro delle modifiche

[English](../../CHANGELOG.md) | [Italiano](CHANGELOG.md)

## 0.5.0 — 12 novembre 2026

- Rilasciare le modifiche alle istruzioni finora elencate come non rilasciate (sotto) e aggiornare la versione del runtime, così che le copie installate siano distinguibili. Gli schemi di configurazione, eventi e cache restano invariati.
- Correggere la dipendenza dello stato delle esecuzioni dall'ordine di acquisizione dei file di eventi. Una ricostruzione della cache o una sincronizzazione fuori ordine poteva lasciare in sospeso esecuzioni chiuse e perderne i dati di raccomandazione/esecuzione; il test di base falliva in modo intermittente per questo motivo. Lo stato deriva ora da tutti gli eventi dell'esecuzione, prevale il profilo d'ambiente verificato più di recente e le cache costruite con la logica precedente vengono ricostruite automaticamente. File di eventi e schemi restano invariati.
- Aggiungere una regola esplicita sulla deperibilità della conoscenza di modelli e strumenti: verificare l'offerta dell'ambiente corrente prima di indicare una risorsa e segnalare come tali i nomi non verificati.
- Documentare i comandi di osservazione (`observe-capability`, `observe-skill`, `observe-pattern`, `query-context`); gli eventi delle esecuzioni non costruiscono da soli la conoscenza delle risorse.
- Rinominare la traduzione italiana della skill in `docs/it/SKILL_IT.md`: un pacchetto con due file chiamati `SKILL.md` viene rifiutato dagli host che installano tramite caricamento, quindi la cartella completa non era installabile lì.
- Richiamare da `SKILL.md` la CLI inclusa e tutti i file di supporto, e definire il comportamento di un'installazione con il solo `SKILL.md`.
- Rivedere i profili degli ambienti Claude, Codex e Antigravity (sessioni Cowork nel cloud, agenti remoti, funzioni multi-agente) e aggiungere le date di revisione.
- Indicare `project.updated` e `artifact.registered` come nomi di evento riservati, non scritti dalla CLI attuale.
- CLI: aggiungere `--version`; segnalare configurazione mancante, esito non valido o JSON non valido con un errore di una riga e codice di uscita 2.
- Aggiungere `tests/package_check.py` e un flusso di integrazione continua; i test stampano la versione letta dal codice. Dichiarare il requisito Python (3.9+).

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
