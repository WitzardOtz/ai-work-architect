---
name: ai-work-architect
license: Apache-2.0
description: >-
  Progettare il lavoro assistito dall'AI prima dell'esecuzione. Usare per decidere come affrontare task o progetti, scomporre attività complesse di ricerca, estrazione, analisi dati, codice, scrittura e verifica o più spazi di lavoro, scegliere modelli/strumenti/impegno di ragionamento/contesto, decidere se creare o riusare una skill, ottimizzare qualità e costi o configurare contesto e policy aziendali. La conoscenza di AWA è condivisa, la disponibilità è locale. La memoria operativa può persistere localmente o in un Vault Google Drive condiviso tramite file di eventi immutabili.
---

# AI Work Architect

[English](../../SKILL.md) | [Italiano](SKILL.md)

Versione: 0.4.0

## Missione

Aiutare l'utente a decidere **come svolgere il lavoro** prima di scegliere il modello.

Ottimizzare per **output accettati con qualità e rischio adeguati e minimo calcolo non necessario**. La scelta del modello viene dopo l'architettura del lavoro.

## Regole fondamentali

1. **Scomporre prima di assegnare risorse.** Risultato → lavoro → piano di esecuzione → risorse.
2. **Un task non equivale a una chiamata al modello.** Può includere Python/SQL/recupero delle informazioni e interpretazione LLM.
3. **Il passaggio di esecuzione è l'unità di assegnazione.** Scegliere modello, strumento, impegno di ragionamento e contesto per ogni passaggio.
4. **Deterministico prima del probabilistico** quando esiste un metodo deterministico.
5. **Recuperare prima di caricare.** Non caricare interi corpora o registri solo perché esistono.
6. **Verificare non significa ragionare di più.** Adattare la verifica alla natura dell'output.
7. **Architettura minima sufficiente.** Non creare burocrazia di progetto per lavori semplici.
8. **La conoscenza è globale, la disponibilità è locale.** Le evidenze condivise possono provenire da ogni ambiente, ma le scelte devono usare capacità verificate nel dispositivo/ambiente/sessione corrente.
9. **Osservabilità senza gonfiare il contesto.** Ogni uso sostanziale di AWA crea o aggiorna una traccia persistente compatta quando la persistenza funziona. Non caricare interamente i log nel contesto.
10. **Nessun apprendimento silenzioso.** Una singola esecuzione è evidenza, non regola.
11. **Riprendere dai file del progetto.** Per progetti su più sessioni, usare task brevi e verificabili con piano, checkpoint e registro mantenuti nei file, affinché un altro agente prosegua senza ricostruire la chat o richiedere un passaggio formale.

## 0. Configurazione iniziale della persistenza

Al primo uso, per una richiesta di setup o un errore di persistenza, seguire [references/first-run-setup.md](references/first-run-setup.md): esaminare la configurazione esistente, guidare la scelta locale/condivisa solo se non configurata, verificare l'archivio e dichiarare cosa funziona realmente. È un setup conversazionale, non una UI separata o un collegamento Drive obbligatorio. Con configurazione funzionante, continuare il lavoro senza ripetere l'onboarding.

Se manca una configurazione della persistenza, chiedere **una sola volta**:

> Vuoi usare stato dei progetti e storico delle prestazioni di AWA su più dispositivi e ambienti AI?
>
> - **No — modalità locale:** AWA conserva il Vault solo su questo dispositivo.
> - **Sì — modalità condivisa:** usare un **Vault AWA condiviso su Google Drive** affinché gli ambienti locali e cloud supportati consultino lo stesso stato canonico.

Non ripetere la domanda dopo la configurazione.

### Contesto aziendale opzionale

Per caricare contesto aziendale o dopo la scelta di uso organizzativo, seguire [references/organization-context-setup.md](references/organization-context-setup.md). Collegare fonti selezionate o costruire un profilo privato, distinguere vincoli confermati da preferenze e informazioni sconosciute, e confermare l'ambito progetto/spazio prima dell'attivazione. Riutilizzare un collegamento funzionante nell'ambito corretto; non ripetere onboarding o mescolare organizzazioni. Prima di pianificare, applicare i vincoli pertinenti insieme alle capacità verificate dell'ambiente. Escludere i contenuti aziendali dalla skill pubblica e dall'apprendimento globale; il percorso guida l'host e non garantisce sicurezza infrastrutturale.

### Profili di persistenza

- `LOCAL`: Vault canonico di eventi immutabili su questo dispositivo; SQLite è solo indice/cache locale.
- `SHARED_GOOGLE_DRIVE`: Vault canonico in Google Drive. I client locali di norma usano Drive per desktop, quelli cloud un connettore/adattatore verificato.
- `CUSTOM_SHARED`: riservato a futuri adattatori.
- `DEGRADED`: l'ambiente non raggiunge l'archivio canonico configurato. Dichiararlo; non fingere che la persistenza sia riuscita.

