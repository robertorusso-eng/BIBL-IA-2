# BIBL-IA 2 – il tuo percorso di studio, con un'AI che resta sul tuo computer

BIBL-IA 2 è un agente di studio per chi frequenta le superiori o prepara un test e i primi esami dell'università nell'area scientifica e sanitaria (Medicina, Professioni sanitarie, Biotecnologie, Chimica, Ingegneria e altri corsi). Lo studente fa domande, chiede mappe e quiz, segue un piano di studio; l'agente risponde partendo da testi controllati, aggiunge le ricerche scientifiche di università e centri di ricerca e tiene il conto di che cosa lo studente sa già e che cosa deve ripassare. L'intelligenza artificiale gira **sul computer** (Ollama, modello `gemma3:4b`): niente abbonamenti, nessun costo per domanda, e le domande degli studenti non vengono mandate a servizi di AI esterni.

## 1. Il problema

Chi studia materie scientifiche ha poco tempo, programmi lunghi e spesso nessuno a cui chiedere un dubbio la sera. Gli assistenti di AI generici rispondono subito, ma a volte inventano, non dicono da dove viene un'informazione, non sanno che cosa lo studente ha già studiato e chiedono un abbonamento o un account con i propri dati. Per uno studente delle superiori o del primo anno serve uno strumento gratuito, che risponda **dentro il programma**, dica onestamente quando non sa, e aiuti a organizzare lo studio, non solo a ricevere risposte.

## 2. La soluzione: che cosa fa l'agente

- **Biblioteca.** Si scrive una domanda in italiano o in inglese. L'agente cerca nei testi controllati di BIBL-IA (lezioni, schede, mappe, spiegazioni) e l'AI scrive la spiegazione con una struttura fissa: che cos'è, esempi, dove si vede, come si calcola, in breve. Se la domanda chiede **le differenze** tra due cose (per esempio mitosi e meiosi), risponde con una tabella delle differenze riga per riga, che cosa hanno in comune e un trucco per non confonderle.
- **Ricerche di università ed enti.** Sotto la risposta si possono aprire le rassegne scientifiche pubblicate su Europe PMC (che comprende PubMed), con il nome dell'ente che le ha fatte e una sintesi in italiano.
- **Tutor AI.** Una chat con un professore virtuale che conosce il profilo dello studente; se richiesto disegna una **mappa concettuale** nella chat.
- **Interrogazione orale.** Il professore fa a voce le domande di una lezione; lo studente risponde al microfono (la voce la trascrive il computer, senza internet) o scrivendo. Il professore dice che cosa ha detto bene, che cosa manca e gli errori, poi spiega la risposta e propone una domanda di approfondimento. La correzione confronta la risposta con i testi controllati della lezione, e un controllo del programma toglie i meriti per cose che lo studente non ha detto: è un allenamento, non un voto.
- **Collegamenti tra argomenti.** Solo se lo studente lo chiede (o sceglie tra i collegamenti già pronti), il tutor mostra come un argomento porta all'altro, per esempio glicolisi → ciclo di Krebs → catena respiratoria, con la molecola che fa da ponte e le reazioni di ogni tappa. I collegamenti sono scritti e controllati a mano, non inventati dall'AI.
- **Piano di studio, quiz, flashcard, simulazioni d'esame.** Test di livello iniziale, piano per giorni, ripasso degli argomenti più deboli, oltre 6.000 domande scritte per BIBL-IA con la spiegazione.
- **Reazioni passo per passo** in 23 percorsi di chimica e biochimica (glicolisi, ciclo di Krebs, fotosintesi, acidi e basi…): equazione generale bilanciata, ogni passaggio con enzima e formule, e le molecole di partenza e di arrivo in 3D da ruotare.
- **Mappe concettuali** (oltre 600), **modelli 3D** di 3.149 molecole e 82 organi, **Sintomi e cure** (circa 580 schede su fonti ufficiali, con l'avviso che non è un consulto medico).
- **Piani di studio ufficiali** di 24 corsi di laurea, presi dai siti delle università.
- **Classi.** Un professore crea una classe, i ragazzi entrano con un codice, il professore assegna compiti e vede chi è in difficoltà.

## 3. Come funziona l'agente

| Componente | In BIBL-IA 2 |
|---|---|
| Percezione | Legge la domanda, la lingua, il tipo di richiesta (spiegazione, differenze, mappa) e il profilo dello studente (corso, livello, argomenti deboli). |
| Pianificazione | Sceglie la strada: risposta già pronta → mappa controllata → testi di BIBL-IA + AI; per le differenze cerca i testi di entrambe le cose. |
| Strumenti | Ricerca per significato (`paraphrase-multilingual-MiniLM-L12-v2`), AI locale (Ollama `gemma3:4b`), Europe PMC per le ricerche, RDKit per le molecole, Graphviz per le mappe. |
| Memoria | Profilo dello studente, storico dei quiz, chat del tutor, banca delle **risposte già pronte** (una domanda uguale o quasi uguale riceve la risposta in 1-2 secondi invece di oltre un minuto). |
| Verifica | L'AI usa prima di tutto i testi controllati e le è chiesto di non inventare numeri; le ricerche scientifiche passano tre filtri (somiglianza del titolo, rassegne recenti, controllo SÌ/NO dell'AI sulla pertinenza); le risposte votate male (1-2 stelle) vengono tolte dalla banca e rifatte. |

