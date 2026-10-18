# Esempi leggibili dal software

[English](../../../templates/machine-examples.md) | [Italiano](machine-examples.md)

Chiavi JSON, comandi, valori degli stati, percorsi e identificatori di versione restano identici nelle due lingue affinché gli esempi siano compatibili con il software. Sono modelli illustrativi, non la configurazione del tuo ambiente. Non trattare identità o disponibilità di esempio come fatti verificati.

## Configurazione della persistenza

[config.example.json](../../../templates/config.example.json) contiene `schema_version`, `mode`, `vault_root`, `device_id`, `environment_id` e `shared_provider`. Sostituire percorso e ID di esempio con valori verificati scelti durante il setup. `LOCAL` conserva il Vault sul dispositivo; `SHARED_GOOGLE_DRIVE` richiede la posizione Drive selezionata. Preferire la CLI di setup alle modifiche manuali: init può sovrascrivere un profilo esistente selezionato.

## Profilo dell'ambiente

[environment-profile.example.json](../../../templates/environment-profile.example.json) identifica la coppia `device_id × environment_id` tramite `environment_key`. `last_verified` registra quando sono state verificate le capacità. Ogni voce di `capabilities` ha uno stato e può includere una versione. `AVAILABLE` richiede evidenza reale; `UNKNOWN` non autorizza l'uso. Non considerare attuali data o capacità dell'esempio.

## Evento

[event.example.json](../../../templates/event.example.json) illustra intestazione e payload. `event_id` e `run_id` devono essere identificatori nuovi e validi, non le stringhe letterali dell'esempio. `occurred_at` riporta il timestamp UTC, `event_type` la transizione. I campi di versione identificano schema e architect. Ambiente, dispositivo, progetto e task delimitano il record; `summary` e `payload.description` sono metadati compatti. Escludere input grezzi sensibili. Gli eventi sono immutabili: usare la CLI esistente o un adattatore verificato.

## Collegamento del contesto aziendale

[context-bindings.example.json](../../../templates/context-bindings.example.json) è un formato privato gestito dall'agente, non letto da `awa_cli.py`. `bindings` delimita le scelte con `scope_ref` e `mode`. Per un'organizzazione conserva ID, riferimenti a profilo e indice delle fonti, revisione/hash osservati e momento della conferma. L'esempio è in modalità personale, con campi aziendali nulli e stato `unconfigured`: non attiva alcuna azienda. Preservare le voci degli altri ambiti quando se ne cambia una. Condividere un profilo non condivide i permessi degli utenti.

## Metadati del pacchetto

[MANIFEST.json](../../../MANIFEST.json) descrive la skill distribuita: nome, versione, punto di ingresso, architettura/profili di persistenza, approccio alle dipendenze Python e licenza. È metadato del pacchetto, non una posizione per configurazioni personali/aziendali o credenziali.
