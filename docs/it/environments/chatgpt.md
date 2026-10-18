# Profilo dell'ambiente ChatGPT

[English](../../../environments/chatgpt.md) | [Italiano](chatgpt.md)

Trattare ogni superficie di ChatGPT come un ambiente distinto.

## Chat cloud

Non presumere filesystem o Python locali. Se è disponibile un connettore Google Drive in grado di accedere al Vault AWA condiviso, usare il protocollo cloud: prima indice o ricerca, poi letture mirate e creazione di eventi immutabili se supportata.

Se Drive non è collegato o non permette di leggere/creare record nel Vault, la persistenza è `DEGRADED` per quella sessione.

## Modalità Work o con accesso al computer

Le capacità possono differire molto dalla chat ordinaria. Verificare browser, computer, file e plugin effettivamente disponibili prima di scegliere le risorse.

## Skill e plugin

Usare l'inventario reale dell'ambiente. Una skill o un connettore disponibile altrove non è necessariamente disponibile nella sessione corrente.
