# -*- coding: utf-8 -*-
"""Impianti delle operazioni unitarie (distillazione, assorbimento, estrazione, evaporazione, cristallizzazione,
essiccamento, filtrazione, membrane, frazionamento dell'aria, scambio ionico, adsorbimento, ciclo frigorifero),
come nei manuali di impianti chimici degli istituti tecnici e di ingegneria chimica.

Stesso formato di IMPIANTI in chimica_v2.py: "reazione", "condizioni", "descrizione" (passaggi), "perche",
"unita" [(nome, tipo)], "correnti" [(da, a, che cosa passa)], "parole" (radici minuscole da cercare nel testo).
I tipi di apparecchio sono quelli di chimica_v2.TIPI_UNITA più TIPI_UNITA_EXTRA (forme graphviz).
"""

# Nuovi tipi di apparecchio → forma graphviz
TIPI_UNITA_EXTRA = {
    "Ribollitore": "egg",
    "Evaporatore": "Msquare",
    "Cristallizzatore": "invtriangle",
    "Essiccatore": "parallelogram",
    "Centrifuga": "doublecircle",
    "Estrattore": "cds",
    "Decantatore": "Mdiamond",
    "Membrana": "component",
    "Torre di raffreddamento": "septagon",
    "Eiettore/pompa a vuoto": "Mcircle",
    "Ciclone": "pentagon",
    "Colonna a riempimento": "cds",
    "Adsorbitore": "folder",
    "Colonna a scambio ionico": "folder",
    "Caldaia": "tab",
    "Valvola di laminazione": "rarrow",
    "Turboespansore": "square",
    "Mulino": "star",
}


