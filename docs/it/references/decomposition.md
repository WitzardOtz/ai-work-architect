# Scomposizione del lavoro

[English](../../../references/decomposition.md) | [Italiano](decomposition.md)

## Confine di un task

Un task è la più piccola unità logica che possiede stabilmente:

- obiettivo;
- insieme di input;
- trasformazione dominante;
- output valutabile;
- criterio di successo.

Un cambio di strumento all'interno dello stesso obiettivo non crea automaticamente un nuovo task.

## Procedura di scomposizione

1. Definire l'output finale.
2. Risalire agli output intermedi indispensabili.
3. Formare i task candidati.
4. Confrontare i rispettivi contratti di esecuzione.
5. Dividere o unire in base al beneficio nella scelta delle risorse rispetto al costo del passaggio di consegne.
6. Costruire le dipendenze.
7. Aggiungere verifiche e approvazioni umane necessarie.
8. Individuare schemi ripetuti e opportunità per una skill.

## Criteri per i confini

Valutare più facilmente una separazione quando cambia:

- un output riutilizzabile in modo indipendente;
- una verifica di qualità;
- il corpus di contesto;
- un requisito di indipendenza;
- il responsabile, lo spazio di lavoro o l'ambiente;
- il rischio di propagazione degli errori.

Non frammentare operazioni semplici come ricerca → apertura → lettura → estrazione quando costituiscono un unico task coerente di recupero delle informazioni.
