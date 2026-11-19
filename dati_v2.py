"""Dati di BIBL-IA 2: corsi, test di ammissione, atenei, programmi delle materie ed esami per anno.

Le strutture dei test vengono dai bandi e dalle guide pubblicate (aggiornate a novembre 2026) e vanno
sempre ricontrollate sul bando del proprio ateneo: per questo ogni test ha la sua fonte e la data.
"""

AGGIORNATO = "novembre 2026"

# --- I test di ammissione -----------------------------------------------------------------------
# sezioni: (nome, quesiti, minuti, materia della banca da cui prendere le domande o None)
TEST = {
    "Semestre filtro": {
        "chi": "Medicina e Chirurgia, Odontoiatria (e Veterinaria), università statali",
        "come": "Non c'è un test prima: ci si iscrive al semestre filtro e si sostengono tre esami nazionali, "
                "uno per materia. Ogni esame si supera con almeno 18/30; due appelli (dicembre e gennaio), "
                "conta il voto migliore.",
        "sezioni": [("Chimica e propedeutica biochimica", 31, 50, "Chimica"),
                    ("Fisica", 31, 50, "Fisica"),
                    ("Biologia", 31, 50, "Biologia")],
        "dettaglio": "Ogni esame: 31 domande (21 a risposta multipla e 10 a completamento) in 50 minuti.",
        "punti": {"giusta": 1.0, "sbagliata": -0.1, "vuota": 0.0},
        "massimo": "31 per esame (93 in tutto), soglia 18/30 per ogni esame",
        "fonte": ("DM n. 941 del 10/7/2026 (a.a. 2026/27)",
                  "https://testbuddy.it/blog/medicina/semestre-filtro-medicina-20262027-tutte-le-novita-"),
        "completamento": 10,
        "nota": "Le domande a completamento si allenano in BIBL-IA scrivendo la parola o il numero che manca.",
    },
    "Test delle professioni sanitarie": {
        "chi": "Lauree delle professioni sanitarie (Infermieristica, Fisioterapia, Ostetricia, Tecniche di "
               "laboratorio, Logopedia, Igiene dentale e altre)",
        "come": "Test unico preparato da ogni ateneo sullo schema del Ministero, di solito a inizio settembre.",
        "sezioni": [("Biologia", 23, None, "Biologia"), ("Chimica", 15, None, "Chimica"),
                    ("Fisica e matematica", 13, None, "Fisica"), ("Logica e comprensione del testo", 9, None,
                                                                 "Ragionamento logico")],
        "dettaglio": "60 domande a risposta multipla (5 opzioni) in 100 minuti. Biologia e chimica valgono 38 "
                     "domande su 60.",
        "minuti_totali": 100,
        "punti": {"giusta": 1.5, "sbagliata": -0.4, "vuota": 0.0},
        "massimo": "90 punti (60 × 1,5); a parità conta biologia, poi chimica, poi fisica e matematica",
        "fonte": ("DM n. 586 del 6/8/2025 e guide di preparazione",
                  "https://futura.study/blog/professioni-sanitarie/test-professioni-sanitarie-2025/"),
        "nota": "La divisione per materia è quella più citata dalle guide: controlla il bando del tuo ateneo.",
    },
    "TOLC-F": {
        "chi": "Farmacia e CTF (Chimica e tecnologia farmaceutiche) in molti atenei",
        "come": "Test online CISIA, a casa (TOLC@CASA) o all'università, ripetibile più volte all'anno.",
        "sezioni": [("Biologia", 15, 20, "Biologia"), ("Chimica", 15, 20, "Chimica"),
                    ("Matematica", 7, 12, "Matematica"), ("Fisica", 7, 12, "Fisica"),
                    ("Logica", 6, 12, "Ragionamento logico")],
        "dettaglio": "50 domande in 5 sezioni, poi 30 domande di inglese (15 minuti, senza penalità).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; ogni ateneo fissa la sua soglia (sotto: OFA da recuperare)",
        "fonte": ("Regolamento TOLC 2026 (CISIA)", "https://cisiaonline.it/sites/default/files/Regolamenti/Regolamento-TOLC-2026.pdf"),
        "nota": "I minuti di Logica non sono pubblicati in modo uniforme: sono indicativi.",
    },
    "TOLC-I": {
        "chi": "Ingegneria in quasi tutti gli atenei (anche Politecnico di Bari, Bologna, Padova, Pisa, Roma)",
        "come": "Test online CISIA, a casa (TOLC@CASA) o all'università, ripetibile; si può fare già dal 4° "
                "anno delle superiori.",
        "sezioni": [("Matematica", 20, 50, "Matematica"), ("Logica", 10, 20, "Ragionamento logico"),
                    ("Scienze (fisica e chimica)", 10, 20, "Scienze"), ("Comprensione verbale", 10, 20, "Comprensione verbale")],
        "dettaglio": "50 domande in 110 minuti, poi 30 domande di inglese in 15 minuti (senza penalità, fuori "
                     "dal punteggio).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; molti atenei chiedono almeno 18-20 e almeno 6-8 in matematica (sotto: OFA)",
        "fonte": ("Regolamento TOLC 2026 (CISIA) e syllabus TOLC-I",
                  "https://testbuddy.it/tolc/tolc-i/struttura-syllabus"),
        "nota": "La comprensione verbale si allena con brani scritti per BIBL-IA, ognuno con le sue domande.",
    },
    "TOL (Politecnico di Milano)": {
        "chi": "Ingegneria al Politecnico di Milano (accetta anche il TOLC-I)",
        "come": "Test online del Politecnico (TOL), più sessioni all'anno, anche dal 4° anno delle superiori.",
        "sezioni": [("Logica, matematica e statistica", 25, 65, "Matematica"), ("Comprensione verbale", 5, 10, "Comprensione verbale"),
                    ("Fisica", 5, 10, "Fisica")],
        "dettaglio": "65 domande in 100 minuti, di cui 30 di inglese (TENG, 15 minuti): per non avere OFA di "
                     "inglese servono almeno 24 risposte giuste su 30.",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "graduatoria del Politecnico (vedi il bando)",
        "fonte": ("Politecnico di Milano, pagina ufficiale del TOL",
                  "https://www.polimi.it/futuri-studenti/test-e-ammissione/laurea/ingegneria/in-cosa-consiste-il-tol-e-come-prepararsi"),
        "nota": "Il punteggio per risposta (+1 / −0,25) è quello usato nelle simulazioni: controlla la pagina "
                "«Il punteggio del TOL».",
    },
    "TIL-I (Politecnico di Torino)": {
        "chi": "Ingegneria al Politecnico di Torino",
        "come": "Test al computer nei laboratori del Politecnico (TIL-I), più sessioni all'anno.",
        "sezioni": [("Matematica", 20, 50, "Matematica"), ("Logica e comprensione", 10, 20, "Ragionamento logico"),
                    ("Fisica", 12, 20, "Fisica")],
        "dettaglio": "Circa 42 domande in 90 minuti (matematica, comprensione e logica, fisica, conoscenze "
                     "tecniche di base). Le guide non concordano sulla divisione: vale quella del bando.",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "graduatoria del Politecnico (vedi il bando)",
        "fonte": ("Guide al TIL-I 2026 (da verificare sul bando del Politecnico di Torino)",
                  "https://testbuddy.it/altri-test/til/struttura-syllabus"),
        "nota": "Struttura indicativa: le fonti pubblicate non sono concordi.",
    },
    "TOLC-B": {
        "chi": "Biotecnologie, Biologia e Scienze biologiche in molti atenei",
        "come": "Test online CISIA, a casa o all'università, ripetibile.",
        "sezioni": [("Matematica di base", 20, 50, "Matematica"), ("Biologia", 10, 20, "Biologia"),
                    ("Chimica", 10, 20, "Chimica"), ("Fisica", 10, 20, "Fisica")],
        "dettaglio": "50 domande in 110 minuti, poi 30 domande di inglese (15 minuti, senza penalità).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; soglia fissata dall'ateneo",
        "fonte": ("Regolamento TOLC 2026 (CISIA) e guide TOLC-B",
                  "https://testbuddy.it/tolc/tolc-b/struttura-syllabus"),
        "nota": "",
    },
}