IMPIANTI_OPERAZIONI = {
    # ------------------------------------------------------------------ DISTILLAZIONE
    "Distillazione continua binaria (colonna a piatti)": {
        "reazione": "Nessuna reazione: operazione fisica — separazione per differenza di volatilità "
                    "(equilibrio liquido-vapore, legge di Raoult); esempio benzene-toluene",
        "condizioni": "pressione atmosferica; testa ≈ 80 °C (benzene, Teb 80,1 °C), fondo ≈ 110 °C (toluene, Teb 110,6 °C); "
                      "volatilità relativa α ≈ 2,4; 20-40 piatti reali (efficienza 50-80%); rapporto di riflusso "
                      "R = L/D ≈ 1,2-1,5 volte il minimo; alimentazione liquida al punto di ebollizione",
        "descrizione": [
            "La miscela da separare arriva in un serbatoio di stoccaggio; una pompa la invia alla colonna a portata "
            "costante, regolata.",
            "Prima di entrare la miscela è preriscaldata fino alla temperatura di ebollizione in uno scambiatore che "
            "recupera il calore del residuo caldo uscito dal fondo (recupero energetico).",
            "La miscela entra al piatto di alimentazione ottimale, quello che ha composizione simile: sopra c'è la zona "
            "di arricchimento (rettifica), sotto la zona di esaurimento (stripping).",
            "Su ogni piatto il vapore che sale gorgoglia nel liquido che scende: il vapore si arricchisce del componente "
            "più volatile (benzene), il liquido di quello meno volatile (toluene).",
            "In testa i vapori sono condensati del tutto nel condensatore, raffreddato con acqua; il liquido va "
            "nell'accumulatore del riflusso.",
            "Dall'accumulatore una pompa rimanda in colonna una parte del liquido (riflusso L) e preleva il resto come "
            "distillato D, quasi benzene puro; il rapporto L/D è il rapporto di riflusso.",
            "Sul fondo il ribollitore, scaldato con vapore di rete, vaporizza parte del liquido e rimanda il vapore in "
            "colonna; il liquido che resta esce come residuo (toluene), cede calore all'alimentazione e va allo stoccaggio.",
        ],
        "perche": "Il vapore in equilibrio con un liquido è più ricco del componente più volatile (Raoult): ogni piatto "
                  "è uno stadio di equilibrio e la colonna li ripete in controcorrente, liquido che scende e vapore che "
                  "sale. Con il metodo di McCabe-Thiele, sul diagramma y-x con le rette di lavoro e la retta q, si "
                  "contano i piatti teorici e si trova il piatto di alimentazione ottimale. Più riflusso significa meno "
                  "piatti ma più vapore al ribollitore e più acqua al condensatore: a riflusso totale servono i piatti "
                  "minimi, a riflusso minimo infiniti piatti; l'ottimo economico è circa 1,2-1,5 volte il minimo.",
        "unita": [("Miscela benzene-toluene", "Alimentazione"), ("Serbatoio di alimentazione", "Serbatoio"),
                  ("Pompa di alimentazione", "Pompa"), ("Preriscaldatore (recupero)", "Scambiatore di calore"),
                  ("Colonna a piatti", "Colonna di distillazione"), ("Condensatore di testa", "Condensatore"),
                  ("Accumulatore del riflusso", "Serbatoio"), ("Pompa di riflusso", "Pompa"),
                  ("Distillato (benzene)", "Prodotto"), ("Ribollitore", "Ribollitore"),
                  ("Residuo (toluene)", "Prodotto"), ("Acqua di raffreddamento", "Alimentazione"),
                  ("Ritorno acqua calda", "Spurgo"), ("Vapore di rete", "Alimentazione"), ("Condensa", "Spurgo")],
        "correnti": [("Miscela benzene-toluene", "Serbatoio di alimentazione", ""),
                     ("Serbatoio di alimentazione", "Pompa di alimentazione", ""),
                     ("Pompa di alimentazione", "Preriscaldatore (recupero)", "alimentazione fredda"),
                     ("Preriscaldatore (recupero)", "Colonna a piatti", "liquido saturo al piatto di alimentazione"),
                     ("Colonna a piatti", "Condensatore di testa", "vapori di testa ≈ 80 °C"),
                     ("Condensatore di testa", "Accumulatore del riflusso", "condensato"),
                     ("Accumulatore del riflusso", "Pompa di riflusso", ""),
                     ("Pompa di riflusso", "Colonna a piatti", "riflusso L"),
                     ("Pompa di riflusso", "Distillato (benzene)", "distillato D"),
                     ("Colonna a piatti", "Ribollitore", "liquido di fondo"),
                     ("Ribollitore", "Colonna a piatti", "vapore (boil-up)"),
                     ("Ribollitore", "Preriscaldatore (recupero)", "residuo caldo ≈ 110 °C"),
                     ("Preriscaldatore (recupero)", "Residuo (toluene)", "residuo raffreddato"),
                     ("Acqua di raffreddamento", "Condensatore di testa", "acqua ≈ 25 °C"),
                     ("Condensatore di testa", "Ritorno acqua calda", "acqua ≈ 40 °C"),
                     ("Vapore di rete", "Ribollitore", "vapore 3-5 bar"),
                     ("Ribollitore", "Condensa", "condensa")],
        "parole": ["piatt", "colonna", "condens", "riflusso", "accumulator", "ribollitor", "distillato", "residuo",
                   "volatil", "raoult", "equilibrio", "alimentazione", "mccabe", "arricchimento", "esaurimento",
                   "vapore", "preriscald"],
    },

    "Distillazione discontinua (batch)": {
        "reazione": "Nessuna reazione: operazione fisica — separazione per differenza di volatilità; la composizione "
                    "nel bollitore cambia nel tempo (equazione di Rayleigh)",
        "condizioni": "pressione atmosferica o vuoto moderato; carica di qualche m³; colonna corta a piatti o a "
                      "riempimento (5-15 stadi teorici); riflusso crescente nel tempo per tenere costante la purezza "
                      "del distillato; durata di un ciclo: alcune ore",
        "descrizione": [
            "La miscela viene caricata tutta insieme nel bollitore, un recipiente con camicia o serpentino scaldato a "
            "vapore; poi l'alimentazione si chiude.",
            "Il liquido bolle e i vapori salgono nella colonna di rettifica sopra il bollitore, dove incontrano il "
            "riflusso che scende.",
            "In testa i vapori condensano nel condensatore ad acqua e il liquido arriva al ripartitore del riflusso, che "
            "rimanda una parte in colonna e manda il resto ai serbatoi dei tagli.",
            "Per prime escono le teste, ricche del componente più volatile; quando la composizione del distillato "
            "cambia si passa al serbatoio successivo.",
            "Si raccoglie il taglio di cuore (il prodotto voluto); per mantenerlo puro mentre il bollitore si impoverisce "
            "si aumenta via via il rapporto di riflusso.",
            "Seguono le code (taglio intermedio, che si ricarica nel lotto successivo); alla fine si spegne il "
            "riscaldamento e si scarica il residuo dal bollitore.",
        ],
        "perche": "Non c'è stato stazionario: il bollitore si impoverisce del componente leggero e le temperature salgono "
                  "nel tempo. L'equazione di Rayleigh, ln(W₀/W) = ∫ dx/(y − x), lega la quantità rimasta alle "
                  "composizioni. La si usa per piccole produzioni, prodotti diversi nello stesso impianto (chimica fine, "
                  "farmaceutica, distillerie di grappa) e per recuperare solventi: è flessibile ma consuma più energia "
                  "della distillazione continua.",
        "unita": [("Carica della miscela", "Alimentazione"), ("Bollitore", "Ribollitore"),
                  ("Colonna di rettifica", "Colonna di distillazione"), ("Condensatore", "Condensatore"),
                  ("Ripartitore del riflusso", "Valvola"), ("Serbatoio teste", "Serbatoio"),
                  ("Prodotto di cuore", "Prodotto"), ("Serbatoio code", "Serbatoio"), ("Residuo", "Spurgo"),
                  ("Vapore di riscaldamento", "Alimentazione"), ("Acqua di raffreddamento", "Alimentazione")],
        "correnti": [("Carica della miscela", "Bollitore", "carica iniziale"),
                     ("Bollitore", "Colonna di rettifica", "vapori"),
                     ("Colonna di rettifica", "Bollitore", "liquido che ricade"),
                     ("Colonna di rettifica", "Condensatore", "vapori di testa"),
                     ("Condensatore", "Ripartitore del riflusso", "condensato"),
                     ("Ripartitore del riflusso", "Colonna di rettifica", "riflusso (crescente)"),
                     ("Ripartitore del riflusso", "Serbatoio teste", "1° taglio"),
                     ("Ripartitore del riflusso", "Prodotto di cuore", "2° taglio"),
                     ("Ripartitore del riflusso", "Serbatoio code", "3° taglio"),
                     ("Serbatoio code", "Bollitore", "ricarica al lotto successivo"),
                     ("Bollitore", "Residuo", "a fine ciclo"),
                     ("Vapore di riscaldamento", "Bollitore", "camicia/serpentino"),
                     ("Acqua di raffreddamento", "Condensatore", "")],
        "parole": ["discontinu", "batch", "carica", "bollitor", "tagli", "teste", "cuore", "code", "riflusso",
                   "rayleigh", "condens", "tempo", "residuo"],
    },

    "Rettifica dell'alcol etilico": {
        "reazione": "Nessuna reazione: operazione fisica — separazione per volatilità dell'etanolo dall'acqua; il limite "
                    "è l'azeotropo di massima volatilità al 95,6% in massa (≈ 97,2% vol) che bolle a 78,2 °C",
        "condizioni": "pressione atmosferica; vino o mosto fermentato all'8-12% vol; flemma al 40-50% vol; alcol "
                      "rettificato al 96% vol; vapore diretto sul fondo della colonna di esaurimento (≈ 100-105 °C), "
                      "testa della colonna di rettifica ≈ 78 °C; rapporti di riflusso alti (3-6)",
        "descrizione": [
            "Il liquido fermentato è preriscaldato con i vapori/residui caldi dell'impianto ed entra in alto nella "
            "colonna di esaurimento (colonna distillatrice).",
            "Nella colonna di esaurimento si immette vapore diretto dal fondo: l'alcol passa nel vapore e dal fondo esce "
            "la borlanda, acqua quasi priva di alcol con i solidi del mosto.",
            "Dalla testa escono le flemme (40-50% vol), che passano nella colonna di depurazione: qui si tolgono le "
            "teste, cioè le sostanze più volatili dell'etanolo (acetaldeide, acetato di etile, metanolo in parte).",
            "Le flemme depurate entrano nella colonna di rettifica, scaldata dal fondo; salendo i piatti l'alcol si "
            "concentra fino a circa il 96% vol.",
            "In testa i vapori condensano nel condensatore e una grande parte del liquido torna in colonna come riflusso; "
            "l'alcol buono si preleva qualche piatto sotto la testa (per lasciare in alto le ultime teste).",
            "Dai piatti intermedi-bassi si spillano gli oli di fusel (alcoli superiori: isoamilico, isobutilico), che "
            "si accumulano dove la gradazione è media; dal fondo esce la flemmaccia, acqua esausta.",
        ],
        "perche": "L'etanolo è più volatile dell'acqua, ma la miscela forma un azeotropo di massima volatilità al 95,6% in "
                  "massa: lì liquido e vapore hanno la stessa composizione e la distillazione non va oltre, per quanti "
                  "piatti si aggiungano. Per l'alcol anidro servono distillazione azeotropica o estrattiva, oppure i "
                  "setacci molecolari. Le impurezze si separano perché si concentrano a diverse altezze della colonna, "
                  "secondo la loro volatilità nella miscela alcol-acqua.",
        "unita": [("Mosto fermentato (8-12% vol)", "Alimentazione"), ("Preriscaldatore", "Scambiatore di calore"),
                  ("Colonna di esaurimento", "Colonna di distillazione"), ("Borlanda", "Spurgo"),
                  ("Colonna di depurazione", "Colonna di distillazione"), ("Teste (aldeidi, esteri)", "Spurgo"),
                  ("Colonna di rettifica", "Colonna di distillazione"), ("Condensatore di testa", "Condensatore"),
                  ("Accumulatore del riflusso", "Serbatoio"), ("Alcol rettificato 96% vol", "Prodotto"),
                  ("Oli di fusel", "Prodotto"), ("Flemmaccia", "Spurgo"), ("Ribollitore", "Ribollitore"),
                  ("Vapore di rete", "Alimentazione"), ("Acqua di raffreddamento", "Alimentazione")],
        "correnti": [("Mosto fermentato (8-12% vol)", "Preriscaldatore", ""),
                     ("Preriscaldatore", "Colonna di esaurimento", "mosto caldo in testa"),
                     ("Vapore di rete", "Colonna di esaurimento", "vapore diretto dal fondo"),
                     ("Colonna di esaurimento", "Borlanda", "fondo"),
                     ("Colonna di esaurimento", "Preriscaldatore", "flemme in vapore (cedono calore)"),
                     ("Preriscaldatore", "Colonna di depurazione", "flemme 40-50% vol"),
                     ("Colonna di depurazione", "Teste (aldeidi, esteri)", "testa"),
                     ("Colonna di depurazione", "Colonna di rettifica", "flemme depurate"),
                     ("Colonna di rettifica", "Condensatore di testa", "vapori ≈ 78 °C"),
                     ("Condensatore di testa", "Accumulatore del riflusso", ""),
                     ("Accumulatore del riflusso", "Colonna di rettifica", "riflusso"),
                     ("Colonna di rettifica", "Alcol rettificato 96% vol", "spillamento sotto la testa"),
                     ("Colonna di rettifica", "Oli di fusel", "spillamento laterale"),
                     ("Colonna di rettifica", "Ribollitore", "liquido di fondo"),
                     ("Ribollitore", "Colonna di rettifica", "vapore"),
                     ("Ribollitore", "Flemmaccia", "acqua esausta"),
                     ("Vapore di rete", "Ribollitore", "vapore indiretto"),
                     ("Acqua di raffreddamento", "Condensatore di testa", "")],
        "parole": ["azeotrop", "95,6", "96", "flemm", "borlanda", "esaurimento", "rettifica", "teste", "fusel",
                   "riflusso", "condens", "vapore", "piatt", "spill"],
    },

    "Distillazione in corrente di vapore (oli essenziali)": {
        "reazione": "Nessuna reazione: operazione fisica — distillazione di liquidi immiscibili con l'acqua: la "
                    "pressione totale è la somma delle tensioni di vapore (Dalton), quindi l'olio distilla sotto i 100 °C",
        "condizioni": "pressione atmosferica; vapore saturo a bassa pressione (0,5-1 bar relativi) attraverso la biomassa; "
                      "miscela che distilla a 95-100 °C; durata 1-3 ore per carica; rese dello 0,1-3% di olio sulla pianta",
        "descrizione": [
            "La caldaia produce vapore saturo a partire da acqua di alimento addolcita.",
            "Il vapore entra dal fondo del distillatore, un recipiente in acciaio inox con cesti forati riempiti con la "
            "pianta (per esempio lavanda, menta, rosmarino).",
            "Passando tra le foglie e i fiori il vapore fa evaporare gli oli essenziali, che sono immiscibili con "
            "l'acqua, e li trascina con sé.",
            "La miscela di vapore acqueo e vapori di olio va al condensatore raffreddato ad acqua, dove torna liquida.",
            "Il condensato entra nel vaso fiorentino (decantatore): l'olio, meno denso e immiscibile, si separa in "
            "superficie e si spilla; sotto resta l'idrolato (acqua aromatica).",
            "Parte dell'idrolato può tornare in caldaia (coobazione) per recuperare l'olio rimasto disciolto; a fine "
            "carica la biomassa esausta si scarica e si usa come compost o combustibile.",
        ],
        "perche": "Con due liquidi immiscibili ognuno esercita la sua tensione di vapore indipendentemente: la miscela "
                  "bolle quando la somma arriva alla pressione esterna, cioè sotto i 100 °C, anche se l'olio da solo "
                  "bollirebbe a 150-250 °C e si decomporrebbe. Così le sostanze profumate, delicate, si separano senza "
                  "degradarsi. Il vaso fiorentino sfrutta la differenza di densità e l'immiscibilità.",
        "unita": [("Acqua di alimento", "Alimentazione"), ("Caldaia", "Caldaia"),
                  ("Distillatore (cesti con la pianta)", "Vasca"), ("Biomassa esausta", "Spurgo"),
                  ("Condensatore", "Condensatore"), ("Vaso fiorentino", "Decantatore"),
                  ("Olio essenziale", "Prodotto"), ("Idrolato (acqua aromatica)", "Prodotto"),
                  ("Acqua di raffreddamento", "Alimentazione")],
        "correnti": [("Acqua di alimento", "Caldaia", ""),
                     ("Caldaia", "Distillatore (cesti con la pianta)", "vapore saturo dal fondo"),
                     ("Distillatore (cesti con la pianta)", "Condensatore", "vapore + vapori di olio"),
                     ("Distillatore (cesti con la pianta)", "Biomassa esausta", "a fine carica"),
                     ("Acqua di raffreddamento", "Condensatore", ""),
                     ("Condensatore", "Vaso fiorentino", "condensato a due fasi"),
                     ("Vaso fiorentino", "Olio essenziale", "fase leggera"),
                     ("Vaso fiorentino", "Idrolato (acqua aromatica)", "fase acquosa"),
                     ("Vaso fiorentino", "Caldaia", "coobazione (idrolato)")],
        "parole": ["vapore", "corrente di vapore", "immiscibil", "olio", "essenzial", "caldaia", "condens",
                   "vaso fiorentino", "fiorentin", "decant", "idrolato", "dalton", "tension", "100"],
    },

    "Distillazione sotto vuoto": {
        "reazione": "Nessuna reazione: operazione fisica — abbassando la pressione si abbassa la temperatura di "
                    "ebollizione (Clausius-Clapeyron), così si distillano sostanze che a pressione ambiente si "
                    "decomporrebbero; esempio glicerina grezza",
        "condizioni": "pressione in testa 5-15 mbar assoluti, fondo 160-190 °C (a 1 atm la glicerina bollirebbe a "
                      "290 °C decomponendosi); colonna a riempimento strutturato (bassa perdita di carico); ribollitore "
                      "a film per ridurre il tempo di permanenza; vuoto con eiettori a vapore",
        "descrizione": [
            "La glicerina grezza è preriscaldata e alimentata alla colonna, tenuta sotto vuoto spinto.",
            "Nella colonna, a riempimento strutturato, i vapori salgono incontrando il riflusso con perdite di carico "
            "piccolissime, indispensabili quando la pressione assoluta è di pochi millibar.",
            "Il ribollitore a film sottile vaporizza il liquido di fondo in pochi secondi, così il prodotto resta "
            "poco tempo ad alta temperatura.",
            "I vapori di testa condensano nel condensatore e il liquido si raccoglie nell'accumulatore; una pompa "
            "rimanda il riflusso in colonna e preleva la glicerina distillata.",
            "Gli incondensabili (aria entrata dalle guarnizioni, gas disciolti) sono aspirati dall'accumulatore "
            "dagli eiettori a vapore, che mantengono il vuoto e scaricano in atmosfera dopo un condensatore barometrico.",
            "Dal fondo esce il residuo pesante (sali, sostanze polimerizzate), raffreddato e smaltito.",
        ],
        "perche": "La temperatura di ebollizione dipende dalla pressione (equazione di Clausius-Clapeyron): a pochi "
                  "millibar una sostanza bolle anche 100 °C più in basso. Per non perdere il vuoto conta la perdita di "
                  "carico: per questo si usano riempimenti invece dei piatti. Lo stesso principio vale per il residuo "
                  "della distillazione del petrolio, per gli acidi grassi, le vitamine e gli aromi.",
        "unita": [("Glicerina grezza", "Alimentazione"), ("Preriscaldatore", "Scambiatore di calore"),
                  ("Colonna sotto vuoto (riempimento)", "Colonna a riempimento"), ("Condensatore di testa", "Condensatore"),
                  ("Accumulatore", "Serbatoio"), ("Pompa del distillato", "Pompa"),
                  ("Glicerina distillata", "Prodotto"), ("Eiettori a vapore", "Eiettore/pompa a vuoto"),
                  ("Scarico incondensabili", "Spurgo"), ("Ribollitore a film", "Ribollitore"),
                  ("Residuo pesante", "Spurgo"), ("Vapore motore", "Alimentazione")],
        "correnti": [("Glicerina grezza", "Preriscaldatore", ""),
                     ("Preriscaldatore", "Colonna sotto vuoto (riempimento)", "alimentazione calda"),
                     ("Colonna sotto vuoto (riempimento)", "Condensatore di testa", "vapori a 5-15 mbar"),
                     ("Condensatore di testa", "Accumulatore", "condensato"),
                     ("Accumulatore", "Pompa del distillato", ""),
                     ("Pompa del distillato", "Colonna sotto vuoto (riempimento)", "riflusso"),
                     ("Pompa del distillato", "Glicerina distillata", "distillato"),
                     ("Accumulatore", "Eiettori a vapore", "incondensabili"),
                     ("Vapore motore", "Eiettori a vapore", "vapore 8-10 bar"),
                     ("Eiettori a vapore", "Scarico incondensabili", "dopo condensatore barometrico"),
                     ("Colonna sotto vuoto (riempimento)", "Ribollitore a film", "liquido di fondo"),
                     ("Ribollitore a film", "Colonna sotto vuoto (riempimento)", "vapore"),
                     ("Ribollitore a film", "Residuo pesante", "")],
        "parole": ["vuoto", "pressione", "eiettor", "pompa a vuoto", "temperatura di ebollizione", "decompo",
                   "termosensibil", "clausius", "riempimento", "perdita di carico", "film", "condens", "riflusso",
                   "incondensabil"],
    },

    "Etanolo anidro (distillazione azeotropica con cicloesano)": {
        "reazione": "Nessuna reazione: operazione fisica — si aggiunge un trascinatore (cicloesano) che forma con acqua "
                    "ed etanolo un azeotropo ternario eterogeneo di minimo, a ≈ 62 °C, che porta via l'acqua in testa",
        "condizioni": "pressione atmosferica; alimentazione: alcol al 95% circa; testa della colonna azeotropica ≈ 62 °C, "
                      "fondo ≈ 78 °C (etanolo 99,5-99,9%); decantatore a 25-40 °C; piccolo reintegro di cicloesano",
        "descrizione": [
            "L'alcol al 95% entra nella colonna azeotropica, dove in testa circola il cicloesano (trascinatore).",
            "Il cicloesano forma con acqua ed etanolo un azeotropo ternario che bolle a circa 62 °C, più in basso di "
            "tutti gli altri componenti: sale in testa portando con sé l'acqua.",
            "Dal fondo della colonna, scaldata dal ribollitore, esce l'etanolo anidro (99,5-99,9%).",
            "I vapori di testa condensano e nel decantatore il liquido si divide in due fasi: una fase leggera ricca "
            "di cicloesano e una fase pesante acquosa.",
            "La fase ricca di cicloesano torna in testa alla colonna azeotropica come riflusso.",
            "La fase acquosa va alla colonna di recupero: in testa si recuperano cicloesano ed etanolo, che tornano al "
            "condensatore/decantatore; dal fondo esce acqua quasi pura.",
        ],
        "perche": "L'azeotropo acqua-etanolo non si supera distillando; il terzo componente crea un nuovo azeotropo, "
                  "ternario ed eterogeneo, che bolle più in basso e si smiscela quando condensa: la separazione delle "
                  "due fasi nel decantatore 'rompe' l'azeotropo e permette di riciclare il trascinatore. In passato si "
                  "usava il benzene, oggi tolto perché cancerogeno; un'alternativa moderna sono i setacci molecolari "
                  "(zeoliti 3 Å) che adsorbono l'acqua.",
        "unita": [("Alcol 95%", "Alimentazione"), ("Colonna azeotropica", "Colonna di distillazione"),
                  ("Ribollitore", "Ribollitore"), ("Etanolo anidro 99,8%", "Prodotto"),
                  ("Condensatore di testa", "Condensatore"), ("Decantatore", "Decantatore"),
                  ("Reintegro cicloesano", "Alimentazione"), ("Colonna di recupero", "Colonna di distillazione"),
                  ("Ribollitore di recupero", "Ribollitore"), ("Acqua", "Spurgo")],
        "correnti": [("Alcol 95%", "Colonna azeotropica", ""),
                     ("Colonna azeotropica", "Condensatore di testa", "azeotropo ternario ≈ 62 °C"),
                     ("Colonna azeotropica", "Ribollitore", "liquido di fondo"),
                     ("Ribollitore", "Colonna azeotropica", "vapore"),
                     ("Ribollitore", "Etanolo anidro 99,8%", ""),
                     ("Condensatore di testa", "Decantatore", "due fasi liquide"),
                     ("Decantatore", "Colonna azeotropica", "fase ricca di cicloesano (riflusso)"),
                     ("Reintegro cicloesano", "Decantatore", "piccole perdite"),
                     ("Decantatore", "Colonna di recupero", "fase acquosa"),
                     ("Colonna di recupero", "Condensatore di testa", "cicloesano + etanolo recuperati"),
                     ("Colonna di recupero", "Ribollitore di recupero", "liquido di fondo"),
                     ("Ribollitore di recupero", "Colonna di recupero", "vapore"),
                     ("Ribollitore di recupero", "Acqua", "acqua quasi pura")],
        "parole": ["azeotrop", "anidro", "cicloesano", "trascinator", "ternario", "decant", "due fasi", "fase",
                   "recupero", "riflusso", "62", "etanolo", "acqua", "setacci"],
    },

    "Etanolo anidro (distillazione estrattiva con glicole)": {
        "reazione": "Nessuna reazione: operazione fisica — un solvente pesante (glicole etilenico, Teb 197 °C) trattiene "
                    "l'acqua più dell'etanolo e cambia la volatilità relativa, facendo sparire l'azeotropo",
        "condizioni": "colonna estrattiva a pressione atmosferica, testa ≈ 78 °C; glicole alimentato pochi piatti sotto la "
                      "testa, in quantità paragonabile alla carica; colonna di recupero sotto vuoto (0,1-0,3 bar) per "
                      "non degradare il glicole; glicole raffreddato a 70-80 °C prima di tornare",
        "descrizione": [
            "L'alcol al 95% entra a metà della colonna estrattiva; poco sotto la testa entra il glicole etilenico "
            "rigenerato.",
            "Il glicole, quasi non volatile, scende lungo tutta la colonna e trattiene l'acqua (con cui forma legami a "
            "idrogeno più forti): l'etanolo diventa molto più volatile dell'acqua.",
            "In testa, dopo il condensatore e l'accumulatore, si ottiene etanolo anidro; una parte torna come riflusso. "
            "I pochi piatti sopra l'ingresso del glicole impediscono che il solvente passi nel distillato.",
            "Dal fondo, scaldato dal ribollitore, esce la miscela glicole + acqua, che va alla colonna di recupero.",
            "La colonna di recupero lavora sotto vuoto: in testa esce l'acqua, dal fondo il glicole rigenerato.",
            "Il glicole caldo è raffreddato in uno scambiatore e pompato di nuovo in cima alla colonna estrattiva "
            "(ciclo chiuso, con un piccolo reintegro).",
        ],
        "perche": "Il solvente modifica i coefficienti di attività: interagisce di più con l'acqua, ne abbassa la "
                  "volatilità e la volatilità relativa etanolo/acqua sale ben sopra 1 anche alle alte concentrazioni. "
                  "A differenza della distillazione azeotropica, il solvente non va in testa ma esce dal fondo, e si "
                  "recupera facilmente perché bolle molto più in alto dell'acqua.",
        "unita": [("Alcol 95%", "Alimentazione"), ("Colonna estrattiva", "Colonna di distillazione"),
                  ("Condensatore", "Condensatore"), ("Accumulatore del riflusso", "Serbatoio"),
                  ("Etanolo anidro 99,8%", "Prodotto"), ("Ribollitore", "Ribollitore"),
                  ("Colonna di recupero (vuoto)", "Colonna di distillazione"),
                  ("Ribollitore di recupero", "Ribollitore"), ("Condensatore di recupero", "Condensatore"),
                  ("Acqua", "Spurgo"), ("Raffreddatore del glicole", "Scambiatore di calore"),
                  ("Pompa del glicole", "Pompa"), ("Reintegro glicole", "Alimentazione")],
        "correnti": [("Alcol 95%", "Colonna estrattiva", "a metà colonna"),
                     ("Colonna estrattiva", "Condensatore", "vapori di etanolo"),
                     ("Condensatore", "Accumulatore del riflusso", ""),
                     ("Accumulatore del riflusso", "Colonna estrattiva", "riflusso"),
                     ("Accumulatore del riflusso", "Etanolo anidro 99,8%", "distillato"),
                     ("Colonna estrattiva", "Ribollitore", "glicole + acqua"),
                     ("Ribollitore", "Colonna estrattiva", "vapore"),
                     ("Ribollitore", "Colonna di recupero (vuoto)", "glicole + acqua"),
                     ("Colonna di recupero (vuoto)", "Condensatore di recupero", "vapore d'acqua"),
                     ("Condensatore di recupero", "Acqua", ""),
                     ("Colonna di recupero (vuoto)", "Ribollitore di recupero", "liquido di fondo"),
                     ("Ribollitore di recupero", "Colonna di recupero (vuoto)", "vapore"),
                     ("Ribollitore di recupero", "Raffreddatore del glicole", "glicole rigenerato caldo"),
                     ("Raffreddatore del glicole", "Pompa del glicole", ""),
                     ("Reintegro glicole", "Pompa del glicole", ""),
                     ("Pompa del glicole", "Colonna estrattiva", "glicole sotto la testa")],
        "parole": ["estrattiv", "glicole", "solvente", "azeotrop", "volatilità", "anidro", "recupero", "vuoto",
                   "riciclo", "ribollitor", "riflusso", "condens"],
    },

    # ------------------------------------------------------------------ ASSORBIMENTO
    "Assorbimento della CO₂ con ammine e rigenerazione (stripping)": {
        "reazione": "Assorbimento chimico reversibile (non una produzione): 2 RNH₂ + CO₂ ⇌ RNHCOO⁻ + RNH₃⁺ "
                    "(carbammato, esotermico); a freddo l'equilibrio va a destra (assorbimento), a caldo a sinistra "
                    "(rigenerazione)",
        "condizioni": "soluzione acquosa di monoetanolammina (MEA) al 30% in massa; assorbitore a 40-60 °C; "
                      "rigeneratore a 110-120 °C e 1,5-2 bar; carico di CO₂ da ≈ 0,2 (ammina povera) a ≈ 0,45-0,5 "
                      "mol CO₂/mol ammina (ammina ricca); 3-4 GJ di vapore per tonnellata di CO₂",
        "descrizione": [
            "Il gas da depurare (per esempio fumi di combustione o gas di sintesi) entra dal fondo dell'assorbitore, una "
            "colonna a riempimento.",
            "Dall'alto scende la soluzione di ammina povera: gas e liquido si incontrano in controcorrente sulla grande "
            "superficie del riempimento e la CO₂ passa nel liquido, legandosi all'ammina.",
            "Dalla testa esce il gas depurato; dal fondo l'ammina ricca, che una pompa manda allo scambiatore ammina "
            "ricca/ammina povera, dove si scalda recuperando calore.",
            "L'ammina ricca entra in testa al rigeneratore (stripper): il vapore prodotto dal ribollitore, scaldato con "
            "vapore di rete, la riscalda e inverte la reazione, liberando la CO₂.",
            "Dalla testa del rigeneratore escono CO₂ e vapore acqueo: nel condensatore l'acqua condensa, "
            "nell'accumulatore si separa e torna come riflusso; la CO₂ va alla compressione e allo stoccaggio o all'uso.",
            "L'ammina povera calda esce dal fondo, cede calore nello scambiatore, è raffreddata ad acqua a ≈ 40 °C e "
            "pompata di nuovo in testa all'assorbitore: il solvente lavora in ciclo chiuso.",
        ],
        "perche": "La solubilità del gas aumenta a bassa temperatura e alta pressione parziale (legge di Henry, qui "
                  "aiutata dalla reazione con l'ammina); diminuisce scaldando, e così il solvente si rigenera. La "
                  "controcorrente fa incontrare il gas più povero con il liquido più povero e mantiene la forza "
                  "motrice in tutta la colonna; il riempimento dà molta superficie di contatto. Lo scambiatore "
                  "ricca/povera riduce molto il consumo di vapore, la voce di costo principale.",
        "unita": [("Gas da depurare", "Alimentazione"), ("Assorbitore (riempimento)", "Colonna a riempimento"),
                  ("Gas depurato", "Prodotto"), ("Pompa ammina ricca", "Pompa"),
                  ("Scambiatore ricca/povera", "Scambiatore di calore"), ("Rigeneratore (stripper)", "Colonna a riempimento"),
                  ("Ribollitore", "Ribollitore"), ("Condensatore", "Condensatore"),
                  ("Accumulatore", "Serbatoio"), ("CO₂ al compressore", "Prodotto"),
                  ("Raffreddatore ammina povera", "Scambiatore di calore"), ("Pompa ammina povera", "Pompa"),
                  ("Vapore di rete", "Alimentazione"), ("Acqua di raffreddamento", "Alimentazione")],
        "correnti": [("Gas da depurare", "Assorbitore (riempimento)", "dal fondo"),
                     ("Assorbitore (riempimento)", "Gas depurato", "dalla testa"),
                     ("Assorbitore (riempimento)", "Pompa ammina ricca", "ammina ricca"),
                     ("Pompa ammina ricca", "Scambiatore ricca/povera", ""),
                     ("Scambiatore ricca/povera", "Rigeneratore (stripper)", "ammina ricca ≈ 100 °C"),
                     ("Rigeneratore (stripper)", "Ribollitore", "liquido di fondo"),
                     ("Ribollitore", "Rigeneratore (stripper)", "vapore di stripping"),
                     ("Vapore di rete", "Ribollitore", ""),
                     ("Rigeneratore (stripper)", "Condensatore", "CO₂ + vapore acqueo"),
                     ("Acqua di raffreddamento", "Condensatore", ""),
                     ("Condensatore", "Accumulatore", ""),
                     ("Accumulatore", "Rigeneratore (stripper)", "riflusso d'acqua"),
                     ("Accumulatore", "CO₂ al compressore", "CO₂ > 99%"),
                     ("Ribollitore", "Scambiatore ricca/povera", "ammina povera ≈ 120 °C"),
                     ("Scambiatore ricca/povera", "Raffreddatore ammina povera", ""),
                     ("Acqua di raffreddamento", "Raffreddatore ammina povera", ""),
                     ("Raffreddatore ammina povera", "Pompa ammina povera", "≈ 40 °C"),
                     ("Pompa ammina povera", "Assorbitore (riempimento)", "ammina povera in testa")],
        "parole": ["assorb", "ammin", "mea", "co2", "co₂", "riempimento", "controcorrente", "rigenera", "stripp",
                   "desorb", "ribollitor", "scambiator", "henry", "solubil", "ricca", "povera", "condens"],
    },

    # ------------------------------------------------------------------ ESTRAZIONE
    "Estrazione liquido-liquido in controcorrente (acido acetico)": {
        "reazione": "Nessuna reazione: operazione fisica — ripartizione di un soluto tra due liquidi immiscibili "
                    "(coefficiente di ripartizione); esempio acido acetico da soluzioni acquose diluite con acetato di etile",
        "condizioni": "25-40 °C, pressione atmosferica; soluzione acquosa al 5-30% di acido acetico; colonna di estrazione "
                      "a piatti forati o a dischi rotanti (5-10 stadi teorici); rapporto solvente/alimentazione "
                      "dell'ordine di 1-3 in massa; recupero del solvente per distillazione",
        "descrizione": [
            "La soluzione acquosa (fase pesante) entra in testa alla colonna di estrazione; il solvente, acetato di etile "
            "(fase leggera), entra dal fondo.",
            "Le due fasi si muovono in controcorrente: le gocce di solvente salgono attraverso l'acqua, che scende, e "
            "l'acido acetico passa dall'acqua al solvente stadio dopo stadio.",
            "Dalla testa esce l'estratto (solvente + acido acetico + un po' d'acqua); dal fondo il raffinato, acqua "
            "quasi priva di acido ma satura di solvente.",
            "L'estratto va alla colonna di recupero del solvente: in testa distilla il solvente (con l'acqua "
            "disciolta, come azeotropo eterogeneo), dal fondo, scaldato dal ribollitore, esce acido acetico concentrato.",
            "I vapori di testa condensano e nel decantatore si separano: il solvente torna all'estrattore, l'acqua va "
            "allo stripper del raffinato.",
            "Lo stripper del raffinato recupera il solvente disciolto nell'acqua (che va al decantatore); l'acqua "
            "esausta esce dal fondo verso la depurazione. Un piccolo reintegro compensa le perdite di solvente.",
        ],
        "perche": "Il soluto si ripartisce tra due liquidi immiscibili secondo il coefficiente di ripartizione K = c(solvente)"
                  "/c(acqua). In controcorrente il solvente più carico incontra la soluzione più ricca e il solvente "
                  "fresco la soluzione più povera, così con pochi stadi si estrae quasi tutto il soluto usando meno "
                  "solvente che in corrente incrociata. Si preferisce alla distillazione diretta quando il soluto è "
                  "diluito o meno volatile dell'acqua: evaporare tutta l'acqua costerebbe troppo. Il recupero del "
                  "solvente è parte essenziale dell'impianto, per costi e ambiente.",
        "unita": [("Soluzione acquosa di acido acetico", "Alimentazione"), ("Colonna di estrazione", "Estrattore"),
                  ("Colonna di recupero del solvente", "Colonna di distillazione"), ("Ribollitore", "Ribollitore"),
                  ("Acido acetico concentrato", "Prodotto"), ("Condensatore", "Condensatore"),
                  ("Decantatore", "Decantatore"), ("Pompa del solvente", "Pompa"),
                  ("Reintegro solvente", "Alimentazione"), ("Stripper del raffinato", "Colonna di distillazione"),
                  ("Acqua esausta alla depurazione", "Spurgo"), ("Vapore di rete", "Alimentazione")],
        "correnti": [("Soluzione acquosa di acido acetico", "Colonna di estrazione", "fase pesante in testa"),
                     ("Pompa del solvente", "Colonna di estrazione", "solvente dal fondo"),
                     ("Colonna di estrazione", "Colonna di recupero del solvente", "estratto"),
                     ("Colonna di estrazione", "Stripper del raffinato", "raffinato"),
                     ("Colonna di recupero del solvente", "Ribollitore", "liquido di fondo"),
                     ("Ribollitore", "Colonna di recupero del solvente", "vapore"),
                     ("Ribollitore", "Acido acetico concentrato", ""),
                     ("Vapore di rete", "Ribollitore", ""),
                     ("Colonna di recupero del solvente", "Condensatore", "solvente + acqua (vapori)"),
                     ("Condensatore", "Decantatore", "due fasi"),
                     ("Decantatore", "Pompa del solvente", "fase organica"),
                     ("Reintegro solvente", "Pompa del solvente", ""),
                     ("Decantatore", "Stripper del raffinato", "fase acquosa"),
                     ("Stripper del raffinato", "Condensatore", "solvente recuperato"),
                     ("Vapore di rete", "Stripper del raffinato", "vapore diretto"),
                     ("Stripper del raffinato", "Acqua esausta alla depurazione", "")],
        "parole": ["estrazione", "estratto", "raffinato", "solvente", "immiscibil", "ripartizione", "controcorrente",
                   "stadi", "fase", "decant", "recupero", "acetato di etile", "acido acetico", "distill"],
    },

    "Estrazione solido-liquido: olio di semi con esano": {
        "reazione": "Nessuna reazione: operazione fisica — lisciviazione: il solvente scioglie l'olio contenuto nel "
                    "solido e lo porta fuori per diffusione",
        "condizioni": "esano (Teb 69 °C) a 55-60 °C; estrattore continuo a nastro o a carosello in controcorrente; "
                      "miscella in uscita al 25-30% di olio; olio residuo nella farina < 1%; desolventizzatore-tostatore "
                      "a 100-110 °C con vapore; stripping finale dell'olio sotto vuoto",
        "descrizione": [
            "I semi (soia, girasole, colza) sono puliti, decorticati, macinati e laminati in fiocchi sottili, così il "
            "solvente raggiunge facilmente le cellule.",
            "I fiocchi avanzano nell'estrattore continuo e sono lavati in controcorrente: i fiocchi freschi incontrano "
            "la miscella più ricca, i fiocchi quasi esausti l'esano puro.",
            "La miscella (olio sciolto in esano) è filtrata e va all'evaporatore, dove gran parte dell'esano evapora; "
            "lo stripper sotto vuoto con vapore toglie le ultime tracce e dà olio grezzo.",
            "La farina esausta, imbevuta di esano, passa nel desolventizzatore-tostatore: il vapore fa evaporare il "
            "solvente e cuoce la farina, che diventa mangime proteico.",
            "Tutti i vapori di esano sono condensati e nel decantatore l'esano si separa dall'acqua di condensa del vapore.",
            "L'esano recuperato va al serbatoio e torna all'estrattore (ciclo chiuso, perdite di circa 1 kg per "
            "tonnellata di semi); l'aria di sfiato passa in un assorbitore a olio minerale che trattiene l'esano.",
        ],
        "perche": "La velocità di estrazione dipende dalla diffusione dell'olio dall'interno del solido: per questo si "
                  "riduce lo spessore (fiocchi) e si lavora a caldo. La controcorrente sfrutta al massimo il solvente e "
                  "lascia pochissimo olio nella farina. Il recupero dell'esano è vitale: è infiammabile, costa ed è "
                  "inquinante. Lo stesso principio serve per lo zucchero dalle barbabietole (con acqua calda) e per il "
                  "caffè solubile.",
        "unita": [("Semi oleosi", "Alimentazione"), ("Preparazione (mulino e laminatoio)", "Mulino"),
                  ("Estrattore continuo", "Estrattore"), ("Filtro della miscella", "Filtro"),
                  ("Evaporatore della miscella", "Evaporatore"), ("Stripper sotto vuoto", "Colonna di distillazione"),
                  ("Olio grezzo", "Prodotto"), ("Desolventizzatore-tostatore", "Essiccatore"),
                  ("Farina proteica", "Prodotto"), ("Condensatore", "Condensatore"), ("Decantatore", "Decantatore"),
                  ("Serbatoio esano", "Serbatoio"), ("Acqua di condensa", "Spurgo"), ("Vapore di rete", "Alimentazione"),
                  ("Reintegro esano", "Alimentazione")],
        "correnti": [("Semi oleosi", "Preparazione (mulino e laminatoio)", ""),
                     ("Preparazione (mulino e laminatoio)", "Estrattore continuo", "fiocchi"),
                     ("Serbatoio esano", "Estrattore continuo", "esano puro (in controcorrente)"),
                     ("Estrattore continuo", "Filtro della miscella", "miscella 25-30% olio"),
                     ("Filtro della miscella", "Evaporatore della miscella", ""),
                     ("Evaporatore della miscella", "Stripper sotto vuoto", "olio concentrato"),
                     ("Stripper sotto vuoto", "Olio grezzo", ""),
                     ("Estrattore continuo", "Desolventizzatore-tostatore", "farina con esano"),
                     ("Desolventizzatore-tostatore", "Farina proteica", ""),
                     ("Vapore di rete", "Desolventizzatore-tostatore", ""),
                     ("Vapore di rete", "Evaporatore della miscella", ""),
                     ("Vapore di rete", "Stripper sotto vuoto", "vapore di stripping"),
                     ("Evaporatore della miscella", "Condensatore", "vapori di esano"),
                     ("Stripper sotto vuoto", "Condensatore", "vapori di esano"),
                     ("Desolventizzatore-tostatore", "Condensatore", "esano + vapore"),
                     ("Condensatore", "Decantatore", ""),
                     ("Decantatore", "Serbatoio esano", "esano recuperato"),
                     ("Decantatore", "Acqua di condensa", ""),
                     ("Reintegro esano", "Serbatoio esano", "")],
        "parole": ["esano", "solvente", "lisciviazion", "solido-liquido", "estratt", "miscella", "controcorrente",
                   "fiocchi", "farina", "desolventizz", "diffusion", "recupero", "evapor", "olio", "condens"],
    },

    "Estrazione dello zucchero dalle barbabietole (diffusione)": {
        "reazione": "Nessuna reazione nell'estrazione: operazione fisica — diffusione del saccarosio dalle cellule "
                    "delle fettucce all'acqua calda (lisciviazione); la successiva depurazione con calce e CO₂ è invece "
                    "chimica (CaO + H₂O → Ca(OH)₂; Ca(OH)₂ + CO₂ → CaCO₃ + H₂O)",
        "condizioni": "barbabietole al 16-18% di saccarosio; fettucce di pochi mm; diffusore in controcorrente a 70-72 °C "
                      "(le cellule si 'aprono' e i microbi sono frenati); sugo greggio al 13-15% di zucchero; "
                      "zucchero estratto ≈ 98%",
        "descrizione": [
            "Le barbabietole sono lavate e tagliate a fettucce sottili, per aumentare la superficie di scambio.",
            "Le fettucce entrano nel diffusore (a torre o a tamburo rotante) e avanzano in senso opposto all'acqua calda "
            "a circa 70 °C: le fettucce fresche incontrano il sugo più concentrato, quelle esauste l'acqua pulita.",
            "Dal diffusore esce il sugo greggio, al 13-15% di zucchero, scuro e torbido per le impurezze.",
            "Le fettucce esauste (polpe) sono pressate: l'acqua di pressatura torna al diffusore, le polpe pressate "
            "si essiccano e diventano mangime.",
            "Il sugo greggio è depurato con latte di calce e poi con CO₂ (prodotti nel forno a calce): il carbonato di "
            "calcio che precipita trascina via le impurezze.",
            "Il fango calco-carbonico è separato con filtri; il sugo leggero e limpido va alla stazione di "
            "evaporazione a multiplo effetto.",
        ],
        "perche": "Lo zucchero passa dalle cellule all'acqua per diffusione, spinto dalla differenza di concentrazione "
                  "(legge di Fick): la controcorrente la mantiene alta lungo tutto il diffusore, così si estrae quasi "
                  "tutto lo zucchero con poca acqua (sugo concentrato = meno acqua da evaporare dopo). A 70 °C le "
                  "membrane cellulari si denaturano e lasciano passare lo zucchero ma trattengono molte sostanze "
                  "colloidali.",
        "unita": [("Barbabietole", "Alimentazione"), ("Lavaggio e tagliafettucce", "Mulino"),
                  ("Diffusore in controcorrente", "Estrattore"), ("Acqua calda ≈ 70 °C", "Alimentazione"),
                  ("Pressa delle polpe", "Filtro"), ("Polpe (mangime)", "Prodotto"),
                  ("Depurazione calco-carbonica", "Reattore"), ("Forno a calce", "Forno"),
                  ("Filtri del fango", "Filtro"), ("Fango calco-carbonico", "Spurgo"),
                  ("Sugo leggero all'evaporazione", "Prodotto")],
        "correnti": [("Barbabietole", "Lavaggio e tagliafettucce", ""),
                     ("Lavaggio e tagliafettucce", "Diffusore in controcorrente", "fettucce"),
                     ("Acqua calda ≈ 70 °C", "Diffusore in controcorrente", "in controcorrente"),
                     ("Diffusore in controcorrente", "Pressa delle polpe", "polpe esauste"),
                     ("Pressa delle polpe", "Diffusore in controcorrente", "acqua di pressatura"),
                     ("Pressa delle polpe", "Polpe (mangime)", ""),
                     ("Diffusore in controcorrente", "Depurazione calco-carbonica", "sugo greggio 13-15%"),
                     ("Forno a calce", "Depurazione calco-carbonica", "latte di calce + CO₂"),
                     ("Depurazione calco-carbonica", "Filtri del fango", ""),
                     ("Filtri del fango", "Fango calco-carbonico", ""),
                     ("Filtri del fango", "Sugo leggero all'evaporazione", "sugo limpido")],
        "parole": ["barbabietol", "fettucce", "diffus", "controcorrente", "acqua calda", "sugo", "polpe", "calce",
                   "carbonatazion", "lisciviazion", "saccarosio", "zucchero", "fick"],
    },

    # ------------------------------------------------------------------ EVAPORAZIONE E CRISTALLIZZAZIONE
    "Evaporazione a multiplo effetto": {
        "reazione": "Nessuna reazione: operazione fisica — concentrazione di una soluzione facendo evaporare il solvente "
                    "(acqua); il vapore prodotto in un effetto scalda l'effetto successivo, a pressione più bassa",
        "condizioni": "esempio sugo zuccherino da ≈ 14-15% a 65-70% di sostanza secca (°Brix); 4-5 effetti a film "
                      "cadente o a tubi; 1° effetto a ≈ 125-130 °C (vapore vivo ≈ 3 bar), ultimo effetto a ≈ 85-90 °C "
                      "sotto leggero vuoto; consumo ≈ 1/n kg di vapore vivo per kg d'acqua evaporata (n = numero di effetti)",
        "descrizione": [
            "Il sugo leggero, preriscaldato, entra nel primo effetto, scaldato con vapore vivo della centrale termica: "
            "l'acqua bolle e si forma vapore (vapore secondario o 'di sugo').",
            "Il vapore secondario del primo effetto va nella camera di riscaldamento del secondo effetto, che lavora "
            "a pressione più bassa, quindi il sugo bolle a temperatura più bassa: quel vapore basta a farlo bollire.",
            "Il sugo, già più concentrato, passa da un effetto all'altro nello stesso verso del vapore (equicorrente) e "
            "si concentra sempre di più.",
            "Il vapore dell'ultimo effetto va al condensatore barometrico, dove condensa a contatto con acqua fredda; "
            "una pompa a vuoto toglie gli incondensabili e mantiene il vuoto.",
            "Le condense dei vapori di riscaldamento sono raccolte: quella del vapore vivo torna in caldaia, le altre "
            "servono come acqua calda di processo.",
            "Dall'ultimo effetto esce lo sciroppo denso (65-70%), pronto per la cristallizzazione; una parte del vapore "
            "secondario viene spillata per altri usi dello stabilimento.",
        ],
        "perche": "Per evaporare 1 kg d'acqua serve circa il suo calore latente (≈ 2,2-2,3 MJ). In un solo effetto ci "
                  "vuole circa 1 kg di vapore vivo per kg evaporato; riusando il vapore prodotto come fluido "
                  "riscaldante in effetti a pressione via via più bassa (dove l'acqua bolle a temperatura più bassa) "
                  "con n effetti il consumo scende a circa 1/n. Il limite è la differenza di temperatura totale "
                  "disponibile, divisa tra gli effetti (e ridotta dall'innalzamento ebullioscopico): più effetti = "
                  "meno vapore ma più superficie e costo d'impianto. Alternative: ricompressione meccanica o termica del vapore.",
        "unita": [("Sugo leggero ≈ 15%", "Alimentazione"), ("Preriscaldatore", "Scambiatore di calore"),
                  ("Vapore vivo", "Alimentazione"), ("1° effetto", "Evaporatore"), ("2° effetto", "Evaporatore"),
                  ("3° effetto", "Evaporatore"), ("4° effetto", "Evaporatore"),
                  ("Condensatore barometrico", "Condensatore"), ("Pompa a vuoto", "Eiettore/pompa a vuoto"),
                  ("Incondensabili", "Spurgo"), ("Acqua fredda", "Alimentazione"),
                  ("Raccolta condense", "Serbatoio"), ("Sciroppo 65-70%", "Prodotto")],
        "correnti": [("Sugo leggero ≈ 15%", "Preriscaldatore", ""),
                     ("Preriscaldatore", "1° effetto", "sugo caldo"),
                     ("Vapore vivo", "1° effetto", "≈ 3 bar"),
                     ("1° effetto", "2° effetto", "vapore secondario"),
                     ("1° effetto", "2° effetto", "sugo più concentrato"),
                     ("2° effetto", "3° effetto", "vapore"),
                     ("2° effetto", "3° effetto", "sugo"),
                     ("3° effetto", "4° effetto", "vapore"),
                     ("3° effetto", "4° effetto", "sugo"),
                     ("4° effetto", "Sciroppo 65-70%", "sciroppo denso"),
                     ("4° effetto", "Condensatore barometrico", "vapore ≈ 85-90 °C"),
                     ("Acqua fredda", "Condensatore barometrico", ""),
                     ("Condensatore barometrico", "Pompa a vuoto", "incondensabili"),
                     ("Pompa a vuoto", "Incondensabili", ""),
                     ("1° effetto", "Raccolta condense", "condensa vapore vivo (in caldaia)"),
                     ("2° effetto", "Raccolta condense", "condense"),
                     ("3° effetto", "Raccolta condense", "condense"),
                     ("4° effetto", "Raccolta condense", "condense"),
                     ("1° effetto", "Preriscaldatore", "vapore spillato")],
        "parole": ["effett", "multiplo", "evapor", "vapore secondario", "vapore vivo", "pressione", "vuoto",
                   "barometric", "concentr", "calore latente", "risparmio", "condens", "ebullioscop", "sciroppo"],
    },

    "Cristallizzazione per evaporazione: zucchero (bolla sotto vuoto, centrifuga, essiccamento)": {
        "reazione": "Nessuna reazione: operazione fisica — si toglie acqua fino a rendere la soluzione sovrasatura, e il "
                    "soluto si deposita in cristalli; una parte della cristallizzazione avviene poi per raffreddamento",
        "condizioni": "bolla di cottura (cristallizzatore evaporativo) sotto vuoto a ≈ 0,2 bar assoluti, 65-75 °C; "
                      "semina con cristalli finissimi; massa cotta con ≈ 50% di cristalli; malassatori raffreddati fino "
                      "a 40-50 °C; centrifughe a cesto a 1000-1500 giri/min; zucchero finale con umidità < 0,05%",
        "descrizione": [
            "Lo sciroppo dell'evaporazione entra nella bolla di cottura, un evaporatore sotto vuoto scaldato con vapore: "
            "a bassa pressione bolle a 65-75 °C e non caramella.",
            "Quando la soluzione è sovrasatura si 'semina' con cristallini di zucchero finissimi; si continua a "
            "evaporare e ad aggiungere sciroppo perché i cristalli crescano senza formarne di nuovi.",
            "I vapori della bolla vanno al condensatore barometrico; la pompa a vuoto toglie gli incondensabili.",
            "La massa cotta (cristalli + sciroppo madre) scende nei malassatori, dove si raffredda lentamente agitando: "
            "altro zucchero cristallizza sui cristalli esistenti.",
            "Le centrifughe a cesto separano i cristalli dallo sciroppo madre; i cristalli sono lavati con un getto "
            "d'acqua calda.",
            "Lo sciroppo madre torna a un'altra cottura (si fanno più cotte successive); l'ultimo, da cui non si "
            "ricava più zucchero conveniente, è la melassa.",
            "Lo zucchero umido passa in un essiccatore a tamburo rotante con aria calda e poi fredda; viene vagliato e "
            "stoccato in silos.",
        ],
        "perche": "Un soluto cristallizza solo se la soluzione è sovrasatura: si ottiene togliendo il solvente "
                  "(evaporazione) o abbassando la temperatura (la solubilità del saccarosio scende col freddo). Il "
                  "vuoto permette di evaporare a bassa temperatura, evitando la caramellizzazione e l'inversione dello "
                  "zucchero. La semina e il controllo della sovrasaturazione (zona metastabile) fanno crescere cristalli "
                  "grandi e uniformi invece di una polvere fine difficile da centrifugare.",
        "unita": [("Sciroppo 65-70%", "Alimentazione"), ("Bolla di cottura (vuoto)", "Cristallizzatore"),
                  ("Vapore di riscaldamento", "Alimentazione"), ("Condensatore barometrico", "Condensatore"),
                  ("Pompa a vuoto", "Eiettore/pompa a vuoto"), ("Incondensabili", "Spurgo"),
                  ("Malassatore (raffreddamento)", "Cristallizzatore"), ("Centrifuga a cesto", "Centrifuga"),
                  ("Serbatoio sciroppo madre", "Serbatoio"), ("Melassa", "Spurgo"),
                  ("Essiccatore a tamburo", "Essiccatore"), ("Aria calda", "Alimentazione"),
                  ("Zucchero cristallino", "Prodotto")],
        "correnti": [("Sciroppo 65-70%", "Bolla di cottura (vuoto)", ""),
                     ("Vapore di riscaldamento", "Bolla di cottura (vuoto)", ""),
                     ("Bolla di cottura (vuoto)", "Condensatore barometrico", "vapori ≈ 0,2 bar"),
                     ("Condensatore barometrico", "Pompa a vuoto", "incondensabili"),
                     ("Pompa a vuoto", "Incondensabili", ""),
                     ("Bolla di cottura (vuoto)", "Malassatore (raffreddamento)", "massa cotta"),
                     ("Malassatore (raffreddamento)", "Centrifuga a cesto", ""),
                     ("Centrifuga a cesto", "Serbatoio sciroppo madre", "sciroppo madre"),
                     ("Serbatoio sciroppo madre", "Bolla di cottura (vuoto)", "a una nuova cotta"),
                     ("Serbatoio sciroppo madre", "Melassa", "ultimo sciroppo"),
                     ("Centrifuga a cesto", "Essiccatore a tamburo", "cristalli umidi"),
                     ("Aria calda", "Essiccatore a tamburo", ""),
                     ("Essiccatore a tamburo", "Zucchero cristallino", "umidità < 0,05%")],
        "parole": ["cristall", "sovrasatur", "solubil", "semina", "vuoto", "evapor", "massa cotta", "centrifug",
                   "essicc", "melassa", "acque madri", "sciroppo madre", "malassator", "raffredd"],
    },

    "Cristallizzazione per raffreddamento: nitrato di potassio": {
        "reazione": "Nessuna reazione: operazione fisica — la solubilità del KNO₃ cresce molto con la temperatura "
                    "(≈ 169 g/100 g d'acqua a 80 °C, ≈ 32 g/100 g a 20 °C): raffreddando la soluzione satura il sale "
                    "in eccesso cristallizza",
        "condizioni": "dissoluzione a 80-90 °C; filtrazione a caldo; cristallizzatore raffreddato ad acqua (camicia o "
                      "scambiatore esterno) fino a 20-25 °C, raffreddamento lento e controllato; centrifuga; essiccatore "
                      "a letto fluido con aria a 60-80 °C",
        "descrizione": [
            "Il sale grezzo si scioglie in acqua calda (con le acque madri riciclate) in un dissolutore agitato, fino "
            "a ottenere una soluzione quasi satura a 80-90 °C.",
            "La soluzione calda è filtrata per togliere le impurezze insolubili, mantenendola calda perché non "
            "cristallizzi nel filtro.",
            "Nel cristallizzatore la soluzione è agitata e raffreddata lentamente con acqua di raffreddamento: la "
            "solubilità cala e il nitrato di potassio cristallizza.",
            "La sospensione di cristalli va alla centrifuga, che separa i cristalli dalle acque madri; i cristalli "
            "sono lavati con poca acqua fredda.",
            "Le acque madri, ancora sature a 20-25 °C, tornano al dissolutore; una piccola parte è spurgata per non "
            "accumulare le impurezze solubili (per esempio cloruri).",
            "I cristalli umidi passano in un essiccatore a letto fluido con aria calda e diventano il prodotto secco.",
        ],
        "perche": "La quantità che cristallizza è la differenza tra la solubilità alla temperatura alta e a quella "
                  "bassa (curva di solubilità). Il metodo funziona bene per i sali la cui solubilità cresce molto con "
                  "la temperatura (KNO₃, CuSO₄·5H₂O); per quelli quasi indifferenti alla temperatura (NaCl) si usa "
                  "l'evaporazione. Raffreddare lentamente tiene la soluzione nella zona metastabile, così crescono "
                  "pochi cristalli grandi e puri invece di molti piccoli; le impurezze restano nelle acque madri.",
        "unita": [("Sale grezzo", "Alimentazione"), ("Acqua", "Alimentazione"), ("Dissolutore a caldo", "Miscelatore"),
                  ("Vapore di riscaldamento", "Alimentazione"), ("Filtro a caldo", "Filtro"),
                  ("Residui insolubili", "Spurgo"), ("Cristallizzatore raffreddato", "Cristallizzatore"),
                  ("Acqua di raffreddamento", "Alimentazione"), ("Centrifuga", "Centrifuga"),
                  ("Serbatoio acque madri", "Serbatoio"), ("Spurgo acque madri", "Spurgo"),
                  ("Essiccatore a letto fluido", "Essiccatore"), ("Aria calda", "Alimentazione"),
                  ("KNO₃ cristallino", "Prodotto")],
        "correnti": [("Sale grezzo", "Dissolutore a caldo", ""), ("Acqua", "Dissolutore a caldo", ""),
                     ("Vapore di riscaldamento", "Dissolutore a caldo", "80-90 °C"),
                     ("Dissolutore a caldo", "Filtro a caldo", "soluzione satura calda"),
                     ("Filtro a caldo", "Residui insolubili", ""),
                     ("Filtro a caldo", "Cristallizzatore raffreddato", "soluzione limpida"),
                     ("Acqua di raffreddamento", "Cristallizzatore raffreddato", ""),
                     ("Cristallizzatore raffreddato", "Centrifuga", "sospensione a 20-25 °C"),
                     ("Centrifuga", "Serbatoio acque madri", "acque madri"),
                     ("Serbatoio acque madri", "Dissolutore a caldo", "riciclo"),
                     ("Serbatoio acque madri", "Spurgo acque madri", "impurezze"),
                     ("Centrifuga", "Essiccatore a letto fluido", "cristalli umidi"),
                     ("Aria calda", "Essiccatore a letto fluido", ""),
                     ("Essiccatore a letto fluido", "KNO₃ cristallino", "")],
        "parole": ["cristall", "raffredd", "solubil", "satur", "temperatura", "acque madri", "centrifug", "essicc",
                   "filtr", "riciclo", "spurgo", "metastabil"],
    },

    # ------------------------------------------------------------------ ESSICCAMENTO E SEPARAZIONI SOLIDO-FLUIDO
    "Essiccamento a spruzzo (spray dryer): latte in polvere": {
        "reazione": "Nessuna reazione: operazione fisica — evaporazione dell'umidità da goccioline finissime a contatto "
                    "con aria calda (trasporto simultaneo di calore e di materia)",
        "condizioni": "latte concentrato al 45-50% di solidi (da evaporatore); aria in ingresso 180-220 °C, in uscita "
                      "80-95 °C; gocce di 20-200 µm; tempo di essiccamento di pochi secondi; polvere finale al 3-4% di "
                      "umidità dopo il letto fluido",
        "descrizione": [
            "L'aria esterna è filtrata e scaldata a 180-220 °C in uno scambiatore a vapore (o con un bruciatore).",
            "Il latte concentrato è pompato all'atomizzatore (disco rotante o ugelli ad alta pressione) in cima alla "
            "camera di essiccamento, che lo nebulizza in goccioline finissime.",
            "Le goccioline incontrano l'aria calda: l'acqua evapora in pochi secondi e la temperatura della goccia "
            "resta vicina a quella di bulbo umido, molto più bassa di quella dell'aria, così le proteine non si alterano.",
            "La polvere più grossa cade sul fondo della camera e passa in un letto fluido vibrato che completa "
            "l'essiccamento e la raffredda.",
            "L'aria umida esce con le particelle fini e passa nel ciclone, che le separa per forza centrifuga; le fini "
            "tornano alla camera, dove si agglomerano con le gocce (polvere istantanea).",
            "Un filtro a maniche trattiene le ultime polveri prima che il ventilatore scarichi l'aria al camino.",
        ],
        "perche": "La nebulizzazione crea una superficie enorme, quindi evaporazione velocissima. Finché la particella è "
                  "bagnata, il calore ricevuto va tutto nell'evaporazione e la sua temperatura resta quella di bulbo "
                  "umido (diagramma psicrometrico): si possono usare arie molto calde senza danneggiare prodotti "
                  "termosensibili. Ciclone e filtro a maniche recuperano prodotto e proteggono l'ambiente. Per solidi "
                  "granulari e robusti si usa invece l'essiccatore a tamburo rotante.",
        "unita": [("Aria esterna", "Alimentazione"), ("Batteria di riscaldamento", "Scambiatore di calore"),
                  ("Vapore di rete", "Alimentazione"), ("Latte concentrato 45-50%", "Alimentazione"),
                  ("Pompa ad alta pressione", "Pompa"), ("Camera di essiccamento (atomizzatore)", "Essiccatore"),
                  ("Letto fluido vibrato", "Essiccatore"), ("Latte in polvere", "Prodotto"),
                  ("Ciclone", "Ciclone"), ("Filtro a maniche", "Filtro"), ("Camino", "Spurgo")],
        "correnti": [("Aria esterna", "Batteria di riscaldamento", "filtrata"),
                     ("Vapore di rete", "Batteria di riscaldamento", ""),
                     ("Batteria di riscaldamento", "Camera di essiccamento (atomizzatore)", "aria 180-220 °C"),
                     ("Latte concentrato 45-50%", "Pompa ad alta pressione", ""),
                     ("Pompa ad alta pressione", "Camera di essiccamento (atomizzatore)", "all'atomizzatore"),
                     ("Camera di essiccamento (atomizzatore)", "Letto fluido vibrato", "polvere umida"),
                     ("Letto fluido vibrato", "Latte in polvere", "umidità 3-4%"),
                     ("Camera di essiccamento (atomizzatore)", "Ciclone", "aria 80-95 °C + polveri fini"),
                     ("Letto fluido vibrato", "Ciclone", "aria + fini"),
                     ("Ciclone", "Camera di essiccamento (atomizzatore)", "fini (agglomerazione)"),
                     ("Ciclone", "Filtro a maniche", "aria"),
                     ("Filtro a maniche", "Camino", "aria pulita")],
        "parole": ["spray", "spruzzo", "atomizz", "nebulizz", "essicc", "aria calda", "bulbo umido", "umidità",
                   "ciclone", "maniche", "letto fluido", "polvere", "psicrometric", "evapor"],
    },

    "Filtrazione con filtropressa": {
        "reazione": "Nessuna reazione: operazione fisica — separazione solido-liquido: il liquido attraversa una tela "
                    "filtrante e la torta che vi si deposita, spinto dalla differenza di pressione (legge di Darcy)",
        "condizioni": "funzionamento discontinuo; pressione di alimentazione 6-15 bar; piastre a camera con tele di "
                      "polipropilene; spremitura con membrane a 12-16 bar; torta con il 50-80% di solidi secondo il "
                      "materiale; ciclo di 1-4 ore",
        "descrizione": [
            "La sospensione (torbida) da filtrare è raccolta in un serbatoio agitato, spesso dopo aver aggiunto un "
            "flocculante o un coadiuvante di filtrazione.",
            "Una pompa la spinge nelle camere tra le piastre della filtropressa, chiusa da un pistone idraulico: il "
            "liquido attraversa le tele ed esce dai canali come filtrato limpido, il solido resta e forma la torta.",
            "Man mano che la torta cresce la resistenza aumenta: la portata cala e la pressione sale fino al massimo; "
            "quando le camere sono piene si ferma l'alimentazione.",
            "Si può lavare la torta facendo passare acqua di lavaggio, per togliere il liquido madre e i sali solubili.",
            "Le membrane delle piastre vengono gonfiate (spremitura) e si soffia aria compressa per togliere altro "
            "liquido dalla torta.",
            "Si apre il pacco di piastre: le torte cadono in un cassone o su un nastro; le tele si lavano e il ciclo "
            "ricomincia.",
        ],
        "perche": "La portata di filtrato è proporzionale alla differenza di pressione e inversamente proporzionale "
                  "alla viscosità del liquido e alla resistenza di tela + torta (Darcy, equazione di Ruth): la torta "
                  "cresce, quindi la filtrazione rallenta nel tempo. Alte pressioni e la spremitura danno torte molto "
                  "secche, che costano meno da smaltire o da essiccare. Per lavorare in continuo si usano filtri "
                  "rotativi sotto vuoto o nastropresse.",
        "unita": [("Sospensione da filtrare", "Alimentazione"), ("Serbatoio agitato", "Serbatoio"),
                  ("Flocculante", "Alimentazione"), ("Pompa di alimentazione", "Pompa"),
                  ("Filtropressa", "Filtro"), ("Filtrato limpido", "Prodotto"), ("Acqua di lavaggio", "Alimentazione"),
                  ("Aria compressa", "Alimentazione"), ("Acque di lavaggio", "Spurgo"), ("Torta", "Prodotto")],
        "correnti": [("Sospensione da filtrare", "Serbatoio agitato", ""),
                     ("Flocculante", "Serbatoio agitato", ""),
                     ("Serbatoio agitato", "Pompa di alimentazione", ""),
                     ("Pompa di alimentazione", "Filtropressa", "6-15 bar"),
                     ("Filtropressa", "Filtrato limpido", "filtrato"),
                     ("Acqua di lavaggio", "Filtropressa", "lavaggio torta"),
                     ("Filtropressa", "Acque di lavaggio", ""),
                     ("Aria compressa", "Filtropressa", "soffiaggio / spremitura"),
                     ("Filtropressa", "Torta", "scarico a fine ciclo")],
        "parole": ["filtr", "filtropressa", "piastre", "tel", "torta", "pressione", "lavaggio", "darcy", "discontinu",
                   "spremitura", "sospensione", "flocculant"],
    },

    # ------------------------------------------------------------------ MEMBRANE
    "Osmosi inversa: dissalazione dell'acqua di mare": {
        "reazione": "Nessuna reazione nella separazione: operazione fisica — si applica una pressione maggiore della "
                    "pressione osmotica (π = i·M·R·T, ≈ 27 bar per l'acqua di mare) e l'acqua passa attraverso una "
                    "membrana semipermeabile lasciando indietro i sali",
        "condizioni": "acqua di mare a ≈ 35 g/L di sali; pressione 55-70 bar; membrane composite in poliammide avvolte "
                      "a spirale; reiezione dei sali > 99%; recupero 40-50% (permeato/alimentazione); consumo ≈ 3-4 "
                      "kWh/m³ con recupero di energia",
        "descrizione": [
            "L'acqua di mare è prelevata da un'opera di presa e passa per la grigliatura.",
            "Pretrattamento: coagulazione e filtri a sabbia o ultrafiltrazione, poi filtri a cartuccia da 5 µm; si "
            "dosano antincrostante e bisolfito (per togliere il cloro, che rovina le membrane).",
            "Una pompa ad alta pressione porta l'acqua a 55-70 bar; una parte della portata è pressurizzata invece "
            "dal recuperatore di energia.",
            "Nei moduli a spirale l'acqua scorre lungo le membrane: l'acqua dolce (permeato) le attraversa, i sali "
            "restano e la salamoia si concentra (≈ 60-70 g/L).",
            "La salamoia esce ancora in pressione e cede la sua energia nel recuperatore (scambiatore di pressione) "
            "all'acqua in arrivo; poi viene scaricata in mare con diffusori.",
            "Il permeato, quasi privo di sali e aggressivo, è remineralizzato con calce e CO₂, disinfettato e mandato "
            "alla rete come acqua potabile.",
        ],
        "perche": "Spontaneamente l'acqua passa dalla soluzione diluita a quella concentrata (osmosi); se sulla parte "
                  "concentrata si applica una pressione superiore alla pressione osmotica il flusso si inverte. Il flusso "
                  "di permeato è proporzionale a ΔP − Δπ: poiché la salamoia si concentra, il recupero non può superare "
                  "circa il 50% senza pressioni eccessive. Il pretrattamento protegge le membrane da sporcamento e "
                  "incrostazioni; il recupero di energia ha ridotto di più della metà i consumi rispetto ai primi impianti.",
        "unita": [("Acqua di mare", "Alimentazione"), ("Pretrattamento (filtri a sabbia)", "Filtro"),
                  ("Filtri a cartuccia 5 µm", "Filtro"), ("Pompa ad alta pressione", "Pompa"),
                  ("Recuperatore di energia", "Scambiatore di calore"), ("Moduli a osmosi inversa", "Membrana"),
                  ("Scarico salamoia", "Spurgo"), ("Remineralizzazione", "Miscelatore"),
                  ("Acqua potabile", "Prodotto"), ("Calce + CO₂", "Alimentazione")],
        "correnti": [("Acqua di mare", "Pretrattamento (filtri a sabbia)", "≈ 35 g/L"),
                     ("Pretrattamento (filtri a sabbia)", "Filtri a cartuccia 5 µm", ""),
                     ("Filtri a cartuccia 5 µm", "Pompa ad alta pressione", "≈ 55% della portata"),
                     ("Filtri a cartuccia 5 µm", "Recuperatore di energia", "≈ 45% della portata"),
                     ("Pompa ad alta pressione", "Moduli a osmosi inversa", "55-70 bar"),
                     ("Recuperatore di energia", "Moduli a osmosi inversa", "acqua pressurizzata"),
                     ("Moduli a osmosi inversa", "Recuperatore di energia", "salamoia in pressione"),
                     ("Recuperatore di energia", "Scarico salamoia", "salamoia ≈ 65 g/L"),
                     ("Moduli a osmosi inversa", "Remineralizzazione", "permeato"),
                     ("Calce + CO₂", "Remineralizzazione", ""),
                     ("Remineralizzazione", "Acqua potabile", "")],
        "parole": ["osmosi", "membran", "pressione osmotica", "semipermeabil", "permeato", "salamoia", "concentrato",
                   "dissala", "pretrattament", "recupero di energia", "alta pressione", "spirale", "reiezione"],
    },

    # ------------------------------------------------------------------ GAS CRIOGENICI
    "Frazionamento dell'aria (processo Linde, doppia colonna)": {
        "reazione": "Nessuna reazione: operazione fisica — liquefazione dell'aria (effetto Joule-Thomson ed espansione "
                    "in turbina) e distillazione criogenica di azoto (Teb −196 °C), argon (−186 °C) e ossigeno (−183 °C)",
        "condizioni": "compressione a 5-6 bar; rimozione di acqua e CO₂ su setacci molecolari; scambiatore principale "
                      "fino a ≈ −175 °C; colonna di alta pressione a 5-6 bar, colonna di bassa pressione a 1,2-1,4 bar; "
                      "ossigeno al 99,5%, azoto fino a 99,999%",
        "descrizione": [
            "L'aria è filtrata, compressa a 5-6 bar in un compressore a più stadi con refrigerazione intermedia e "
            "raffreddata con acqua.",
            "Negli adsorbitori a setacci molecolari (due, uno lavora e uno si rigenera) si tolgono acqua e CO₂, che "
            "altrimenti gelerebbero e intaserebbero gli scambiatori.",
            "Nello scambiatore principale, a piastre di alluminio, l'aria si raffredda in controcorrente con l'ossigeno "
            "e l'azoto freddi che escono; una parte passa nel turboespansore, che la raffredda ancora producendo lavoro "
            "e fornisce il freddo per compensare le perdite.",
            "L'aria quasi liquida entra nella colonna di alta pressione: in testa si separa azoto quasi puro, sul fondo "
            "un liquido ricco di ossigeno (≈ 35-40% O₂).",
            "L'azoto di testa condensa nel condensatore-vaporizzatore cedendo calore all'ossigeno liquido sul fondo "
            "della colonna di bassa pressione, che bolle: lo stesso apparecchio è condensatore della prima colonna e "
            "ribollitore della seconda.",
            "Il liquido ricco di ossigeno e una parte dell'azoto liquido sono laminati in valvole (effetto "
            "Joule-Thomson) ed entrano nella colonna di bassa pressione, rispettivamente a metà e in testa come riflusso.",
            "Dalla testa della colonna di bassa pressione esce azoto gassoso, dal fondo ossigeno (gassoso o liquido); "
            "da un piatto intermedio si spilla l'argon grezzo; i prodotti freddi ripassano nello scambiatore principale "
            "e l'azoto impuro rigenera gli adsorbitori.",
        ],
        "perche": "Per liquefare l'aria bisogna scendere sotto la temperatura critica dei componenti: si raffredda con lo "
                  "scambio in controcorrente e con l'espansione (laminazione Joule-Thomson, nel processo Linde "
                  "originario, e turboespansore, più efficiente). L'azoto a 5-6 bar condensa a una temperatura più alta "
                  "di quella a cui bolle l'ossigeno a 1,3 bar: per questo le due colonne, a pressioni diverse, possono "
                  "essere accoppiate con un unico condensatore-vaporizzatore senza un frigorifero esterno. La separazione "
                  "sfrutta le diverse temperature di ebollizione, come in ogni distillazione.",
        "unita": [("Aria atmosferica", "Alimentazione"), ("Compressore multistadio", "Compressore"),
                  ("Refrigerante finale", "Scambiatore di calore"), ("Adsorbitori a setacci molecolari", "Adsorbitore"),
                  ("Scambiatore principale", "Scambiatore di calore"), ("Turboespansore", "Turboespansore"),
                  ("Colonna di alta pressione (5-6 bar)", "Colonna di distillazione"),
                  ("Condensatore-vaporizzatore", "Ribollitore"),
                  ("Valvola di laminazione (liquido ricco)", "Valvola di laminazione"),
                  ("Valvola di laminazione (azoto)", "Valvola di laminazione"),
                  ("Colonna di bassa pressione (1,3 bar)", "Colonna di distillazione"),
                  ("Ossigeno 99,5%", "Prodotto"), ("Azoto", "Prodotto"), ("Argon grezzo", "Prodotto"),
                  ("Azoto impuro (rigenerazione)", "Spurgo")],
        "correnti": [("Aria atmosferica", "Compressore multistadio", "filtrata"),
                     ("Compressore multistadio", "Refrigerante finale", "5-6 bar"),
                     ("Refrigerante finale", "Adsorbitori a setacci molecolari", "aria umida"),
                     ("Adsorbitori a setacci molecolari", "Scambiatore principale", "aria secca, senza CO₂"),
                     ("Scambiatore principale", "Colonna di alta pressione (5-6 bar)", "aria ≈ −175 °C"),
                     ("Scambiatore principale", "Turboespansore", "parte dell'aria"),
                     ("Turboespansore", "Colonna di bassa pressione (1,3 bar)", "aria espansa e fredda"),
                     ("Colonna di alta pressione (5-6 bar)", "Condensatore-vaporizzatore", "azoto gassoso"),
                     ("Condensatore-vaporizzatore", "Colonna di alta pressione (5-6 bar)", "azoto liquido (riflusso)"),
                     ("Condensatore-vaporizzatore", "Valvola di laminazione (azoto)", "azoto liquido"),
                     ("Valvola di laminazione (azoto)", "Colonna di bassa pressione (1,3 bar)", "riflusso in testa"),
                     ("Colonna di alta pressione (5-6 bar)", "Valvola di laminazione (liquido ricco)", "liquido 35-40% O₂"),
                     ("Valvola di laminazione (liquido ricco)", "Colonna di bassa pressione (1,3 bar)", "a metà colonna"),
                     ("Colonna di bassa pressione (1,3 bar)", "Condensatore-vaporizzatore", "ossigeno liquido"),
                     ("Condensatore-vaporizzatore", "Colonna di bassa pressione (1,3 bar)", "ossigeno vapore"),
                     ("Condensatore-vaporizzatore", "Scambiatore principale", "ossigeno freddo"),
                     ("Scambiatore principale", "Ossigeno 99,5%", ""),
                     ("Colonna di bassa pressione (1,3 bar)", "Scambiatore principale", "azoto freddo"),
                     ("Scambiatore principale", "Azoto", ""),
                     ("Colonna di bassa pressione (1,3 bar)", "Argon grezzo", "spillamento laterale"),
                     ("Scambiatore principale", "Azoto impuro (rigenerazione)", "agli adsorbitori")],
        "parole": ["aria", "linde", "liquef", "criogen", "compress", "laminazion", "joule", "thomson", "espansion",
                   "turboespansor", "doppia colonna", "alta pressione", "bassa pressione", "azoto", "ossigeno", "argon",
                   "setacci", "scambiator", "controcorrente", "condensatore-vaporizzatore"],
    },

    # ------------------------------------------------------------------ SCAMBIO IONICO E ADSORBIMENTO
    "Scambio ionico: demineralizzazione dell'acqua": {
        "reazione": "Scambio ionico (equilibrio reversibile sulla resina, non produzione di una sostanza nuova): "
                    "R–SO₃H + Na⁺ ⇌ R–SO₃Na + H⁺ (cationica);  R–N(CH₃)₃OH + Cl⁻ ⇌ R–N(CH₃)₃Cl + OH⁻ (anionica);  "
                    "H⁺ + OH⁻ → H₂O.  Rigenerazione con HCl e NaOH, che spostano gli equilibri all'indietro",
        "condizioni": "temperatura ambiente; colonne a letto fisso di resina (velocità 10-40 volumi di letto/ora); "
                      "rigenerazione con HCl al 4-6% (cationica) e NaOH al 3-4% (anionica); acqua finale con "
                      "conducibilità < 0,1-1 µS/cm dopo il letto misto",
        "descrizione": [
            "L'acqua grezza (di pozzo o di rete) passa in un filtro a sabbia e su carbone attivo, che tolgono solidi "
            "sospesi e cloro (dannoso per le resine).",
            "Nella colonna cationica, con resina in forma H⁺, i cationi (Ca²⁺, Mg²⁺, Na⁺) restano sulla resina e al loro "
            "posto passano ioni H⁺: l'acqua diventa acida.",
            "Nel degasatore, una torre in cui l'acqua scende contro una corrente d'aria, si elimina la CO₂ formata dai "
            "bicarbonati, alleggerendo il lavoro della resina anionica.",
            "Nella colonna anionica, con resina in forma OH⁻, gli anioni (Cl⁻, SO₄²⁻, silice) sono scambiati con OH⁻, "
            "che con gli H⁺ formano acqua.",
            "Un letto misto (resine cationica e anionica mescolate) fa da finitura e dà acqua demineralizzata, per "
            "caldaie ad alta pressione, laboratori, industria elettronica e farmaceutica.",
            "Quando le resine sono esaurite (la conducibilità sale) si rigenerano: HCl nella cationica, NaOH "
            "nell'anionica, poi risciacquo; gli eluati acidi e basici si neutralizzano a vicenda prima dello scarico.",
        ],
        "perche": "Le resine sono polimeri con gruppi ionici fissi e ioni mobili che si scambiano con quelli della "
                  "soluzione secondo un equilibrio: la resina preferisce gli ioni a carica più alta (Ca²⁺ più di Na⁺). "
                  "Una soluzione concentrata di rigenerante sposta l'equilibrio all'indietro (Le Châtelier). "
                  "L'addolcimento è più semplice: una sola resina cationica in forma Na⁺ scambia Ca²⁺ e Mg²⁺ con Na⁺ "
                  "(toglie la durezza, non i sali) e si rigenera con salamoia di NaCl.",
        "unita": [("Acqua grezza", "Alimentazione"), ("Filtro a sabbia e carbone", "Filtro"),
                  ("Colonna cationica (H⁺)", "Colonna a scambio ionico"), ("Degasatore (CO₂)", "Colonna a riempimento"),
                  ("Aria del ventilatore", "Alimentazione"), ("CO₂ in atmosfera", "Spurgo"),
                  ("Pompa di rilancio", "Pompa"), ("Colonna anionica (OH⁻)", "Colonna a scambio ionico"),
                  ("Letto misto", "Colonna a scambio ionico"), ("Acqua demineralizzata", "Prodotto"),
                  ("HCl 4-6% (rigenerazione)", "Alimentazione"), ("NaOH 3-4% (rigenerazione)", "Alimentazione"),
                  ("Vasca di neutralizzazione", "Vasca"), ("Scarico neutralizzato", "Spurgo")],
        "correnti": [("Acqua grezza", "Filtro a sabbia e carbone", ""),
                     ("Filtro a sabbia e carbone", "Colonna cationica (H⁺)", "acqua filtrata, senza cloro"),
                     ("Colonna cationica (H⁺)", "Degasatore (CO₂)", "acqua acida"),
                     ("Aria del ventilatore", "Degasatore (CO₂)", "in controcorrente"),
                     ("Degasatore (CO₂)", "CO₂ in atmosfera", ""),
                     ("Degasatore (CO₂)", "Pompa di rilancio", ""),
                     ("Pompa di rilancio", "Colonna anionica (OH⁻)", ""),
                     ("Colonna anionica (OH⁻)", "Letto misto", "acqua quasi pura"),
                     ("Letto misto", "Acqua demineralizzata", "< 1 µS/cm"),
                     ("HCl 4-6% (rigenerazione)", "Colonna cationica (H⁺)", "rigenerazione"),
                     ("NaOH 3-4% (rigenerazione)", "Colonna anionica (OH⁻)", "rigenerazione"),
                     ("Colonna cationica (H⁺)", "Vasca di neutralizzazione", "eluato acido"),
                     ("Colonna anionica (OH⁻)", "Vasca di neutralizzazione", "eluato basico"),
                     ("Vasca di neutralizzazione", "Scarico neutralizzato", "")],
        "parole": ["scambio ionico", "resin", "cationic", "anionic", "rigenera", "letto misto", "demineralizz",
                   "addolc", "durezza", "degasator", "conducibilità", "hcl", "naoh", "eluat", "h⁺", "oh⁻"],
    },

    "Adsorbimento su carboni attivi con rigenerazione a vapore (recupero di solventi)": {
        "reazione": "Nessuna reazione: operazione fisica — adsorbimento: le molecole del solvente aderiscono alla "
                    "superficie dei pori del carbone attivo (forze di van der Waals); il vapore caldo le libera (desorbimento)",
        "condizioni": "aria con vapori di solvente (per esempio toluene, da verniciatura o stampa) a 20-40 °C; carbone "
                      "attivo con 800-1200 m²/g di superficie; due adsorbitori alternati, cicli di alcune ore; "
                      "rigenerazione con vapore a 110-130 °C; capacità utile ≈ 0,1-0,3 kg di solvente per kg di carbone",
        "descrizione": [
            "L'aria carica di vapori di solvente è filtrata dalle polveri, raffreddata se serve, e spinta da un "
            "ventilatore in uno dei due adsorbitori.",
            "Attraversando il letto di carbone attivo il solvente resta adsorbito; dall'adsorbitore esce aria depurata, "
            "scaricata al camino. Il fronte di saturazione avanza lentamente nel letto.",
            "Prima che il solvente 'sfondi' all'uscita, l'aria viene deviata sul secondo adsorbitore e il primo passa "
            "in rigenerazione.",
            "Nel letto saturo si manda vapore dal basso verso l'alto: il calore fa desorbire il solvente, che esce "
            "con il vapore.",
            "La miscela di vapore e solvente condensa nel condensatore e nel decantatore si separa in due fasi: il "
            "toluene, immiscibile, è recuperato e riutilizzato; l'acqua, con tracce di solvente, va a uno stripper o "
            "alla depurazione.",
            "Il letto rigenerato è asciugato e raffreddato con aria, poi è pronto per un nuovo ciclo di adsorbimento.",
        ],
        "perche": "L'adsorbimento è favorito dalla bassa temperatura e dall'alta concentrazione (isoterme di "
                  "adsorbimento, per esempio di Langmuir o Freundlich); scaldando l'equilibrio si sposta verso il "
                  "desorbimento. L'enorme superficie interna del carbone attivo trattiene molto solvente anche da "
                  "correnti diluite. Due letti alternati rendono continuo il trattamento; con lo stesso principio si "
                  "depura l'acqua potabile e si purifica l'idrogeno (PSA, che rigenera abbassando la pressione).",
        "unita": [("Aria con solvente", "Alimentazione"), ("Filtro polveri", "Filtro"),
                  ("Ventilatore", "Compressore"), ("Adsorbitore A (in adsorbimento)", "Adsorbitore"),
                  ("Adsorbitore B (in rigenerazione)", "Adsorbitore"), ("Camino (aria depurata)", "Spurgo"),
                  ("Vapore di rete", "Alimentazione"), ("Condensatore", "Condensatore"),
                  ("Decantatore", "Decantatore"), ("Solvente recuperato", "Prodotto"),
                  ("Acqua alla depurazione", "Spurgo"), ("Aria di asciugatura", "Alimentazione")],
        "correnti": [("Aria con solvente", "Filtro polveri", ""),
                     ("Filtro polveri", "Ventilatore", ""),
                     ("Ventilatore", "Adsorbitore A (in adsorbimento)", "aria + solvente"),
                     ("Adsorbitore A (in adsorbimento)", "Camino (aria depurata)", "aria depurata"),
                     ("Vapore di rete", "Adsorbitore B (in rigenerazione)", "vapore 110-130 °C"),
                     ("Adsorbitore B (in rigenerazione)", "Condensatore", "vapore + solvente desorbito"),
                     ("Condensatore", "Decantatore", "due fasi"),
                     ("Decantatore", "Solvente recuperato", "fase organica"),
                     ("Decantatore", "Acqua alla depurazione", "fase acquosa"),
                     ("Aria di asciugatura", "Adsorbitore B (in rigenerazione)", "asciugatura e raffreddamento"),
                     ("Adsorbitore B (in rigenerazione)", "Camino (aria depurata)", "aria di asciugatura")],
        "parole": ["adsorb", "carbon", "carboni attivi", "desorb", "rigenera", "vapore", "superficie", "pori",
                   "saturazion", "alternat", "due letti", "condens", "decant", "solvente", "isoterm"],
    },

    # ------------------------------------------------------------------ SERVIZI: FREDDO E ACQUA DI RAFFREDDAMENTO
    "Ciclo frigorifero a compressione con torre di raffreddamento": {
        "reazione": "Nessuna reazione: ciclo termodinamico — un fluido frigorigeno (per esempio ammoniaca, R717) "
                    "evapora a bassa pressione assorbendo calore e condensa ad alta pressione cedendolo; nella torre "
                    "l'acqua si raffredda evaporandone una piccola parte",
        "condizioni": "NH₃: evaporazione a ≈ −10 °C (≈ 2,9 bar), condensazione a ≈ 35 °C (≈ 13,5 bar); COP 3-5; "
                      "acqua di torre 30 → 35 °C; la torre raffredda l'acqua fino a 3-5 °C sopra la temperatura di bulbo "
                      "umido dell'aria; evapora l'1-2% dell'acqua in circolo",
        "descrizione": [
            "Nell'evaporatore il fluido frigorigeno liquido, a bassa pressione, bolle a circa −10 °C sottraendo calore "
            "al fluido da raffreddare (salamoia, glicole o acqua refrigerata di processo).",
            "Il vapore freddo è aspirato dal compressore, che ne alza pressione e temperatura (compressione, che "
            "consuma il lavoro elettrico).",
            "Nel condensatore il vapore caldo cede calore all'acqua di torre e condensa a circa 35 °C; il liquido si "
            "raccoglie nel ricevitore di liquido.",
            "Il liquido attraversa la valvola di laminazione: la pressione crolla, una parte evapora e la temperatura "
            "scende fino a −10 °C; il fluido torna all'evaporatore e il ciclo si chiude.",
            "L'acqua calda uscita dal condensatore va alla torre di raffreddamento: è spruzzata sul riempimento e "
            "scende contro l'aria aspirata dal ventilatore; l'evaporazione di una piccola parte raffredda il resto.",
            "L'acqua fredda raccolta nel bacino è ripompata al condensatore; si reintegra l'acqua evaporata e si fa "
            "uno spurgo continuo per non concentrare i sali; si dosano anche anticrostanti e biocidi.",
        ],
        "perche": "Il calore passa spontaneamente solo dal caldo al freddo: per toglierlo da un corpo freddo e cederlo "
                  "all'ambiente caldo serve lavoro (secondo principio). Il frigorigeno sfrutta il calore latente: "
                  "evapora a bassa temperatura perché è a bassa pressione e condensa a temperatura ambiente perché è ad "
                  "alta pressione. Il COP = calore sottratto / lavoro speso. La torre di raffreddamento raffredda per "
                  "evaporazione (calore latente dell'acqua) e può scendere sotto la temperatura dell'aria, fino quasi a "
                  "quella di bulbo umido. Usato al contrario, prendendo il calore del condensatore, lo stesso ciclo è una "
                  "pompa di calore.",
        "unita": [("Fluido da raffreddare", "Alimentazione"), ("Evaporatore", "Evaporatore"),
                  ("Fluido refrigerato", "Prodotto"), ("Compressore", "Compressore"),
                  ("Condensatore", "Condensatore"), ("Ricevitore di liquido", "Serbatoio"),
                  ("Valvola di laminazione", "Valvola di laminazione"),
                  ("Torre di raffreddamento", "Torre di raffreddamento"), ("Aria ambiente", "Alimentazione"),
                  ("Aria calda e umida", "Spurgo"), ("Pompa acqua di torre", "Pompa"),
                  ("Reintegro acqua", "Alimentazione"), ("Spurgo acqua di torre", "Spurgo")],
        "correnti": [("Fluido da raffreddare", "Evaporatore", "es. glicole a 0 °C"),
                     ("Evaporatore", "Fluido refrigerato", "es. glicole a −5 °C"),
                     ("Evaporatore", "Compressore", "vapore di NH₃ ≈ 2,9 bar, −10 °C"),
                     ("Compressore", "Condensatore", "vapore surriscaldato ≈ 13,5 bar"),
                     ("Condensatore", "Ricevitore di liquido", "NH₃ liquida ≈ 35 °C"),
                     ("Ricevitore di liquido", "Valvola di laminazione", ""),
                     ("Valvola di laminazione", "Evaporatore", "liquido + vapore ≈ −10 °C"),
                     ("Condensatore", "Torre di raffreddamento", "acqua ≈ 35 °C"),
                     ("Aria ambiente", "Torre di raffreddamento", "aspirata dal ventilatore"),
                     ("Torre di raffreddamento", "Aria calda e umida", ""),
                     ("Torre di raffreddamento", "Pompa acqua di torre", "acqua ≈ 30 °C"),
                     ("Pompa acqua di torre", "Condensatore", ""),
                     ("Reintegro acqua", "Torre di raffreddamento", "acqua evaporata"),
                     ("Torre di raffreddamento", "Spurgo acqua di torre", "spurgo sali")],
        "parole": ["frigorifer", "frigorigen", "ammoniaca", "compressor", "evaporator", "condensator", "laminazion",
                   "valvola", "ciclo", "cop", "pompa di calore", "torre di raffreddamento", "bulbo umido",
                   "calore latente", "reintegro", "spurgo"],
    },
}


