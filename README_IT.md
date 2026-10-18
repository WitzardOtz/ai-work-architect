# AI Work Architect v0.4.0

[English](README.md) | [Italiano](README_IT.md)

AWA aiuta a decidere **come strutturare il lavoro assistito dall'AI** prima di scegliere un modello. Scompone attività complesse, definisce passaggi di esecuzione, li abbina a strumenti/modelli/impegno di ragionamento disponibili nell'ambiente corrente, prepara passaggi di contesto quando conviene cambiare spazio o dispositivo e apprende dagli esiti senza caricare tutta la cronologia nel contesto del modello.

## Inizia da qui

**[Guida pratica in italiano](USER_GUIDE_IT.md)** — installazione, primo utilizzo, configurazione aziendale, messaggio per i colleghi, accessi, continuità e limiti.

| Situazione | Come iniziare |
|---|---|
| Primo utilizzo | Chiedere ad AWA di guidare il setup iniziale; scegliere memoria locale o condivisa. |
| Primo configuratore aziendale | Chiedere il setup del contesto e fornire fonti selezionate. Rivedere il profilo, confermare l'ambito e ricevere un messaggio copiabile per i colleghi. |
| Collega che riusa un setup | Fornire il riferimento al profilo condiviso. AWA verifica accesso e versione, poi chiede solo i dettagli mancanti sul ruolo/progetto. |
| Ripresa di un progetto | Riutilizzare checkpoint e riferimento al profilo nel suo ambito; chiarire cambiamenti rilevanti senza ricreare il setup. |

Il wizard aziendale è una guida conversazionale seguita dall'agente host, non un'applicazione ospitata. Il percorso completo è nella [configurazione del contesto aziendale](docs/it/references/organization-context-setup.md).

## Primo utilizzo guidato

AWA controlla la configurazione esistente e guida nella scelta di persistenza locale o condivisa quando necessario. Google Drive è opzionale. L'agente verifica l'adattatore disponibile, segnala limiti di accesso e riprende il task. I profili funzionanti vengono riutilizzati senza ripetere il setup. Vedere [configurazione iniziale](docs/it/references/first-run-setup.md).

## Ultimi aggiornamenti della skill — 18 ottobre 2026

- Documentazione in italiano e inglese, con versioni collegate per README, guide, istruzioni, riferimenti, ambienti e modelli. Vedere l'[indice bilingue](docs/it/README.md).
- Task brevi e verificabili, con piano, checkpoint e log nei file del progetto, permettono a un altro agente di riprendere senza ricostruire la chat o richiedere un handoff formale. Vedere il [modello di lavoro](docs/it/templates/project-work.md).
- Il [miglioramento controllato](docs/it/references/controlled-improvement.md) opzionale confronta una base recuperabile con candidate circoscritte, usa casi separati di validazione e registra decisioni e criteri di arresto. Vedere il [modello di esperimento](docs/it/templates/improvement-experiment.md).
- Il runtime resta v0.4.0. Le modifiche alle istruzioni sono sotto Unreleased nel [registro modifiche](docs/it/CHANGELOG.md). Controlli strutturali e test runtime passano; l'efficacia comportamentale comparativa non è dimostrata.

## Ottenere la skill

Clonare il repository o scaricare lo ZIP e collocare la cartella estratta, chiamata `ai-work-architect`, nella posizione delle skill supportata dall'ambiente AI. La radice contiene `SKILL.md`.

```bash
git clone https://github.com/WitzardOtz/ai-work-architect.git
```

Il repository contiene istruzioni, script, modelli e test riutilizzabili. Configurazione personale, eventi del Vault, cache e artefatti restano fuori dal pacchetto. L'installazione non collega account o configura automaticamente la persistenza condivisa: il primo setup accompagna quella scelta.

## Contesto aziendale

Chiedere: **«Aiutami a configurare il contesto della nostra azienda»**, oppure usare la propria lingua. AWA guida nella scelta di organizzazione e ambito, collegamento dei documenti o creazione del profilo, separazione di policy e preferenze, revisione delle lacune e conferma. Riutilizza i collegamenti di progetto funzionanti.

Il [wizard](docs/it/references/organization-context-setup.md) usa file locali selezionati o archivi collegati supportati; Google Drive è opzionale. Profili e indici privati restano fuori dal pacchetto pubblico. AWA recupera materiale pertinente e usa vincoli applicabili per pianificare e scegliere strumenti. Non implementa controllo accessi o garanzia di conformità; la CLI attuale non carica automaticamente questi profili gestiti dall'agente.

Dopo il primo setup riutilizzabile, AWA fornisce un messaggio copiabile per i colleghi, con riferimento al profilo e istruzione per collegare il contesto esistente. Ogni collega verifica i propri accessi; messaggi e permessi non vengono inviati o modificati automaticamente.

Modelli: [profilo aziendale](docs/it/templates/organization-profile.md), [indice delle fonti](docs/it/templates/organization-sources.md), [collegamento con ambito](templates/context-bindings.example.json). Nessun dato aziendale reale è incluso. I JSON mantengono chiavi e valori tecnici comuni alle lingue; la [spiegazione italiana](docs/it/templates/machine-examples.md) descrive gli esempi.

## Novità della v0.4

Il cambiamento principale riguarda persistenza e consapevolezza dell'ambiente.

### 1. Vault AWA immutabile

Un database SQLite vivo sincronizzato non è più lo stato canonico: questo è un insieme di **file di eventi immutabili**.