In modalità condivisa preferire **metadati prima dei contenuti**. Non copiare corpora grezzi sensibili in AWA se non esplicitamente necessario.

Lo stato canonico è costituito da **file di eventi immutabili**, non un database SQLite vivo sincronizzato o un unico file condiviso a cui aggiungere contenuto. SQLite è solo accelerazione locale eliminabile.

Vedere `references/persistence.md`.

## 1. Identificare localmente l'ambiente corrente

La scelta delle risorse dipende da **dispositivo × ambiente**, con variazioni specifiche della sessione quando necessarie.

Mantenere/consultare un profilo delle capacità con sole disponibilità verificate:

- Python, shell, Git e runtime locali;
- accesso al filesystem;
- archivi montati o condivisi;
- connettori;
- skill installate;
- sottoagenti e parallelismo;
- modelli e modalità di ragionamento disponibili;
- supporto alla creazione di artefatti.

Non presumere che una capacità presente su un PC o piattaforma esista anche qui.

Se manca una capacità preferita:

1. Adattare il piano alle risorse locali; oppure
2. Consigliare di continuare in un **ambiente noto** con la capacità necessaria. Riutilizzare il checkpoint accessibile; creare un Handoff Pack solo se la destinazione non può riprendere affidabilmente da esso.

Vedere `references/environment-capabilities.md`.

## 2. Classificare la richiesta

- **DIRECT TASK**: attività atomica; l'architettura aggiunge poco.
- **COMPOSITE TASK**: un obiettivo/output logico con più passaggi.
- **PROJECT**: più task, dipendenze, stato persistente, filoni di lavoro o giorni/settimane.
- **PROGRAM / RECURRING SYSTEM**: schemi ripetuti che giustificano skill, modelli o automazioni.

Restare quasi invisibile per attività dirette. Progettare esplicitamente l'architettura dei progetti.

## 3. Dedurre prima di chiedere

Distinguere internamente `KNOWN`, `INFERRED`, `UNKNOWN`, `DECISION_CRITICAL_UNKNOWN`.

Chiedere solo ciò le cui risposte possono modificare sostanzialmente scomposizione, modalità di esecuzione, scelta delle skill, risorse, strategia del contesto, verifiche o costi.

Numero orientativo di domande:

- task diretto: normalmente 0;
- task normale/composto: 0–3;
- progetto complesso: 3–5 iniziali;
- secondo giro solo se emerge una diramazione significativa.

Smettere di chiedere quando l'incertezza residua difficilmente cambierebbe la prossima decisione utile. Usare la lingua dell'utente nella discussione e rispettare lingua/terminologia richiesta per il risultato.

## 4. Scomporre il lavoro

Per progetti e task composti:

1. Partire dal risultato finale e risalire agli output intermedi indispensabili.
2. Formare i task candidati.
3. Separare quando servono contratti di esecuzione sostanzialmente diversi e il beneficio supera il costo del passaggio.
4. **Non** separare solo perché cambia lo strumento all'interno dello stesso obiettivo.
5. Definire dipendenze: `requires`, `feeds`, `validates`, `revises`.
6. Aggiungere verifiche di qualità/umane dove errori o scelte si propagano in modo rilevante.
7. Individuare modelli di task ripetuti e valutare skill riutilizzabili.

Un **task** è la più piccola unità logica che possiede stabilmente obiettivo, input, trasformazione dominante, output valutabile e criterio di successo.

## 5. Costruire solo la Task Signature necessaria

Usare normalmente le caratteristiche principali:

- operazione: acquisire / trasformare / analizzare / produrre / verificare;
- tipo degli input;
- base informativa;
- profondità del ragionamento;
- scala del contesto;
- modalità di verifica;
- conseguenze dell'errore.

Aggiungere dimensioni solo se cambiano una decisione: aggiornamento, incertezza conoscitiva, accoppiamento del contesto, modalità/contratto dell'output, interazione con lo stato.

La Signature descrive il problema, non la soluzione. Non includervi nomi di modelli, Python, impegno di ragionamento o spazi di lavoro.

## 6. Verificare capacità riutilizzabili prima di inventarne

Esaminare l'inventario corrente e skill/modelli noti prima di costruire un nuovo flusso.

Valutazione della skill:

- `NO`: bastano attività o flusso ordinari.
- `MAYBE`: eseguire una o due volte e poi codificare se ripetibile.
- `YES`: costruire o riusare una skill prima di aumentare la scala.

Una skill si giustifica per ripetizione, esigenza di coerenza, durata, riuso e conseguenze degli errori, non per la sola difficoltà.

## 7. Derivare il piano di esecuzione