# --- I corsi ------------------------------------------------------------------------------------
CORSI = {
    "Medicina e Chirurgia": {
        "anni": 6, "test": ["Semestre filtro"], "icona": "🩺",
        "materie_test": ["Biologia", "Chimica", "Fisica"],
        # Le versioni del corso: gli esami sono quelli comuni, cambiano lingua o approfondimenti.
        "indirizzi": {
            "Medicina e Chirurgia (in italiano)": {},
            "Medicine and Surgery (in inglese)": {1: ["Chemistry and Introductory Biochemistry", "Medical Physics",
                                                      "Biology and Genetics", "Histology and Embryology",
                                                      "Human Anatomy I"]},
            "Medicina e Chirurgia tecnologica (MedTec)": {1: ["Chimica e propedeutica biochimica", "Fisica medica",
                                                             "Biologia e genetica", "Analisi matematica",
                                                             "Fondamenti di informatica", "Anatomia umana I"],
                                                         3: ["Fisiologia umana II", "Patologia generale",
                                                             "Bioingegneria", "Elettronica per la medicina"]},
        },
        "esami": {
            1: ["Chimica e propedeutica biochimica", "Fisica medica", "Biologia e genetica", "Istologia ed embriologia",
                "Anatomia umana I", "Inglese scientifico"],
            2: ["Biochimica", "Anatomia umana II", "Fisiologia umana I", "Genetica medica", "Microbiologia"],
            3: ["Fisiologia umana II", "Patologia generale e fisiopatologia", "Immunologia", "Semeiotica medica",
                "Metodologia clinica"],
            4: ["Anatomia patologica", "Farmacologia", "Malattie dell'apparato cardiovascolare e respiratorio",
                "Gastroenterologia", "Nefrologia e urologia", "Malattie infettive"],
            5: ["Medicina interna", "Chirurgia generale", "Neurologia", "Psichiatria", "Ginecologia e ostetricia",
                "Pediatria", "Igiene e sanità pubblica", "Medicina legale"],
            6: ["Clinica medica", "Clinica chirurgica", "Emergenze medico-chirurgiche", "Tirocinio e tesi"],
        },
    },
    "Odontoiatria e protesi dentaria": {
        "anni": 6, "test": ["Semestre filtro"], "icona": "🦷",
        "materie_test": ["Biologia", "Chimica", "Fisica"],
        "esami": {
            1: ["Chimica e propedeutica biochimica", "Fisica", "Biologia e genetica", "Istologia", "Anatomia umana"],
            2: ["Biochimica", "Fisiologia", "Microbiologia", "Materiali dentari", "Anatomia dell'apparato stomatognatico"],
            3: ["Patologia generale", "Farmacologia", "Radiologia odontoiatrica", "Patologia speciale odontostomatologica"],
            4: ["Odontoiatria conservativa", "Parodontologia", "Ortognatodonzia", "Protesi dentaria"],
            5: ["Chirurgia orale", "Endodonzia", "Implantologia", "Pedodonzia"],
            6: ["Tirocinio clinico integrato", "Gnatologia", "Tesi"],
        },
    },
    "Medicina Veterinaria": {
        "anni": 5, "test": ["Semestre filtro"], "icona": "🐾",
        "materie_test": ["Biologia", "Chimica", "Fisica"],
        "esami": {
            1: ["Chimica e propedeutica biochimica", "Fisica", "Biologia e genetica", "Anatomia degli animali domestici",
                "Istologia ed embriologia"],
            2: ["Biochimica", "Fisiologia veterinaria", "Zootecnica", "Microbiologia e immunologia veterinaria"],
            3: ["Patologia generale", "Farmacologia e tossicologia veterinaria", "Parassitologia", "Malattie infettive"],
            4: ["Clinica medica veterinaria", "Chirurgia veterinaria", "Ostetricia veterinaria",
                "Ispezione e controllo degli alimenti"],
            5: ["Clinica degli animali da reddito", "Tirocinio", "Tesi"],
        },
    },
    "Professioni sanitarie": {
        "anni": 3, "test": ["Test delle professioni sanitarie"], "icona": "🩹",
        "materie_test": ["Biologia", "Chimica", "Fisica", "Matematica", "Ragionamento logico"],
        # Le 22 lauree delle professioni sanitarie (classi L/SNT1-4): il 1° anno è in gran parte comune,
        # dal 2° anno gli esami caratteristici della professione.
        "indirizzi": {
            "Infermieristica": {2: ["Infermieristica clinica medica", "Infermieristica clinica chirurgica", "Farmacologia",
                                    "Patologia generale"],
                                3: ["Infermieristica in area critica", "Infermieristica di comunità", "Salute mentale",
                                    "Management sanitario, deontologia e legislazione"]},
            "Infermieristica pediatrica": {2: ["Pediatria generale", "Infermieristica pediatrica clinica", "Farmacologia"],
                                           3: ["Neonatologia", "Urgenze pediatriche", "Neuropsichiatria infantile"]},
            "Ostetricia": {2: ["Ostetricia fisiologica", "Ginecologia", "Farmacologia", "Patologia generale"],
                           3: ["Ostetricia patologica", "Neonatologia", "Medicina legale e deontologia"]},
            "Fisioterapia": {2: ["Chinesiologia", "Riabilitazione neurologica", "Riabilitazione muscolo-scheletrica",
                                 "Neurologia"],
                             3: ["Riabilitazione cardio-respiratoria", "Terapia manuale", "Riabilitazione in pediatria"]},
            "Logopedia": {2: ["Linguistica e fonetica", "Audiologia e foniatria", "Neuropsicologia"],
                          3: ["Disturbi del linguaggio in età evolutiva", "Disfagia", "Afasie"]},
            "Ortottica e assistenza oftalmologica": {2: ["Fisiopatologia della visione binoculare", "Oftalmologia"],
                                                     3: ["Strabismo e ambliopia", "Ipovisione e riabilitazione visiva"]},
            "Podologia": {2: ["Biomeccanica del piede", "Dermatologia", "Ortopedia"],
                          3: ["Podologia del piede diabetico", "Ortesi plantari"]},
            "Terapia della neuro e psicomotricità dell'età evolutiva": {2: ["Neuropsichiatria infantile",
                                                                            "Psicologia dello sviluppo"],
                                                                        3: ["Terapia psicomotoria", "Disturbi del neurosviluppo"]},
            "Terapia occupazionale": {2: ["Terapia occupazionale nell'adulto", "Neurologia", "Ergonomia"],
                                      3: ["Terapia occupazionale in pediatria", "Ausili e domotica"]},
            "Educazione professionale": {2: ["Pedagogia speciale", "Psichiatria", "Psicologia clinica"],
                                         3: ["Dipendenze patologiche", "Disabilità e inclusione"]},
            "Tecnica della riabilitazione psichiatrica": {2: ["Psichiatria", "Psicologia clinica", "Psicofarmacologia"],
                                                          3: ["Riabilitazione psicosociale", "Psichiatria di comunità"]},
            "Tecniche audioprotesiche": {2: ["Audiologia", "Elettroacustica", "Tecnologia degli apparecchi acustici"],
                                         3: ["Applicazione delle protesi acustiche", "Impianti cocleari"]},
            "Tecniche audiometriche": {2: ["Audiologia", "Audiometria tonale e vocale", "Otorinolaringoiatria"],
                                       3: ["Potenziali evocati uditivi", "Audiologia infantile"]},
            "Tecniche di laboratorio biomedico": {2: ["Biochimica clinica", "Microbiologia clinica", "Patologia clinica"],
                                                  3: ["Ematologia di laboratorio", "Anatomia patologica",
                                                      "Biologia molecolare clinica"]},
            "Tecniche di radiologia medica per immagini e radioterapia": {2: ["Fisica delle radiazioni", "Radiologia",
                                                                              "Tomografia computerizzata"],
                                                                          3: ["Risonanza magnetica", "Medicina nucleare",
                                                                              "Radioterapia", "Radioprotezione"]},
            "Tecniche di neurofisiopatologia": {2: ["Neurofisiologia", "Elettroencefalografia", "Neurologia"],
                                                3: ["Elettromiografia", "Potenziali evocati", "Polisonnografia"]},
            "Tecniche ortopediche": {2: ["Biomeccanica", "Ortopedia", "Materiali per ortesi e protesi"],
                                     3: ["Protesi d'arto", "Ortesi della colonna"]},
            "Tecniche di fisiopatologia cardiocircolatoria e perfusione cardiovascolare": {
                2: ["Fisiopatologia cardiovascolare", "Cardiologia", "Tecniche di circolazione extracorporea"],
                3: ["Cardiochirurgia", "Emodinamica", "Ecocardiografia"]},
            "Igiene dentale": {2: ["Parodontologia", "Igiene orale professionale", "Microbiologia del cavo orale"],
                               3: ["Prevenzione odontoiatrica di comunità", "Igiene dentale nel paziente speciale"]},
            "Dietistica": {2: ["Scienze dell'alimentazione", "Dietetica", "Biochimica della nutrizione"],
                           3: ["Dietoterapia", "Nutrizione clinica", "Educazione alimentare"]},
            "Assistenza sanitaria": {2: ["Igiene e medicina preventiva", "Epidemiologia", "Educazione alla salute"],
                                     3: ["Vaccinazioni e profilassi", "Sanità pubblica"]},
            "Tecniche della prevenzione nell'ambiente e nei luoghi di lavoro": {
                2: ["Igiene ambientale", "Medicina del lavoro", "Tossicologia"],
                3: ["Sicurezza alimentare", "Diritto sanitario e vigilanza"]},
        },
        "esami": {
            1: ["Anatomia umana", "Fisiologia", "Biochimica", "Biologia e genetica", "Fisica e statistica",
                "Infermieristica generale (o le basi della propria professione)"],
            2: ["Patologia generale", "Farmacologia", "Microbiologia e igiene", "Infermieristica clinica medica",
                "Infermieristica clinica chirurgica"],
            3: ["Infermieristica in area critica", "Pediatria", "Ostetricia e ginecologia", "Salute mentale",
                "Management sanitario, deontologia e legislazione"],
        },
    },
    "Farmacia e CTF": {
        "anni": 5, "test": ["TOLC-F"], "icona": "💊",
        "materie_test": ["Biologia", "Chimica", "Matematica", "Fisica", "Ragionamento logico"],
        "esami": {
            1: ["Chimica generale e inorganica", "Biologia animale e vegetale", "Matematica", "Fisica",
                "Anatomia umana"],
            2: ["Chimica organica", "Chimica analitica", "Fisiologia", "Microbiologia", "Biochimica"],
            3: ["Chimica farmaceutica I", "Farmacologia", "Analisi dei medicinali", "Patologia generale"],
            4: ["Chimica farmaceutica II", "Tecnologia farmaceutica", "Farmacoterapia", "Tossicologia"],
            5: ["Legislazione farmaceutica", "Farmacognosia", "Tirocinio in farmacia", "Tesi"],
        },
    },
    "Ingegneria": {
        "anni": 5, "test": ["TOLC-I", "TOL (Politecnico di Milano)", "TIL-I (Politecnico di Torino)"], "icona": "⚙️",
        "materie_test": ["Matematica", "Ragionamento logico", "Fisica", "Chimica"],
        "esami": {
            1: ["Analisi matematica 1", "Geometria e algebra lineare", "Fisica 1 (meccanica)",
                "Fondamenti di informatica", "Chimica", "Disegno tecnico"],
            2: ["Analisi matematica 2", "Fisica 2 (elettromagnetismo)", "Meccanica razionale", "Elettrotecnica",
                "Calcolo numerico", "Probabilità e statistica"],
        },
        # Dal 3° anno gli esami dipendono dall'indirizzo (3° = triennale, 4°-5° = magistrale).
        "indirizzi": {
            "Informatica": {3: ["Algoritmi e strutture dati", "Basi di dati", "Sistemi operativi", "Reti di calcolatori",
                                "Ingegneria del software"],
                            4: ["Intelligenza artificiale", "Sistemi distribuiti", "Sicurezza informatica"],
                            5: ["Machine learning", "Cloud computing", "Tesi magistrale"]},
            "Gestionale": {3: ["Economia e organizzazione aziendale", "Ricerca operativa", "Gestione della produzione",
                               "Impianti industriali"],
                           4: ["Logistica", "Gestione dei progetti", "Analisi dei dati per le decisioni"],
                           5: ["Strategia d'impresa", "Supply chain", "Tesi magistrale"]},
            "Meccanica": {3: ["Termodinamica applicata", "Meccanica applicata alle macchine", "Scienza delle costruzioni",
                              "Tecnologia meccanica", "Costruzione di macchine"],
                          4: ["Macchine a fluido", "Progettazione meccanica", "Dinamica dei sistemi meccanici"],
                          5: ["Meccanica delle vibrazioni", "Robotica industriale", "Tesi magistrale"]},
            "Elettronica": {3: ["Elettronica analogica", "Elettronica digitale", "Segnali e sistemi", "Campi elettromagnetici",
                                "Controlli automatici"],
                            4: ["Microelettronica", "Sistemi embedded", "Telecomunicazioni"],
                            5: ["Progettazione di circuiti integrati", "Fotonica", "Tesi magistrale"]},
            "Elettrica": {3: ["Macchine elettriche", "Sistemi elettrici per l'energia", "Elettronica di potenza",
                              "Misure elettriche"],
                          4: ["Azionamenti elettrici", "Reti elettriche intelligenti"],
                          5: ["Mobilità elettrica", "Tesi magistrale"]},
            "Civile": {3: ["Scienza delle costruzioni", "Tecnica delle costruzioni", "Geotecnica", "Idraulica", "Topografia"],
                       4: ["Costruzioni in calcestruzzo armato", "Infrastrutture viarie", "Dinamica delle strutture"],
                       5: ["Ingegneria sismica", "Ponti", "Tesi magistrale"]},
            "Biomedica": {3: ["Bioingegneria", "Fisiologia per l'ingegneria", "Strumentazione biomedica",
                              "Elaborazione di segnali biomedici", "Biomeccanica"],
                          4: ["Biomateriali", "Bioimmagini", "Organi artificiali"],
                          5: ["Ingegneria dei tessuti", "Dispositivi medici", "Tesi magistrale"]},
            "Chimica": {3: ["Principi di ingegneria chimica", "Termodinamica dell'ingegneria chimica", "Fenomeni di trasporto",
                            "Impianti chimici"],
                        4: ["Reattori chimici", "Processi di separazione"],
                        5: ["Processi industriali sostenibili", "Tesi magistrale"]},
            "Aerospaziale": {3: ["Aerodinamica", "Meccanica del volo", "Strutture aerospaziali", "Propulsione"],
                             4: ["Gasdinamica", "Dinamica e controllo dei satelliti"],
                             5: ["Progetto di velivoli", "Tesi magistrale"]},
            "Energetica": {3: ["Fisica tecnica", "Macchine", "Impianti energetici", "Fonti rinnovabili"],
                           4: ["Sistemi energetici", "Efficienza energetica degli edifici"],
                           5: ["Idrogeno e accumulo", "Tesi magistrale"]},
            "Ambiente e territorio": {3: ["Idrologia", "Ingegneria sanitaria-ambientale", "Geologia applicata"],
                                      4: ["Trattamento delle acque", "Valutazione d'impatto ambientale"],
                                      5: ["Rischio idrogeologico", "Tesi magistrale"]},
        },
    },
    "Biotecnologie": {
        "anni": 3, "test": ["TOLC-B"], "icona": "🧬",
        "materie_test": ["Matematica", "Biologia", "Chimica", "Fisica"],
        "esami": {
            1: ["Chimica generale e inorganica", "Biologia cellulare", "Matematica", "Fisica", "Chimica organica"],
            2: ["Biochimica", "Genetica", "Microbiologia", "Biologia molecolare"],
            3: ["Biotecnologie cellulari", "Immunologia", "Bioinformatica", "Tirocinio e tesi"],
        },
    },
}

