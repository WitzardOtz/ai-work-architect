# Adattatori cloud

[English](../../../references/cloud-adapters.md) | [Italiano](cloud-adapters.md)

Un client cloud può non avere shell o filesystem locali. La persistenza condivisa dipende quindi da un **connettore cloud verificato** verso lo stesso Vault Google Drive.

## Lettura

1. Cercare o consultare prima `AWA/index/`.
2. Selezionare solo i record pertinenti di esecuzioni, progetti, ambienti e capacità.
3. Leggere pochi file di eventi immutabili mirati se servono dettagli.
4. Non enumerare o leggere nel contesto l'intero Vault.

## Scrittura

Quando il connettore permette di creare file:

1. Creare un nuovo file JSON immutabile sotto `events/YYYY/MM/` per ogni evento.
2. Usare un `event_id`/ULID univoco appena generato.
3. Non modificare o aggiungere contenuto a un file di evento esistente.
4. Non aggiornare gli indici condivisi dal cloud se l'ambiente non può farlo in sicurezza; gli indici possono essere in ritardo e restano ricostruibili.

Se il connettore non può creare il file di evento, la persistenza è `DEGRADED`. Non dichiarare che l'esecuzione è stata registrata tra sessioni.

## Differenze tra connettori

Le capacità dei connettori variano per prodotto e possono cambiare. Verificare durante l'uso il supporto effettivo a creazione, ricerca e lettura, senza presumerlo da regole fisse.
