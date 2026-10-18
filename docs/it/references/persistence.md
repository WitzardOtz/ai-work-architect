# Architettura della persistenza

[English](../../../references/persistence.md) | [Italiano](persistence.md)

## Principio

Lo stato canonico deve sopravvivere alle sessioni senza essere caricato integralmente nel contesto del modello.

AWA v0.4 usa un **Vault di eventi immutabili** come fonte autorevole. SQLite è solo un indice/cache locale eliminabile.

Per configurazione guidata e verifiche degli adattatori, leggere [first-run-setup.md](first-run-setup.md).

## Scelta al primo utilizzo

Chiedere una volta se l'utente desidera continuità tra dispositivi e ambienti.

- **LOCAL**: Vault canonico su questo dispositivo.
- **SHARED_GOOGLE_DRIVE**: Vault canonico in Google Drive; i client locali usano il filesystem sincronizzato, quelli cloud un connettore Drive verificato.
- **CUSTOM_SHARED**: adattatore futuro.
- **DEGRADED**: archivio canonico configurato non raggiungibile nell'ambiente corrente.

L'utente deve poter scegliere la modalità locale senza collegare obbligatoriamente un archivio cloud.

## Modello degli eventi

Ogni transizione di stato crea un nuovo file. Non aggiungere contenuto a un file condiviso e non aggiornare eventi esistenti.

Tipi di evento iniziali:

- `run.started`
- `run.recommended`
- `run.execution`
- `run.rerouted`
- `run.closed`
- `project.updated`
- `artifact.registered`
- `environment.profile_published`
- `capability.observed`
- `skill.observed`
- `pattern.observed`

Le intestazioni degli eventi restano compatte:

```json
{
  "schema_version": "1.0",
  "event_id": "<ULID>",
  "occurred_at": "<UTC timestamp>",
  "event_type": "run.closed",
  "architect_version": "0.4.0",
  "environment": "claude-cowork",
  "device_id": "MY-PC",
  "run_id": "R_<ULID>",
  "project_id": "EXAMPLE_PROJECT",
  "task_family": "data_to_insight",
  "summary": "Network analysis accepted",
  "payload": {}
}
```

## Nomi dei file

Usare solo `[A-Za-z0-9._-]`. Non usare timestamp ISO grezzi contenenti `:`.

Forma consigliata:

```text
<ULID>__<event_type>__<run_id>__<project_slug>__<environment_slug>.json
```

La chiave semantica di deduplicazione è `event_id`, non il nome del file.

## Sicurezza delle scritture locali

Scrivere un file `.tmp-*`, eseguire flush/fsync, quindi rinominarlo nel nome finale univoco. I lettori ignorano `.tmp-*`.

## Gli indici sono proiezioni

I file sotto `index/` sono ricostruibili e mai canonici. Viste utili:

- `pending.json`
- `recent-runs.json`
- `environments.json`
- `capability-view.json`
- `manifest.json`

I lettori cloud devono preferire indici o ricerca, poi letture mirate degli eventi.

## Cache SQLite

La cache è locale, usa WAL ed è ricostruibile dagli eventi del Vault. Non deve trovarsi nella cartella canonica condivisa o sincronizzata.

## Riservatezza

Preferire metadati e riferimenti. Non duplicare nel Vault corpora grezzi, email personali, dataset sensibili o intere cronologie di chat solo per comodità.