# --- Gli atenei (corsi e test usati) --------------------------------------------------------------
# Atenei statali con Medicina e Chirurgia (semestre filtro) e, quasi sempre, le professioni sanitarie.
MEDICINA = ["Bari (anche sede di Taranto)", "Basilicata", "Bologna", "Brescia", "Cagliari", "Calabria", "Campania "
            "«Luigi Vanvitelli»", "Catania", "Catanzaro «Magna Græcia»", "Chieti-Pescara", "Ferrara", "Firenze",
            "Foggia", "Genova", "Insubria", "L'Aquila", "Messina", "Milano", "Milano-Bicocca",
            "Modena e Reggio Emilia", "Molise", "Napoli Federico II", "Padova", "Palermo", "Parma", "Pavia",
            "Perugia", "Piemonte Orientale", "Pisa", "Politecnica delle Marche", "Roma La Sapienza",
            "Roma Tor Vergata", "Salerno", "Salento", "Sassari", "Siena", "Torino", "Trento", "Trieste", "Udine",
            "Verona"]
MEDICINA_PRIVATE = ["Cattolica del Sacro Cuore (Roma)", "Humanitas University", "Vita-Salute San Raffaele",
                    "Campus Bio-Medico", "UniCamillus", "LUM", "Link Campus"]
INGEGNERIA = {
    "TOLC-I": ["Politecnico di Bari (anche sede di Taranto)", "Bologna", "Brescia", "Bergamo", "Cagliari",
               "Calabria", "Campania «Luigi Vanvitelli»", "Cassino", "Catania", "Ferrara", "Firenze", "Genova",
               "L'Aquila", "Messina", "Modena e Reggio Emilia", "Napoli Federico II", "Napoli Parthenope", "Padova",
               "Palermo", "Parma", "Pavia", "Perugia", "Pisa", "Politecnica delle Marche", "Roma La Sapienza",
               "Roma Tor Vergata", "Roma Tre", "Salento", "Salerno", "Sannio", "Siena", "Trento", "Trieste", "Udine",
               "Basilicata"],
    "TOL (Politecnico di Milano)": ["Politecnico di Milano (accetta anche il TOLC-I)"],
    "TIL-I (Politecnico di Torino)": ["Politecnico di Torino"],
}
FARMACIA = ["Bari", "Bologna", "Cagliari", "Calabria", "Camerino", "Catania", "Catanzaro", "Chieti-Pescara",
            "Ferrara", "Firenze", "Genova", "Messina", "Milano", "Modena e Reggio Emilia", "Napoli Federico II",
            "Padova", "Palermo", "Parma", "Pavia", "Perugia", "Pisa", "Roma La Sapienza", "Salerno", "Sassari",
            "Siena", "Torino", "Trieste", "Urbino"]
BIOTECNOLOGIE = ["Bari", "Bologna", "Brescia", "Cagliari", "Catania", "Ferrara", "Firenze", "Genova",
                 "Milano", "Milano-Bicocca", "Modena e Reggio Emilia", "Napoli Federico II", "Padova", "Palermo",
                 "Parma", "Pavia", "Perugia", "Pisa", "Roma La Sapienza", "Roma Tor Vergata", "Salerno",
                 "Siena", "Torino", "Trieste", "Verona"]


VETERINARIA = ["Bari", "Bologna", "Camerino", "Messina", "Milano", "Napoli Federico II", "Padova", "Parma", "Perugia",
               "Pisa", "Sassari", "Teramo", "Torino"]


def atenei(corso):
    """[(ateneo, test)] per il corso. Le liste sono le principali sedi statali: il bando dell'ateneo è
    sempre la fonte che conta."""
    if corso in ("Medicina e Chirurgia", "Odontoiatria e protesi dentaria"):
        return [(a, "Semestre filtro") for a in MEDICINA] + [(a, "Test proprio dell'ateneo (privata)")
                                                               for a in MEDICINA_PRIVATE]
    if corso == "Medicina Veterinaria":
        return [(a, "Semestre filtro") for a in VETERINARIA]
    if corso == "Professioni sanitarie":
        return [(a, "Test delle professioni sanitarie") for a in MEDICINA]
    if corso == "Ingegneria":
        return [(a, t) for t, lista in INGEGNERIA.items() for a in lista]
    if corso == "Farmacia e CTF":
        return [(a, "TOLC-F") for a in FARMACIA]
    if corso == "Biotecnologie":
        return [(a, "TOLC-B") for a in BIOTECNOLOGIE]
    return []


# --- I programmi delle materie (gli argomenti del piano di studi) ---------------------------------
# Per Biologia e Chimica gli argomenti sono quelli delle prove MUR 2024 della banca (domande collegate);
# per le altre si riconoscono dalle parole chiave della domanda.

