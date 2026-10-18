# Tracciamento e apprendimento

[English](../../../references/logging-learning.md) | [Italiano](logging-learning.md)

## Osservabilità

Un uso sostanziale di AWA deve creare una traccia persistente compatta quando l'archivio canonico è raggiungibile.

Il Vault degli eventi è la base delle evidenze. I registri aggregati sono viste derivate.

## Raccomandazione ed esecuzione effettiva

Mantenere sempre distinti:

- ciò che AWA ha raccomandato prima dell'esecuzione;
- ciò che è stato effettivamente eseguito;
- eventuali variazioni introdotte dall'utente o dall'ambiente.

## Esiti delle esecuzioni

Gli identificatori restano invariati:

- FIRST_PASS_ACCEPTED
- MINOR_CORRECTION
- MAJOR_CORRECTION
- REROUTED
- FAILED
- ABANDONED
- OUTCOME_UNKNOWN

Un'esecuzione con `run.started` e senza `run.closed` viene rappresentata come `PENDING`.

## Classi di errore

Categorie utili: fatti, ragionamento, copertura, istruzioni, contesto, strumenti, formato, allucinazioni, stile, efficienza, architettura e scelta delle risorse.

## Governo dell'apprendimento

```text
osservazione → schema ripetuto → proposta di regola → aggiornamento della regola
```

Non cambiare la scelta predefinita delle risorse sulla base di una sola esecuzione. Conservare provenienza, ambiente e data delle evidenze.

## Confronti controllati

Per esperimenti richiesti o problemi ricorrenti, usare [controlled-improvement.md](controlled-improvement.md). Collegare versioni di base e candidate, evidenze comparative, ambito della decisione e riferimento per il ripristino tramite gli eventi esistenti. Le decisioni sperimentali (`ADOPT`, `REVISE`, `REJECT`, `KEEP_BASE`) sono metadati del payload, non nuovi esiti delle esecuzioni. Distinguere verifiche strutturali, evidenze comportamentali e accettazione dell'utente. Le conclusioni restano osservazioni limitate al proprio ambito finché evidenze ripetute non ne supportano un uso più ampio.

## Disciplina dei token

Anche il tracciamento deve essere deterministico e compatto. Il modello non deve rileggere tutti i log per continuare un task. Usare indici compatti e interrogazioni mirate.
