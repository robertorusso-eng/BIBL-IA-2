# Come scrivere un percorso BIBL-IA (per chi aiuta a scriverli)

Lavora SOLO nei due file della tua parte: `mappe/parti/percorsi_N.json` e `mappe/parti/schede_N.json`
(N = il tuo numero). Non toccare altri file del progetto.

Esempi completi da imitare: le chiavi "glicolisi", "fosforilazione ossidativa", "gluconeogenesi" in
`mappe/percorsi.json` e le schede in `mappe/schede.json` (leggile prima di iniziare).

## percorsi_N.json — un oggetto { "<argomento>": {...} }
La chiave deve essere IDENTICA al campo "argomento" della mappa in `mappe/mappe_pronte.json`.
Campi:
- "titolo": breve e chiaro (es. "Apparato respiratorio: il percorso dell'aria")
- "dove": dove avviene
- "inizio": nome del primo elemento (deve avere una scheda)
- "intro": 2-4 frasi chiare
- "fasi": [{"da": numero_passaggio, "nome": "..."}] (può essere [])
- "passaggi": 5-12 passaggi in ordine, ognuno:
  {"da": [nomi], "a": [nomi], "enzima": "chi fa il lavoro (enzima, organo, struttura, cellula, ormone...)",
   "entra": [nomi], "esce": [nomi], "nota": "1-2 frasi corrette", facoltativi: "irreversibile": true,
   "limitante": true (tappa che regola), "volte": 2}
  Il campo si chiama "enzima" anche quando chi lavora è un organo o una struttura.
  "a" di un passaggio è normalmente il "da" del successivo (è un percorso, non una ragnatela).
- "titolo_bilancio": per argomenti non chimici usa "In sintesi"
- "bilancio": 2-4 righe di riassunto
- facoltativi: "dopo": {"titolo", "strade": [{"condizione","da","a","enzima","entra","esce","nota","prossimo"?}]}
  e "da_sapere": [{"titolo": "...", "voci": [["titolo voce", [nomi con scheda]], ...]}]
  (es. per il digerente: monosaccaridi/disaccaridi/polisaccaridi; usa i nomi già esistenti quando ci sono).

## schede_N.json — un oggetto { "<nome>": {...} }
OGNI nome usato in inizio/da/a/enzima/entra/esce/da_sapere deve avere una scheda, qui o già in
`mappe/schede.json` (se esiste già lì NON riscriverla, riusa il nome identico).
Campi: "tipo" (uno di: zucchero, molecola, enzima, energia, coenzima, piccola, struttura),
"base" (primaria e medie: parole semplici, esempi di vita quotidiana, niente nomi tecnici),
"superiore" (liceo: definizione corretta e classificazione, es. «disaccaride: glucosio + galattosio»),
"universita" (dettagli precisi: per gli enzimi classe/EC, substrati, cofattori, regolazione; per strutture
istologia/fisiologia con valori numerici quando utili), "clinica" (nota per Medicina 4°-6° anno: malattia,
esame o farmaco collegato; "" se non c'è niente di davvero utile), facoltativo "smiles" SOLO per molecole
piccole di cui sei sicuro (verifica con RDKit: ./venv/bin/python -c "from rdkit import Chem; ...").
Usa "struttura" per organi, tessuti, cellule, parti del corpo e fasi/strutture cellulari.

## Regole
- Italiano corretto, frasi brevi, contenuti scientificamente esatti (livello di un buon manuale
  universitario). Niente invenzioni: se non sei sicuro di un numero, non metterlo.
- Unicode per pedici e apici (O₂, Ca²⁺, Na⁺).
- Alla fine esegui il controllo: ./venv/bin/python mappe/parti/controlla.py N  e correggi finché dice OK.

## Argomenti nuovi (non ancora tra le mappe pronte): anche pronte_N.json e base_N.json
Per un argomento che non è in `mappe/mappe_pronte.json` scrivi anche:
- `mappe/parti/pronte_N.json` — una LISTA di mappe pronte, come quelle di `mappe/mappe_pronte.json`:
  {"argomento": "<stessa chiave del percorso>", "categoria": "<area>", "parole": [sinonimi italiani e
  inglesi per trovarla], "relazioni": [10-25 × {"da", "relazione", "a"}], "fonti": ["Mappa pronta BIBL-IA"]}.
  La mappa pronta è il quadro d'insieme (cosa è, dove, chi, perché, regolazione, legami con altri argomenti),
  non la copia dei passaggi.
- `mappe/parti/base_N.json` — un oggetto {"<argomento in minuscolo>": [[da, relazione, a], ...]}: 9-14 righe
  per primaria e medie, parole semplici, esempi di vita quotidiana, niente nomi tecnici (come le chiavi
  "glicolisi" o "mitosi" di `mappe/mappe_base.json`). Le prime 6 righe da sole devono già avere senso
  (primaria 1ª-2ª), le prime 9 la primaria 3ª-5ª.
Il controllo (`controlla.py N`) legge anche questi due file.
