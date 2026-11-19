# Come scrivere una voce di risposte_cure

Ogni file è una lista JSON di oggetti {"nome": ..., "sinonimi": [...], "testo": ..., "sintomo": true/false}.

- **nome**: nome base in minuscolo, senza articolo.
- **sinonimi**: altri modi in cui uno studente potrebbe scriverla: sigle, nomi comuni, nome del germe se è usato come nome della malattia, varianti senza accenti, plurali.
  - MAI parole ambigue che indicano un'altra malattia (per esempio "tifo" da solo, "angina" da sola, "ulcera" da sola, "cellulite" da sola).
  - MAI parole che sono già il nome di una voce esistente: controlla con lo script qui sotto.
- **sintomo**: true solo se la voce è un sintomo (per esempio nausea, prurito), altrimenti false.
- **testo**: Markdown di 250-450 parole, con esattamente questi titoli numerati:
  1. **Di che cosa si tratta**: causa (agente eziologico preciso se è infettiva), come si manifesta e, se è contagiosa, come si trasmette.
  2. **Come si cura**: misure non farmacologiche e classi o principi attivi di prima scelta secondo le linee guida attuali (OMS, ISS, AIFA, ESC, NICE, CDC, IDSA). Spiega brevemente il meccanismo d'azione solo se ne sei certo. Se non c'è una terapia specifica, dillo chiaramente. Per i tumori descrivi le opzioni in generale (chirurgia, radioterapia, terapie mediche), senza schemi.
  3. **Prevenzione**: i vaccini, precisando se sono obbligatori o raccomandati in Italia, e le altre misure.
  4. **Quando rivolgersi al medico**: i segnali d'allarme.
- MAI dosi, posologie, durate in mg o nomi commerciali; niente diagnosi.
- Scrivi solo fatti certi e verificati. Se un punto è controverso, ometti il dettaglio invece di rischiare un errore. Ricontrolla ogni meccanismo d'azione.
- Nessun saluto e nessuna frase introduttiva: si comincia dal punto 1.
- Usa un italiano corretto, per studenti di medicina e farmacia.

Nomi e sinonimi già usati (non ripeterli):
  python3 -c "import json,glob;print(sorted({s for f in glob.glob('risposte_cure/parte*.json') for x in json.load(open(f)) for s in [x['nome'],*x['sinonimi']]}))"

Alla fine controlla che il file sia JSON valido e conta le voci.