# Dati verificati il 14/11/2026 sui decreti MUR, sul sito CISIA e sui bandi dei Politecnici
# (contenuti_v2/verifica_test.md): sostituiscono quelli scritti sopra.
TEST.update({
    "Semestre filtro": {
        "chi": "Medicina e Chirurgia, Odontoiatria (e Veterinaria), università statali",
        "come": "Non c'è un test prima: ci si iscrive al semestre filtro (lezioni dal 1° settembre) e si "
                "sostengono tre esami nazionali, uno per materia, uguali in tutta Italia. Due appelli: giovedì "
                "10 dicembre 2026 e lunedì 11 gennaio 2027, ore 11. Ogni esame si supera con almeno 18/30; se "
                "lo ripeti conta la prova migliore (se almeno 18), poi accetti o rifiuti il voto.",
        "sezioni": [("Chimica e propedeutica biochimica", 31, 50, "Chimica"),
                    ("Fisica", 31, 50, "Fisica"),
                    ("Biologia", 31, 50, "Biologia")],
        "dettaglio": "Ogni esame: 31 domande in 50 minuti, 30 minuti di pausa tra un esame e l'altro. 21 a "
                     "risposta multipla (5 opzioni, una giusta) e 10 a completamento: scrivi a mano, in "
                     "stampatello maiuscolo, la risposta mancante (un solo concetto). Ogni risposta si può "
                     "correggere una sola volta.",
        "punti": {"giusta": 1.0, "sbagliata": -0.1, "vuota": 0.0},
        "massimo": "31 per esame (30 e lode), 93 in tutto; soglia 18/30 per ogni esame. Graduatoria in tre "
                   "fasce: 3 esami superati (300 + voti), 2 (200 + voti), 1 (100 + voti)",
        "fonte": ("DM n. 941 del 10/7/2026 (artt. 7-8 e Allegato 2) e DD n. 249 del 13/7/2026 (date)",
                  "https://www.mur.gov.it/it/atti-e-normativa/decreto-ministeriale-n-941-del-10-7-2026"),
        "completamento": 10,
        "nota": "In BIBL-IA le domande a completamento si allenano scrivendo la parola o il numero che manca.",
    },
    "Test delle professioni sanitarie": {
        "chi": "Lauree delle professioni sanitarie (Infermieristica, Fisioterapia, Ostetricia, Tecniche di "
               "laboratorio, Logopedia, Igiene dentale e altre)",
        "come": "Test unico preparato da ogni ateneo sullo schema del Ministero, uguale per tutti i corsi "
                "dell'ateneo. Nel 2026: 16 settembre (in italiano) e 17 settembre (in inglese), ore 11.",
        "sezioni": [("Biologia", 23, None, "Biologia"), ("Chimica", 15, None, "Chimica"),
                    ("Fisica e matematica", 13, None, "Fisica"),
                    ("Ragionamento logico e problemi", 5, None, "Ragionamento logico"),
                    ("Competenze di lettura e conoscenze acquisite negli studi", 4, None, "Comprensione verbale")],
        "dettaglio": "60 domande a risposta multipla (5 opzioni) in 100 minuti. Biologia e chimica valgono 38 "
                     "domande su 60.",
        "minuti_totali": 100,
        "punti": {"giusta": 1.5, "sbagliata": -0.4, "vuota": 0.0},
        "massimo": "90 punti (60 × 1,5); idonei solo con più di 0 punti. A parità conta biologia, poi chimica, "
                   "fisica e matematica, logica, lettura; poi il candidato più giovane",
        "fonte": ("DM n. 1003 del 6/8/2026 (a.a. 2026/27)",
                  "https://www.mur.gov.it/sites/default/files/2026-08/Decreto%20Ministeriale%20n.%201003%20del%2006-08-2026.pdf"),
        "nota": "Divisione per materia ufficiale (DM 1003/2026, art. 2). Le competenze di lettura si allenano con i brani di comprensione verbale.",
    },
    "TOLC-F": {
        "chi": "Farmacia e CTF (Chimica e tecnologia farmaceutiche) in molti atenei",
        "come": "Test online CISIA, a casa (TOLC@CASA) o all'università; ogni tipo di TOLC si può rifare al "
                "massimo una volta al mese, già dal 4° anno delle superiori.",
        "sezioni": [("Biologia", 15, 20, "Biologia"), ("Chimica", 15, 20, "Chimica"),
                    ("Matematica", 7, 12, "Matematica"), ("Fisica", 7, 12, "Fisica"),
                    ("Logica", 6, 8, "Ragionamento logico")],
        "dettaglio": "50 domande in 72 minuti in 5 sezioni, poi 30 domande di inglese (15 minuti, senza "
                     "penalità, fuori dal punteggio).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; ogni ateneo fissa la sua soglia (sotto: OFA da recuperare)",
        "fonte": ("CISIA, struttura del TOLC-F (sillabo 2026) e Regolamento TOLC 2026",
                  "https://www.cisiaonline.it/tolc/tolc-f/struttura-della-prova-e-sillabo"),
        "nota": "",
    },
    "TOLC-I": {
        "chi": "Ingegneria in quasi tutti gli atenei (anche Politecnico di Bari, Bologna, Padova, Pisa, Roma)",
        "come": "Test online CISIA, a casa (TOLC@CASA) o all'università, al massimo una volta al mese; si può "
                "fare già dal 4° anno delle superiori.",
        "sezioni": [("Matematica", 20, 50, "Matematica"), ("Logica", 10, 20, "Ragionamento logico"),
                    ("Scienze (fisica e chimica)", 10, 20, "Scienze"), ("Comprensione verbale", 10, 20, "Comprensione verbale")],
        "dettaglio": "50 domande in 110 minuti, poi 30 domande di inglese in 15 minuti (senza penalità, fuori "
                     "dal punteggio).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; ogni ateneo fissa nel bando la soglia (spesso anche un minimo in matematica; "
                   "sotto: OFA)",
        "fonte": ("CISIA, struttura del TOLC-I (sillabo 2026) e Regolamento TOLC 2026",
                  "https://www.cisiaonline.it/tolc/tolc-i/struttura-della-prova-e-sillabo"),
        "nota": "La comprensione verbale si allena con brani scritti per BIBL-IA, ognuno con le sue domande.",
    },
    "TOL (Politecnico di Milano)": {
        "chi": "Ingegneria al Politecnico di Milano (valgono anche TOLC-I, CEnT-S e SAT, convertiti in "
               "centesimi)",
        "come": "Test online del Politecnico (TOL), più sessioni all'anno, anche dal 4° anno delle superiori "
                "(con almeno 75/100 al penultimo anno si entra senza graduatoria).",
        "sezioni": [("Logica, matematica e statistica", 25, 65, "Matematica"), ("Comprensione verbale", 5, 10, "Comprensione verbale"),
                    ("Fisica", 5, 10, "Fisica")],
        "dettaglio": "65 domande in 100 minuti, di cui 30 di inglese (15 minuti, anche qui −0,25 per errore): "
                     "per non avere OFA di inglese servono almeno 24 risposte giuste su 30. Il punteggio è "
                     "pesato: 2,6 × logica-matematica + 3 × comprensione + 2 × fisica + 1/3 × inglese.",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "100 punti (pesati); servono almeno 30/100 per la graduatoria",
        "fonte": ("Politecnico di Milano, bando Ingegneria 2026/27 e fase anticipata 2027/28 (artt. 2.4-2.5) e "
                  "pagina «Punteggi e formulazione delle graduatorie»",
                  "https://www.polimi.it/futuri-studenti/test-e-ammissione/laurea/ingegneria/punteggi-e-formulazione-delle-graduatorie"),
        "nota": "Il bando per l'immatricolazione ordinaria 2027/28 non è ancora uscito: controlla che pesi e "
                "soglie restino uguali.",
    },
    "TIL-I (Politecnico di Torino)": {
        "chi": "Ingegneria al Politecnico di Torino (in alternativa: SAT con almeno 650 in ciascuna sezione)",
        "come": "Test al computer nei laboratori del Politecnico (Torino e Mondovì), più sessioni all'anno, "
                "dall'ultimo anno delle superiori; al massimo 3 volte, conta il risultato migliore.",
        "sezioni": [("Matematica", 16, 36, "Matematica"),
                    ("Comprensione del testo e logica", 10, 20, "Ragionamento logico"),
                    ("Fisica", 10, 22, "Fisica"),
                    ("Conoscenze tecniche di base", 6, 12, None)],
        "dettaglio": "42 domande (5 risposte, una giusta) in 90 minuti, in 4 sezioni a tempo.",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "punteggio in centesimi: almeno 30/100 per la graduatoria, 60/100 per entrare sicuri nel "
                   "corso scelto; sotto 4,8/16 in matematica si hanno OFA",
        "fonte": ("Politecnico di Torino, bando Ingegneria a.a. 2026/27 (artt. 3, 7, 8)",
                  "https://www.polito.it/sites/default/files/2025-12/Bando%20Ingegneria%20comunitari%20Extra%2026_27.pdf"),
        "nota": "Il bando 2027/28 non è ancora uscito (di solito a dicembre): controlla che la struttura resti "
                "uguale.",
    },
    "TOLC-B": {
        "chi": "Biotecnologie, Biologia e Scienze biologiche in molti atenei",
        "come": "Test online CISIA, a casa o all'università, al massimo una volta al mese.",
        "sezioni": [("Matematica di base", 20, 50, "Matematica"), ("Biologia", 10, 20, "Biologia"),
                    ("Fisica", 10, 20, "Fisica"), ("Chimica", 10, 20, "Chimica")],
        "dettaglio": "50 domande in 110 minuti, poi 30 domande di inglese (15 minuti, senza penalità).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; soglia fissata dall'ateneo",
        "fonte": ("CISIA, struttura del TOLC-B (sillabo 2026) e Regolamento TOLC 2026",
                  "https://www.cisiaonline.it/tolc/tolc-b/struttura-della-prova-e-sillabo"),
        "nota": "",
    },
})

ARGOMENTI = {
    "Biologia": ["Cellula e divisione cellulare", "Biologia molecolare (DNA, RNA, sintesi proteica)",
                 "Genetica ed ereditarietà", "Metabolismo ed energia", "Anatomia e fisiologia umana",
                 "Microbiologia, virus e immunità", "Evoluzione, ecologia e biologia vegetale"],
    "Chimica": ["Atomo, tavola periodica e legami", "Nomenclatura e reazioni inorganiche",
                "Stechiometria, moli e reazioni", "Concentrazioni e proprietà delle soluzioni",
                "Acidi, basi, pH e tamponi", "Ossidoriduzioni ed elettrochimica",
                "Termodinamica, cinetica ed equilibrio", "Chimica organica e biomolecole"],
    "Fisica": ["Grandezze, unità di misura e vettori", "Cinematica", "Dinamica e quantità di moto",
               "Lavoro, energia e potenza", "Meccanica dei fluidi", "Termologia e termodinamica",
               "Elettrostatica e circuiti", "Magnetismo ed elettromagnetismo", "Onde, ottica e radiazioni"],
    "Matematica": ["Insiemi, numeri e calcolo algebrico", "Equazioni e disequazioni",
                   "Esponenziali e logaritmi", "Funzioni e grafici", "Geometria piana e solida",
                   "Geometria analitica", "Trigonometria", "Probabilità e statistica"],
    "Ragionamento logico": ["Deduzioni e sillogismi", "Sequenze numeriche e di lettere", "Problemi e calcolo",
                            "Insiemi e diagrammi", "Comprensione e analisi del testo"],
    "Comprensione verbale": ["Brani scientifici", "Brani di attualità e cultura", "Brani storici e letterari",
                             "Lessico e significato delle parole"],
    "Inglese": ["Grammatica", "Lessico (vocabulary)", "Comprensione di un testo (reading)", "Inglese scientifico"],
}

