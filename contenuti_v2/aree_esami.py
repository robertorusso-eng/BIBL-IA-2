"""Le aree d'esame: ogni esame dei corsi (dati_v2.CORSI) si collega a un'area con le sue domande."""
import re

AREE = [
    # Aree dei corsi scientifici aggiunti il 15/11/2026: prima delle altre, perché sono più specifiche.
    ("Geologia e mineralogia", "geologia|mineralog|petrograf|stratigraf|geomorfolog|paleontolog|vulcanolog|sismolog|"
                               "geochimica|rilevamento geologico|scienze della terra"),
    ("Botanica e zoologia", "botanica|zoologia|anatomia comparata|biologia vegetale|biologia animale|arboricoltura|"
                            "entomologia"),
    ("Ecologia e scienze ambientali", "ecologia|scienze ambientali|biodiversità|conservazione della natura|"
                                      "climatolog"),
    ("Agraria e scienze degli alimenti", "agronom|agrari|coltivazion|tecnologie alimentari|microbiologia degli "
                                         "alimenti|sicurezza alimentare|pedologia"),
    ("Scienze motorie e sport", "sport|attività motori|allenamento|esercizio fisico|biomeccanica del movimento|"
                                "pedagogia del movimento"),
    ("Fisica moderna", "fisica moderna|meccanica quantistica|struttura della materia|fisica nucleare|relatività|"
                       "fisica atomica|astrofisica"),
    ("Anatomia umana", r"anatomia(?! patologica)|anatomia umana|anatomia topografica|apparato locomotore|human anatomy"),
    ("Neurofisiopatologia e tecniche diagnostiche", r"elettroencefalograf|elettromiograf|potenziali evocati|polisonnograf|neurofisiopatolog|ecocardiograf|emodinamica|circolazione extracorporea|cardiologia|bioimmagini"),
    ("Logopedia e disturbi del linguaggio", r"afasi|disfagia|linguaggio|linguistica|fonetica|neurosviluppo|psicomotori"),
    ("Tecniche ortopediche e ausili", r"ortesi|protesi d'arto|ausili|domotica|disabilità|ortognatodonzia"),
    ("Ingegneria aerospaziale", r"aerodinamica|gasdinamica|volo|velivoli|propulsione|satelliti"),
    ("Energia e impianti energetici", r"fonti rinnovabili|idrogeno|sistemi energetici|impianti energetici|mobilità elettrica|azionamenti"),
    ("Ingegneria gestionale e ricerca operativa", r"logistica|supply chain|ricerca operativa|analisi dei dati per le decisioni|impianti industriali|ergonomia"),
    ("Telecomunicazioni e segnali", r"telecomunicazion|segnali|fotonica|elaborazione di segnali"),
    ("Istologia ed embriologia", r"istologia|embriologia|histology"),
    ("Biologia e genetica", r"biologia|genetica|citologia|biotecnolog|biology"),
    ("Fisiologia", r"fisiologia|neurofisiologia"),
    ("Biochimica", r"biochimica|nutrizione|alimentazione|dietetica|dietoterapia"),
    ("Microbiologia e malattie infettive", r"microbiologia|malattie infettive|parassitolog|virologia"),
    ("Immunologia", r"immunolog"),
    ("Patologia generale e anatomia patologica", r"patologia generale|fisiopatologia|anatomia patologica|patologia"),
    ("Farmacologia e tossicologia", r"farmacolog|farmacoterapia|tossicolog|farmacognosia|farmaceutica|tecnologia farmaceutica|farmacia|medicinali"),
    ("Igiene, sanità pubblica e statistica medica", r"igiene|sanità pubblica|epidemiolog|management sanitario|organizzazione|economia sanitaria|statistica medica|educazione alla salute|educazione alimentare|vaccinazion|medicina del lavoro|sicurezza alimentare|ispezione e controllo|dipendenze"),
    ("Medicina interna e specialità mediche", r"medicina interna|clinica medica|semeiotica|metodologia clinica|cardiovascolare|gastroenterolog|nefrolog|endocrinolog|reumatolog|ematolog|oncolog|geriatri|pneumolog|dermatolog|malattie dell"),
    ("Chirurgia e specialità chirurgiche", r"chirurgia|clinica chirurgica|ortopedia|urologia|anestesi|emergenz|area critica|otorino|oftalmolog"),
    ("Pediatria, ginecologia e ostetricia", r"pediatri|neonatolog|ginecolog|ostetric|perinatal"),
    ("Neurologia e psichiatria", r"neurolog|psichiatr|salute mentale|neuropsichiatr|neuroscienze"),
    ("Psicologia e scienze umane", r"psicolog|pedagog|sociolog|antropolog|scienze umane|comunicazione"),
    ("Medicina legale, deontologia e legislazione", r"medicina legale|deontolog|legislazion|bioetica|diritto"),
    ("Scienze infermieristiche", r"infermieristic|assistenza"),
    ("Riabilitazione e fisioterapia", r"riabilitazion|fisioterap|chinesiolog|biomeccanica|terapia occupazionale|logopedi|ortottica|podolog|massoterap|terapia manuale"),
    ("Odontoiatria", r"odontoiatri|parodontolog|protesi dentaria|ortodonzia|conservativa|endodonzia|igiene dentale|gnatolog|implantolog|pedodonzia|odontostomatolog|materiali dentari"),
    ("Medicina veterinaria", r"veterinari|zootecni|anatomia degli animali|animali|ispezione degli alimenti|clinica degli animali"),
    ("Diagnostica per immagini e radioterapia", r"radiolog|diagnostica per immagini|radioterapia|medicina nucleare|radioprotezione|risonanza|tomografia|tecniche di imaging"),
    ("Scienze di laboratorio biomedico", r"laboratorio|biochimica clinica|patologia clinica|ematologia di laboratorio|analisi cliniche"),
    ("Audiologia e scienze della vista", r"audiolog|audioprotesi|ottica e optometria|contattolog|protesi acustiche|audiometria|cocleari|elettroacustica|apparecchi acustici|strabismo"),
    ("Chimica generale e inorganica", r"chimica generale|chimica e propedeutica|chimica inorganica|propedeutica biochimica|^chimica$|chemistry"),
    ("Chimica organica", r"chimica organica"),
    ("Chimica analitica e fisica", r"chimica analitica|chimica fisica|analisi dei medicinali|elettrochimica"),
    ("Analisi matematica", r"analisi matematica|analisi i|analisi ii|calcolo|matematica"),
    ("Geometria e algebra lineare", r"geometria|algebra"),
    ("Fisica generale (meccanica e termodinamica)", r"fisica generale|fisica i\b|fisica 1|^fisica$|fisica medica|medical physics|fisica applicata|meccanica razionale|fisica delle radiazioni"),
    ("Fisica II (elettromagnetismo e ottica)", r"fisica ii|fisica 2|elettromagnetismo|ottica"),
    ("Statistica e probabilità", r"statistica|probabilità|biostatistica"),
    ("Informatica e programmazione", r"informatica|programmazione|algoritmi|basi di dati|calcolatori|software|reti|sistemi operativi|bioinformatica|cloud|machine learning|intelligenza artificiale|sistemi distribuiti|sistemi embedded"),
    ("Elettrotecnica ed elettronica", r"elettrotecnica|elettronica|circuiti|macchine elettriche|sistemi elettrici|campi elettromagnetici|misure elettriche"),
    ("Fisica tecnica e termodinamica applicata", r"fisica tecnica|termodinamica|trasmissione del calore|energetica|impianti termotecnici|macchine a fluido|macchine"),
    ("Scienza e tecnica delle costruzioni", r"scienza delle costruzioni|tecnica delle costruzioni|statica|geotecnica|strutture|costruzioni|ponti|sismica|geologia|topografia"),
    ("Meccanica e disegno tecnico", r"meccanica applicata|disegno|tecnologia meccanica|costruzione di macchine|meccanica dei|progettazione meccanica|vibrazioni|dinamica dei sistemi meccanici"),
    ("Impianti chimici e principi di ingegneria chimica", r"impianti chimici|ingegneria chimica|principi di ingegneria|fenomeni di trasporto|operazioni unitarie|reattori|processi chimici|processi di separazione|processi industriali"),
    ("Scienza e tecnologia dei materiali", r"materiali|metallurgia|polimeri"),
    ("Controlli automatici e sistemi", r"controlli|automatica|sistemi dinamici|teoria dei sistemi|robotica"),
    ("Idraulica e ingegneria ambientale", r"idraulica|ambientale|idrologia|acque|ecologia|idrogeologico"),
    ("Economia e gestione", r"economia|gestione|organizzazione aziendale|impresa"),
    ("Biotecnologie e bioingegneria", r"bioingegneria|biomateriali|strumentazione biomedica|biomedica|dispositivi medici|biosensori|organi artificiali|ingegneria dei tessuti"),
    ("Inglese scientifico", r"inglese|english"),
]


def area_esame(nome):
    n = nome.lower()
    for area, schema in AREE:
        if re.search(schema, n):
            return area
    return None
