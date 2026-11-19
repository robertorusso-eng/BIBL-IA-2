# Nuove domande di BIBL-IA 2 (con risposta e spiegazione)

Scrivi domande ORIGINALI (non copiate da libri o da prove protette), nello stile dei test di ammissione italiani
(o degli esami universitari, se richiesto), ognuna già con la spiegazione. File di uscita: una LISTA JSON.

## Domanda a risposta multipla
```json
{"id": "<prefisso>-<numero>", "materia": "...", "argomento": "uno degli argomenti indicati", "livello": "test" | "università",
 "domanda": "...", "opzioni": {"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}, "giusta": "C",
 "perche": "3-6 frasi: perché è giusta e qual è l'errore tipico (nomina le opzioni trappola)",
 "semplice": "3-5 frasi semplici con un esempio concreto",
 "passaggi": ["passaggi numerati del calcolo/ragionamento, con il risultato che coincide con l'opzione giusta"] oppure [],
 "concetto": "concetto chiave in 2-6 parole"}
```
## Domanda a completamento (solo dove richiesto)
```json
{"id": "...", "materia": "...", "argomento": "...", "livello": "test", "tipo": "completamento",
 "domanda": "frase con ___ al posto della parola o del numero mancante", "risposta": "parola o numero",
 "accettate": ["varianti giuste accettate: sinonimi, singolare/plurale, con o senza unità…"],
 "perche": "...", "semplice": "...", "passaggi": [...], "concetto": "..."}
```
Regole:
- Una sola risposta giusta, senza ambiguità; distrattori plausibili (errori tipici veri); niente «tutte le precedenti».
- Varia la posizione della lettera giusta (A-E distribuite in modo uniforme) e il tipo di domanda (definizioni,
  ragionamento, applicazione, calcolo, casi).
- Rifai sempre i conti; unità di misura corrette; simboli Unicode (H₂O, m/s², ⇌, √).
- Difficoltà mista: 30% facili, 50% medie, 20% difficili, come nei test veri.
- Salva a blocchi di circa 25 domande (carica il file se esiste, aggiungi, riscrivi con json.dump ensure_ascii=False
  indent=1). Usa per gli script una TUA sottocartella dello scratchpad, mai file con nomi generici condivisi.
- Alla fine controlla con uno script: id unici, campi completi, «giusta» tra le opzioni, lettere giuste ben distribuite,
  nessuna domanda ripetuta.

## Domande degli esami universitari (file esami_*.json)
Stesso formato della risposta multipla, con in più `"area": "<nome dell'area, esatto>"` e `"livello": "università"`.
Domande da esame universitario vero del primo-quinto anno (non da test di ammissione): concetti, applicazione,
casi semplici, esercizi; per l'ingegneria e le materie scientifiche molti esercizi con il calcolo nei "passaggi".
Copri in modo equilibrato i diversi esami dell'area (l'elenco degli esami di ogni area è nel file del tuo lotto).
Contenuti da manuale universitario: per farmaci, tossici e procedure cliniche solo meccanismi, indicazioni, effetti
avversi e principi generali (niente dosaggi da applicare a un paziente, niente usi impropri).
Salva ogni 10 domande.