# Parole chiave per riconoscere l'argomento delle domande di Fisica, Matematica e Logica.
PAROLE_ARGOMENTO = {
    "Grandezze, unità di misura e vettori": r"unità di misura|dimension|vettor|notazione scientifica|grandezz",
    "Cinematica": r"velocità|accelerazion|moto (?:rettilineo|uniform|circolare|parabolico)|caduta|traiettori",
    "Dinamica e quantità di moto": r"forz|newton|attrito|quantità di moto|impulso|massa|peso|piano inclinato",
    "Lavoro, energia e potenza": r"lavoro|energia (?:cinetica|potenziale|meccanica)|potenza|watt|joule",
    "Meccanica dei fluidi": r"pressione|fluid|archimede|stevino|pascal|bernoulli|portata|densità",
    "Termologia e termodinamica": r"calore|temperatura|irraggiamento|conduzione termica|convezione|termodinamic|gas (?:perfett|ideal)|entropia|calorie|kelvin",
    "Elettrostatica e circuiti": r"carica|coulomb|campo elettrico|potenziale elettrico|condensator|resistenz|"
                                r"corrente|ohm|circuit|volt",
    "Magnetismo ed elettromagnetismo": r"magnet|induzione|lorentz|solenoid|faraday|tesla",
    "Onde, ottica e radiazioni": r"onda|frequenz|lunghezza d'onda|suono|luce|lente|specchi|rifrazion|riflession|"
                                 r"radiazion|decadimento|nucle",
    "Insiemi, numeri e calcolo algebrico": r"insiem|frazion|potenz|radic|polinom|divisibil|numero (?:primo|intero)|"
                                           r"m\.c\.m|mcd|percentual",
    "Equazioni e disequazioni": r"equazion|disequazion|sistema|soluzion",
    "Esponenziali e logaritmi": r"logaritm|log|esponenzial|\be\^",
    "Funzioni e grafici": r"funzion|grafic|dominio|crescent|decrescent",
    "Geometria piana e solida": r"triangol|quadrat|cerchio|circonferenza|area|perimetro|volume|cubo|sfera|cilindro|"
                                r"cono|poligon|rettangol|angol",
    "Geometria analitica": r"retta|coordinat|parabola|ellisse|iperbole|piano cartesiano|punto \(",
    "Trigonometria": r"seno|coseno|tangente|\bsen\b|\bcos\b|radianti|trigonometr",
    "Probabilità e statistica": r"probabilit|media|mediana|moda|varianza|dado|dadi|estra|statistic|frequenz",
    "Deduzioni e sillogismi": r"se .* allora|tutti|nessun|alcuni|vero|falso|deduc|conclusion|ne consegue",
    "Sequenze numeriche e di lettere": r"sequenz|successione|serie|completa|termine mancante|lettere",
    "Problemi e calcolo": r"quant[ieao]|età|anni|euro|costo|prezzo|percorr|ore|minuti",
    "Insiemi e diagrammi": r"insiem|diagramm|venn|tabella",
    "Comprensione e analisi del testo": r"brano|testo|autore|affermazion|si deduce|secondo il",
}

# Le 12 molecole in evidenza (il file è in modelli_3d/molecole) e i giochi.
MOLECOLE_IN_EVIDENZA = ["acqua", "glucosio", "caffeina", "aspirina", "paracetamolo", "adenina", "etanolo",
                        "atp", "colesterolo", "urea", "anidride_carbonica", "metano"]

LIVELLI = {"basso": 8, "intermedio": 6, "alto": 4}   # settimane del piano


# --- Tutte le materie scientifiche e i corsi di laurea scientifici (aggiunti il 15/11/2026) ----------------
# Strutture dei test verificate il 15/11/2026 sul portale CISIA («Struttura della prova e sillabo») e sul
# Regolamento TOLC 2026.
TEST.update({
    "TOLC-S": {
        "chi": "Corsi di laurea scientifici: Chimica, Fisica, Matematica, Informatica, Scienze geologiche, Scienze "
               "naturali e ambientali (in molti atenei)",
        "come": "Test online CISIA, a casa o all'università, al massimo una volta al mese.",
        "sezioni": [["Matematica di base", 20, 50, "Matematica"],
                    ["Ragionamento, problemi e comprensione del testo", 15, 30, "Ragionamento logico"],
                    ["Biologia", 5, 10, "Biologia"], ["Chimica", 5, 10, "Chimica"], ["Fisica", 5, 10, "Fisica"],
                    ["Scienze della Terra", 5, 10, "Scienze della Terra"]],
        "dettaglio": "55 domande in 120 minuti, poi 30 domande di inglese in 15 minuti (senza penalità).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "55 punti; soglia fissata dall'ateneo (sotto la soglia: OFA)",
        "fonte": ["CISIA, struttura del TOLC-S 2026 e Regolamento TOLC 2026",
                  "https://www.cisiaonline.it/tolc/tolc-s/struttura-della-prova-e-sillabo"], "nota": ""},
    "TOLC-AV": {
        "chi": "Agraria, Scienze e tecnologie alimentari, Scienze forestali e alcuni corsi di area veterinaria",
        "come": "Test online CISIA, a casa o all'università, al massimo una volta al mese.",
        "sezioni": [["Biologia", 8, 16, "Biologia"], ["Chimica", 8, 16, "Chimica"], ["Fisica", 8, 16, "Fisica"],
                    ["Matematica", 8, 16, "Matematica"], ["Logica", 8, 16, "Ragionamento logico"],
                    ["Comprensione verbale", 10, 20, "Comprensione verbale"]],
        "dettaglio": "50 domande in 100 minuti, poi 30 domande di inglese in 15 minuti (senza penalità).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; soglia fissata dall'ateneo",
        "fonte": ["CISIA, struttura del TOLC-AV 2026 e Regolamento TOLC 2026",
                  "https://www.cisiaonline.it/tolc/tolc-av/struttura-della-prova-e-sillabo"], "nota": ""},
    "Verifica delle conoscenze (test dell'ateneo)": {
        "chi": "Corsi ad accesso libero o con un test proprio dell'ateneo (per esempio molte lauree in Scienze motorie)",
        "come": "Ogni ateneo decide nel bando se c'è un test e com'è fatto: questa simulazione serve solo ad allenarsi "
                "sulle basi scientifiche.",
        "sezioni": [["Biologia", 10, 15, "Biologia"], ["Chimica", 5, 8, "Chimica"], ["Fisica", 5, 8, "Fisica"],
                    ["Matematica", 10, 15, "Matematica"], ["Logica", 10, 15, "Ragionamento logico"]],
        "dettaglio": "Simulazione indicativa: 40 domande in circa 60 minuti.",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "Indicativo: controlla sempre il bando del tuo ateneo",
        "fonte": ["Bandi dei singoli atenei", ""], "nota": "Simulazione indicativa, non un test ufficiale."},
})

ARGOMENTI.update({
    "Scienze della Terra": ["Minerali e rocce", "Struttura interna della Terra e tettonica delle placche",
                            "Vulcani e terremoti", "Atmosfera, clima e meteorologia",
                            "Idrosfera: oceani e acque continentali", "Il pianeta Terra nel Sistema solare",
                            "Geologia storica e risorse naturali"],
    "Informatica": ["Rappresentazione dei dati e sistema binario", "Algoritmi e diagrammi di flusso",
                    "Programmazione (Python)", "Strutture dati", "Basi di dati e SQL", "Reti e Internet",
                    "Architettura del computer e sistemi operativi"],
})