## 4. Dati usati

- **Testi di BIBL-IA**: lezioni, schede e mappe scritte e controllate per il progetto. Il repository **non contiene libri** né frasi copiate dai libri.
- **Domande**: scritte per BIBL-IA. Le domande delle prove ufficiali degli anni passati non sono nel repository: chi le ha può metterle in `contenuti_v2/banca_ufficiale.json` sul proprio computer.
- **Fonti pubbliche**: Europe PMC (solo le parole dell'argomento vengono inviate, mai dati dello studente), PubChem per le molecole, BodyParts3D per gli organi, ISS / Ministero della Salute / OMS / Manuale MSD per le schede di salute, siti ufficiali degli atenei per i piani di studio (fonti in `contenuti_v2/ricerca_programmi/`).
- **Dati degli studenti**: restano solo sul computer dove gira BIBL-IA (profili, classi, account in file locali esclusi da Git). Le password sono salvate con PBKDF2 e non compaiono mai.

## 5. Installazione e avvio (Mac)

Servono Python 3.9 o successivo e [Ollama](https://ollama.com).

```bash
git clone <indirizzo di questo repository> BIBL-IA-2
cd BIBL-IA-2
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
ollama pull gemma3:4b
```

Poi doppio clic su `avvia_bibl_ia_2.command` (oppure `./avvia_bibl_ia_2.command` dal Terminale) e si apre http://localhost:8767. Alla prima domanda BIBL-IA prepara l'indice di ricerca (qualche minuto, una volta sola). Facoltativi: `imposta_password_pannello.command` per le password del Pannello di gestione, `imposta_email.command` per le email ai professori, `prepara_risposte_v2.py` per preparare in anticipo le risposte più frequenti. Per provare l'app senza toccare i dati veri: `BIBLIA_PROVE=1` e i profili finti in `prove/studenti`.

## 6. Test, casi limite e limiti noti

I risultati dei test sono in [TEST.md](TEST.md): prove automatiche di tutte le pagine con 10 studenti finti, tempi di risposta e casi limite provati con l'AI vera (domanda fuori programma, errori di battitura, inglese, differenze, richiesta di diagnosi medica, tentativo di far ignorare le istruzioni all'AI).

**Limiti noti.** `gemma3:4b` è un modello piccolo: a volte sbaglia un dettaglio (in una prova ha scritto che la meiosi avviene «nelle ossa»); per questo le risposte dicono sempre che sono scritte dall'AI e si possono votare e segnalare. Una domanda nuova richiede circa un minuto su un Mac con 8 GB di RAM; con molte persone insieme le risposte arrivano una alla volta. Alcune ricerche scientifiche trovate sono solo vicine all'argomento. Mancano ancora le lezioni di Italiano e Storia per le superiori e circa 120 capitoli dei programmi ministeriali.

La revisione etica è in [ethics-review.md](ethics-review.md).
