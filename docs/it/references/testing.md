# Protocollo di verifica

[English](../../../references/testing.md) | [Italiano](testing.md)

Dopo l'installazione, verificare l'ambiente oltre a leggere la skill.

Controlli minimi:

1. Inizializzare il profilo locale o condiviso.
2. Pubblicare il profilo dell'ambiente.
3. Aprire un'esecuzione.
4. Verificare che `pending` la trovi.
5. Scrivere gli eventi di raccomandazione ed esecuzione.
6. Chiuderla con `close-latest`.
7. Generare gli indici con `compact`.
8. Eliminare la cache locale di prova ed eseguire `rebuild-cache`: lo stato ricostruito deve coincidere.
9. Verificare che due ambienti distinti possano scrivere eventi immutabili differenti nello stesso Vault condiviso.
10. Verificare che `query-context` restituisca evidenze compatte e non tutto il Vault.

La validazione reale deve includere:

- un task semplice che non deve essere sovrastrutturato;
- un task ibrido con calcolo deterministico e successiva interpretazione LLM;
- un progetto lungo che richiede scomposizione e continuità/passaggio di contesto.

Preferire 5–10 esecuzioni reali prima di riprogettare ancora l'architettura, salvo errori bloccanti.

## Esperimenti opzionali di miglioramento

Per valutare una modifica di AWA, seguire [controlled-improvement.md](controlled-improvement.md). Fissare criteri e budget prima dell'esecuzione, confrontare una versione di base conservata e una candidata, usare casi di validazione separati. Ricontrollare un candidato composto. I test del runtime e il validatore della skill verificano struttura e compatibilità; non dimostrano miglioramenti nella scelta delle risorse, nella scomposizione o nei risultati dell'utente. Indicare l'efficacia comportamentale come non testata finché un confronto reale non la supporta.