CORSI.update({
    "Scienze biologiche": {"anni": 3, "test": ["TOLC-B"], "icona": "🦠",
                           "materie_test": ["Matematica", "Biologia", "Chimica", "Fisica"],
                           "esami": {"1": ["Chimica generale e inorganica", "Citologia e istologia", "Matematica",
                                           "Fisica", "Botanica"],
                                     "2": ["Chimica organica", "Zoologia", "Genetica", "Biochimica", "Microbiologia"],
                                     "3": ["Fisiologia", "Biologia molecolare", "Ecologia", "Anatomia comparata",
                                           "Tirocinio e tesi"]}},
    "Chimica": {"anni": 3, "test": ["TOLC-S"], "icona": "⚗️",
                "materie_test": ["Matematica", "Ragionamento logico", "Chimica", "Fisica", "Biologia",
                                 "Scienze della Terra"],
                "esami": {"1": ["Chimica generale e inorganica", "Analisi matematica 1", "Fisica 1",
                                "Laboratorio di chimica"],
                          "2": ["Chimica organica", "Chimica analitica", "Chimica fisica", "Fisica 2"],
                          "3": ["Chimica inorganica", "Biochimica", "Chimica industriale", "Tirocinio e tesi"]}},
    "Fisica": {"anni": 3, "test": ["TOLC-S"], "icona": "🔭",
               "materie_test": ["Matematica", "Ragionamento logico", "Fisica", "Chimica", "Biologia",
                                "Scienze della Terra"],
               "esami": {"1": ["Analisi matematica 1", "Geometria e algebra lineare", "Fisica 1 (meccanica)",
                               "Laboratorio di fisica"],
                         "2": ["Analisi matematica 2", "Fisica 2 (elettromagnetismo)", "Meccanica razionale",
                               "Termodinamica", "Programmazione"],
                         "3": ["Meccanica quantistica", "Struttura della materia", "Fisica nucleare",
                               "Relatività", "Tirocinio e tesi"]}},
    "Matematica": {"anni": 3, "test": ["TOLC-S"], "icona": "➗",
                   "materie_test": ["Matematica", "Ragionamento logico", "Fisica", "Chimica", "Biologia",
                                    "Scienze della Terra"],
                   "esami": {"1": ["Analisi matematica 1", "Geometria 1", "Algebra 1", "Programmazione"],
                             "2": ["Analisi matematica 2", "Geometria 2", "Fisica 1", "Probabilità e statistica"],
                             "3": ["Analisi numerica", "Fisica matematica", "Algebra 2", "Tirocinio e tesi"]}},
    "Informatica": {"anni": 3, "test": ["TOLC-S", "TOLC-I"], "icona": "💻",
                    "materie_test": ["Matematica", "Ragionamento logico", "Informatica", "Fisica", "Chimica"],
                    "esami": {"1": ["Programmazione", "Analisi matematica", "Architettura degli elaboratori",
                                    "Matematica discreta", "Algebra lineare"],
                              "2": ["Algoritmi e strutture dati", "Basi di dati", "Sistemi operativi",
                                    "Probabilità e statistica", "Fisica"],
                              "3": ["Reti di calcolatori", "Ingegneria del software", "Intelligenza artificiale",
                                    "Tirocinio e tesi"]}},
    "Scienze geologiche": {"anni": 3, "test": ["TOLC-S"], "icona": "🌋",
                           "materie_test": ["Matematica", "Ragionamento logico", "Scienze della Terra", "Chimica",
                                            "Fisica", "Biologia"],
                           "esami": {"1": ["Chimica generale", "Matematica", "Fisica", "Geologia generale",
                                           "Mineralogia"],
                                     "2": ["Petrografia", "Paleontologia", "Geologia strutturale", "Stratigrafia",
                                           "Geochimica"],
                                     "3": ["Geomorfologia", "Geologia applicata", "Vulcanologia e sismologia",
                                           "Rilevamento geologico", "Tirocinio e tesi"]}},
    "Scienze naturali e ambientali": {"anni": 3, "test": ["TOLC-S", "TOLC-B"], "icona": "🌿",
                                      "materie_test": ["Matematica", "Biologia", "Chimica", "Fisica",
                                                       "Scienze della Terra", "Ragionamento logico"],
                                      "esami": {"1": ["Chimica generale", "Matematica e statistica", "Botanica",
                                                      "Zoologia", "Geologia generale"],
                                                "2": ["Ecologia", "Fisica", "Chimica organica", "Genetica",
                                                      "Mineralogia"],
                                                "3": ["Conservazione della natura e biodiversità",
                                                      "Climatologia", "Scienze ambientali e inquinamento",
                                                      "Tirocinio e tesi"]}},
    "Scienze agrarie e alimentari": {"anni": 3, "test": ["TOLC-AV"], "icona": "🌾",
                                     "materie_test": ["Biologia", "Chimica", "Fisica", "Matematica",
                                                      "Ragionamento logico", "Comprensione verbale"],
                                     "esami": {"1": ["Matematica", "Chimica generale", "Botanica", "Fisica",
                                                     "Biologia"],
                                               "2": ["Chimica agraria", "Agronomia", "Microbiologia degli alimenti",
                                                     "Coltivazioni erbacee", "Economia agraria"],
                                               "3": ["Scienze e tecnologie alimentari", "Arboricoltura",
                                                     "Entomologia", "Sicurezza alimentare", "Tirocinio e tesi"]}},
    "Scienze motorie": {"anni": 3, "test": ["Verifica delle conoscenze (test dell'ateneo)"], "icona": "🏃",
                        "materie_test": ["Biologia", "Chimica", "Fisica", "Matematica", "Ragionamento logico"],
                        "esami": {"1": ["Anatomia umana", "Biologia", "Chimica e biochimica",
                                        "Teoria e metodologia dell'allenamento", "Psicologia dello sport"],
                                  "2": ["Fisiologia dell'esercizio fisico", "Biomeccanica del movimento",
                                        "Igiene e sanità pubblica", "Sport individuali e di squadra"],
                                  "3": ["Attività motoria preventiva e adattata", "Pedagogia del movimento",
                                        "Traumatologia dello sport", "Tirocinio e tesi"]}},
})

_atenei_base = atenei


def atenei(corso):
    """Per i corsi scientifici aggiunti: il test che usano quasi tutti gli atenei (il bando resta la fonte che conta)."""
    elenco = _atenei_base(corso)
    if elenco or corso not in CORSI:
        return elenco
    return [("Atenei statali: controlla il bando del tuo ateneo", t) for t in CORSI[corso]["test"]]


# --- Altre materie scientifiche di superiori e università (capitoli in contenuti_v2/materie_nuove.json) -------------
def _materie_nuove():
    import json
    from pathlib import Path
    try:
        return json.loads((Path(__file__).resolve().parent / "contenuti_v2" / "materie_nuove.json").read_text(
            encoding="utf-8"))
    except (OSError, ValueError):
        return {}


MATERIE_NUOVE = _materie_nuove()
ARGOMENTI.update({materia: voce["capitoli"] for materia, voce in MATERIE_NUOVE.items()})


# --- Gli altri test di accesso delle facoltà (verificati il 15/11/2026 sulle fonti ufficiali) -----------------
_TOLC_COME = ("Test online CISIA, a casa (TOLC@CASA) o all'università (TOLC@UNI); ogni tipo di TOLC si può rifare al "
              "massimo una volta al mese. Ogni sezione ha il suo tempo: non si torna indietro.")
_TOLC_INGLESE = " Poi 30 domande di inglese in 15 minuti (senza penalità, fuori dal punteggio: indicano il livello A1-B1)."
_REG = "https://cisiaonline.it/sites/default/files/Regolamenti/Regolamento-TOLC-2026.pdf"

