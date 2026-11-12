# Scelta delle risorse

[English](../../../references/routing.md) | [Italiano](routing.md)

## Requisiti di capacità prima dei nomi delle risorse

Tradurre la Task Signature in capacità necessarie, importanti o opzionali, quindi costruire il piano di esecuzione.

Classi di esecuzione:

- recupero delle informazioni;
- calcolo deterministico;
- trasformazione semantica;
- ragionamento;
- generazione;
- verifica.

## Scelta per singolo passaggio

Per ogni passaggio:

1. Classe di risorsa.
2. Vincoli inderogabili, comprese le policy aziendali confermate e applicabili.
3. Fattibilità nell'ambiente corrente.
4. Adattamento locale o passaggio a un altro ambiente.
5. Evidenze globali sulle prestazioni, se necessarie.
6. Strategia del contesto.
7. Configurazione concreta.
8. Verifica.
9. Alternativa o escalation.

## Invarianti

- Deterministico prima del probabilistico.
- Recuperare prima di caricare.
- Strutturare prima del ragionamento costoso.
- La verifica deve corrispondere alla natura della conoscenza prodotta.
- Modello × impegno di ragionamento × ambiente conta più del solo nome del modello.
- Ottimizzare il costo totale fino a un output accettato, non il prezzo grezzo della chiamata.

## Attualità della conoscenza delle risorse

Nomi, prezzi, limiti e funzioni di modelli e strumenti sono deperibili e restano volutamente fuori da questa skill. Evidenze per una scelta concreta, in ordine di preferenza:

1. ciò che l'ambiente corrente offre ora in modo verificabile (selettore dei modelli, inventario degli strumenti, documentazione del fornitore consultata nella sessione);
2. osservazioni datate nel Vault (`query-context`), lette insieme ad ambiente e data;
3. le conoscenze interne del modello host, trattate come potenzialmente superate.

Considerare superata un'osservazione quando esiste una generazione più recente di quella risorsa o, come regola pratica, quando ha più di circa tre mesi, e riverificarla prima che una decisione ne dipenda. Senza evidenze attuali, raccomandare classe di risorsa e impegno di ragionamento, indicare un modello specifico solo come suggerimento non verificato e dire che cosa lo confermerebbe. Dopo la chiusura di un'esecuzione, registrare ciò che si è appreso (vedere [logging-learning.md](logging-learning.md)). Un registro vuoto significa assenza di evidenze, non una scelta neutra predefinita.

## Contesto aziendale

Per un'organizzazione collegata, seguire [organization-context-setup.md](organization-context-setup.md). Leggere il profilo compatto e verificarne ambito e revisione prima di scegliere le risorse. Intersecare i requisiti del task con capacità verificate e permessi applicabili. Uno strumento disponibile non è automaticamente autorizzato. Recuperare solo fonti pertinenti; mantenere esplicite le informazioni sconosciute, segnalare conflitti e fermare solo l'azione interessata quando non si può accertare un permesso necessario. Le preferenze restano subordinate ai vincoli obbligatori applicabili e alle istruzioni che governano l'host.
