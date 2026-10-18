# Configurazione guidata al primo utilizzo

[English](../../../references/first-run-setup.md) | [Italiano](first-run-setup.md)

Usare al primo utilizzo, per una richiesta esplicita di configurazione/riconfigurazione o per un problema di persistenza. Conversare brevemente nella lingua dell'utente. Chiedere solo informazioni che cambiano il prossimo passo; di norma basta una decisione alla volta. Il setup supporta il task corrente, non lo sostituisce.

## Contesto personale o aziendale opzionale

Configurare il contesto è indipendente dal configurare l'archivio. Al primo utilizzo in un ambito sconosciuto, chiedere se AWA verrà usata personalmente o per un'organizzazione; riusare una scelta esplicita esistente. Per uso aziendale seguire [organization-context-setup.md](organization-context-setup.md) per collegare fonti o creare e confermare un profilo privato. Una richiesta esplicita di contesto aziendale attiva quel percorso anche se la persistenza è già configurata. L'uso personale lo salta. Non ripetere un profilo valido nell'ambito corretto e non confondere la configurazione del Vault con quella delle policy aziendali. Se si sta riparando un problema dell'archivio, risolverlo senza imporre un nuovo onboarding del contesto.

## 1. Verificare prima di chiedere

Verificare accesso effettivo a shell, Python, filesystem o connettori. Non dedurre capacità dal nome del prodotto. Nei client locali, esaminare la configurazione indicata da `AWA_CONFIG_PATH`, altrimenti `~/.ai-work-architect/config.json`. Non esporre credenziali o riversare la configurazione nella chat.

- Configurazione esistente funzionante: indicare brevemente la modalità e continuare, senza ripetere la scelta iniziale o azzerare impostazioni.
- Configurazione con archivio irraggiungibile: conservarla, spiegare il controllo fallito e proporre riconnessione o un profilo locale separato. Non creare silenziosamente un secondo Vault canonico o passare al locale dichiarando persistenza condivisa.
- Configurazione assente: porre la domanda locale/condiviso prevista da SKILL.md. Spiegare che il locale basta per un dispositivo; la condivisione permette continuità tra ambienti che raggiungono effettivamente lo stesso Vault.

## 2. Configurare il percorso scelto

### Modalità locale con Python e filesystem verificati

Usare la CLI inclusa. Scegliere ID stabili di dispositivo e ambiente da metadati verificati, oppure chiedere se ambigui. Usare il Vault locale predefinito salvo scelta diversa dell'utente. Esempio:

```text
python scripts/awa_cli.py init-local --device-id MY-PC --environment-id local-agent
```

Eseguire dalla cartella della skill oppure usare il percorso assoluto dello script. Sostituire gli identificatori di esempio con quelli reali. L'inizializzazione scrive file: farlo solo nella modalità selezionata dall'utente e negli archivi accessibili.

### Modalità condivisa con cartella Google Drive sincronizzata localmente

Verificare disponibilità di Drive per desktop e della cartella prevista. Chiedere il percorso reale del Vault se non emerge dalla configurazione o dal contesto fornito dall'utente. Non inventare lettere di unità, esplorare cartelle personali estranee, installare Drive o collegare account automaticamente.

Se esiste già un Vault AWA, riutilizzarlo consultando solo i metadati necessari. Mantenere la cache SQLite fuori dall'archivio sincronizzato. Configurare con il percorso reale, per esempio:

```text
python scripts/awa_cli.py init-shared --device-id MY-PC --environment-id local-agent --vault "G:/My Drive/AWA"
```

I comandi init sovrascrivono la configurazione selezionata. Non usarli su un profilo esistente salvo richiesta di modifica dell'utente. Usare un percorso `--config` distinto per un profilo intenzionalmente separato; questo non costituisce migrazione degli eventi esistenti.

### Ambienti cloud o con soli connettori

Seguire [cloud-adapters.md](cloud-adapters.md). Verificare capacità di lettura/ricerca/creazione e il riferimento esatto al Vault scelto dall'utente. Non inventare percorsi locali o inizializzare localmente dove non possibile. Se i metadati di collegamento non possono persistere, conservarli solo nella sessione e spiegare che le successive potrebbero richiederli di nuovo.

Se collegare account o ottenere accesso richiede un'azione umana, spiegare il passo concreto e continuare il lavoro indipendente. Un connettore in sola lettura può consultare evidenze ma non garantire persistenza. Indicare `DEGRADED` per la scrittura. Non dichiarare connettori non supportati o sincronizzazione automatica tra dispositivi.

## 3. Verificare l'adattatore configurato

Per una nuova configurazione fare un minimo ciclo di scrittura e rilettura di soli metadati, con un'esecuzione di setup univoca:

1. Controllare `status` e il profilo rilevato dell'ambiente. Pubblicare un nuovo `probe` quando serve aggiornare le capacità.
2. Usare `run-start --project-id AWA_SETUP --task-family setup-verification` con una breve descrizione del controllo. Conservare l'ID restituito.
3. Verificare che `pending` contenga esattamente quell'ID tramite l'adattatore selezionato.
4. Chiudere per ID con `OUTCOME_UNKNOWN`, annotando che il controllo dell'archivio è completo ma l'accettazione dell'utente non è ancora nota. Verificare che l'esecuzione non sia più in attesa. Con la CLI locale, usare `compact` per aggiornare gli indici derivati consultati dai connettori.

Questi comandi sono in `scripts/awa_cli.py`; usare `--help` per gli argomenti esatti. Preferire la CLI agli eventi scritti a mano. Un adattatore solo con connettore usa eventi immutabili equivalenti e letture mirate come descritto in cloud-adapters.md. Se un controllo fallisce, registrare ciò che funziona e ciò che resta indisponibile; non inventare una chiusura riuscita. Non creare ripetutamente esecuzioni di setup se persiste lo stesso problema di accesso.

Il successo di lettura/scrittura locale dimostra solo quell'adattatore. La continuità tra dispositivi resta non verificata finché un secondo ambiente non legge lo stesso evento univoco; una cartella sincronizzata localmente non dimostra da sola la sincronizzazione remota. Per profili esistenti funzionanti basta un controllo quando pertinente, senza nuove esecuzioni di prova a ogni task.

## 4. Spiegare risultato e prossimo passo

Riportare brevemente, in linguaggio semplice:

- modalità scelta e posizione/riferimento verificato dell'archivio;
- capacità effettivamente controllate ed eventuali limiti di accesso o sincronizzazione;
- cosa conserva AWA: metadati compatti e riferimenti, non materiale grezzo sensibile;
- stato del setup: pronto localmente, pronto tramite connettore oppure degradato, e prossima azione concreta dell'utente se necessaria.

Fornire dettagli tecnici su richiesta. Non dichiarare che il setup valida la qualità delle decisioni di AWA. Non conservare credenziali nel Vault né pubblicare configurazione personale, eventi o cache insieme alla skill.