TEST.update({
    "TOLC-E": {
        "chi": "Economia, Management, Statistica e corsi affini in molti atenei",
        "come": _TOLC_COME,
        "sezioni": [["Logica", 13, 30, "Ragionamento logico"], ["Comprensione verbale", 10, 30, "Comprensione verbale"],
                    ["Matematica", 13, 30, "Matematica"]],
        "dettaglio": "36 domande in 90 minuti." + _TOLC_INGLESE,
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "36 punti; soglia fissata dall'ateneo nel bando",
        "fonte": ["CISIA, TOLC-E: struttura della prova e sillabo 2026",
                  "https://www.cisiaonline.it/tolc/tolc-e/struttura-della-prova-e-sillabo"], "nota": ""},
    "TOLC-PSI": {
        "chi": "Psicologia (lauree triennali) in molti atenei",
        "come": _TOLC_COME,
        "sezioni": [["Comprensione del testo", 10, 20, "Comprensione verbale"], ["Matematica di base", 10, 20, "Matematica"],
                    ["Ragionamento verbale", 10, 25, "Ragionamento logico"],
                    ["Ragionamento numerico", 10, 20, "Matematica"], ["Biologia", 10, 15, "Biologia"]],
        "dettaglio": "50 domande in 100 minuti." + _TOLC_INGLESE,
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; soglia fissata dall'ateneo nel bando",
        "fonte": ["CISIA, TOLC-PSI: struttura della prova e sillabo 2026",
                  "https://www.cisiaonline.it/tolc/tolc-psi/struttura-della-prova-e-sillabo"],
        "nota": "Ragionamento verbale e numerico si allenano con le domande di logica e di matematica."},
    "TOLC-SU": {
        "chi": "Lettere, Filosofia, Storia, Beni culturali, Scienze dell'educazione e altri studi umanistici",
        "come": _TOLC_COME,
        "sezioni": [["Comprensione del testo e lingua italiana", 30, 60, "Comprensione verbale"],
                    ["Conoscenze e competenze acquisite negli studi", 10, 20, None],
                    ["Ragionamento logico", 10, 20, "Ragionamento logico"]],
        "dettaglio": "50 domande in 100 minuti." + _TOLC_INGLESE,
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; soglia fissata dall'ateneo nel bando",
        "fonte": ["CISIA, TOLC-SU: struttura della prova e sillabo 2026",
                  "https://www.cisiaonline.it/tolc/tolc-su/struttura-della-prova-e-sillabo"],
        "nota": "La sezione di conoscenze (storia, letteratura, cultura generale) non è ancora nella banca di BIBL-IA: "
                "la simulazione allena comprensione del testo e logica."},
    "TOLC-SPS": {
        "chi": "Scienze politiche, Sociologia, Servizio sociale, Relazioni internazionali",
        "come": _TOLC_COME,
        "sezioni": [["Comprensione del testo", 10, 30, "Comprensione verbale"],
                    ["Conoscenze acquisite negli studi", 15, 30, None],
                    ["Ragionamento e linguaggio matematico", 15, 30, "Matematica"]],
        "dettaglio": "40 domande in 90 minuti (comprensione: 2 brani da 5 domande)." + _TOLC_INGLESE,
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "40 punti; soglia fissata dall'ateneo nel bando",
        "fonte": ["CISIA, TOLC-SPS: struttura della prova e sillabo 2026",
                  "https://www.cisiaonline.it/tolc/tolc-sps/struttura-della-prova-e-sillabo"],
        "nota": "La sezione di conoscenze (storia, società, istituzioni) non è ancora nella banca di BIBL-IA."},
    "TOLC-LP": {
        "chi": "Lingue e letterature straniere, Mediazione linguistica",
        "come": _TOLC_COME,
        "sezioni": [["Logica", 10, 30, "Ragionamento logico"], ["Comprensione verbale", 10, 30, "Comprensione verbale"],
                    ["Matematica", 10, 30, "Matematica"]],
        "dettaglio": "30 domande in 90 minuti." + _TOLC_INGLESE,
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "30 punti; soglia fissata dall'ateneo nel bando",
        "fonte": ["CISIA, TOLC-LP: struttura della prova e sillabo 2026 e Regolamento TOLC 2026",
                  "https://www.cisiaonline.it/tolc/tolc-lp/struttura-della-prova-e-sillabo"], "nota": ""},
    "CEnT-S (test CISIA in inglese)": {
        "chi": "Corsi in inglese di Ingegneria, Economia, Farmacia e altri corsi scientifici (ha sostituito English "
               "TOLC-I, TOLC-E e TOLC-F dal novembre 2025)",
        "come": "Test CISIA tutto in inglese, all'università (@UNI) o da casa (@HOME), una volta per periodo di prove.",
        "sezioni": [["Reading and comprehension", 10, 30, "Comprensione verbale"], ["Mathematics", 15, 30, "Matematica"],
                    ["Reasoning on texts and data", 15, 30, "Ragionamento logico"], ["Biology", 10, 20, "Biologia"],
                    ["Chemistry", 10, 20, "Chimica"], ["Physics", 5, 10, "Fisica"]],
        "dettaglio": "65 domande in 140 minuti, tutte in inglese (sezione Reading aggiunta a novembre 2026). Al punteggio "
                     "si aggiunge una correzione per la difficoltà, calcolata alla fine del periodo.",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "Soglia e massimo fissati dagli atenei (punteggio corretto per la difficoltà)",
        "fonte": ["CISIA, CEnT-S: struttura della prova e sillabo",
                  "https://www.cisiaonline.it/cent/cent-s/struttura-della-prova-e-sillabo"],
        "nota": "In BIBL-IA le domande sono in italiano: per allenarti sulla lingua usa anche la sezione Inglese."},
    "IMAT (Medicina in inglese)": {
        "chi": "Medicina e Chirurgia, Odontoiatria e Veterinaria nei corsi in lingua inglese (il semestre filtro non "
               "vale per questi corsi)",
        "come": "Prova nazionale in presenza, una sola volta l'anno: 29 settembre 2026.",
        "sezioni": [["Competenze di lettura e conoscenze", 4, None, "Comprensione verbale"],
                    ["Ragionamento logico e problemi", 5, None, "Ragionamento logico"], ["Biologia", 23, None, "Biologia"],
                    ["Chimica", 15, None, "Chimica"], ["Fisica e matematica", 13, None, "Fisica"]],
        "dettaglio": "60 domande a risposta multipla (5 opzioni) in 100 minuti, in inglese.",
        "minuti_totali": 100,
        "punti": {"giusta": 1.5, "sbagliata": -0.4, "vuota": 0.0},
        "massimo": "90 punti; soglia 20 punti per i candidati UE (sopra 0 per i non UE residenti all'estero)",
        "fonte": ["DM n. 1005 del 6/8/2026",
                  "https://www.mur.gov.it/sites/default/files/2026-08/Decreto%20Ministeriale%20n.%201005%20del%2006-08-2026.pdf"],
        "nota": "In BIBL-IA le domande sono in italiano: gli argomenti sono gli stessi."},
    "Test di Scienze della formazione primaria": {
        "chi": "Scienze della formazione primaria (laurea magistrale a ciclo unico, per insegnare all'infanzia e alla primaria)",
        "come": "Prova preparata da ogni ateneo sullo schema del Ministero, in presenza.",
        "sezioni": [["Competenza linguistica e ragionamento logico", 40, None, "Comprensione verbale"],
                    ["Cultura letteraria, storico-sociale e geografica", 20, None, None],
                    ["Cultura matematico-scientifica", 20, None, "Matematica"]],
        "dettaglio": "80 domande a 4 opzioni in 150 minuti. Bonus per la certificazione d'inglese: B1 +3, B2 +5, C1 +7, "
                     "C2 +10 (vale la più alta).",
        "minuti_totali": 150,
        "punti": {"giusta": 1.0, "sbagliata": 0.0, "vuota": 0.0},
        "massimo": "80 punti più il bonus d'inglese; soglia 55/80",
        "fonte": ["DM n. 931 del 3/7/2026",
                  "https://www.mur.gov.it/it/atti-e-normativa/decreto-ministeriale-n-931-del-03-07-2026"],
        "nota": "La cultura letteraria e storica non è ancora nella banca di BIBL-IA. Nella sezione linguistica e logica "
                "BIBL-IA allena la comprensione del testo."},
    "Test di Architettura": {
        "chi": "Architettura (lauree magistrali a ciclo unico e triennali), anche il TIL-A del Politecnico di Torino",
        "come": "Prova organizzata da ogni ateneo sullo schema del Ministero, in una o più sessioni entro il 30 settembre.",
        "sezioni": [["Comprensione del testo", 10, 20, "Comprensione verbale"], ["Ragionamento logico", 10, 20,
                                                                                 "Ragionamento logico"],
                    ["Storia (anche dell'arte)", 10, 20, None], ["Disegno e rappresentazione", 10, 20, None],
                    ["Fisica e matematica", 10, 20, "Matematica"]],
        "dettaglio": "50 domande a risposta multipla (5 opzioni) in 100 minuti (al Politecnico di Torino 5 sezioni da 20 "
                     "minuti; OFA sotto 3/10 in fisica e matematica).",
        "punti": {"giusta": 1.0, "sbagliata": -0.25, "vuota": 0.0},
        "massimo": "50 punti; la soglia la decide l'ateneo",
        "fonte": ["DM n. 706 del 4/6/2026 (comunicato MUR)",
                  "https://www.mur.gov.it/it/atti-e-normativa/decreto-ministeriale-n-706-del-04-06-2026"],
        "nota": "Storia dell'arte e disegno non sono ancora nella banca di BIBL-IA."},
    "Test online Bocconi": {
        "chi": "Lauree triennali e Giurisprudenza all'Università Bocconi",
        "come": "Online da casa con sorveglianza a distanza, fino a 4 tentativi l'anno (non in giorni consecutivi), "
                "60 € a tentativo.",
        "sezioni": [["Matematica", 24, None, "Matematica"], ["Comprensione del testo", 11, None, "Comprensione verbale"],
                    ["Ragionamento numerico", 6, None, "Matematica"], ["Pensiero critico", 9, None, "Ragionamento logico"]],
        "dettaglio": "50 domande in 75 minuti (test standard; per Giurisprudenza più logica e ragionamento verbale).",
        "minuti_totali": 75,
        "punti": {"giusta": 1.0, "sbagliata": -0.2, "vuota": 0.0},
        "massimo": "50 punti; almeno 17/50 per essere valutati",
        "fonte": ["Università Bocconi, Test online Bocconi",
                  "https://unibocconi.it/it/entrare-bocconi/corsi-di-laurea-triennale-e-giurisprudenza/ammissione/test-online-bocconi"],
        "nota": "Le domande a 3 opzioni valgono −0,33 se sbagliate."},
})

CORSI.update({
    "Economia": {"anni": 3, "test": ["TOLC-E", "Test online Bocconi", "CEnT-S (test CISIA in inglese)"], "icona": "📈",
                 "materie_test": ["Ragionamento logico", "Comprensione verbale", "Matematica"],
                 "esami": {"1": ["Matematica generale", "Economia aziendale", "Microeconomia", "Diritto privato",
                                 "Storia economica"],
                           "2": ["Macroeconomia", "Statistica", "Ragioneria", "Diritto commerciale", "Economia politica"],
                           "3": ["Finanza aziendale", "Marketing", "Economia internazionale", "Tirocinio e tesi"]}},
    "Psicologia": {"anni": 3, "test": ["TOLC-PSI"], "icona": "🧠",
                   "materie_test": ["Comprensione verbale", "Matematica", "Ragionamento logico", "Biologia"],
                   "esami": {"1": ["Psicologia generale", "Psicobiologia", "Statistica psicometrica",
                                   "Psicologia dello sviluppo"],
                             "2": ["Psicologia sociale", "Psicologia dinamica", "Psicometria", "Neuropsicologia"],
                             "3": ["Psicologia clinica", "Psicologia del lavoro", "Tirocinio e tesi"]}},
    "Studi umanistici (Lettere, Filosofia, Storia)": {
        "anni": 3, "test": ["TOLC-SU"], "icona": "📜",
        "materie_test": ["Comprensione verbale", "Ragionamento logico"],
        "esami": {"1": ["Letteratura italiana", "Linguistica generale", "Storia medievale", "Filosofia teoretica"],
                  "2": ["Storia moderna", "Letteratura latina", "Geografia", "Storia dell'arte"],
                  "3": ["Storia contemporanea", "Filologia", "Tirocinio e tesi"]}},
    "Scienze politiche e sociali": {
        "anni": 3, "test": ["TOLC-SPS"], "icona": "🏛️",
        "materie_test": ["Comprensione verbale", "Matematica"],
        "esami": {"1": ["Scienza politica", "Diritto pubblico", "Sociologia generale", "Economia politica"],
                  "2": ["Storia delle relazioni internazionali", "Statistica sociale", "Diritto internazionale"],
                  "3": ["Politiche pubbliche", "Tirocinio e tesi"]}},
    "Lingue e mediazione linguistica": {
        "anni": 3, "test": ["TOLC-LP"], "icona": "🗣️",
        "materie_test": ["Ragionamento logico", "Comprensione verbale", "Matematica", "Inglese"],
        "esami": {"1": ["Lingua inglese 1", "Seconda lingua 1", "Linguistica generale", "Letteratura italiana"],
                  "2": ["Lingua inglese 2", "Seconda lingua 2", "Traduzione"],
                  "3": ["Lingua inglese 3", "Mediazione e interpretariato", "Tirocinio e tesi"]}},
    "Architettura": {"anni": 5, "test": ["Test di Architettura"], "icona": "🏗️",
                     "materie_test": ["Comprensione verbale", "Ragionamento logico", "Matematica", "Fisica"],
                     "esami": {"1": ["Analisi matematica e geometria", "Disegno dell'architettura", "Storia dell'architettura",
                                     "Laboratorio di progettazione 1"],
                               "2": ["Statica", "Fisica tecnica", "Laboratorio di progettazione 2", "Urbanistica"],
                               "3": ["Scienza delle costruzioni", "Tecnologia dell'architettura", "Restauro"],
                               "4": ["Tecnica delle costruzioni", "Progettazione urbana"],
                               "5": ["Laboratorio di sintesi", "Tesi di laurea"]}},
    "Scienze della formazione primaria": {
        "anni": 5, "test": ["Test di Scienze della formazione primaria"], "icona": "🧒",
        "materie_test": ["Comprensione verbale", "Ragionamento logico", "Matematica", "Biologia", "Fisica"],
        "esami": {"1": ["Pedagogia generale", "Psicologia dello sviluppo", "Linguistica italiana", "Matematica di base"],
                  "2": ["Didattica generale", "Storia", "Geografia", "Fondamenti di fisica"],
                  "3": ["Didattica della matematica", "Biologia e didattica delle scienze", "Letteratura per l'infanzia"],
                  "4": ["Pedagogia speciale", "Didattica della lingua inglese"],
                  "5": ["Tirocinio", "Tesi di laurea"]}},
    "Medicina in inglese (IMAT)": {
        "anni": 6, "test": ["IMAT (Medicina in inglese)"], "icona": "🩺",
        "materie_test": ["Biologia", "Chimica", "Fisica", "Matematica", "Ragionamento logico", "Comprensione verbale"],
        "esami": {"1": ["Chemistry and introductory biochemistry", "Physics", "Biology", "Histology", "Anatomy 1"],
                  "2": ["Anatomy 2", "Physiology", "Biochemistry", "Genetics"],
                  "3": ["Pathology", "Microbiology", "Immunology", "Pharmacology"],
                  "4": ["Internal medicine 1", "Surgery 1", "Neurology"],
                  "5": ["Paediatrics", "Obstetrics and gynaecology", "Psychiatry"],
                  "6": ["Internal medicine 2", "Surgery 2", "Thesis"]}},
})


