# AI Work Architect v0.6.1

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

## Ultima versione — v0.6.1, 19 novembre 2026

- Pacchetti pronti per ogni ambiente, allegati a ogni versione pubblicata: uno per Codex, con un manifest che mostra la versione giusta, e uno per Claude, Claude Code, Antigravity e altri agenti. Vedere [Ottenere la skill](#ottenere-la-skill).

- Documentazione in italiano e inglese, con versioni collegate per README, guide, istruzioni, riferimenti, ambienti e modelli. Vedere l'[indice bilingue](docs/it/README.md).
- Task brevi e verificabili, con piano, checkpoint e log nei file del progetto, permettono a un altro agente di riprendere senza ricostruire la chat o richiedere un handoff formale. Vedere il [modello di lavoro](docs/it/templates/project-work.md).
- Il [miglioramento controllato](docs/it/references/controlled-improvement.md) opzionale confronta una base recuperabile con candidate circoscritte, usa casi separati di validazione e registra decisioni e criteri di arresto. Vedere il [modello di esperimento](docs/it/templates/improvement-experiment.md).
- AWA consulta il [registro pubblico delle risorse](https://github.com/WitzardOtz/awa-resource-registry) prima di indicare un modello: che cosa esiste e che cosa hanno misurato altri, con date e fonti. Il tuo Vault stabilisce che cosa ha funzionato per te; vedere [come si combinano](docs/it/references/resource-registry.md).
- La conoscenza di modelli e strumenti è trattata come deperibile: AWA verifica che cosa offre l'ambiente corrente prima di indicare una risorsa, e i [comandi di osservazione](docs/it/references/logging-learning.md) che ne costruiscono le evidenze sono documentati.
- I profili degli ambienti Claude, Codex e Antigravity sono stati rivisti e datati; `SKILL.md` richiama ora la CLI e tutti i file di supporto.
- Tutte le modifiche sono nel [registro modifiche](docs/it/CHANGELOG.md). Controlli strutturali e test runtime passano; l'efficacia comportamentale comparativa non è dimostrata.

## Ottenere la skill

Scaricare il pacchetto pronto per il proprio ambiente dall'[ultima versione pubblicata](https://github.com/WitzardOtz/ai-work-architect/releases/latest):

| Ambiente | Pacchetto | Come installare |
|---|---|---|
| Codex (app desktop di ChatGPT) | [`ai-work-architect-codex-plugin.zip`](https://github.com/WitzardOtz/ai-work-architect/releases/latest/download/ai-work-architect-codex-plugin.zip) | In Personalizza aprire Plugin, scegliere Aggiungi e caricare lo ZIP. Codex mostra la versione di AWA letta dal manifest del plugin. |
| App Claude (claude.ai, desktop) | [`ai-work-architect-skill.zip`](https://github.com/WitzardOtz/ai-work-architect/releases/latest/download/ai-work-architect-skill.zip) | Caricare lo ZIP dove l'app accetta le skill. |
| Claude Code, Antigravity e altri agenti che leggono una cartella di skill | [`ai-work-architect-skill.zip`](https://github.com/WitzardOtz/ai-work-architect/releases/latest/download/ai-work-architect-skill.zip) | Estrarlo nella cartella delle skill dell'agente, in modo da ottenere `.../skills/ai-work-architect/SKILL.md`. Claude Code legge `~/.claude/skills/`. Nelle installazioni di Antigravity osservate, le skill globali sono in `~/.gemini/config/skills/`; controllare l'elenco delle skill dell'agente dopo un riavvio. |

I due pacchetti contengono la stessa skill completa: `SKILL.md` rimanda a file sotto `references/`, `templates/`, `environments/` e `scripts/`, quindi non installare il solo `SKILL.md`. Una copia installata non si aggiorna da sola: dopo ogni nuova versione installare il nuovo pacchetto. Le istruzioni non richiedono alcun runtime; la CLI locale opzionale richiede Python 3.9 o successivo e usa solo la libreria standard.

Chi sviluppa può anche clonare il repository. Gli archivi automatici "Source code" di GitHub si estraggono come `ai-work-architect-main` e non hanno il manifest per Codex: per l'installazione usare i pacchetti indicati sopra.

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

La cartella installata deve chiamarsi `ai-work-architect`, come il campo `name:` in `SKILL.md`. I due pacchetti delle versioni pubblicate si creano con:

```bash
python scripts/build_release.py
```

Il comando scrive `dist/ai-work-architect-skill.zip` e `dist/ai-work-architect-codex-plugin.zip`. Il pacchetto per Codex aggiunge `.codex-plugin/plugin.json`, la cui `version` viene dal codice, così Codex mostra la versione giusta. Sono inclusi solo i file del pacchetto; configurazione privata, dati del Vault e cache non vengono mai inseriti.

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

### Registrare e interrogare le evidenze

```bash
python scripts/awa_cli.py observe-capability \
  --resource-id EXAMPLE_MODEL \
  --task-family data-to-insight \
  --capability long-context-synthesis \
  --assessment ADEQUATE --confidence LOW --evidence-type run

python scripts/awa_cli.py query-context --task-family data-to-insight
```

Gli eventi delle esecuzioni non costruiscono da soli la conoscenza delle risorse: lo fanno le osservazioni. Vedere [tracciamento e apprendimento](docs/it/references/logging-learning.md).

### Consultare e riparare

```bash
python scripts/awa_cli.py --version
python scripts/awa_cli.py status
python scripts/awa_cli.py env-list
python scripts/awa_cli.py rebuild-cache
```

Ogni comando accetta `--help`. Una configurazione mancante o un input non valido producono un errore di una riga e codice di uscita 2.

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
python tests/package_check.py
```

Risultati attesi:

```text
AWA v0.6.1 smoke test: PASS
AWA v0.6.1 regression test: PASS
AWA v0.6.1 package check: PASS
```

I primi due esercitano il runtime in cartelle temporanee. Il terzo controlla la struttura del pacchetto: metadati iniziali, link locali, coppie linguistiche e coerenza della versione.

## Stato del progetto

La v0.4 congela l'architettura principale per le prove reali. Le evoluzioni devono essere guidate soprattutto da esecuzioni chiuse e problemi osservati negli ambienti, non da ulteriore progettazione speculativa.

## Licenza

Copyright 2026 WitzardOtz.

Istruzioni, script, riferimenti e modelli del pacchetto AWA sono sotto [Apache License 2.0](LICENSE). Il testo legale resta quello ufficiale inglese; è disponibile una [spiegazione italiana](docs/it/LICENSE.md).

La licenza copre il pacchetto distribuito, non configurazioni private, contenuti del Vault, documenti aziendali o altri materiali degli utenti. I materiali di terze parti mantengono le proprie condizioni.
