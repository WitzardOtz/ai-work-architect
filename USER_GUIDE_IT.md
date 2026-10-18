# AWA: guida pratica

AWA aiuta un agente AI a organizzare il lavoro: chiarire il risultato, dividerlo in task verificabili, scegliere risorse disponibili e consentite, controllare i risultati e mantenere la continuita nei file del progetto.

E una skill con istruzioni, modelli e strumenti di supporto. Il wizard e una conversazione con l'agente che usa la skill: non e un'applicazione separata con schermate proprie. Le funzioni effettivamente disponibili dipendono dall'ambiente, dagli strumenti e dai permessi.

## 1. Installare e iniziare

Scarica o clona il repository e installa la cartella come `ai-work-architect` nella posizione prevista dal tuo ambiente AI. Il file `SKILL.md` deve trovarsi nella radice della cartella. Lo ZIP automatico di GitHub puo estrarsi come `ai-work-architect-main`: in quel caso rinomina la cartella.

Poi scrivi all'agente:

> Usa AI Work Architect e aiutami a configurarlo per il primo utilizzo.

AWA controlla la configurazione esistente. Se manca, ti accompagna nella scelta tra memoria locale e condivisa e verifica l'accesso possibile. Google Drive e opzionale. Un ambiente senza accesso alla memoria scelta deve dichiarare il limite, senza fingere di aver salvato il lavoro.

Il setup della memoria e quello aziendale sono indipendenti: avere un Vault non significa avere gia configurato le policy della tua azienda.

## 2. Se sei il primo a configurare l'azienda

Scrivi:

> Configuriamo AWA per la mia azienda. Aiutami a collegare i documenti esistenti e a preparare un contesto riutilizzabile dai colleghi.

AWA ti guida attraverso questi passaggi:

1. Identificare azienda e ambito: tutta l'organizzazione, un team o un progetto specifico.
2. Scegliere una posizione privata per il profilo e indicare i documenti o collegamenti da consultare. Puoi anche partire senza documenti, lasciando esplicite le informazioni da verificare.
3. Distinguere contesto generale, procedure, policy obbligatorie e preferenze. Le regole estratte mantengono il riferimento alla fonte; le ipotesi non diventano policy approvate.
4. Riepilogare fonti consultate, accessi mancanti, regole, conflitti e informazioni ancora sconosciute.
5. Confermare il profilo da usare nell'ambito scelto e salvarne un riferimento privato per riprendere il lavoro.

Il risultato puo includere un profilo compatto, un indice delle fonti e un riferimento dal progetto. I documenti originali restano nelle loro posizioni; AWA recupera solo il materiale pertinente. Per il riuso tra colleghi serve un riferimento condiviso raggiungibile dai destinatari: un percorso locale del tuo PC non basta.

### Il messaggio per i colleghi

Al termine del primo setup riutilizzabile, AWA prepara automaticamente un messaggio da copiare ai colleghi. Contiene il riferimento reale al profilo, l'ambito e la frase per collegarlo senza ricrearlo. Se il riferimento condiviso manca, il messaggio resta una bozza e AWA indica cosa completare. Il sistema non invia il messaggio e non concede accessi automaticamente.

Esempio illustrativo, da completare con i dati effettivi:

> Abbiamo configurato il contesto aziendale per AWA. Installa la skill, se non l'hai gia fatto, poi chiedi: "Collega il profilo aziendale esistente a [collegamento condiviso] per [azienda e ambito]. Verifica il mio accesso e la versione corrente, mostrami le regole applicabili e chiedimi solo i dettagli mancanti sul mio ruolo e progetto. Riutilizza il contesto gia configurato."

## 3. Se un collega ha gia configurato l'azienda

Usa il messaggio ricevuto e il collegamento al profilo. AWA verifica il tuo accesso, l'ambiente e la versione, chiarisce il tuo ambito e completa solo i dettagli mancanti. Il profilo aziendale condiviso viene riutilizzato; il tuo ruolo, gli accessi e il collegamento al tuo progetto restano distinti da quelli del primo configuratore.

| Livello | Cosa contiene |
|---|---|
| Azienda | Fonti, policy, procedure, terminologia e preferenze comuni |
| Utente e ambiente | Ruolo, accessi effettivi e strumenti disponibili |
| Progetto | Obiettivo, vincoli applicabili, piano, checkpoint e log |

Condividere un profilo non concede gli stessi permessi a tutti. Se una fonte e irraggiungibile, AWA segnala il limite. Non copia automaticamente l'archivio completo o le autorizzazioni del collega.

## 4. Durante il lavoro

AWA usa i vincoli pertinenti prima di selezionare strumenti, ambienti e percorsi dei dati. Per esempio, se una regola confermata vieta l'invio di documenti riservati a servizi esterni, la disponibilita tecnica di uno strumento esterno non lo rende utilizzabile per quei documenti.

Per lavori su piu sessioni, mantiene task brevi, piano, checkpoint e log nei file del progetto. Il checkpoint indica completato/aperto, file modificati, decisioni, controlli realmente eseguiti con risultati e prossima azione. Il modello iniziale e [project-work.md](templates/project-work.md).

Alla ripresa verifica il riferimento al profilo e la versione. Se emergono modifiche rilevanti o fonti obsolete, chiarisce l'effetto prima dell'azione interessata. Questo controllo e eseguito dall'agente durante il lavoro: non esiste un servizio che invia notifiche automatiche a tutti gli utenti.

Puoi chiedere di aggiornare le policy, cambiare organizzazione o tornare alla modalita personale. Scollegare un profilo non cancella automaticamente i documenti aziendali o le tracce precedenti.

## 5. Dove stanno i dati e quali sono i limiti

Il repository pubblico contiene solo la skill, istruzioni e modelli generici. Profili aziendali compilati, documenti, configurazione personale, eventi e cache restano fuori dal pacchetto pubblico. Il Vault e il registro compatto delle esecuzioni, non una copia della knowledge base aziendale.

L'host AI deve essere autorizzato a trattare il materiale prima che venga aperto. Il profilo guida l'agente, ma non sostituisce permessi, controlli di rete o protezioni dell'infrastruttura e non certifica la conformita. I collegamenti ai profili sono gestiti dall'agente: il programma `awa_cli.py` gestisce il Vault, ma non carica o applica automaticamente le policy aziendali.

Struttura, riferimenti e pubblicazione sono stati verificati. Il percorso aziendale deve ancora essere validato con un onboarding reale; non e dimostrata una maggiore efficacia delle decisioni. Il [protocollo di miglioramento](references/controlled-improvement.md) serve a confrontare varianti sulla base di prove.

## Riferimenti

- [Configurazione iniziale](references/first-run-setup.md)
- [Wizard aziendale e istruzioni per i colleghi](references/organization-context-setup.md)
- [Modello di profilo aziendale](templates/organization-profile.md)
- [Indice delle fonti](templates/organization-sources.md)
- [Cronologia degli aggiornamenti](CHANGELOG.md)
- [Licenza Apache 2.0](LICENSE), applicata al pacchetto AWA e non ai tuoi documenti privati
