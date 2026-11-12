# Evidenze progettuali della v0.4

[English](../../SOURCES.md) | [Italiano](SOURCES.md)

Questa versione deriva principalmente dalla validazione della v0.3.x in più ambienti, non da risultati di benchmark esterni.

Vincoli osservati incorporati:

- SQLite vivo sincronizzato può fallire o bloccarsi in cartelle montate/sincronizzate;
- creare file immutabili è più sicuro per flussi con sincronizzazione cloud su più dispositivi;
- ambienti AI locali possono usare Python, PowerShell e filesystem che mancano nelle sessioni cloud;
- le sessioni cloud richiedono un connettore o altro adattatore verificato verso l'archivio condiviso;
- grandi registri condivisi vanno interrogati o indicizzati, non caricati interamente nel contesto;
- la disponibilità delle capacità varia per dispositivo, client e talvolta sessione.

Le dichiarazioni sulle prestazioni specifiche dei modelli non appartengono al nucleo della skill. Vanno nelle osservazioni/registri AWA e aggiornate da evidenze attuali.

## Aggiunta del miglioramento controllato — 18 ottobre 2026

Il protocollo opzionale si ispira a [Harness2](https://github.com/google-research/harness2/tree/1cfe254e8d25b15f37048c3730134686abe60335): proposte legate alle evidenze, Propose-Probe-Compose e KEEP_BASE. Riferimento e modello sono adattamenti originali per AWA; non viene importato codice runtime esterno. I benchmark del progetto originale non costituiscono validazione locale di AWA. Vedere `references/controlled-improvement.md` per ambito e criteri di adozione.

## Revisione degli ambienti — 12 novembre 2026

I profili di Claude, Codex e Antigravity sono stati riletti rispetto a documentazione e registri delle modifiche dei fornitori, più una sessione Cowork osservata. Cambiamenti registrati: le sessioni Cowork possono girare nel cloud e raggiungere le cartelle dell'utente tramite l'app desktop; un Vault su disco virtuale può essere raggiungibile file per file ma non dalla CLI; Antigravity ha aggiunto agenti remoti e spostato la configurazione per progetto; Codex ha aggiunto funzioni multi-agente. I profili riportano la data di revisione e restano evidenze da verificare. La revisione ha inoltre trovato vuoto, dopo 17 esecuzioni, il registro delle risorse di un Vault reale: da qui la regola esplicita sull'attualità e i comandi di osservazione documentati. Nessun nome di modello, prezzo o risultato di benchmark è stato aggiunto alla skill.