- In `LOCAL`, il Vault risiede su un dispositivo.
- In `SHARED_GOOGLE_DRIVE`, risiede in Drive ed è raggiungibile localmente tramite Drive per desktop o dal cloud con connettore verificato.
- SQLite resta una **cache/indice locale eliminabile**, ricostruibile dagli eventi.

### 2. La conoscenza è globale; la disponibilità è locale

AWA separa:

- **conoscenza globale delle risorse**: ciò che si è appreso su modelli, strumenti, skill e schemi nei vari ambienti;
- **profili delle capacità**: ciò che è realmente disponibile sul dispositivo/client/sessione;
- **evidenze delle prestazioni**: risultati delle configurazioni distinti per ambiente.

Un task può essere assegnato all'ambiente corrente o a un altro noto.

### 3. Configurazione iniziale

Al primo uso, AWA chiede una volta se la persistenza deve essere locale o condivisa tra dispositivi/ambienti.

Architettura condivisa consigliata:

```text
ChatGPT / Claude / Codex / Antigravity
                  │
                  ▼
           Google Drive /AWA
       Vault di eventi immutabili
                  │
        ┌─────────┴─────────┐
        │                   │
 cache locale        letture cloud mirate
 SQLite eliminabile  tramite connettore
```

## Pacchetto installabile

La cartella installata deve chiamarsi `ai-work-architect`, come il campo `name:` in `SKILL.md`. Gli ZIP sorgente GitHub possono estrarsi come `ai-work-architect-main`; rinominare la cartella per l'installazione.

## CLI locale

L'adattatore locale è `scripts/awa_cli.py` e usa solo la libreria standard Python. Eseguire gli esempi dalla radice della skill. I comandi sono identici in entrambe le lingue.

### Inizializzare la modalità locale

```bash
python scripts/awa_cli.py init-local \
  --device-id MY-PC \
  --environment-id antigravity-local
```

### Inizializzare la modalità Google Drive condivisa

```bash
python scripts/awa_cli.py init-shared \
  --device-id MY-PC \
  --environment-id antigravity-local \
  --vault "G:/My Drive/AWA"
```

Usare il percorso locale reale creato da Google Drive per desktop.

### Aprire, consultare e chiudere un'esecuzione

```bash
python scripts/awa_cli.py run-start \
  --project-id EXAMPLE_PROJECT \
  --task-family data-to-insight \
  --description "Interpret network metrics and identify hypotheses"

python scripts/awa_cli.py pending --project-id EXAMPLE_PROJECT

python scripts/awa_cli.py close-latest \
  --project-id EXAMPLE_PROJECT \
  --outcome FIRST_PASS_ACCEPTED
```

### Pubblicare le capacità attuali dell'ambiente

```bash
python scripts/awa_cli.py probe
```

Solo capacità aggiuntive effettivamente verificate possono essere fornite tramite JSON:

```bash
python scripts/awa_cli.py probe --extra '{"subagents":{"status":"AVAILABLE"}}'
```

### Compattare e pubblicare gli indici

```bash
python scripts/awa_cli.py compact
```

Genera viste ricostruibili sotto `AWA/index/`: `pending.json`, `recent-runs.json`, `environments.json`, `capability-view.json`. Gli eventi restano la fonte autorevole.

## Struttura del Vault

```text
AWA/
├── events/
│   └── YYYY/MM/<ULID>__<event_type>__<run>__<project>__<environment>.json
├── index/
│   ├── pending.json
│   ├── recent-runs.json
│   ├── environments.json
│   ├── capability-view.json
│   └── manifest.json
└── meta/
```

Non aggiungere contenuto ai file condivisi e non modificare eventi esistenti. Ogni nuovo fatto o transizione crea un nuovo evento.

## Ambienti cloud

Un ambiente cloud **non** necessita di SQLite locale. Deve:

1. Verificare la raggiungibilità del Vault Google Drive condiviso.
2. Leggere prima indici compatti o ricerca.
3. Recuperare solo pochi eventi pertinenti alla decisione.
4. Scrivere nuovi file immutabili se il connettore supporta la creazione.
5. Altrimenti dichiarare persistenza `DEGRADED`, senza fingere scritture riuscite.

Vedere [adattatori cloud](docs/it/references/cloud-adapters.md).

## Sicurezza tra dispositivi

Il modello degli eventi è pensato per la sincronizzazione:

- un nuovo file per evento;
- ID ULID univoci;
- nomi con caratteri sicuri;
- nessun blocco su un database condiviso;
- nessun registro condiviso a sole aggiunte;
- deduplicazione delle copie Drive tramite `event_id` durante l'indicizzazione;
- ignorare file `.tmp-*`.

## Test

```bash
python tests/smoke_test.py
python tests/regression_test.py
```

Risultati attesi:

```text
AWA v0.4.0 smoke test: PASS
AWA v0.4.0 regression test: PASS
```

## Stato del progetto

La v0.4 congela l'architettura principale per le prove reali. Le evoluzioni devono essere guidate soprattutto da esecuzioni chiuse e problemi osservati negli ambienti, non da ulteriore progettazione speculativa.

## Licenza

Copyright 2026 WitzardOtz.

Istruzioni, script, riferimenti e modelli del pacchetto AWA sono sotto [Apache License 2.0](LICENSE). Il testo legale resta quello ufficiale inglese; è disponibile una [spiegazione italiana](docs/it/LICENSE.md).

La licenza copre il pacchetto distribuito, non configurazioni private, contenuti del Vault, documenti aziendali o altri materiali degli utenti. I materiali di terze parti mantengono le proprie condizioni.
