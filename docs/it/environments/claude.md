# Profilo dell'ambiente Claude

[English](../../../environments/claude.md) | [Italiano](claude.md)

Ultima revisione: 2026-11-12. Sono note datate da verificare nella sessione, non garanzie.

Trattare Claude come più ambienti distinti.

## Chat Claude o Project

Potenzialmente solo cloud. Verificare i connettori disponibili; non presumere filesystem o Python locali.

Se un connettore verificato raggiunge il Vault Google Drive condiviso, usare il modello dell'adattatore cloud. Altrimenti la persistenza della sessione è `DEGRADED`.

## Claude Cowork

- Una sessione Cowork può essere eseguita in uno spazio di lavoro cloud e non sul dispositivo dell'utente. La documentazione di supporto di Anthropic indica il cloud come impostazione predefinita per le nuove sessioni da ottobre 2026, mentre le sessioni avviate localmente prima restano locali. Non presumere una VM locale: verificare dove gira la shell.
- In una sessione cloud, Python e shell appartengono allo spazio di lavoro cloud. Le cartelle dell'utente sono raggiungibili solo tramite l'app desktop, solo mentre è in esecuzione e solo se collegate; l'accesso può richiedere un'autorizzazione.
- Una cartella collegata su un disco virtuale, come Google Drive per desktop, può essere leggibile e scrivibile file per file ma non montabile in una shell. Osservato una volta (2026-11): in quel caso la CLI inclusa non poteva operare sul Vault.
- In tal caso trattare l'accesso ai singoli file come adattatore cloud: leggere prima `index/`, creare nuovi file di eventi immutabili e lasciare gli indici condivisi a un ambiente che può eseguire `compact`. Un connettore Google Drive verificato è un'alternativa. Se nessuno dei due può creare file di eventi, la persistenza è `DEGRADED`.
- SQLite in cartelle sincronizzate era fragile nelle prove precedenti, da cui l'uso di file immutabili nel Vault. Qualsiasi cache nello spazio di lavoro della sessione è eliminabile.

## Claude Code

Quando opera localmente, preferire `scripts/awa_cli.py` e un Vault Google Drive sincronizzato sul dispositivo.

## Revisione indipendente

Dove sono disponibili sottoagenti o lavoratori isolati, usare `ISOLATE` / `PARALLEL` solo dopo aver verificato la funzionalità nella modalità corrente.

## Skill

Le skill installate o specifiche dell'utente sono locali all'ambiente. Verificare l'inventario reale; non presumere che una skill esista perché era disponibile in una sessione precedente.

Un'installazione può contenere solo `SKILL.md` (osservato una volta, 2026-11). Verificare che `references/`, `templates/` e `scripts/` siano presenti prima di farvi affidamento.