# --- Tutti i capitoli (17/11/2026): il programma completo delle superiori (classi 1-5) e i capitoli degli esami
# universitari (6 = università). Si aggiungono a quelli già presenti, che restano uguali e nello stesso ordine.
# Come nei libri di «Chimica organica, biochimica e biotecnologie» del quinto anno, la chimica organica comprende
# anche le biomolecole, il metabolismo (carboidrati, lipidi, proteine) e le biotecnologie.
UNIVERSITA = 6
CAPITOLI_AGGIUNTI = {
    "Chimica": [
        ("Materia, miscugli e sostanze pure", 1), ("Stati della materia e passaggi di stato", 1),
        ("Leggi dei gas", 2), ("Modelli atomici e configurazione elettronica", 2),
        ("Reazioni chimiche e bilanciamento", 2), ("Forma delle molecole (VSEPR) e legami intermolecolari", 3),
        ("Proprietà colligative", 3), ("Cinetica chimica e catalizzatori", 4), ("Equilibrio chimico e Le Châtelier", 4),
        ("Pile, elettrolisi e potenziali standard", 4), ("Chimica nucleare e radioattività", 4),
        ("Termodinamica chimica: entalpia, entropia ed energia libera", UNIVERSITA),
        ("Equilibri di solubilità e prodotto di solubilità", UNIVERSITA),
        ("Composti di coordinazione", UNIVERSITA), ("Chimica degli elementi dei gruppi principali", UNIVERSITA),
    ],
    "Chimica organica": [
        ("Il carbonio: ibridazione e legami", 4), ("Nomenclatura dei composti organici", 4),
        ("Alogenuri alchilici: sostituzione ed eliminazione", 5), ("Esteri, ammidi, anidridi e saponi", 5),
        ("Composti eterociclici", 5), ("Polimeri e materie plastiche", 5),
        ("Carboidrati", 5), ("Lipidi", 5), ("Amminoacidi e proteine", 5), ("Nucleotidi e acidi nucleici", 5),
        ("Enzimi e catalisi biologica", 5), ("Metabolismo energetico e ATP", 5),
        ("Metabolismo dei carboidrati: glicolisi, fermentazione, gluconeogenesi e glicogeno", 5),
        ("Respirazione cellulare: ciclo di Krebs e catena di trasporto degli elettroni", 5),
        ("Metabolismo dei lipidi: beta-ossidazione, corpi chetonici, sintesi di acidi grassi e colesterolo", 5),
        ("Metabolismo delle proteine: transaminazione e ciclo dell'urea", 5),
        ("Regolazione ormonale del metabolismo", 5), ("Fotosintesi", 5),
        ("Biotecnologie: DNA ricombinante, PCR, clonaggio e applicazioni", 5),
        ("Meccanismi di reazione e intermedi (carbocationi, radicali, carbanioni)", UNIVERSITA),
        ("Spettroscopia: IR, NMR e spettrometria di massa", UNIVERSITA),
        ("Enolati e reazioni di condensazione", UNIVERSITA), ("Reazioni pericicliche", UNIVERSITA),
    ],
    "Biochimica": [
        ("Vitamine e coenzimi", 5), ("Bioenergetica e ATP", 5), ("Fotosintesi", 5),
        ("Metabolismo dei lipidi: beta-ossidazione e corpi chetonici", 5),
        ("Metabolismo degli amminoacidi e ciclo dell'urea", 5),
        ("Enzimi: cinetica e regolazione", UNIVERSITA), ("Gluconeogenesi", UNIVERSITA),
        ("Metabolismo del glicogeno", UNIVERSITA), ("Via dei pentoso fosfati", UNIVERSITA),
        ("Sintesi degli acidi grassi e del colesterolo", UNIVERSITA), ("Lipoproteine e trasporto dei lipidi", UNIVERSITA),
        ("Metabolismo dei nucleotidi", UNIVERSITA), ("Emoglobina e trasporto dell'ossigeno", UNIVERSITA),
        ("Ormoni e trasduzione del segnale", UNIVERSITA),
        ("Integrazione metabolica: digiuno, pasto ed esercizio fisico", UNIVERSITA),
    ],
    "Biologia": [
        ("Caratteristiche dei viventi e classificazione", 1), ("Le molecole della vita", 1),
        ("Ecologia: ecosistemi, catene alimentari e cicli", 1), ("Membrana cellulare e trasporti", 2),
        ("Mitosi, meiosi e ciclo cellulare", 2), ("Evoluzione: Darwin e la selezione naturale", 2),
        ("Tessuti del corpo umano", 3), ("Sistema nervoso e organi di senso", 3),
        ("Apparato cardiovascolare e sangue", 3), ("Apparato respiratorio", 3),
        ("Apparato digerente e nutrizione", 3), ("Sistema endocrino", 3), ("Apparato riproduttore e sviluppo", 3),
        ("Sistema immunitario", 4), ("Genetica di virus e batteri", 5), ("Regolazione genica ed epigenetica", 5),
        ("Biotecnologie e loro applicazioni", 5),
    ],
    "Fisica": [
        ("Statica ed equilibrio dei corpi", 2), ("Gravitazione universale", 3), ("Moto armonico e oscillazioni", 3),
        ("Ottica geometrica: specchi e lenti", 4), ("Corrente elettrica e leggi di Ohm", 4),
        ("Induzione elettromagnetica e onde elettromagnetiche", 5), ("Relatività ristretta", 5),
        ("Fisica quantistica", 5), ("Fisica nucleare e radioattività", 5),
        ("Meccanica del corpo rigido e momento angolare", UNIVERSITA), ("Equazioni di Maxwell", UNIVERSITA),
    ],
    "Matematica": [
        ("Logica e insiemi", 1), ("Calcolo combinatorio", 4), ("Successioni e progressioni", 4),
        ("Vettori e matrici", 4), ("Geometria dello spazio", 5), ("Limiti e continuità", 5),
        ("Derivate e studio di funzione", 5), ("Integrali", 5), ("Equazioni differenziali", 5),
        ("Distribuzioni di probabilità", 5),
    ],
    "Anatomia e fisiologia umana": [
        ("Sangue ed emopoiesi", 4), ("Sistema immunitario e linfatico", 4), ("Organi di senso", 4),
        ("Apparato riproduttore", 4), ("Apparato tegumentario (pelle)", 4), ("Muscoli e contrazione muscolare", 4),
        ("Equilibrio idroelettrolitico e acido-base", UNIVERSITA), ("Termoregolazione", UNIVERSITA),
        ("Neurofisiologia: potenziale d'azione e sinapsi", UNIVERSITA),
    ],
    "Genetica e biologia molecolare": [
        ("Ciclo cellulare, controllo e cancro", 5), ("Genetica di popolazione", UNIVERSITA),
        ("Genomica ed epigenetica", UNIVERSITA), ("Tecniche di biologia molecolare", UNIVERSITA),
    ],
    "Microbiologia e immunologia": [
        ("Struttura della cellula batterica", 5), ("Crescita e metabolismo batterico", UNIVERSITA),
        ("Genetica batterica", UNIVERSITA), ("Patogenicità e tossine", UNIVERSITA),
        ("Resistenza agli antibiotici", UNIVERSITA), ("Diagnosi microbiologica", UNIVERSITA),
        ("Parassiti", UNIVERSITA), ("Infiammazione", UNIVERSITA), ("Ipersensibilità e allergie", UNIVERSITA),
    ],
}
ANNO_CAPITOLI = {}
for _materia, _capitoli in CAPITOLI_AGGIUNTI.items():
    if _materia in ARGOMENTI:
        ARGOMENTI[_materia] = list(ARGOMENTI[_materia]) + [c for c, _ in _capitoli if c not in ARGOMENTI[_materia]]
        ANNO_CAPITOLI.update({f"{_materia}|{c}": a for c, a in _capitoli})


# I piani di studio confrontati con quelli ufficiali degli atenei (a.a. 2025/26 e 2026/27, almeno due atenei grandi
# per corso: Sapienza, Bologna, Padova, Milano Statale, Torino, Pisa, Politecnici…): gli esami obbligatori che
# compaiono nella maggior parte degli atenei, anno per anno. Le fonti sono nel file, corso per corso.
def _piani_ufficiali():
    import json
    from pathlib import Path
    try:
        piani = json.loads((Path(__file__).resolve().parent / "contenuti_v2" / "piani_di_studio.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    for corso, voce in piani.items():
        if corso not in CORSI:
            continue
        CORSI[corso]["esami"] = {int(a): v for a, v in voce["esami"].items() if v}
        if voce.get("indirizzi"):
            CORSI[corso]["indirizzi"] = {nome: {int(a): v for a, v in anni.items() if v}
                                         for nome, anni in voce["indirizzi"].items()}
        CORSI[corso]["fonti_piano"] = voce.get("fonti", [])


_piani_ufficiali()
