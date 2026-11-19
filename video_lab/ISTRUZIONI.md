# Video per il Laboratorio di BIBL-IA 2

Per ogni chiave della tua lista trova i video YouTube MIGLIORI per spiegare quell'argomento a uno studente
(superiori / primo anno di università): 2-3 in italiano e 1-2 in inglese quando ci sono, chiari, corretti, di
canali affidabili (docenti, università, canali didattici noti), preferibilmente brevi (3-20 minuti). Niente
video di bassa qualità, clickbait, solo musica o con dati sbagliati.

Per OGNI video verifica che esista davvero e prendi titolo e canale reali con l'oEmbed di YouTube:
`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<ID>&format=json`
(se l'oEmbed dà errore, il video non va messo). Il titolo deve corrispondere all'argomento.

Formato del file di uscita (JSON, chiave esatta → lista ordinata dal migliore):
```json
{"<chiave esatta>": [{"id": "<ID>", "titolo": "<titolo dall'oEmbed>", "canale": "<author_name dall'oEmbed>",
  "url": "https://www.youtube.com/watch?v=<ID>", "lingua": "it" oppure "en"}]}
```
Salva il file a blocchi (ogni 5-8 chiavi carica, aggiungi, riscrivi con json.dump ensure_ascii=False indent=1),
così il lavoro fatto resta. Se per una chiave non trovi niente di buono, metti una lista vuota.
Usa per i tuoi script una sottocartella tua dello scratchpad (non file con nomi generici condivisi).
