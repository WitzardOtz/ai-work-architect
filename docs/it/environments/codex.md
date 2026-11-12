# Profilo dell'ambiente Codex

[English](../../../environments/codex.md) | [Italiano](codex.md)

Ultima revisione: 2026-11-12.

Quando Codex opera localmente con shell e filesystem, preferire la CLI locale di AWA e un Vault sincronizzato tramite Google Drive per desktop. Una sessione Codex che non gira sul dispositivo dell'utente è per AWA un ambiente cloud: seguire lì il modello dell'adattatore cloud.

Verificare, senza presumere:

- runtime Python;
- accesso a repository e filesystem;
- percorso del disco/cartella Google Drive;
- skill e strumenti installati;
- disponibilità di sottoagenti o esecuzione multi-agente;
- modelli offerti e possibilità di impostare o cambiare l'impegno di ragionamento nella sessione;
- runtime per test e build.

Scrivere codice ed eseguire test sono capacità distinte dal ragionamento generico. Assegnare i test deterministici all'ambiente che può effettivamente eseguirli.
