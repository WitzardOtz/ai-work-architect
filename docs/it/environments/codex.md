# Profilo dell'ambiente Codex

[English](../../../environments/codex.md) | [Italiano](codex.md)

Quando Codex opera localmente con shell e filesystem, preferire la CLI locale di AWA e un Vault sincronizzato tramite Google Drive per desktop.

Verificare, senza presumere:

- runtime Python;
- accesso a repository e filesystem;
- percorso del disco/cartella Google Drive;
- skill e strumenti installati;
- runtime per test e build.

Scrivere codice ed eseguire test sono capacità distinte dal ragionamento generico. Assegnare i test deterministici all'ambiente che può effettivamente eseguirli.