# Parole che fanno riconoscere un impianto in una richiesta («spiegami la distillazione», «impianto di osmosi»).
PAROLE_IMPIANTO_OPERAZIONI = {
    "Distillazione continua binaria (colonna a piatti)": [
        "distillazione continua", "colonna di distillazione", "colonna a piatti", "impianto di distillazione",
        "distillazione binaria", "distillazione frazionata", "benzene-toluene", "benzene e toluene", "mccabe",
        "rapporto di riflusso", "distillazione"],
    "Distillazione discontinua (batch)": ["distillazione discontinua", "distillazione batch", "distillazione a lotti",
                                          "rayleigh", "distillazione differenziale"],
    "Rettifica dell'alcol etilico": ["rettifica", "alcol etilico", "distillazione dell'alcol", "distilleria",
                                     "distillazione del vino", "azeotropo acqua-etanolo", "flemme", "borlanda"],
    "Distillazione in corrente di vapore (oli essenziali)": ["corrente di vapore", "distillazione in vapore",
                                                             "oli essenziali", "olio essenziale", "vaso fiorentino",
                                                             "distillazione a vapore", "steam distillation"],
    "Distillazione sotto vuoto": ["sotto vuoto", "distillazione sottovuoto", "distillazione a pressione ridotta",
                                  "distillazione della glicerina", "vacuum"],
    "Etanolo anidro (distillazione azeotropica con cicloesano)": ["distillazione azeotropica", "etanolo anidro",
                                                                  "alcol anidro", "cicloesano", "trascinatore",
                                                                  "rompere l'azeotropo"],
    "Etanolo anidro (distillazione estrattiva con glicole)": ["distillazione estrattiva", "glicole etilenico",
                                                              "solvente pesante"],
    "Assorbimento della CO₂ con ammine e rigenerazione (stripping)": [
        "assorbimento", "colonna di assorbimento", "assorbitore", "stripping", "strippaggio", "ammine",
        "lavaggio con ammine", "cattura della co2", "cattura della co₂", "desorbimento", "colonna a riempimento"],
    "Estrazione liquido-liquido in controcorrente (acido acetico)": [
        "estrazione liquido-liquido", "estrazione liquido liquido", "estrazione con solvente", "estrattore",
        "raffinato", "coefficiente di ripartizione", "mixer-settler"],
    "Estrazione solido-liquido: olio di semi con esano": ["estrazione solido-liquido", "estrazione solido liquido",
                                                         "lisciviazione", "olio di semi", "esano", "estrazione dell'olio",
                                                         "estrazione con esano"],
    "Estrazione dello zucchero dalle barbabietole (diffusione)": ["barbabietole", "zuccherificio", "diffusore",
                                                                  "estrazione dello zucchero", "fettucce",
                                                                  "zucchero dalle barbabietole"],
    "Evaporazione a multiplo effetto": ["multiplo effetto", "multiplo-effetto", "evaporatore", "evaporatori",
                                        "evaporazione", "concentrazione per evaporazione", "triplo effetto",
                                        "doppio effetto"],
    "Cristallizzazione per evaporazione: zucchero (bolla sotto vuoto, centrifuga, essiccamento)": [
        "cristallizzazione", "cristallizzatore", "bolla di cottura", "massa cotta", "cristallizzazione dello zucchero",
        "cristallizzazione per evaporazione", "produzione dello zucchero"],
    "Cristallizzazione per raffreddamento: nitrato di potassio": ["cristallizzazione per raffreddamento",
                                                                  "nitrato di potassio", "acque madri",
                                                                  "curva di solubilità"],
    "Essiccamento a spruzzo (spray dryer): latte in polvere": ["essiccamento", "essiccatore", "essiccazione",
                                                              "spray dryer", "spray-dryer", "atomizzatore",
                                                              "latte in polvere", "essiccamento a spruzzo",
                                                              "tamburo rotante"],
    "Filtrazione con filtropressa": ["filtrazione", "filtropressa", "filtro pressa", "filtro-pressa",
                                     "separazione solido-liquido", "torta di filtrazione"],
    "Osmosi inversa: dissalazione dell'acqua di mare": ["osmosi", "osmosi inversa", "dissalazione", "dissalatore",
                                                        "membrane", "acqua di mare", "desalinizzazione",
                                                        "dissalazione dell'acqua"],
    "Frazionamento dell'aria (processo Linde, doppia colonna)": ["frazionamento dell'aria", "distillazione dell'aria",
                                                                "liquefazione dell'aria", "processo linde", "linde",
                                                                "ossigeno liquido", "azoto liquido", "aria liquida",
                                                                "distillazione criogenica", "doppia colonna"],
    "Scambio ionico: demineralizzazione dell'acqua": ["scambio ionico", "resine a scambio", "resine scambiatrici",
                                                      "demineralizzazione", "acqua demineralizzata", "addolcimento",
                                                      "addolcitore", "durezza dell'acqua", "deionizzazione"],
    "Adsorbimento su carboni attivi con rigenerazione a vapore (recupero di solventi)": [
        "adsorbimento", "carboni attivi", "carbone attivo", "carbone attivato", "recupero di solventi",
        "recupero dei solventi", "adsorbitore"],
    "Ciclo frigorifero a compressione con torre di raffreddamento": [
        "ciclo frigorifero", "frigorifero", "impianto frigorifero", "pompa di calore", "torre di raffreddamento",
        "torri di raffreddamento", "refrigerazione", "acqua di raffreddamento", "fluido frigorigeno"],
}
