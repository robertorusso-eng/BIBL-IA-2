# Fonti e controllo delle schede di risposte_cure

Ogni file `parteN.json` è una lista di schede {nome, sinonimi, testo, sintomo}.
Per OGNI scheda dei file assegnati:

1. **Trova 2-3 fonti affidabili** che parlano proprio di quella malattia o di quel sintomo, preferendo questo ordine:
   - fonti italiane: ISS EpiCentro (epicentro.iss.it), ISSalute (issalute.it), Ministero della Salute (salute.gov.it), AIFA (aifa.gov.it);
   - fonti internazionali: OMS (who.int, fact sheet), CDC (cdc.gov), ECDC (ecdc.europa.eu), NICE (nice.org.uk, CKS o linee guida), NHS (nhs.uk), Manuale MSD in italiano (msdmanuals.com/it), MedlinePlus (medlineplus.gov).

   Usa la ricerca web e APRI ogni pagina (WebFetch) per controllare che:
   - esista;
   - parli di quella malattia;
   - dica come si cura.

   NON inventare link e NON costruirli a memoria. Ogni URL deve essere stato aperto con successo da te. Niente Wikipedia, blog, siti commerciali o di cliniche private.

   Le ricerche web della sessione sono limitate e condivise con altri agenti, quindi usale con parsimonia. Trova i link soprattutto navigando gli indici ufficiali dei siti:
   - elenco dei fact sheet OMS: https://www.who.int/news-room/fact-sheets
   - indice delle malattie di EpiCentro: https://www.epicentro.iss.it/
   - mappa del sito di ISSalute;
   - indici del Manuale MSD in italiano;
   - elenco delle malattie NHS: https://www.nhs.uk/conditions/
   - indice di MedlinePlus;
   - indice A-Z del CDC.

   Le pagine di salute.gov.it e di NICE spesso non si aprono (controllo anti-bot o errore 403): non usarle.

2. **Confronta il testo della scheda con le fonti**, in particolare la parte «Come si cura». Se trovi:
   - un errore di fatto;
   - un farmaco di prima scelta diverso;
   - un'indicazione superata;

   correggi il testo. Se manca un'informazione importante sulla cura o sulla prevenzione (per esempio un vaccino raccomandato in Italia), aggiungila in una frase.

   Restano le regole di sempre:
   - mai dosi, posologie, durate in mg o nomi commerciali;
   - i 4 titoli numerati;
   - 250-480 parole.

3. **Aggiungi alla scheda il campo** `"fonti": [{"titolo": "Ente – Titolo della pagina", "url": "https://..."}]`, con le fonti nell'ordine di importanza. Per esempio: `{"titolo": "ISS EpiCentro – Tubercolosi", "url": "https://www.epicentro.iss.it/tubercolosi/"}`.

4. **Scrivi il file** con `json.dump(..., ensure_ascii=False, indent=1)`, mantenendo l'ordine delle schede e tutti gli altri campi. Salva il file appena hai finito le sue schede, prima di passare al file successivo, così il lavoro non si perde se ti interrompi.

5. **Tieni un registro delle correzioni** in `risposte_cure/correzioni_fonti/<parteN>.json`: una lista di {"nome", "prima": "frase originale", "dopo": "frase nuova", "fonte": "url"}. Se non ci sono correzioni, la lista è vuota.

Lavora per gruppi di schede. Se una pagina non si apre, cercane un'altra affidabile. Ogni scheda deve avere almeno 2 fonti; se per una malattia rara ne trovi solo una affidabile, va bene una.

Alla fine rispondi con:
- il numero di schede completate;
- il numero di correzioni;
- le 3 correzioni più importanti.