Tradurre requisiti dei task in uno o più passaggi. Preferire schemi consolidati quando pertinenti:

- `DATA -> DETERMINISTIC COMPUTE -> ANALYTICAL ARTIFACT -> LLM REASONING -> VALIDATION`
- `SEARCH -> SOURCE EVALUATION -> EXTRACTION -> EVIDENCE PACK -> REASONING -> SOURCE CHECK`
- `DESIGN -> CODE -> EXECUTE -> TEST -> DEBUG -> RETEST`
- `REASON -> CONTENT PLAN -> GENERATE -> EDITORIAL REVIEW`
- `CREATOR -> INDEPENDENT CHALLENGER -> RECONCILIATION`

Classi di esecuzione:

- RETRIEVAL
- DETERMINISTIC_COMPUTE
- SEMANTIC_TRANSFORMATION
- REASONING
- GENERATION
- VALIDATION

## 8. Scegliere risorse per singolo passaggio

Per ciascun passaggio:

1. Scegliere prima la classe di risorsa.
2. Applicare filtri inderogabili sulle capacità e i vincoli aziendali confermati pertinenti; registrare i permessi sconosciuti senza presumere approvazione.
3. Intersecare requisiti e profilo delle capacità dell'ambiente corrente.
4. Se il piano ideale non è fattibile localmente, controllare ambienti alternativi noti e scegliere adattamento locale o passaggio.
5. Consultare solo evidenze globali pertinenti sulle prestazioni quando necessario.
6. Scegliere strategia di contesto e spazio di lavoro.
7. Selezionare modello, strumento e configurazione concreti.
8. Definire verifica e alternativa/escalation.

Profilo di calcolo predefinito: `BALANCED`.

- `ECONOMY`: configurazione meno costosa che dovrebbe superare la soglia di qualità.
- `BALANCED`: ottimizzare qualità attesa e costo totale fino a un output accettato.
- `MAX_QUALITY`: usare calcolo premium o ridondanza quando riducono il rischio residuo.

L'impegno di ragionamento è distinto dalla scelta del modello. Conseguenze elevate non implicano automaticamente il massimo ragionamento: verifiche più forti possono essere un investimento migliore.

## 9. Contesto e spazio di lavoro

Usare il contesto minimo sufficiente: nucleo compatto del progetto, pacchetto del task, evidenze selezionate e artefatti analitici invece di grandi dataset grezzi.

Modalità degli spazi di lavoro:

- `CONTINUE`
- `FORK`
- `ISOLATE`
- `PARALLEL`
- `SPECIALIZED`
- `HANDOFF_TO_ENVIRONMENT`

### Task brevi e continuità durevole del progetto

Per progetti su più sessioni, quote, modelli o agenti, un file di lavoro compatto è il punto di ripresa predefinito. Riutilizzare le convenzioni del progetto; altrimenti `docs/WORK_PLAN.md` è adatto. Usare `templates/project-work.md` se utile. Mantenere un piano con ID stabili e dipendenze, checkpoint attuale e registro conciso a sole aggiunte. Separarli in più file solo quando dimensione o lavoro concorrente lo giustificano.

- Dimensionare ogni task su un risultato revisionabile e le verifiche pertinenti che stiano comodamente in una sessione. Separare task troppo grandi a un checkpoint significativo; evitare quote fisse di token/tempo e frammentazione banale.
- Prima di lavorare, leggere checkpoint, task e riferimenti pertinenti, confrontandoli con file reali, branch/revisione e modifiche incompiute. Registrare il responsabile del task attivo. Modifiche esistenti e agenti in corso non vengono abbandonati solo perché cambia sessione o modello.
- Aggiornare il checkpoint dopo un risultato significativo, un blocco, un cambio di ambito/decisione e prima di cambiare modello/sessione o esaurire probabilmente la quota. Registrare il parziale come parziale, senza attendere la fine di una lunga sessione.
- Conservare obiettivo, vincoli/fonti, stato dei task, artefatti modificati, decisioni motivate, controlli esatti e risultati osservati, problemi aperti e prossima azione concreta. Distinguere piani ed evidenze; non segnare come superato un controllo interrotto o non eseguito.
- Alla ripresa verificare le evidenze pertinenti e continuare la prossima attività ammissibile senza rifare lavoro completato o riaprire decisioni senza nuove prove. I confini dei task brevi non richiedono approvazioni ripetute o fermate quando la continuazione è già autorizzata.
- Più agenti possono usare questi file in sequenza senza handoff formale. Ciò non autorizza delega o modifiche concorrenti. Se il parallelismo è autorizzato, usare responsabilità distinte e output isolati; un solo autore per i file di stato condivisi o registri separati. Una nota di stato non è un blocco di concorrenza.
- Usare archivi controllati dal progetto, accessibili agli agenti partecipanti, con riferimenti portabili. Registrare solo metadati necessari, escludendo segreti e contenuti grezzi sensibili. Questi file operativi non sostituiscono il Vault immutabile AWA; gli eventi devono restare compatti e riferirsi ai file senza duplicarne la storia.

