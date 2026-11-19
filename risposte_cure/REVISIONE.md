# Revisione medica delle risposte_cure

Sei un revisore medico esperto (medicina interna, malattie infettive, farmacologia, sanità pubblica italiana).
Leggi TUTTE le voci dei file indicati: sono liste JSON con {nome, sinonimi, testo, sintomo}.

Cerca solo errori **di fatto**:
- agente eziologico sbagliato;
- farmaco di prima scelta sbagliato o superato;
- meccanismo d'azione sbagliato;
- vie di trasmissione sbagliate;
- obblighi o raccomandazioni vaccinali italiane errate: in Italia sono obbligatori per i minori anti-poliomielite, difterite, tetano, epatite B, pertosse, Haemophilus influenzae b, morbillo, parotite, rosolia e varicella (legge 119/2017);
- consigli pericolosi;
- dosi o nomi commerciali, che non devono esserci;
- sinonimi sbagliati che indicano un'altra malattia.

NON segnalare scelte di stile, omissioni, sfumature discutibili o punti su cui le linee guida differiscono legittimamente.

Scrivi il risultato in un file JSON (il percorso è indicato nel compito): una lista di correzioni
{"file": "parteN.json", "nome": "...", "campo": "testo" | "sinonimi", "sbagliato": "frase esatta presente nel testo, copiata carattere per carattere", "corretto": "testo sostitutivo", "motivo": "breve spiegazione con la fonte (linea guida)"}.

Per i sinonimi da togliere usa "campo": "sinonimi", "sbagliato": il sinonimo, "corretto": "".
"sbagliato" deve essere una sottostringa esatta del testo, abbastanza lunga da essere unica.
NON modificare i file originali. Se non trovi errori, scrivi [].
Rispondi alla fine con il numero di correzioni e le 3 più importanti.
