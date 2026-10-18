# Profilo dell'ambiente Claude

[English](../../../environments/claude.md) | [Italiano](claude.md)

Trattare Claude come più ambienti distinti.

## Chat Claude o Project

Potenzialmente solo cloud. Verificare i connettori disponibili; non presumere filesystem o Python locali.

Se un connettore verificato raggiunge il Vault Google Drive condiviso, usare il modello dell'adattatore cloud. Altrimenti la persistenza della sessione è `DEGRADED`.

## Claude Cowork

Osservazioni delle prove precedenti:

- Python disponibile nella VM Cowork;
- le cartelle collegate possono persistere tra sessioni, ma l'accesso può richiedere un'autorizzazione per sessione;
- SQLite in cartelle sincronizzate era fragile, da cui l'uso di file di eventi immutabili nella v0.4;
- spazio temporaneo e cache locale sono eliminabili a ogni sessione;
- il Vault condiviso è canonico; la cache locale va ricostruita se necessario.

## Claude Code

Quando opera localmente, preferire `scripts/awa_cli.py` e un Vault Google Drive sincronizzato sul dispositivo.

## Revisione indipendente

Dove sono disponibili sottoagenti o lavoratori isolati, usare `ISOLATE` / `PARALLEL` solo dopo aver verificato la funzionalità nella modalità corrente.

## Skill

Le skill installate o specifiche dell'utente sono locali all'ambiente. Verificare l'inventario reale; non presumere che una skill esista perché era disponibile in una sessione precedente.