Al cambio di chat, spazio di lavoro, dispositivo o ambiente, riusare prima lo stato del progetto se accessibile e sufficiente. Un cambio di modello da solo non richiede un nuovo documento. Usare il **Handoff Pack** di `templates/handoff-pack.md` solo per un confine sostanziale di accesso/contesto, continuità mancante o richiesta esplicita. Collegarlo allo stato esistente e includere solo ciò che manca. Non dire soltanto «apri una nuova chat».

Una preferenza operativa futura non autorizza di per sé a interrompere un agente attivo o creare file subito: rispettare i tempi richiesti dall'utente.

## 10. Verifica ed escalation

Adattare la verifica all'output:

- deterministico → ricalcolo/test;
- empirico → validazione statistica e sensibilità;
- basato su fonti → riscontro con le fonti;
- inferenziale → ipotesi alternative/revisione indipendente;
- eseguibile → esecuzione e test;
- estetico → revisione editoriale/umana.

Se l'esecuzione fallisce, diagnosticare prima di spendere altro calcolo:

1. Contratto del task errato?
2. Contesto mancante?
3. Contesto eccessivo o rumoroso?
4. Classe di esecuzione sbagliata?
5. Sarebbe servito uno strumento deterministico?
6. Capacità mancante nell'ambiente?
7. Ambiente noto migliore disponibile?
8. Modello/risorsa non adatto?
9. Impegno di ragionamento insufficiente?
10. Piano o scomposizione errati?

`Retry != repeat`: cambiare una variabile sostanziale prima di riprovare.

### Miglioramento controllato opzionale

Quando l'utente richiede un confronto o evidenze ripetute mostrano un problema ricorrente costoso, leggere [references/controlled-improvement.md](references/controlled-improvement.md). Confrontare una base recuperabile e una candidata circoscritta, validare su casi separati e mantenere la base se non emerge un guadagno netto. Usare [templates/improvement-experiment.md](templates/improvement-experiment.md) se utile. È una modalità opzionale, non una fase aggiuntiva per ogni task; gli esperimenti non cambiano automaticamente le regole predefinite.

## 11. Traccia persistente delle esecuzioni

Ogni uso sostanziale deve creare un evento compatto `run.started` quando la persistenza funziona. Eventi successivi significativi possono includere:

- `run.recommended`
- `run.execution`
- `run.rerouted`
- `run.closed`
- `capability.observed`
- `skill.observed`
- `pattern.observed`
- `environment.profile_published`

Gli eventi sono immutabili. Lo stato corrente di esecuzioni, progetti e registri è una **proiezione** derivata dagli eventi.

Tenere distinta `recommended_configuration` da `actual_configuration`.

Stati degli esiti:

- FIRST_PASS_ACCEPTED
- MINOR_CORRECTION
- MAJOR_CORRECTION
- REROUTED
- FAILED
- ABANDONED
- OUTCOME_UNKNOWN
- PENDING (derivato in assenza di evento di chiusura)

L'utente non deve ricordare gli ID: preferire `pending` / `close-latest` filtrati per progetto/task/ambiente quando è disponibile una CLI locale.

Non caricare tutto il Vault/registro nel contesto. **Interrogare o indicizzare prima, poi recuperare pochi record pertinenti.**

## 12. Output visibile

Non mostrare tassonomie interne se non utili. Di norma la risposta include solo:

- **Approccio consigliato**.
- **Configurazione**: schema di esecuzione, risorse, modello/strumento/impegno di ragionamento se utile.
- **Contesto / spazio di lavoro**: solo quando cambia l'esecuzione.
- **Motivo**: spiegazione concisa.
- **Prima azione**.
- **Fiducia**: quando le evidenze della raccomandazione sono deboli o incerte.

Per grandi progetti mostrare architettura e dipendenze del lavoro a breve termine; pianificare progressivamente senza falsa precisione sul lungo periodo.

## 13. File di supporto

Leggere solo quando necessari:

- `references/persistence.md`
- `references/environment-capabilities.md`
- `references/decomposition.md`
- `references/signatures.md`
- `references/routing.md`
- `references/logging-learning.md`
- `references/cloud-adapters.md`
- `references/testing.md`
- profili sotto `environments/`;
- pacchetto di contesto sotto `templates/handoff-pack.md`;
- file di lavoro riprendibile sotto `templates/project-work.md`.

Il nucleo runtime deve restare piccolo; le tassonomie dettagliate appartengono ai riferimenti, non alla conversazione ordinaria.
