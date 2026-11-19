"""Modelli 3D per BIBL-IA: molecole (PubChem), proteine, acidi nucleici, virus e tossine
(Protein Data Bank). I file scaricati restano in modelli_3d/ e si riaprono senza internet.

PubChem: dati di pubblico dominio (NCBI). Protein Data Bank: dati CC0 (RCSB PDB).
Il visualizzatore è 3Dmol.js (licenza BSD), caricato da cdnjs.
"""

import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CARTELLA = Path(__file__).resolve().parent / "modelli_3d"
AGENTE = {"User-Agent": "Mozilla/5.0 (Macintosh) BIBL-IA (uso didattico)"}
AGENTE_WIKIPEDIA = {"User-Agent": "BIBL-IA/1.0 (programma didattico per studenti di medicina e farmacia)"}
LIBRERIA_3D = "https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js"

# Macromolecole del Protein Data Bank: nome italiano → (codice, descrizione).
# Ogni codice è stato controllato sul titolo della struttura nel PDB.
STRUTTURE_PDB = {
    "emoglobina": ("1HHO", "Ossiemoglobina umana"),
    "mioglobina": ("1MBN", "Mioglobina (capodoglio), la prima proteina risolta in 3D"),
    "insulina": ("4INS", "Insulina (maiale), esamero con zinco"),
    "dna": ("1BNA", "DNA a doppia elica, forma B"),
    "trna": ("1EHZ", "RNA transfer della fenilalanina (lievito)"),
    "rna transfer": ("1EHZ", "RNA transfer della fenilalanina (lievito)"),
    "collagene": ("1CAG", "Tripla elica di un peptide simile al collagene"),
    "immunoglobulina": ("1IGT", "Immunoglobulina G (anticorpo) intera"),
    "anticorpo": ("1IGT", "Immunoglobulina G (anticorpo) intera"),
    "lisozima": ("1LYZ", "Lisozima dell'albume"),
    "actina": ("1J6Z", "Actina"),
    "emoagglutinina": ("1RU7", "Emoagglutinina H1 del virus influenzale (ceppo del 1934)"),
    "neuraminidasi": ("2HU4", "Neuraminidasi N1 del virus influenzale con oseltamivir"),
    "spike": ("6VXX", "Proteina spike del SARS-CoV-2 (forma chiusa)"),
    "proteina spike": ("6VXX", "Proteina spike del SARS-CoV-2 (forma chiusa)"),
    "sars-cov-2": ("6VXX", "Proteina spike del SARS-CoV-2 (forma chiusa)"),
    "proteasi hiv": ("1HVR", "Proteasi dell'HIV-1 con un inibitore"),
    "capside hiv": ("3H4E", "Esamero della proteina del capside (CA) dell'HIV-1"),
    "hiv": ("3H4E", "Esamero della proteina del capside (CA) dell'HIV-1"),
    "trascrittasi inversa": ("1RTD", "Trascrittasi inversa dell'HIV-1 con DNA"),
    "tossina botulinica": ("3BTA", "Neurotossina botulinica di tipo A"),
    "tossina colerica": ("1XTC", "Tossina colerica"),
    "tossina difterica": ("1DDT", "Tossina difterica (dimero)"),
    "tossina tetanica": ("1A8D", "Frammento C della tossina tetanica"),
    "rodopsina": ("1F88", "Rodopsina bovina"),
    "canale del potassio": ("1BL8", "Canale del potassio KcsA"),
    "recettore beta-2 adrenergico": ("2RH1", "Recettore β2-adrenergico umano (GPCR)"),
    "recettore adrenergico": ("2RH1", "Recettore β2-adrenergico umano (GPCR)"),
    "acetilcolinesterasi": ("1EA5", "Acetilcolinesterasi (Torpedo californica)"),
    "albumina": ("1AO6", "Albumina del siero umano"),
    "nucleosoma": ("1AOI", "Nucleosoma: istoni con 146 coppie di basi di DNA"),
    "proteasoma": ("1RYP", "Proteasoma 20S (lievito)"),
    "gfp": ("1EMA", "Proteina fluorescente verde (GFP)"),
    "proteina fluorescente verde": ("1EMA", "Proteina fluorescente verde (GFP)"),
    "pbp2a": ("1VQQ", "PBP2a di Staphylococcus aureus resistente alla meticillina (MRSA)"),
    "beta-lattamasi": ("1BTL", "β-lattamasi TEM-1 di Escherichia coli"),
    "cftr": ("5UAK", "Canale CFTR umano (fibrosi cistica)"),
    "egfr": ("1M17", "Dominio tirosin-chinasico di EGFR con un inibitore"),
    "fibrinogeno": ("3GHG", "Fibrinogeno umano"),
}

# Nomi italiani che non si traducono con le regole dei suffissi.
NOMI_ITALIANI = {
    # Farmaci che sono miscele: si mostra il componente principale.
    "ivermectina": "ivermectin B1a",
    "acqua": "water", "ammoniaca": "ammonia", "ossigeno": "oxygen", "idrogeno": "hydrogen",
    "azoto": "nitrogen", "anidride carbonica": "carbon dioxide", "biossido di carbonio": "carbon dioxide",
    "monossido di carbonio": "carbon monoxide", "acqua ossigenata": "hydrogen peroxide",
    "perossido di idrogeno": "hydrogen peroxide", "cloruro di sodio": "sodium chloride",
    "bicarbonato di sodio": "sodium bicarbonate", "acido cloridrico": "hydrochloric acid",
    "acido solforico": "sulfuric acid", "acido nitrico": "nitric acid", "acido fosforico": "phosphoric acid",
    "urea": "urea", "colesterolo": "cholesterol", "aspirina": "aspirin", "paracetamolo": "acetaminophen",
    "penicillina": "penicillin G", "caffeina": "caffeine", "nicotina": "nicotine", "morfina": "morphine",
    "adrenalina": "epinephrine", "noradrenalina": "norepinephrine", "serotonina": "serotonin",
    "dopamina": "dopamine", "istamina": "histamine", "acetilcolina": "acetylcholine",
    "vitamina c": "ascorbic acid", "acido ascorbico": "ascorbic acid", "vitamina a": "retinol",
    "vitamina d": "cholecalciferol", "vitamina e": "alpha-tocopherol", "vitamina k": "phylloquinone",
    "vitamina b1": "thiamine", "vitamina b2": "riboflavin", "vitamina b6": "pyridoxine",
    "vitamina b12": "cyanocobalamin", "acido folico": "folic acid", "glucosio": "glucose",
    "fruttosio": "fructose", "saccarosio": "sucrose", "lattosio": "lactose", "maltosio": "maltose",
    "ribosio": "ribose", "desossiribosio": "deoxyribose", "atp": "adenosine triphosphate",
    "adp": "adenosine diphosphate", "amp": "adenosine monophosphate", "nad": "NAD+", "nadh": "NADH",
    "fad": "flavin adenine dinucleotide", "coenzima a": "coenzyme A", "eme": "heme",
    "clorofilla": "chlorophyll a", "testosterone": "testosterone", "estradiolo": "estradiol",
    "cortisolo": "cortisol", "progesterone": "progesterone", "tiroxina": "thyroxine",
    "etanolo": "ethanol", "metanolo": "methanol", "glicerolo": "glycerol", "benzene": "benzene",
    "fenolo": "phenol", "toluene": "toluene", "acetone": "acetone", "formaldeide": "formaldehyde",
    "acetaldeide": "acetaldehyde", "acido acetico": "acetic acid", "acido lattico": "lactic acid",
    "acido piruvico": "pyruvic acid", "acido citrico": "citric acid", "acido palmitico": "palmitic acid",
    "acido oleico": "oleic acid", "acido stearico": "stearic acid", "acido linoleico": "linoleic acid",
}

PAROLE_TROPPO_GENERICHE = set("""proteina proteine medicina vitamina enzima ormone farmaco sostanza
molecola acido base sale estere zucchero grasso lipide amminoacido nucleotide trigliceride
trigliceridi fosfolipide fosfolipidi steroide steroidi polisaccaride polisaccaridi peptide peptidi
amminoacidi nucleoside nucleosidi carboidrato carboidrati alcano alcani alchene alcheni alchino alchini
alcol alcoli ammina ammine ammide ammidi aldeide aldeidi chetone chetoni etere eteri tossina tossine""".split())


def _richiesta(url, limite=None, tempo=30):
    agente = AGENTE_WIKIPEDIA if "wikipedia.org" in url else AGENTE
    with urllib.request.urlopen(urllib.request.Request(url, headers=agente), timeout=tempo) as r:
        return r.read(limite) if limite else r.read()


def senza_accenti(testo):
    return unicodedata.normalize("NFKD", testo).encode("ascii", "ignore").decode().casefold().strip()


METALLI = {"sodio": "sodium", "potassio": "potassium", "calcio": "calcium", "magnesio": "magnesium",
            "ferro": "iron", "ammonio": "ammonium", "litio": "lithium", "rame": "copper", "zinco": "zinc",
            "argento": "silver", "idrogeno": "hydrogen", "alluminio": "aluminum", "bario": "barium",
            "mercurio": "mercury", "piombo": "lead", "manganese": "manganese", "cobalto": "cobalt"}


def _radici_inglesi(parola):
    """Le radici della nomenclatura che in inglese si scrivono diverse: met→meth, fen→phen..."""
    sostituzioni = [(r"mm", "m"), (r"^met(?=[aeiloy])", "meth"), (r"^et(?=[aeiloy])", "eth"),
                    (r"(?<=[a-z])met(?=il)", "meth"), (r"(?<=[a-z])et(?=il)", "eth"),
                    (r"fen", "phen"), (r"fosf", "phosph"), (r"tio", "thio"), (r"solf", "sulf"),
                    (r"ossi", "oxy"), (r"idr", "hydr"), (r"gli", "gly"), (r"^tir", "tyr"), (r"^trip", "tryp"), (r"cicl", "cycl"),
                    (r"^pir", "pyr"), (r"ciano", "cyano"), (r"cis", "cys"), (r"z(?=[aeiou])", "z")]
    for modello, sostituto in sostituzioni:
        parola = re.sub(modello, sostituto, parola)
    return parola


def _suffisso_inglese(parola):
    regole = [(r"ossido$", "oxide"), (r"ofano$", "ophan"), (r"aldeide$", "aldehyde"), (r"ammide$", "amide"),
              (r"ammina$", "amine"), (r"osio$", "ose"), (r"olo$", "ol"), (r"ano$", "ane"), (r"ene$", "ene"),
              (r"ino$", "yne"), (r"ina$", "ine"), (r"ato$", "ate"), (r"ito$", "ite"), (r"uro$", "ide"),
              (r"one$", "one"), (r"ale$", "al"), (r"ilene$", "ylene"), (r"ile$", "yl"), (r"ide$", "ide"),
              (r"eina$", "eine"), (r"ico$", "ic"), (r"oso$", "ous")]
    for modello, sostituto in regole:
        if re.search(modello, parola):
            return re.sub(modello, sostituto, parola)
    return parola


def nome_inglese(nome):
    """Il nome inglese con cui PubChem conosce la molecola: elenco dei nomi comuni, poi le
    regole della nomenclatura (glicina → glycine, cloruro di sodio → sodium chloride)."""
    n = senza_accenti(nome)
    if n in NOMI_ITALIANI:
        return NOMI_ITALIANI[n]
    sale = re.fullmatch(r"([a-z]+) di ([a-z]+)", n)
    if sale and sale.group(2) in METALLI:
        return f"{METALLI[sale.group(2)]} {_suffisso_inglese(_radici_inglesi(sale.group(1)))}"
    acido = re.fullmatch(r"acido ([a-z0-9,-]+)", n)
    if acido:
        return f"{_suffisso_inglese(_radici_inglesi(acido.group(1)))} acid"
    return " ".join(_suffisso_inglese(_radici_inglesi(p)) for p in n.split())


def traduzione_modello(nome):
    """Ultima possibilità: il modello del Mac traduce il nome; PubChem poi controlla che esista."""
    dati = json.dumps({"model": "llama3.2:3b", "stream": False, "options": {"temperature": 0, "num_predict": 20},
                       "prompt": "Translate this Italian chemical or drug name into its English name. "
                                 f"Reply with the English name only.\n\n{nome}"}).encode()
    try:
        richiesta = urllib.request.Request("http://localhost:11434/api/generate", data=dati,
                                           headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(richiesta, timeout=40) as r:
            testo = json.load(r).get("response", "").strip().splitlines()[0].strip(" .\"'*")
        return testo if 2 <= len(testo) <= 80 else ""
    except Exception:
        return ""


def cartella(tipo):
    percorso = CARTELLA / tipo
    percorso.mkdir(parents=True, exist_ok=True)
    return percorso


def varianti_inglesi(nome, inglese):
    """Altre grafie da provare su PubChem: ivermectine → ivermectin, permetrin → permethrin,
    benzoato di benzile → benzyl benzoate."""
    varianti = []
    for v in (inglese[:-1] if inglese.endswith("ine") else "",):
        if v:
            varianti += [v, v.replace("tr", "thr"), v.replace("f", "ph")]
    estere = re.fullmatch(r"([a-z]+) di ([a-z]+)", senza_accenti(nome))
    if estere:
        varianti.append(f"{nome_inglese(estere.group(2))} {nome_inglese(estere.group(1))}")
    return [v for v in dict.fromkeys(varianti) if v and v != inglese]


def forma_3d(sdf, massimo_atomi=180):
    """Da una struttura 2D (PubChem non calcola il 3D delle molecole grandi) una geometria 3D
    con RDKit: idrogeni, conformazione ETKDG e ottimizzazione MMFF. Stringa vuota se non riesce."""
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
        molecola = Chem.MolFromMolBlock(sdf, removeHs=False)
        if molecola is None or molecola.GetNumHeavyAtoms() > massimo_atomi:
            return ""
        molecola = Chem.AddHs(molecola)
        parametri = AllChem.ETKDGv3()
        parametri.randomSeed = 7
        if AllChem.EmbedMolecule(molecola, parametri) != 0:
            return ""
        if AllChem.MMFFHasAllMoleculeParams(molecola):
            AllChem.MMFFOptimizeMolecule(molecola, maxIters=500)
        return Chem.MolToMolBlock(molecola)
    except Exception:
        return ""


def forma_piana(sdf):
    """La stessa molecola stesa su un piano, come la formula di struttura (catene di carboni
    dritte, anelli regolari), con tutti gli atomi e gli idrogeni: si guarda nello stesso
    visualizzatore 3D, con gli stessi colori, e si gira. Stringa vuota se non riesce."""
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
        molecola = Chem.MolFromMolBlock(sdf, removeHs=False)
        if molecola is None:
            return ""
        molecola = Chem.AddHs(molecola, addCoords=False)
        AllChem.Compute2DCoords(molecola)
        return Chem.MolToMolBlock(molecola)
    except Exception:
        return ""


def molecola_pubchem(nome, scarica=True, usa_modello=True):
    """Informazioni e modello 3D di una molecola da PubChem. Restituisce un dizionario
    {nome, inglese, cid, formula, peso, iupac, sdf, tridimensionale} oppure None."""
    inglese = nome_inglese(nome)
    chiave = re.sub(r"[^a-z0-9]+", "_", senza_accenti(nome)).strip("_")
    file_info = cartella("molecole") / f"{chiave}.json"
    if file_info.exists():
        info = json.loads(file_info.read_text(encoding="utf-8"))
        return info or None
    if not scarica:
        return None
    proprieta = None
    # Anche il nome così com'è: un nome già inglese («tripalmitin») non va «tradotto».
    for tentativo in (list(dict.fromkeys([inglese, nome, *varianti_inglesi(nome, inglese)]))
                      + ([] if not usa_modello else [traduzione_modello(nome)])):
        if not tentativo:
            continue
        base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/" + urllib.parse.quote(tentativo)
        try:
            dati = json.loads(_richiesta(base + "/property/MolecularFormula,MolecularWeight,IUPACName/JSON"))
            proprieta, inglese = dati["PropertyTable"]["Properties"][0], tentativo
            break
        except Exception:
            continue
    if proprieta is None:
        file_info.write_text("{}", encoding="utf-8")  # non trovata: non si richiede di nuovo
        return None
    cid = proprieta["CID"]
    sdf, tridimensionale = "", True
    for tipo in ("3d", "2d"):
        try:
            sdf = _richiesta(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/SDF?record_type={tipo}").decode()
            tridimensionale = tipo == "3d"
            break
        except Exception:
            continue
    if sdf and not tridimensionale:
        tre_d = forma_3d(sdf)
        if tre_d:
            sdf, tridimensionale = tre_d, True
    info = {"nome": nome, "inglese": inglese, "cid": cid, "formula": proprieta.get("MolecularFormula", ""),
            "peso": proprieta.get("MolecularWeight", ""), "iupac": proprieta.get("IUPACName", ""),
            "sdf": sdf, "tridimensionale": tridimensionale}
    file_info.write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    return info


def struttura_pdb(codice, scarica=True):
    """Struttura del Protein Data Bank: {codice, titolo, metodo, risoluzione, pdb} oppure None."""
    codice = codice.upper()
    file_info = cartella("strutture") / f"{codice}.json"
    if file_info.exists():
        return json.loads(file_info.read_text(encoding="utf-8")) or None
    if not scarica:
        return None
    try:
        voce = json.loads(_richiesta(f"https://data.rcsb.org/rest/v1/core/entry/{codice}"))
        testo = _richiesta(f"https://files.rcsb.org/download/{codice}.pdb", tempo=90).decode()
    except Exception:
        return None
    info = {"codice": codice, "titolo": voce["struct"]["title"],
            "metodo": ", ".join(e.get("method", "") for e in voce.get("exptl", [])),
            "risoluzione": (voce.get("rcsb_entry_info", {}).get("resolution_combined") or [None])[0],
            "atomi": voce.get("rcsb_entry_info", {}).get("deposited_atom_count"), "pdb": testo}
    file_info.write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    return info


METODI_PDB = {"X-RAY DIFFRACTION": "diffrazione di raggi X (cristallografia)",
              "ELECTRON MICROSCOPY": "microscopia elettronica (crio-EM)", "SOLUTION NMR": "risonanza magnetica nucleare (NMR) in soluzione",
              "SOLID-STATE NMR": "risonanza magnetica nucleare (NMR) allo stato solido", "NEUTRON DIFFRACTION": "diffrazione di neutroni",
              "FIBER DIFFRACTION": "diffrazione da fibre", "ELECTRON CRYSTALLOGRAPHY": "cristallografia elettronica"}


def metodo_italiano(metodo):
    return ", ".join(METODI_PDB.get(m.strip(), m.strip().lower()) for m in (metodo or "").split(",") if m.strip()) or "n.d."


def cerca(nome):
    """Cosa mostrare per un nome scritto dallo studente: ("pdb", info, descrizione) per le
    macromolecole, ("pubchem", info, None) per le molecole, oppure None."""
    n = senza_accenti(nome)
    if re.fullmatch(r"[0-9][a-z0-9]{3}", n):
        info = struttura_pdb(n)
        return ("pdb", info, info["titolo"].capitalize()) if info else None
    for chiave in sorted(STRUTTURE_PDB, key=len, reverse=True):
        if re.search(rf"(?<![a-z]){re.escape(chiave)}(?![a-z])", n):
            codice, descrizione = STRUTTURE_PDB[chiave]
            info = struttura_pdb(codice)
            return ("pdb", info, descrizione) if info else None
    if n in PAROLE_TROPPO_GENERICHE:
        return None
    info = molecola_pubchem(nome)
    return ("pubchem", info, None) if info else None


# Categorie delle molecole: la prima regola che corrisponde al nome decide (l'ordine conta:
# «nadololo» è un farmaco, non un nucleotide).
CATEGORIE_MOLECOLE = [
 ("Antibiotici", r"cillin|micin|mycin|floxacin|^cef|ciclin|cyclin|sulfa|^colistin|bacitracin|vancomicin|teicoplanin|acido clavulanico|acido nalidixico|quinolon|chinolon|metronidazol|tinidazol|nitazoxanid|isoniazid|rifamp|rifab|etambutol|pirazinamid|etionamid|clofazimin|dapson|cicloserin|mupirocin|monensin|acido fusidico|oxazolidinon|fosfomicin|linezolid|metenamin|optochin|amikacin|tigeciclin|clindamicin|cloramfenicol|trimetoprim|nitrofurant|penicillin|carbapenem|penem$|aztreonam|polimixin"),
 ("Antivirali", r"vir$|virina$|udina$|citabina$|vudina|amantadin|rimantadin|ribavirin|didanosin|zalcitabin|stavudin|enfuvirtid|tromantadin|aciclo|nevirapin|delavirdin|vidarabin|trifluridin|arildone|fosfonoformat|foscarnet|interferon"),
 ("Antifungini e antiparassitari", r"conazol|fungin|terbinafin|griseofulvin|amfotericin|nistatin|flucitosin|bendazol|pentamidin|melarsoprol|stibogluconat|naftifin|amorolfin|furazolidon|bitionol|diloxanid|suramin|chinin|chinacrin|quinacrin|artemis|artesunat|lumefantrin|atovaquon|miltefosin|niclosamid|praziquantel|ivermectin|benznidazol|nifurtimox|metrifonat|santonin|clotrimazol|miconazol|econazol|fumagillin|piperazin|tiabendazol|clorochin|meflochin|primachin|pirimetamin|clorochina"),
 ("Altri farmaci", r"aspirin|paracetamol|ibuprofen|morfin|codein|cocain|procain|lidocain|atorvastatin|statin$|prednison|cortison|omeprazol|cimetidin|ranitidin|propranolol|atenolol|labetalol|albuterol|salbutamol|cetirizin|fluoxetin|clozapin|talidomid|ciclosporin|meperidin|propossifen|dicumarol|warfarin|cromoglicat|amfetamin|captopril|enalapril|furosemid|digossin|metformin|diazepam|eparin|naprossen|ketoprofen|diclofenac|meglumin|acido folinico|nitroglicerin|levodop|loratadin|fenitoin|valproat|ololo$|lolo$|tioguanin|mercaptopurin|doxorubicin|allopurinol|famotidin|bupropion|meclizin|aloperidol|caina$|desametason|azatioprin|misoprostol|fluticason|paroxetin|meprobamat|difenidramin|nifedipin|fensuccimmid|flutamid|venlafaxin|nabumeton|toremifen|ibutilid|bumetanid|fenflurammin|bidisomid|acetanilid|unoproston|nonoxinol|gabapentin|pregabalin"),
 ("Tossine e veleni", r"citreoviridin|deossinivalenol|ciclopiazon|cereulid|aflatossin|tetrodotossin|ocratossin|patulin|stricnin|amanitin|muscarin|saxitossin"),
 ("Amminoacidi e peptidi", r"^(?:[dl]-)?(?:glicina|alanina|valina|leucina|isoleucina|serina|treonina|cisteina|cistina|metionina|acido aspartico|asparagina|acido glutammico|glutammina|lisina|arginina|istidina|fenilalanina|tirosina|triptofano|prolina|selenocisteina|ornitina|citrullina|omocisteina|taurina|glutatione|pentaglicina|aspartato|glutammato|carnitina|creatina|creatinina)$|acido diaminopimelico|acido meso-diaminopimelico|acido muramico"),
 ("Zuccheri e carboidrati", r"osio$|(?<!nitr)osammina|itolo$|acido glucuronico|acido l-iduronico|acido gluconico|gluconato|gliceraldeide|diidrossiacetone|inositolo|udp-glucosio|amido|glicogeno|cellulosa|chitina|eparina|acido ialuronico|alginato|salicina|acido sialico|pentosio"),
 ("Lipidi, steroidi e ormoni steroidei", r"^acido (?:palmitico|stearico|oleico|linoleico|a-linolenico|arachidonico|miristico|laurico|butanoico|fosfatidico|mevalonico)|sterol|^colesterol|testosteron|progesteron|estron|estradiol|cortisol|aldosteron|squalen|caroten|retinol|lanosterol|prostaglandin|trigliceridi|tripalmitin|fosfatidil|sfingo|ceramid|lecitina|isopren|mevalonat|farnesol|geraniol|bactoprenol|undecaprenol|glicerofosfat|limonen|terpen|calcitriol|androsteron|stanozolol|metandrostenolon|linoleat|acido (?:dodecanoico|decanoico|prostanoico)"),
 ("Nucleotidi e acidi nucleici", r"adenosin|guanosin|citidin|timidin|uridin|inosin|uracil|adenin|guanin|citosin|timina|acido deossiribonucleico|acido ribonucleico|^atp$|^adp$|^amp$|ampc|gmpc|^nadp?h?$|^fadh?2?$|adp-ribosio|pirofosfat"),
 ("Vitamine e coenzimi", r"biotin|riboflavin|tiamin|nicotinammid|acido nicotinico|niacin|cobalamin|acido ascorbico|acido folico|folat|tetraidrofol|diidrofolat|diidropteroat|piridossal|piridossin|tocoferol|calciferol|fillochinon|menachinon|coenzima|acido pantotenico|ubichinon|lipoic|menadion|tocotrienol|ascorbat"),
 ("Ormoni e neurotrasmettitori", r"istamina|serotonin|dopamin|adrenalin|noradrenalin|acetilcolin|vasopressin|ossitocin|insulin|glucagon|tiroxin|melatonin|^gaba$|acido gamma|acido 4-amminobutanoico|endorfin|angiotensin|bradichinin|ossido nitrico"),
 ("Metabolismo (intermedi)", r"piruvat|acido piruvico|lattat|acido lattico|citrat|acido citrico|isocitrat|succinat|acido succinico|fumarat|acido fumarico|malat|ossalacetat|chetoglutarat|acetoacetat|acido acetoacetico|idrossibutan|acetil-coa|urea$|ammoniaca|bilirubin|biliverdin|ossaloacetat|fosfoenol|glicerolo|^glicerol|creatin|acido urico|acetato$|malonat|carbammat|acido carbammico|betaina|cadaverina|putrescin|etanolamin|acido mandelico|glicerat|fosfoglicerat|spermin|malondialdeid"),
]
def categoria_molecola(nome, formula):
    """La categoria di una molecola per dividerle nella scheda Modelli 3D (dal nome e dalla formula)."""
    n = nome.casefold()
    for cat, regola in CATEGORIE_MOLECOLE:
        if re.search(regola, n):
            return cat
    if "C" not in re.sub(r"Cl|Ca|Cu|Co|Cr|Cs|Cd", "", formula or ""):
        return "Composti inorganici e ioni"
    if re.search(r"(?:di|d') (?:sodio|potassio|calcio|bario|ammonio|alluminio|zinco|rame|magnesio)$|^(?:carbonato|bicarbonato|acido carbonico|cianuro)", n):
        return "Composti inorganici e ioni"
    return "Chimica organica di base"


def html_visualizzatore(modello, formato, stile="bastoncini", altezza=460, ruota=False):
    """Pagina HTML con il modello 3D (3Dmol.js): si ruota con il mouse e si ingrandisce con la rotella."""
    stili = {
        # Colori Jmol: gli stessi della legenda (COLORI_ATOMI), così ogni colore corrisponde al suo atomo.
        "bastoncini": "{stick: {radius: 0.15, colorscheme: 'Jmol'}, sphere: {scale: 0.25, colorscheme: 'Jmol'}}",
        "sfere": "{sphere: {colorscheme: 'Jmol'}}",
        "linee": "{line: {colorscheme: 'Jmol'}}",
        "nastri": "{cartoon: {color: 'spectrum'}}",
    }
    superficie = stile == "superficie"
    if stile == "nastri" and formato != "pdb":
        stile = "bastoncini"  # i nastri esistono solo per le catene di proteine e acidi nucleici
    stile_js = stili.get(stile, stili["nastri"] if formato == "pdb" else stili["bastoncini"])
    if superficie:
        stile_js = stili["nastri"] if formato == "pdb" else stili["bastoncini"]
    return f"""<div id="v" style="width:100%;height:{altezza}px;position:relative;border-radius:10px;
background:#0f1218"></div>
<script src="{LIBRERIA_3D}"></script>
<script>
const v = $3Dmol.createViewer("v", {{backgroundColor: "#0f1218"}});
v.addModel({json.dumps(modello)}, "{formato}");
v.setStyle({{}}, {stile_js});
{"v.addSurface($3Dmol.SurfaceType.VDW, {opacity: 0.85, colorscheme: 'whiteCarbon'});" if superficie else ""}
v.zoomTo(); v.render();
{"v.spin('y', 0.6);" if ruota else ""}
</script>"""


def _nomi_riconoscibili():
    """Nomi da riconoscere nel testo di una risposta: le molecole dei libri e delle schede (già scaricate)
    e le macromolecole dell'elenco PDB. Si rilegge l'elenco solo quando cambia."""
    elenchi = [e for e in (CARTELLA / "molecole_libri.json", CARTELLA / "molecole_schede.json") if e.exists()]
    data = tuple(e.stat().st_mtime_ns for e in elenchi)
    if _CACHE_NOMI.get("data") != data:
        nomi = {}
        for elenco in elenchi:
            for m in json.loads(elenco.read_text(encoding="utf-8")):
                if len(m["nome"]) >= 5 and m["nome"] not in PAROLE_TROPPO_GENERICHE:
                    nomi[senza_accenti(m["nome"])] = m["nome"]
        for nome in NOMI_ITALIANI:
            if nome not in ("acqua", "ossigeno", "idrogeno", "azoto", "amp", "eme"):
                nomi[senza_accenti(nome)] = nome
        for nome in STRUTTURE_PDB:
            if len(nome) >= 4 and nome not in ("hiv", "spike", "dna"):
                nomi[senza_accenti(nome)] = nome
        nomi["dna"] = "dna"
        modello = re.compile(r"(?<![a-z0-9-])(" + "|".join(
            re.escape(n) for n in sorted(nomi, key=len, reverse=True)) + r")(?![a-z0-9-])") if nomi else None
        _CACHE_NOMI.update(data=data, nomi=nomi, modello=modello)
    return _CACHE_NOMI["nomi"], _CACHE_NOMI["modello"]


_CACHE_NOMI = {}


def molecole_nel_testo(testo, massimo=6):
    """Le molecole nominate in un testo (risposta o domanda), nell'ordine in cui compaiono."""
    nomi, modello = _nomi_riconoscibili()
    if not modello:
        return []
    trovate = []
    for m in modello.finditer(senza_accenti(testo)):
        nome = nomi[m.group(1)]
        if nome not in trovate:
            trovate.append(nome)
        if len(trovate) >= massimo:
            break
    return trovate


# Organi in 3D (atlante BodyParts3D, © DBCLS, CC BY-SA 2.1 Japan): nomi e aggettivi con cui
# un testo medico li nomina («tubercolosi polmonare» → polmoni).
LIBRERIA_ORGANI = "https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js"
NOMI_ORGANI = {
    "cuore": "cuore, cardiaco, cardiaca, cardiache, cardiaci, miocardio", "aorta": "aorta, aortico, aortica",
    "valvola mitrale": "valvola mitrale", "valvola aortica": "valvola aortica",
    "polmoni": "polmone, polmoni, polmonare, polmonari", "trachea": "trachea, tracheale",
    "diaframma": "diaframma", "esofago": "esofago, esofageo, esofagea", "stomaco": "stomaco, gastrico, gastrica",
    "duodeno": "duodeno, duodenale", "intestino tenue": "intestino tenue, ileo, digiuno",
    "intestino crasso": "intestino crasso, colon", "appendice": "appendice", "retto": "retto, rettale",
    "fegato": "fegato, epatico, epatica, epatiche, epatici", "colecisti": "colecisti, cistifellea",
    "pancreas": "pancreas, pancreatico, pancreatica", "lingua": "lingua",
    "reni": "rene, reni, renale, renali", "vescica": "vescica urinaria, vescica", "prostata": "prostata, prostatico",
    "cervello": "cervello, cerebrale, encefalo", "cervelletto": "cervelletto, cerebellare",
    "tronco encefalico": "tronco encefalico", "midollo spinale": "midollo spinale",
    "ipotalamo": "ipotalamo", "ipofisi": "ipofisi, ipofisario", "surrene": "surrene, surrenale, surrenali",
    "timo": "timo", "occhio": "occhio, occhi, oculare, retina", "scheletro": "scheletro",
    "cranio": "cranio, cranico", "mandibola": "mandibola", "colonna vertebrale": "colonna vertebrale, vertebre",
    "gabbia toracica": "gabbia toracica, costole", "sterno": "sterno", "bacino": "bacino",
    "femore": "femore", "omero": "omero", "pelle": "pelle, cute, cutaneo, cutanea, cutanee",
}


def elenco_organi():
    indice = CARTELLA / "organi" / "organi.json"
    return json.loads(indice.read_text(encoding="utf-8")) if indice.exists() else []


def organi_nel_testo(testo, massimo=3):
    """Gli organi nominati in un testo (anche con l'aggettivo), nell'ordine in cui compaiono."""
    disponibili = {o["nome"] for o in elenco_organi()}
    if not disponibili:
        return []
    forme = {f: organo for organo, parole in NOMI_ORGANI.items() if organo in disponibili
             for f in ([organo] + [p.strip() for p in parole.split(",")])}
    modello = re.compile(r"(?<![a-z])(" + "|".join(re.escape(f) for f in sorted(forme, key=len, reverse=True))
                         + r")(?![a-z])")
    trovati = []
    for m in modello.finditer(senza_accenti(testo)):
        organo = forme[m.group(1)]
        if organo not in trovati:
            trovati.append(organo)
        if len(trovati) >= massimo:
            break
    return trovati


def schede_parti():
    """Le schede delle parti degli organi: {nome inglese dell'atlante: {"it": {...}, "en": {...}}}."""
    file = CARTELLA / "organi" / "schede_parti.json"
    data = file.stat().st_mtime_ns if file.exists() else 0
    if _CACHE_SCHEDE.get("data") != data:
        _CACHE_SCHEDE.update(data=data, schede=json.loads(file.read_text(encoding="utf-8")) if data else {})
    return _CACHE_SCHEDE["schede"]


_CACHE_SCHEDE = {}

TESTI_SCHEDA = {
    "it": {"aiuto": "👆 Tocca una parte dell'organo: vedi come si chiama, cosa fa, come è vascolarizzata e innervata.",
           "cosa": "Cos'è e cosa succede qui", "vasi": "Vascolarizzazione", "nervi": "Innervazione",
           "clinica": "In clinica", "manca": "Scheda non ancora disponibile per questa parte.",
           "elenco": "Oppure scegli una parte dall'elenco", "scegli": "— scegli —",
           "nascondi": "🙈 Nascondi la parte scelta (per vedere sotto)", "mostra": "👁️ Rimetti tutte le parti",
           "fronte": "↺ Vista iniziale", "spaccato": "L'organo è tagliato a metà, come in un atlante: si vedono gli strati e le parti interne."},
    "en": {"aiuto": "👆 Tap a part of the organ: see its name, what it does, its blood supply and innervation.",
           "cosa": "What it is and what happens here", "vasi": "Blood supply", "nervi": "Innervation",
           "clinica": "Clinical note", "manca": "No card available yet for this part.",
           "elenco": "Or choose a part from the list", "scegli": "— choose —",
           "nascondi": "🙈 Hide the chosen part (to see underneath)", "mostra": "👁️ Show all parts again",
           "fronte": "↺ Starting view", "spaccato": "The organ is cut in half, as in an atlas: you can see its layers and inner parts."},
}


def html_organo(nome, altezza=460, ruota=True, lingua="it", interno=False):
    """Pagina HTML con l'organo in 3D (model-viewer): si ruota con il mouse, si ingrandisce con la
    rotella e, toccando una parte, la parte si illumina e sotto compare la sua scheda. Con
    `interno` l'organo è tagliato a metà, come in un atlante, e si vede com'è fatto dentro."""
    import base64
    import html as html_lib
    voce = next((o for o in elenco_organi() if o["nome"] == nome), None)
    if not voce:
        return ""
    lingua = "en" if lingua == "en" else "it"
    interno = interno and bool(voce.get("interno"))
    dati = base64.b64encode((CARTELLA / "organi" / voce["interno" if interno else "file"]).read_bytes()).decode()
    tutte = schede_parti()
    schede = {p: tutte[p][lingua] for p in voce.get("nomi_parti", []) if p in tutte and lingua in tutte[p]}
    testi = TESTI_SCHEDA[lingua]
    opzioni = "".join(f'<option value="{html_lib.escape(p)}">{html_lib.escape(schede.get(p, {}).get("nome", p))}</option>'
                      for p in sorted(voce.get("nomi_parti", []), key=lambda p: schede.get(p, {}).get("nome", p)))
    elenco = (f'<label style="font-size:13px;opacity:.8">{testi["elenco"]}: <select id="parte" style="max-width:100%;'
              f'background:#161b24;color:#e8e8e8;border:1px solid #2B3240;border-radius:6px;padding:3px">'
              f'<option value="">{testi["scegli"]}</option>{opzioni}</select></label>') if len(voce.get("nomi_parti", [])) > 1 else ""
    # Intero: di fronte, appena dall'alto. Tagliato: dal lato del taglio.
    vista = voce["vista_interno"] if interno else "0deg 80deg auto"
    bottone = ("background:#161b24;color:#e8e8e8;border:1px solid #2B3240;border-radius:6px;padding:4px 10px;"
               "margin:6px 6px 0 0;font-size:13px;cursor:pointer")
    return f"""<script type="module" src="{LIBRERIA_ORGANI}"></script>
<div style="font-family:-apple-system,Segoe UI,sans-serif;color:#e8e8e8">
<model-viewer id="mv" src="data:model/gltf-binary;base64,{dati}" camera-controls {"auto-rotate" if ruota else ""}
  camera-orbit="{vista}" environment-image="neutral" shadow-intensity="0.6" exposure="1.0"
  interaction-prompt="none" min-camera-orbit="auto auto 5%"
  style="width:100%;height:{altezza}px;background:radial-gradient(circle,#1d2330,#0f1218);border-radius:10px;cursor:pointer"></model-viewer>
<div><button id="nascondi" style="{bottone}" disabled>{testi["nascondi"]}</button><button id="mostra" style="{bottone}">{testi["mostra"]}</button><button id="fronte" style="{bottone}">{testi["fronte"]}</button></div>
{f'<div style="font-size:13px;margin:6px 0;opacity:.85">✂️ {testi["spaccato"]}</div>' if interno else ""}
<div style="font-size:13px;margin:6px 0;opacity:.85">{testi["aiuto"]}</div>
{elenco}
<div id="scheda" style="display:none;background:#161b24;border:1px solid #2B3240;border-radius:10px;padding:10px 14px;margin-top:8px;font-size:14px;line-height:1.45"></div>
</div>
<script type="module">
const schede = {json.dumps(schede, ensure_ascii=False)};
const testi = {json.dumps(testi, ensure_ascii=False)};
const mv = document.getElementById("mv"), box = document.getElementById("scheda"), elenco = document.getElementById("parte");
const nascondi = document.getElementById("nascondi");
let scelto = null;
const nascoste = new Set();
const originali = new Map();  // colore e modo di trasparenza di ogni parte, come nel modello
mv.addEventListener("load", () => {{
  for (const m of mv.model.materials)
    originali.set(m, [m.pbrMetallicRoughness.baseColorFactor.slice(), m.getAlphaMode()]);
}});
// Colora tutte le parti: quella scelta in giallo; quelle nascoste diventano invisibili, così si
// vede che cosa c'è sotto (le valvole dentro il cuore, i lobi sotto la superficie del cervello).
function colora() {{
  for (const [m, [colore, modo]] of originali) {{
    const pbr = m.pbrMetallicRoughness;
    if (nascoste.has(m)) {{ m.setAlphaMode("BLEND"); pbr.setBaseColorFactor([colore[0], colore[1], colore[2], 0]); }}
    else if (m === scelto) {{ m.setAlphaMode(modo); pbr.setBaseColorFactor([1.0, 0.82, 0.15, colore[3]]); }}
    else {{ m.setAlphaMode(modo); pbr.setBaseColorFactor(colore); }}
  }}
  nascondi.disabled = !scelto;
}}
function riga(titolo, testo) {{
  if (!testo) return;
  const p = document.createElement("p"); p.style.margin = "6px 0";
  const b = document.createElement("b"); b.textContent = titolo + ": "; b.style.color = "#E3A857";
  p.appendChild(b); p.appendChild(document.createTextNode(testo)); box.appendChild(p);
}}
function mostra(materiale) {{
  scelto = materiale; colora();
  mv.autoRotate = false;
  const s = schede[materiale.name];
  box.innerHTML = ""; box.style.display = "block";
  const h = document.createElement("div"); h.style.cssText = "font-size:16px;font-weight:600;margin-bottom:4px";
  h.textContent = s ? s.nome : materiale.name; box.appendChild(h);
  if (!s) {{ riga("", testi.manca); return; }}
  riga(testi.cosa, s.cosa); riga(testi.vasi, s.vasi); riga(testi.nervi, s.nervi); riga(testi.clinica, s.clinica);
  if (elenco) elenco.value = materiale.name;
}}
let inizio = null;  // dove è cominciato il trascinamento: girare il modello non è un tocco
mv.addEventListener("pointerdown", ev => {{ inizio = [ev.clientX, ev.clientY]; }});
mv.addEventListener("click", ev => {{
  if (inizio && Math.hypot(ev.clientX - inizio[0], ev.clientY - inizio[1]) > 6) return;
  const m = mv.materialFromPoint(ev.clientX, ev.clientY);
  if (m && !nascoste.has(m)) mostra(m);
}});
if (elenco) elenco.addEventListener("change", () => {{
  const m = mv.model && mv.model.materials.find(x => x.name === elenco.value);
  if (m) mostra(m);
}});
nascondi.onclick = () => {{ if (scelto) {{ nascoste.add(scelto); scelto = null; box.style.display = "none"; colora(); }} }};
document.getElementById("mostra").onclick = () => {{ nascoste.clear(); colora(); }};
document.getElementById("fronte").onclick = () => {{ mv.cameraOrbit = "{vista}"; mv.cameraTarget = "auto auto auto"; mv.fieldOfView = "auto"; }};
</script>"""


# Malattie → la molecola o il microrganismo che le caratterizza (codici PDB controllati sul titolo).
MALATTIE_PDB = [
    (r"anemia falciforme|drepanocitosi", "2HBS", "Emoglobina S (deossi), la forma che si polimerizza nell'anemia falciforme"),
    (r"alzheimer", "2BEG", "Fibrille di β-amiloide (Aβ 1-42), che formano le placche dell'Alzheimer"),
    (r"parkinson", "6A6B", "Fibra di α-sinucleina, che forma i corpi di Lewy del Parkinson"),
    (r"ebola", "5JQ3", "Glicoproteina di superficie del virus Ebola"),
    (r"epatite b\b|hbv", "1QGT", "Capside del virus dell'epatite B (HBcAg)"),
    (r"poliomielite|poliovirus", "1HXS", "Poliovirus (ceppo Mahoney), capside intero"),
    (r"papillomavirus|\bhpv\b|condilom|collo dell.utero", "1DZL", "Proteina L1 del capside del papillomavirus 16"),
    (r"raffreddore|rhinovirus", "4RHV", "Rhinovirus umano 14, la causa più comune del raffreddore"),
    (r"covid|sars-cov-2|coronavirus", "6M0J", "Dominio della spike del SARS-CoV-2 legato al recettore ACE2"),
    (r"\baids\b|\bhiv\b", "3H4E", "Capside (proteina CA) dell'HIV-1"),
    (r"influenza", "1RU7", "Emoagglutinina H1 del virus influenzale"),
    (r"botulism", "3BTA", "Neurotossina botulinica di tipo A"),
    (r"colera", "1XTC", "Tossina colerica"),
    (r"difterite", "1DDT", "Tossina difterica"),
    (r"tetano", "1A8D", "Tossina tetanica (frammento C)"),
    (r"fibrosi cistica", "5UAK", "Canale CFTR, difettoso nella fibrosi cistica"),
    (r"diabete", "4INS", "Insulina"),
    (r"mrsa|meticillino-resistente|resistente alla meticillina", "1VQQ", "PBP2a, la proteina che rende MRSA resistente"),
]


def strutture_malattia(testo, massimo=2):
    """Le strutture 3D legate alle malattie nominate in un testo: [(codice, descrizione)]."""
    n = senza_accenti(testo)
    trovate = []
    for modello, codice, descrizione in MALATTIE_PDB:
        if re.search(modello, n) and codice not in [c for c, _ in trovate]:
            trovate.append((codice, descrizione))
        if len(trovate) >= massimo:
            break
    return trovate


# --- Formula di struttura (2D), descrizione e legenda dei colori -----------------------------
# Colori degli atomi nel modello 3D (schema CPK/Jmol di 3Dmol.js) e nome in italiano.
COLORI_ATOMI = {
    "H": ("#FFFFFF", "idrogeno", "bianco"), "C": ("#909090", "carbonio", "grigio"),
    "N": ("#3050F8", "azoto", "blu"), "O": ("#FF0D0D", "ossigeno", "rosso"),
    "S": ("#FFFF30", "zolfo", "giallo"), "P": ("#FF8000", "fosforo", "arancione"),
    "F": ("#90E050", "fluoro", "verde chiaro"), "Cl": ("#1FF01F", "cloro", "verde"),
    "Br": ("#A62929", "bromo", "rosso scuro"), "I": ("#940094", "iodio", "viola"),
    "Na": ("#AB5CF2", "sodio", "viola chiaro"), "K": ("#8F40D4", "potassio", "viola"),
    "Ca": ("#3DFF00", "calcio", "verde brillante"), "Mg": ("#8AFF00", "magnesio", "verde giallo"),
    "Fe": ("#E06633", "ferro", "arancione scuro"), "Zn": ("#7D80B0", "zinco", "grigio-blu"),
    "Cu": ("#C88033", "rame", "marrone"), "Co": ("#F090A0", "cobalto", "rosa"),
    "B": ("#FFB5B5", "boro", "rosa chiaro"), "Si": ("#F0C8A0", "silicio", "beige"),
    "As": ("#BD80E3", "arsenico", "lilla"), "Hg": ("#B8B8D0", "mercurio", "grigio chiaro"),
    "Ag": ("#C0C0C0", "argento", "argento"), "Sb": ("#9E63B5", "antimonio", "viola"),
    "Mn": ("#9C7AC7", "manganese", "lilla"), "Ga": ("#C28F8F", "gallio", "rosa scuro"),
}


def legenda_atomi(formula):
    """Gli elementi della formula con il colore che hanno nel modello 3D: [(simbolo, colore, nome, colore a parole)]."""
    simboli = list(dict.fromkeys(re.findall(r"[A-Z][a-z]?", formula or "")))
    if "C" in simboli and "H" not in simboli:
        pass
    return [(s, *COLORI_ATOMI[s]) for s in simboli if s in COLORI_ATOMI]


def _pedice(n):
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(c)] for c in str(n))


def molecola_pesante(sdf):
    """La molecola RDKit senza idrogeni espliciti (None se non si legge): la stessa per il disegno
    e per il confronto tra reagenti e prodotti, così gli indici degli atomi coincidono."""
    try:
        from rdkit import Chem
    except ImportError:
        return None
    molecola = Chem.MolFromMolBlock(sdf, removeHs=False, sanitize=True) if sdf else None
    return Chem.RemoveHs(molecola) if molecola is not None else None


def formula_struttura_svg(sdf, larghezza=440, altezza=330, evidenzia=(), colore=(1.0, 0.62, 0.2)):
    """La formula di struttura disegnata in piano: ogni carbonio con i suoi idrogeni (CH₃, CH₂, CH),
    i doppi e tripli legami come linee doppie e triple, gli eteroatomi con gli idrogeni (OH, NH₂).
    Gli atomi di `evidenzia` (indici della molecola senza idrogeni) hanno un alone colorato."""
    try:
        from rdkit.Chem import AllChem
        from rdkit.Chem.Draw import rdMolDraw2D
    except ImportError:
        return ""
    molecola = molecola_pesante(sdf)
    if molecola is None:
        return ""
    AllChem.Compute2DCoords(molecola)
    piccola = molecola.GetNumHeavyAtoms() <= 24
    if piccola:
        # Nelle molecole piccole si scrive ogni carbonio (CH₃, CH₂...): si vede come è fatta davvero.
        for atomo in molecola.GetAtoms():
            if atomo.GetSymbol() == "C":
                idrogeni = atomo.GetTotalNumHs()
                atomo.SetProp("atomLabel", "C" + ("H" + (f"<sub>{idrogeni}</sub>" if idrogeni > 1 else "") if idrogeni else ""))
    disegno = rdMolDraw2D.MolDraw2DSVG(larghezza, altezza)
    opzioni = disegno.drawOptions()
    opzioni.addStereoAnnotation = False
    opzioni.bondLineWidth = 2
    opzioni.minFontSize = 11 if piccola else 9
    opzioni.setBackgroundColour((1, 1, 1, 1))
    evidenzia = [i for i in evidenzia if i < molecola.GetNumAtoms()]
    legami = [l.GetIdx() for l in molecola.GetBonds()
              if l.GetBeginAtomIdx() in evidenzia and l.GetEndAtomIdx() in evidenzia]
    rdMolDraw2D.PrepareAndDrawMolecule(disegno, molecola, highlightAtoms=evidenzia, highlightBonds=legami,
                                       highlightAtomColors={i: colore for i in evidenzia},
                                       highlightBondColors={i: colore for i in legami})
    disegno.FinishDrawing()
    return disegno.GetDrawingText()


# --- Reazioni chimiche: i passaggi con gli atomi che cambiano --------------------------

def reazioni():
    file = CARTELLA / "reazioni.json"
    return json.loads(file.read_text(encoding="utf-8")) if file.exists() else []


def atomi_che_cambiano(molecola, altre):
    """Gli atomi di `molecola` che non si ritrovano nella parte comune più grande con nessuna
    delle `altre` (dall'altra parte della freccia): sono quelli che la reazione aggiunge o toglie.
    Le molecole minuscole (acqua, CO₂, O₂) e quelle che non cambiano non si evidenziano."""
    try:
        from rdkit.Chem import rdFMCS
    except ImportError:
        return []
    if molecola is None or molecola.GetNumAtoms() <= 3:
        return []
    migliore = set()
    for altra in altre:
        if altra is None or altra.GetNumAtoms() <= 3:
            continue
        comune = rdFMCS.FindMCS([molecola, altra], timeout=2, ringMatchesRingOnly=True,
                                completeRingsOnly=False, atomCompare=rdFMCS.AtomCompare.CompareElements,
                                bondCompare=rdFMCS.BondCompare.CompareOrder)
        if not comune.numAtoms:
            continue
        from rdkit import Chem
        schema = Chem.MolFromSmarts(comune.smartsString)
        corrispondenza = molecola.GetSubstructMatch(schema) if schema is not None else ()
        if len(corrispondenza) > len(migliore):
            migliore = set(corrispondenza)
    # Senza nessuna parte in comune (o quasi) la molecola è tutta nuova: niente alone su tutto.
    if len(migliore) < 0.3 * molecola.GetNumAtoms():
        return []
    return [i for i in range(molecola.GetNumAtoms()) if i not in migliore]


TESTI_REAZIONE = {
    "it": {"passaggio": "Passaggio", "di": "di", "indietro": "◀ Indietro", "avanti": "Avanti ▶",
           "tutti": "▶ Guarda tutti i passaggi", "ferma": "⏸ Ferma", "enzima": "Enzima",
           "legenda": "In rosso gli atomi che si staccano o cambiano, in arancione quelli nuovi.",
           "palco": "🎬 Le molecole in 3D che reagiscono", "pausa": "⏸ Pausa", "riprendi": "▶ Riprendi",
           "ricomincia": "🔁 Ricomincia", "vera": "Forma vera (3D)", "piana": "Struttura lineare (piana)",
           "scritte": "🔤 Scritte CH₃ CH₂ OH",
           "gira": "🔄 Fai girare", "avvia": "▶ Avvia la reazione", "inizio": "molecole di partenza", "fine": "prodotti",
           "reazione": "reazione",
           "colori": "Colori degli atomi:<i style='background:#909090'></i>carbonio (C)<i style='background:#fff'></i>"
                     "idrogeno (H)<i style='background:#ff0d0d'></i>ossigeno (O)<i style='background:#3050f8'></i>azoto (N)"
                     "<i style='background:#ff8000'></i>fosforo (P)<i style='background:#ffff30'></i>zolfo (S). "
                     "Le scritte come CH₃ (un carbonio con tre idrogeni) o OH (ossigeno con un idrogeno) dicono "
                     "il gruppo di atomi: puoi toglierle con il pulsante «Scritte».",
           "aiuto": "A sinistra le molecole di partenza, al centro l'enzima, a destra quello che si forma. "
                    "La scena è ferma sul piano: per girarla usa «Fai girare» oppure trascinala con il mouse "
                    "(rotella per ingrandire). Con «Pausa» o con la barra sotto la scena scegli il momento "
                    "della reazione da guardare.",
           "mancano": "Senza modello 3D: "},
    "en": {"passaggio": "Step", "di": "of", "indietro": "◀ Back", "avanti": "Next ▶",
           "tutti": "▶ Play all steps", "ferma": "⏸ Pause", "enzima": "Enzyme",
           "legenda": "Atoms that leave or change are in red, new ones in orange.",
           "palco": "🎬 The reacting molecules in 3D", "pausa": "⏸ Pause", "riprendi": "▶ Resume",
           "ricomincia": "🔁 Restart", "vera": "True shape (3D)", "piana": "Linear structure (flat)",
           "scritte": "🔤 CH₃ CH₂ OH labels",
           "gira": "🔄 Rotate", "avvia": "▶ Start the reaction", "inizio": "starting molecules", "fine": "products",
           "reazione": "reaction",
           "colori": "Atom colours:<i style='background:#909090'></i>carbon (C)<i style='background:#fff'></i>"
                     "hydrogen (H)<i style='background:#ff0d0d'></i>oxygen (O)<i style='background:#3050f8'></i>nitrogen (N)"
                     "<i style='background:#ff8000'></i>phosphorus (P)<i style='background:#ffff30'></i>sulfur (S). "
                     "Labels like CH₃ (a carbon with three hydrogens) or OH (oxygen with one hydrogen) name the "
                     "group of atoms: turn them off with the «Labels» button.",
           "aiuto": "Starting molecules on the left, the enzyme in the middle, what forms on the right. "
                    "The scene stays flat: to turn it use «Rotate» or drag it with the mouse (scroll to "
                    "zoom). With «Pause» or the bar under the scene pick the moment of the reaction.",
           "mancano": "No 3D model: "},
}


def _carte_molecole(voci, altre, colore, lingua):
    """Le formule di struttura di un lato del passaggio, con gli atomi che cambiano evidenziati."""
    import base64
    import html as html_lib
    pezzi = []
    for k, (m, info, rd) in enumerate(voci):
        nome = html_lib.escape(m.get(lingua) or m["it"])
        quante = f'<span class="n">{m["n"]}</span>' if m.get("n", 1) > 1 else ""
        if rd is not None and rd.GetNumAtoms() > 1:
            svg = formula_struttura_svg(info["sdf"], 230, 170, atomi_che_cambiano(rd, altre), colore)
            figura = (f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}">'
                      if svg else f'<div class="testo">{nome}</div>')
        else:
            formula = (html_lib.escape(re.sub(r"\d+", lambda c: _pedice(int(c.group())), info["formula"]))
                       if info else nome)
            figura = f'<div class="testo">{formula}</div>'
        if k:
            pezzi.append('<div class="piu">+</div>')
        pezzi.append(f'<div class="carta">{quante}{figura}<div class="nome">{nome}</div></div>')
    return "".join(pezzi)


def html_reazione(reazione, lingua="it"):
    """La reazione passaggio per passaggio: per ogni passaggio le molecole prima e dopo (formule di
    struttura con gli atomi che cambiano colorati), l'enzima che lo compie e che cosa succede.
    Si va avanti e indietro con i pulsanti o si guardano tutti i passaggi di seguito."""
    import html as html_lib
    testi = TESTI_REAZIONE.get(lingua, TESTI_REAZIONE["it"])
    molecole = {}

    def voce(m):
        if m.get("pubchem") and m["pubchem"] not in molecole:
            info = molecola_pubchem(m["pubchem"], usa_modello=False)
            molecole[m["pubchem"]] = (info, molecola_pesante(info["sdf"]) if info and info.get("sdf") else None)
        info, rd = molecole.get(m.get("pubchem"), (None, None))
        return m, info, rd

    passaggi = reazione.get("passaggi") or [{"titolo": reazione["nome"], "testo": reazione["cosa_succede"],
                                             "da": reazione["reagenti"], "a": reazione["prodotti"],
                                             "enzima": reazione.get("enzima")}]
    schede = []
    for n, p in enumerate(passaggi):
        prima, dopo = [voce(m) for m in p.get("da", [])], [voce(m) for m in p.get("a", [])]
        enzima = html_lib.escape((p.get("enzima") or {}).get(lingua, ""))
        parti = []
        if prima:
            parti.append(f'<div class="lato prima">{_carte_molecole(prima, [r for _, _, r in dopo], (0.95, 0.35, 0.35), lingua)}</div>')
        if dopo:
            parti.append(f'<div class="freccia"><div class="f">→</div>'
                         + (f'<div class="e">{testi["enzima"]}: {enzima}</div>' if enzima else "") + "</div>")
            parti.append(f'<div class="lato dopo">{_carte_molecole(dopo, [r for _, _, r in prima], (1.0, 0.62, 0.2), lingua)}</div>')
        elif enzima:
            parti.append(f'<div class="freccia"><div class="e">{testi["enzima"]}: {enzima}</div></div>')
        titolo = html_lib.escape(p["titolo"][lingua])
        testo = html_lib.escape(p["testo"][lingua])
        schede.append(f'<section class="passo" data-n="{n}"><div class="intestazione">{testi["passaggio"]} '
                      f'{n + 1} {testi["di"]} {len(passaggi)} · <b>{titolo}</b></div>'
                      f'<div class="schema">{"".join(parti)}</div><p class="spiega">{testo}</p></section>')
    # La scena 3D: per ogni passaggio le molecole prima e dopo, con la forma vera e quella piana
    # (una volta sola ciascuna; le molecole troppo grandi non si animano).
    modelli, scene = {}, []
    for p in passaggi:
        scena = {"da": [], "a": [], "senza": [],
                 "enzima": (p.get("enzima") or {}).get(lingua, "")}
        for lato in ("da", "a"):
            for m in p.get(lato, []):
                _, info, _ = voce(m)
                nome = m.get(lingua) or m["it"]
                if not info or not info.get("sdf") or info["sdf"].count("\n") > 700:
                    scena["senza"].append(nome)
                    continue
                if m["pubchem"] not in modelli:
                    modelli[m["pubchem"]] = {"vera": info["sdf"], "piana": forma_piana(info["sdf"]) or info["sdf"]}
                scena[lato].append({"k": m["pubchem"], "nome": nome, "n": m.get("n", 1)})
        scene.append(scena)
    dati_3d = json.dumps({"modelli": modelli, "scene": scene}, ensure_ascii=False).replace("</", "<\\/")
    puntini = "".join(f'<button class="punto" data-n="{n}" title="{html_lib.escape(p["titolo"][lingua])}">{n + 1}</button>'
                      for n, p in enumerate(passaggi))
    return f"""<style>
body{{margin:0;font-family:-apple-system,system-ui,sans-serif;color:#e8ecf3}}
.comandi{{display:flex;gap:8px;align-items:center;margin:4px 2px 10px;flex-wrap:wrap}}
button{{background:#2b6cff;color:#fff;border:0;border-radius:8px;padding:8px 14px;font-size:15px;cursor:pointer}}
button:disabled{{opacity:.35;cursor:default}}
.punti{{display:flex;gap:4px;flex-wrap:wrap;margin:0 2px 10px}}
.punto{{background:#2a3140;padding:4px 10px;font-size:13px;border-radius:14px}}
.punto.fatto{{background:#38507a}} .punto.ora{{background:#ffd54a;color:#111;font-weight:700}}
.passo{{display:none;background:#0f1218;border-radius:12px;padding:12px}}
.passo.visibile{{display:block}}
.intestazione{{font-size:16px;color:#cfd6e2;margin-bottom:8px}} .intestazione b{{color:#fff}}
.schema{{display:flex;flex-direction:column;align-items:center;gap:4px}}
.lato{{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px;transition:opacity 1s ease,transform 1s ease}}
.carta{{position:relative;background:#fff;border-radius:10px;padding:4px;text-align:center;width:180px}}
.carta img{{width:100%;display:block}}
.testo{{color:#111;font-size:22px;font-weight:600;padding:46px 0}}
.nome{{color:#333;font-size:13px;padding:2px 4px 4px}}
.n{{position:absolute;left:8px;top:4px;color:#0b5;font-weight:700;font-size:20px}}
.piu{{font-size:26px;color:#9aa4b2}}
.freccia{{display:flex;align-items:center;gap:12px}}
.freccia .f{{font-size:40px;line-height:1;transform:rotate(90deg);transition:color .5s,text-shadow .5s}}
.freccia .e{{font-size:13px;color:#9fd3ff;max-width:420px}}
.attiva .f{{color:#ffd54a;text-shadow:0 0 14px #ffd54a}}
.nascosto{{opacity:0;transform:translateY(-14px) scale(.9)}}
.spiega{{font-size:15px;line-height:1.5;color:#e8ecf3;background:#1a2030;border-left:4px solid #ffd54a;
border-radius:8px;padding:10px 12px;margin:12px 0 0}}
.legenda{{font-size:12px;color:#9aa4b2;margin-top:8px}}
.palco{{margin-top:14px;background:#0f1218;border-radius:12px;padding:10px}}
.palco h4{{margin:2px 2px 8px;font-size:16px;color:#fff}}
.palco .comandi button{{padding:6px 12px;font-size:14px}}
.palco .comandi button.forma{{background:#2a3140}}
.palco .comandi button.forma.scelta{{background:#ffd54a;color:#111;font-weight:600}}
#scena{{width:100%;height:440px;position:relative;border-radius:10px;background:#0b0e14}}
@media (max-width:560px){{#scena{{height:330px}}}}
.tempo{{display:flex;align-items:center;gap:8px;font-size:12px;color:#9aa4b2;margin-top:8px}}
.tempo input{{flex:1;accent-color:#ffd54a}}
.colori{{font-size:13px;color:#e8ecf3;margin-top:8px;line-height:1.7}}
.colori i{{display:inline-block;width:11px;height:11px;border-radius:50%;margin:0 3px 0 8px;vertical-align:middle}}
.palco .aiuto{{font-size:12px;color:#9aa4b2;margin-top:6px}}
@media (max-width:520px){{.carta{{width:140px}}}}
</style>
<div class="comandi"><button id="indietro">{testi["indietro"]}</button><button id="avanti">{testi["avanti"]}</button>
<button id="tutti">{testi["tutti"]}</button></div>
<div class="punti">{puntini}</div>
{"".join(schede)}
<div class="legenda">{testi["legenda"]}</div>
<div class="palco"><h4>{testi["palco"]}</h4>
<div class="comandi"><button id="pausa">{testi["avvia"]}</button><button id="ricomincia">{testi["ricomincia"]}</button>
<button class="forma scelta" data-f="piana">{testi["piana"]}</button><button class="forma" data-f="vera">{testi["vera"]}</button>
<button class="forma scelta" id="scritte">{testi["scritte"]}</button><button class="forma" id="gira">{testi["gira"]}</button></div>
<div id="scena"></div>
<div class="tempo"><span>{testi["inizio"]}</span><input type="range" id="momento" min="0" max="100" value="0"><span>{testi["fine"]}</span></div>
<div class="colori">{testi["colori"]}</div><div class="aiuto">{testi["aiuto"]} <span id="senza"></span></div></div>
<script src="{LIBRERIA_3D}"></script>
<script>
// --- La scena: su un piano, a sinistra le molecole di partenza, al centro l'enzima, a destra i prodotti ---
const R={dati_3d};
const DURATA=8000, MANCANO={json.dumps(testi["mancano"])};
let V=null,parti=[],forma="piana",scritte=true,gira=false,scena=0,inizio=performance.now(),fermo=true,visibile=false,
  pausaDa=0,ultimo=0,enzR=0,fondo=null;
try{{V=$3Dmol.createViewer("scena",{{backgroundColor:"#0b0e14"}});}}catch(e){{V=null;}}
const lisc=x=>x<=0?0:x>=1?1:x*x*(3-2*x);
const M=document.getElementById("momento");
function colonna(lista,x0,verso){{ // molecole una sotto l'altra, centrate in altezza
  if(!lista.length)return 0;
  const largo=Math.max(...lista.map(p=>p.mx*2));
  const alto=lista.reduce((s,p)=>s+p.my*2+1.4,0)+1.5*(lista.length-1);let y=alto/2;
  lista.forEach(p=>{{p.fx=x0+verso*largo/2;p.fy=y-p.my;y-=p.my*2+1.4+1.5;}});
  return alto;
}}
function prepara(n){{
  scena=n;if(!V)return;V.removeAllModels();V.removeAllShapes();V.removeAllLabels();parti=[];
  const sc=R.scene[n]||{{da:[],a:[],senza:[]}};
  document.getElementById("senza").textContent=sc.senza.length?MANCANO+sc.senza.join(", "):"";
  for(const lato of ["da","a"])for(const m of sc[lato]){{
    const modello=V.addModel(R.modelli[m.k][forma],"sdf"),atomi=modello.selectedAtoms({{}});
    const c=[0,0,0];atomi.forEach(a=>{{c[0]+=a.x;c[1]+=a.y;c[2]+=a.z;}});c.forEach((v,i)=>c[i]=v/atomi.length);
    const base=atomi.map(a=>[a.x-c[0],a.y-c[1],a.z-c[2]]);
    const raggio=Math.max(1.2,...base.map(b=>Math.hypot(b[0],b[1],b[2])));
    // Mezza larghezza (anche quando la molecola gira) e mezza altezza.
    const mx=Math.max(1.2,...base.map(b=>Math.hypot(b[0],b[2]))),my=Math.max(1,...base.map(b=>Math.abs(b[1])));
    // Le scritte dei gruppi: ogni atomo non di idrogeno con i suoi idrogeni (CH₃, CH₂, OH, NH₂, H₂O).
    const perIndice={{}};atomi.forEach(a=>perIndice[a.index]=a);const PED=["","","₂","₃","₄"];
    const gruppi=atomi.map((a,i)=>{{if(a.elem=="H")return null;
      const vicini=(a.bonds||[]).map(j=>perIndice[j]).filter(x=>x);
      const h=vicini.filter(x=>x.elem=="H").length;
      if(a.elem=="O"&&h==2&&vicini.length==2)return {{i,testo:"H₂O",elem:"O"}};
      return {{i,testo:a.elem+(h?"H"+PED[h]:""),elem:a.elem}};}}).filter(g=>g);
    parti.push({{modello,atomi,base,raggio,mx,my,gruppi,lato,nome:(m.n>1?m.n+" × ":"")+m.nome}});
  }}
  const prima=parti.filter(p=>p.lato=="da"),dopo=parti.filter(p=>p.lato=="a");
  enzR=sc.enzima&&prima.length&&dopo.length?4:(prima.length&&dopo.length?1.5:0);
  // Con un solo lato (nessuna trasformazione) le molecole stanno al centro, una sotto l'altra.
  if(!dopo.length||!prima.length){{const sole=dopo.length?dopo:prima;
    const largo=Math.max(...sole.map(p=>p.mx*2));colonna(sole,-largo/2,1);}}
  else{{colonna(prima,-(enzR+4),-1);colonna(dopo,enzR+4,1);}}
  const alto=Math.max(8,...parti.map(p=>Math.abs(p.fy)+p.my+1.5))*2+2;
  const largo=Math.max(14,...parti.map(p=>Math.abs(p.fx)+p.mx))*2+3;
  fondo={{w:largo,h:alto,z:-Math.max(...parti.map(p=>p.raggio),1)-1.5}};
  inquadra();
  // Ogni passaggio parte fermo, all'inizio: si muove solo con «Avvia».
  fermo=true;ultimo=0;if(M)M.value=0;
  document.getElementById("pausa").textContent={json.dumps(testi["avvia"])};
  quadro(0);
}}
// L'inquadratura comprende le molecole di partenza e i prodotti nella loro posizione finale.
function inquadra(){{
  if(!V||!parti.length||!document.getElementById("scena").clientWidth)return;
  parti.forEach(p=>posa(p,p.fx,p.fy,0,1,1));V.resize();V.zoomTo();V.zoom(document.getElementById("scena").clientWidth<560?1.4:1.7);
}}
function adesso(){{return fermo?(+M.value/100)*DURATA*0.999:performance.now()-inizio;}}
function posa(p,x,y,ang,scala,op){{
  const co=Math.cos(ang),si=Math.sin(ang);
  p.atomi.forEach((a,i)=>{{const b=p.base[i];
    a.x=(b[0]*co+b[2]*si)*scala+x;a.y=b[1]*scala+y;a.z=(-b[0]*si+b[2]*co)*scala;}});
  p.cx=x;p.cy=y;
  if(op<=0.02){{p.modello.setStyle({{}},{{}});return;}}
  p.modello.setStyle({{}},{{stick:{{radius:0.15,opacity:op}},sphere:{{scale:0.25,opacity:op}}}});
  if(!scritte)return;
  // Con le scritte gli idrogeni sono già nel nome del gruppo: si nascondono.
  p.modello.setStyle({{elem:"H"}},{{}});
  if(op<0.5||p.gruppi.length>60||!p.quiete)return;
  const COL={{C:"#3a3f47",O:"#c0392b",N:"#2b5fd9",S:"#b8960b",P:"#d9822b"}};
  p.gruppi.forEach(g=>{{const a=p.atomi[g.i];if(g.testo=="C")return;
    V.addLabel(g.testo,{{position:{{x:a.x,y:a.y,z:a.z}},fontSize:10,fontColor:"#fff",
      backgroundColor:COL[g.elem]||"#555",backgroundOpacity:0.75,alignment:"center",inFront:true}});}});
}}
function disegna(ora){{
  requestAnimationFrame(disegna);
  // Si disegna solo se la scena si vede e si muove: niente lavoro quando è ferma o fuori vista.
  if(!V||!parti.length||!visibile||(fermo&&!gira)||ora-ultimo<50)return;ultimo=ora;
  quadro(fermo?(+M.value/100)*DURATA*0.999:ora-inizio,ora);
}}
function quadro(tempo,ora){{
  const t=((tempo%DURATA)+DURATA)%DURATA/DURATA, sc=R.scene[scena];
  if(M&&!fermo)M.value=Math.round(t*100);
  const prodotti=parti.some(q=>q.lato=="a"), reagenti=parti.some(q=>q.lato=="da"), cambia=prodotti&&reagenti;
  // 0-35%: le molecole entrano nell'enzima; 35-50%: l'enzima lavora; 50-75%: escono i prodotti.
  const entra=cambia?lisc((t-0.05)/0.3):0, reagisce=cambia?lisc((t-0.35)/0.13):0,
    escono=cambia?lisc((t-0.47)/0.28):1;
  const ang=gira?((ora||0)/1000)*0.8:0;
  // Le scritte CH₂, OH… (pesanti da disegnare) solo quando le molecole sono ferme.
  const quiete=!gira&&(fermo||!cambia||t<0.05||t>0.78);parti.forEach(p=>p.quiete=quiete);
  V.removeAllShapes();V.removeAllLabels();
  // Il piano: lo sfondo su cui stanno le molecole.
  if(fondo)V.addBox({{center:{{x:0,y:0,z:fondo.z}},dimensions:{{w:fondo.w,h:fondo.h,d:0.1}},color:"#1d3b7a",opacity:0.45}});
  parti.forEach(p=>{{
    let x,y,op,scala;
    if(p.lato=="da"){{x=p.fx*(1-entra);y=p.fy*(1-entra);op=cambia?1-reagisce:1;scala=1-0.4*reagisce;}}
    else{{x=p.fx*escono;y=p.fy*escono;op=escono;scala=0.6+0.4*escono;}}
    posa(p,x,y,ang,scala,op);
    if(op>0.5)V.addLabel(p.nome,{{position:{{x,y:y-p.my*scala-1,z:0}},fontSize:13,
      fontColor:p.lato=="da"?"#fff":"#111",backgroundColor:p.lato=="da"?"#c0392b":"#ffb84d",
      backgroundOpacity:0.9,alignment:"center",inFront:true}});
  }});
  // L'enzima: sempre al centro; mentre lavora si illumina.
  if(cambia){{
    const lavora=Math.sin(Math.PI*Math.min(1,Math.max(0,(t-0.3)/0.25)));
    V.addSphere({{center:{{x:0,y:0,z:0}},radius:enzR*(1+0.12*lavora),color:lavora>0.05?"#ffd54a":"#8fbaff",
      opacity:0.38+0.2*lavora}});
    V.addLabel("⚙️ "+(sc.enzima||{json.dumps(testi["reazione"])}),{{position:{{x:0,y:enzR+1.3,z:0}},fontSize:14,
      fontColor:"#111",backgroundColor:"#ffd54a",backgroundOpacity:0.95,alignment:"center",inFront:true}});
    V.addArrow({{start:{{x:-enzR-1.6,y:-enzR-1.5,z:0}},end:{{x:enzR+1.6,y:-enzR-1.5,z:0}},radius:0.12,color:"#9aa4b2",opacity:0.8}});
  }}
  V.render();
}}
requestAnimationFrame(disegna);
if(!window.IntersectionObserver)visibile=true;
if(window.IntersectionObserver)new IntersectionObserver(e=>{{const prima=visibile;visibile=e[0].isIntersecting;
  // Quando la scena torna in vista (per esempio aprendo la scheda) si rifà l'inquadratura.
  if(visibile&&!prima){{inquadra();quadro(adesso(),performance.now());}}}}).observe(document.getElementById("scena"));
if(window.ResizeObserver){{let largh=0;new ResizeObserver(e=>{{const w=e[0].contentRect.width;
  if(w&&Math.abs(w-largh)>20){{largh=w;prepara(scena);}}}}).observe(document.getElementById("scena"));}}
function pausa(si){{const b=document.getElementById("pausa");
  if(!si&&fermo){{inizio=performance.now()-(+M.value/100)*DURATA;fermo=false;b.textContent={json.dumps(testi["pausa"])};}}
  else if(si&&!fermo){{fermo=true;b.textContent={json.dumps(testi["riprendi"])};quadro((+M.value/100)*DURATA*0.999,0);}}}}
document.getElementById("pausa").onclick=()=>pausa(!fermo);
document.getElementById("ricomincia").onclick=()=>prepara(scena);
// La barra del tempo: si ferma la scena e si guarda il momento scelto.
M.oninput=()=>{{pausa(true);quadro((+M.value/100)*DURATA*0.999,0);}};
document.querySelectorAll(".forma[data-f]").forEach(b=>b.onclick=()=>{{forma=b.dataset.f;
  document.querySelectorAll(".forma[data-f]").forEach(x=>x.classList.toggle("scelta",x==b));prepara(scena);}});
document.getElementById("scritte").onclick=e=>{{scritte=!scritte;e.target.classList.toggle("scelta",scritte);
  if(fermo&&parti.length)quadro((+M.value/100)*DURATA*0.999,0);}};
document.getElementById("gira").onclick=e=>{{gira=!gira;e.target.classList.toggle("scelta",gira);
  if(!gira&&parti.length){{inizio=performance.now()-(+M.value/100)*DURATA;quadro((+M.value/100)*DURATA*0.999,0);}}}};

const S=[...document.querySelectorAll(".passo")],D=[...document.querySelectorAll(".punto")],
I=document.getElementById("indietro"),A=document.getElementById("avanti"),T=document.getElementById("tutti");
let ora=0,timer=null,attese=[];
function mostra(n){{
  attese.forEach(clearTimeout);attese=[];ora=n;
  S.forEach((s,k)=>s.classList.toggle("visibile",k==n));
  D.forEach((d,k)=>{{d.classList.toggle("ora",k==n);d.classList.toggle("fatto",k<n);}});
  I.disabled=n==0;A.disabled=n==S.length-1;prepara(n);
  // Prima le molecole di partenza, poi l'enzima lavora, infine compaiono i prodotti.
  const s=S[n],dopo=s.querySelector(".dopo"),f=s.querySelector(".freccia");
  if(dopo){{dopo.classList.add("nascosto");f&&f.classList.remove("attiva");
    attese.push(setTimeout(()=>f&&f.classList.add("attiva"),700));
    attese.push(setTimeout(()=>{{dopo.classList.remove("nascosto");f&&f.classList.remove("attiva");}},1700));}}
}}
function ferma(){{clearInterval(timer);timer=null;T.textContent={json.dumps(testi["tutti"])};}}
I.onclick=()=>{{ferma();mostra(Math.max(0,ora-1));}};
A.onclick=()=>{{ferma();mostra(Math.min(S.length-1,ora+1));}};
D.forEach(d=>d.onclick=()=>{{ferma();mostra(+d.dataset.n);}});
T.onclick=()=>{{if(timer){{ferma();return;}}
  if(ora==S.length-1)mostra(0);T.textContent={json.dumps(testi["ferma"])};
  timer=setInterval(()=>{{if(ora>=S.length-1){{ferma();return;}}mostra(ora+1);}},7000);}};
mostra(0);
</script>"""


CHIMICA = re.compile(r"chimic|compost|molecol|farmac|acid|ione|ormon|vitamin|zuccher|sugar|monosacc|disacc|"
                     r"protein|ammin|amin|alcol|alcohol|enzim|enzym|antibiot|drug|medication|compound|"
                     r"nucleo|lipid|steroid|ester|salt|sale |metabol|neurotrasmett|neurotransmitter|C\d", re.I)


def descrizione_wikipedia(info, lingua):
    """Il riassunto della voce di Wikipedia sulla molecola, nella lingua chiesta («it» o «en»):
    scritto per chi studia, al posto della descrizione tecnica di PubChem. Salvato con la molecola."""
    campo = f"wikipedia_{lingua}"
    if campo not in info:
        titolo = (info["nome"] if lingua == "it" else info.get("inglese") or info["nome"]).strip()
        risultato = {}
        # «Glucosio», poi «ATP» (le sigle si scrivono in maiuscolo), poi la voce italiana collegata
        # a quella inglese («Adenosine triphosphate» → «Adenosina trifosfato»).
        prove = [titolo.capitalize(), titolo.upper()] if len(titolo) <= 5 else [titolo.capitalize()]
        if lingua != "en" and info.get("inglese"):
            try:
                collegamenti = json.loads(_richiesta(
                    "https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&redirects=1&format=json"
                    f"&lllang={lingua}&titles=" + urllib.parse.quote(info["inglese"]), tempo=15))
                for pagina in collegamenti.get("query", {}).get("pages", {}).values():
                    prove += [l["*"] for l in pagina.get("langlinks", [])]
            except Exception:
                pass
        # Il titolo dato da Wikidata (collegato al numero PubChem della molecola) è il più sicuro:
        # i nomi inglesi ricavati a volte sono sbagliati («chinine», «griseofulvine»).
        sicuro = info.get("wikipedia_titoli", {}).get(lingua)
        if sicuro:
            prove.insert(0, sicuro)
        for prova in dict.fromkeys(prove):
            try:
                dati = json.loads(_richiesta(f"https://{lingua}.wikipedia.org/api/rest_v1/page/summary/"
                                             + urllib.parse.quote(prova.replace(" ", "_")), tempo=15))
            except urllib.error.HTTPError as errore:
                if errore.code == 429:
                    return {}  # troppe richieste: non vuol dire che la voce non c'è, si riprova dopo
                continue  # voce che non esiste
            except Exception:
                return {}  # rete assente: si riprova la prossima volta
            testo = dati.get("extract", "")
            # Solo voci vere su una sostanza: niente pagine di disambiguazione o su altri significati.
            if dati.get("type") == "standard" and len(testo) >= 80 and (prova == sicuro or CHIMICA.search(testo)):
                risultato = {"testo": testo, "url": dati.get("content_urls", {}).get("desktop", {}).get("page", ""),
                             "titolo": dati.get("title", prova)}
                break
        info[campo] = risultato
        chiave = re.sub(r"[^a-z0-9]+", "_", senza_accenti(info["nome"])).strip("_")
        file_info = cartella("molecole") / f"{chiave}.json"
        if file_info.exists():
            file_info.write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    return info[campo]


def descrizione_pubchem(info):
    """La descrizione della molecola secondo PubChem (in inglese), salvata con le altre informazioni."""
    if "descrizione_en" not in info:
        testo = ""
        try:
            dati = json.loads(_richiesta(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{info['cid']}/description/JSON"))
            testi = [d["Description"] for d in dati.get("InformationList", {}).get("Information", []) if d.get("Description")]
            # La descrizione più completa ma non lunghissima.
            testi.sort(key=lambda t: (len(t) > 900, -len(t)))
            testo = testi[0] if testi else ""
        except Exception:
            testo = ""
        info["descrizione_en"] = testo
        chiave = re.sub(r"[^a-z0-9]+", "_", senza_accenti(info["nome"])).strip("_")
        file_info = cartella("molecole") / f"{chiave}.json"
        if file_info.exists():
            file_info.write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    return info["descrizione_en"]


# --- Scheda completa della molecola: la voce di Wikipedia divisa per argomento ---------------
# Le sezioni della voce si raggruppano per quello che serve a chi studia; il titolo della sezione
# decide il gruppo (il primo che corrisponde). Note, bibliografia e collegamenti si scartano.
GRUPPI_SCHEDA = [
    ("dove", r"\bus[oi]\b|impieg|applicazion|indicazion|utilizz|terapi|presenza|fonti|diffusione|occorrenz|"
             r"in natura|alimenti|alimentazione|produzione|commercio|dosaggio|posologia",
             r"\buses?\b|medical|applications?|occurrence|sources|indications?|therapeutic|production|"
             r"natural|dietary|food|dosage|commercial"),
    ("corpo", r"ruolo|funzion|meccanismo|farmacodinamica|farmacocinetica|farmacologia|metabolismo|biochimic|"
              r"biosintesi|fisiologi|attivit|\bazione|assorbimento|eliminazione|trasporto",
              r"biolog|function|mechanism|pharmacodynamic|pharmacokinetic|pharmacology|metabolism|"
              r"biosynthesis|physiolog|role|absorption|elimination"),
    ("rischi", r"effett|tossic|controindicazion|interazion|avvertenz|sicurezza|sovradosaggio|rischi|antidot|"
               r"gravidanza|resistenz",
               r"adverse|side.effect|toxicity|contraindication|interaction|overdose|safety|hazard|pregnan|resistance"),
    ("chimica", r"caratteristic|propriet|struttura|sintesi|isomer|reattivit|chimic|fisic|preparazione",
                r"propert|structure|synthesis|chemi|isomer|reaction|physical|preparation"),
    ("storia", r"storia|scoperta|etimologia|nome", r"history|discovery|etymology|name"),
]
SEZIONI_INUTILI = re.compile(r"note|bibliografia|voci correlate|altri progetti|collegamenti|see also|references|"
                             r"further reading|external links|notes|gallery|galleria", re.I)


# Sezioni di sole liste di dati (spettri, identificativi) o di laboratorio: non spiegano nulla.
SEZIONI_DATI = re.compile(r"spettr|spectr|\bnmr\b|identificativ|identifiers?\b|incompatibilit|dati chimico|"
                          r"chemical data|infobox|tabella|table", re.I)
PAROLE_INGLESI = re.compile(r"\b(the|and|of|is|are|with|which|its|by|from|was|were|this|that|has|it|as|to|for|an|or|"
                            r"on|at|be|can|also)\b", re.I)
PAROLE_ITALIANE = re.compile(r"\b(il|lo|la|gli|le|di|del|della|che|è|sono|con|per|nel|nella|una|un)\b", re.I)


def _riga_di_dati(riga):
    """Righe che non sono testo: formule LaTeX, spettri, numeri con unità, sigle sole («GC-MS»)."""
    r = riga.strip()
    if re.search(r"[⟶→⇌]", r) and len(r) < 160 and "{" not in r:
        return False  # un'equazione di reazione («C7H7Cl + NH3 ⟶ C7H9N + HCl») si tiene
    lettere = sum(c.isalpha() for c in r)
    return (len(r) <= 3 or "\\displaystyle" in r or "{" in r or lettere < 0.5 * len(r)
            or re.match(r"(spettro|spectrum)\b", r, re.I) or (len(r) < 80 and re.search(r"Å²|\[M[+-]|\bDa$", r))
            or (len(r) < 14 and " " not in r and not r.islower()))


def _pulisci_blocco(blocco, lingua):
    """Il blocco «**Titolo.** testo» senza le parti inutili, oppure "" se non serve a chi studia."""
    titolo = re.match(r"\*\*(.+?)\.\*\*", blocco)
    if titolo and SEZIONI_DATI.search(titolo.group(1)):
        return ""
    tenute = []
    for r in blocco.split("\n"):
        if not r.strip():
            continue
        if _riga_di_dati(r) and not (titolo and r.startswith("**")):
            continue
        # Paragrafi rimasti nell'altra lingua (la Wikipedia italiana a volte ha pezzi non tradotti).
        en, it = len(PAROLE_INGLESI.findall(r)), len(PAROLE_ITALIANE.findall(r))
        if (en >= 4 and en > 2 * it or en >= 3 and not it) if lingua == "it" else (it >= 4 and it > 2 * en or it >= 3 and not en):
            continue
        tenute.append(r)
    # In Markdown un solo a capo unisce le righe: gli elenchi diventano punti, il resto paragrafi.
    righe = []
    for i, r in enumerate(tenute):
        dopo_due_punti = i and (tenute[i - 1].rstrip().endswith(":") or righe[-1].startswith("- "))
        elenco = len(r) < 90 and not r.startswith("**") and (
            not r.rstrip().endswith((".", ":")) or (r.rstrip().endswith(".") and len(r) < 60 and i
                                                    and righe[-1].startswith("- ")))
        righe.append(f"- {r.strip()}" if elenco and dopo_due_punti else r)
    # Un «…le seguenti caratteristiche:» rimasto senza elenco (tolto perché erano dati) non serve.
    def senza_elenco(i, r):
        if not r.rstrip().endswith(":") or (i + 1 < len(righe) and righe[i + 1].startswith("- ")):
            return r
        if i + 1 < len(righe) and not righe[i + 1].startswith("**") and not re.search(r"seguent|following", r, re.I):
            return r  # l'elenco continua con paragrafi lunghi
        # Le frasi lunghe restano (con il punto); «…le seguenti caratteristiche:» da sola no.
        return r.rstrip()[:-1].rstrip() + "." if r.startswith("**") or len(r) > 150 else None
    righe = [senza_elenco(i, r) for i, r in enumerate(righe)]
    righe = [r for r in righe if r]
    testo = ""
    for r in righe:
        testo += ("\n" if testo and r.startswith("- ") and testo.rsplit("\n", 1)[-1].startswith(("- ",))
                  or testo.endswith(":") and r.startswith("- ") else "\n\n" if testo else "") + r
    return testo


def _formula_latex(latex):
    """«{\\ce {ADP + P{}_{i} -> ATP}}» → «ADP + Pi → ATP»."""
    for comando, segno in ((r"\\to\b", "→"), (r"\\rightarrow\b", "→"), (r"->", "→"), (r"<=>|\\rightleftharpoons", "⇌"),
                           (r"\\downarrow", "↓"), (r"\\uparrow", "↑"), (r"\\cdot", "·"), (r"\\times", "×")):
        latex = re.sub(comando, segno, latex)
    latex = re.sub(r"\[\{?\\text\s*\{([^{}]*)\}\}?\]", r"[\1]", latex)
    latex = re.sub(r"\\[a-zA-Z]+\s*", "", latex)  # \ce, \mathrm, \text...
    latex = re.sub(r"[{}_^]", "", latex)
    return re.sub(r"\s+", " ", latex).strip()


def _ricomponi_formule(testo):
    """Le formule di Wikipedia arrivano spezzate su molte righe (un pezzo per riga) e poi ripetute in
    LaTeX: si tiene solo la versione LaTeX, resa leggibile, al posto giusto nella frase."""
    if "\\displaystyle" not in testo:
        return testo
    righe = []
    attesa = False  # dopo una formula: la riga seguente continua la stessa frase?
    for riga in testo.split("\n"):
        latex = re.fullmatch(r"\s*\{\\displaystyle (.+)\}\s*", riga)
        if latex:
            # Via i pezzi spezzati che la precedono (righe corte o vuote).
            while righe and len(righe[-1].strip()) <= 25 and not righe[-1].strip().endswith((".", ":")):
                if righe[-1].startswith("**") or len(righe) == 1 and righe[-1].strip():
                    break
                righe.pop()
            formula = _formula_latex(latex.group(1))
            prima = righe[-1].rstrip() if righe else ""
            righe[-1:] = [prima + ("" if not prima or prima.endswith("(") else " ") + formula]
            attesa = True
            continue
        if attesa and not riga.strip():
            continue
        if attesa and righe:
            pezzo = riga.strip()
            if pezzo and (pezzo[0].islower() or pezzo[0] in ").,;:"):
                righe[-1] += ("" if pezzo[0] in ").,;:" else " ") + pezzo
                attesa = False
                continue
        attesa = False
        righe.append(riga)
    return "\n".join(righe)


def pulisci_scheda(scheda, lingua):
    """La scheda senza blocchi di dati, liste di sigle e paragrafi nella lingua sbagliata."""
    pulita = {}
    for chiave, valore in scheda.items():
        if chiave in ("titolo", "url") or not isinstance(valore, str):
            pulita[chiave] = valore
            continue
        blocchi = [_pulisci_blocco(b, lingua)
                   for b in re.split(r"\n(?=\*\*[^*\n]+\.\*\* )", _ricomponi_formule(valore))]
        testo = "\n\n".join(b for b in blocchi if b.strip()).strip()
        if testo and not re.fullmatch(r"\*\*[^*]+\.\*\*", testo):
            pulita[chiave] = testo
    return pulita


def _taglia(testo, massimo):
    """Il testo fino a `massimo` caratteri, chiuso alla fine di una frase."""
    testo = re.sub(r"\n{2,}", "\n\n", testo).strip()
    if len(testo) <= massimo:
        return testo
    pezzo = testo[:massimo]
    fine = max(pezzo.rfind(". "), pezzo.rfind(".\n"))
    return (pezzo[:fine + 1] if fine > massimo // 3 else pezzo.rsplit(" ", 1)[0] + "…").strip()


def _sezioni_testo(testo, lingua):
    """{"intro": testo iniziale, gruppo: testo} dal testo semplice di una voce di Wikipedia."""
    pezzi = re.split(r"\n(={2,})\s*(.+?)\s*\1\n", "\n" + testo)
    sezioni = {"intro": _taglia(pezzi[0], 1400)}
    raccolti = {}
    gruppo_padre = None
    for i in range(1, len(pezzi) - 2, 3):
        livello, titolo, corpo = len(pezzi[i]), pezzi[i + 1], pezzi[i + 2].strip()
        if SEZIONI_INUTILI.fullmatch(titolo.strip()) or SEZIONI_INUTILI.match(titolo.strip()):
            gruppo_padre = None if livello == 2 else gruppo_padre
            continue
        gruppo = next((g for g, it, en in GRUPPI_SCHEDA if re.search(it if lingua == "it" else en, titolo, re.I)), None)
        if livello == 2:
            gruppo_padre = gruppo
        gruppo = gruppo or gruppo_padre
        if gruppo and corpo:
            raccolti.setdefault(gruppo, []).append((titolo if livello > 2 or len(raccolti.get(gruppo, [])) else "", corpo))
    for gruppo, voci in raccolti.items():
        testo_g = "\n\n".join((f"**{t}.** " if t else "") + c for t, c in voci)
        sezioni[gruppo] = _taglia(testo_g, 1800)
    return sezioni


def scheda_wikipedia(info, lingua, scarica=True):
    """La voce di Wikipedia della molecola divisa per argomento, nella lingua chiesta:
    {"titolo", "url", "intro", "dove", "corpo", "rischi", "chimica", "storia"} (solo i gruppi
    presenti), oppure {} se la voce non c'è. Salvata con la molecola."""
    campo = f"scheda_{lingua}"
    if campo in info or not scarica:
        return pulisci_scheda(info.get(campo, {}), lingua)
    voce = descrizione_wikipedia(info, lingua)
    if not voce:
        return {} if f"wikipedia_{lingua}" not in info else _salva_campo(info, campo, {})
    indirizzo = (f"https://{lingua}.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1"
                 "&redirects=1&format=json&titles=" + urllib.parse.quote(voce["titolo"]))
    testo = None
    for _ in range(3):
        try:
            # Wikipedia chiede ai programmi di presentarsi con un nome proprio, non da browser.
            with urllib.request.urlopen(urllib.request.Request(indirizzo, headers=AGENTE_WIKIPEDIA), timeout=20) as r:
                testo = next(iter(json.load(r)["query"]["pages"].values())).get("extract", "")
            break
        except urllib.error.HTTPError as errore:
            if errore.code != 429:
                break
            time.sleep(min(int(errore.headers.get("retry-after") or 5), 30))  # troppe richieste: si aspetta
        except Exception:
            break
    if testo is None:
        return {}  # rete assente: si riprova la prossima volta
    scheda = _sezioni_testo(testo, lingua) if testo else {}
    if scheda:
        scheda.update(titolo=voce["titolo"], url=voce["url"])
    return pulisci_scheda(_salva_campo(info, campo, scheda), lingua)


def _salva_campo(info, campo, valore):
    info[campo] = valore
    chiave = re.sub(r"[^a-z0-9]+", "_", senza_accenti(info["nome"])).strip("_")
    file_info = cartella("molecole") / f"{chiave}.json"
    if file_info.exists():
        file_info.write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    return valore


# --- Gli atomi della molecola: quali, quanti, come sono legati -------------------------------
NOMI_ELEMENTI = {
    "H": "idrogeno", "C": "carbonio", "N": "azoto", "O": "ossigeno", "S": "zolfo", "P": "fosforo",
    "F": "fluoro", "Cl": "cloro", "Br": "bromo", "I": "iodio", "Na": "sodio", "K": "potassio",
    "Ca": "calcio", "Mg": "magnesio", "Fe": "ferro", "Zn": "zinco", "Cu": "rame", "Co": "cobalto",
    "B": "boro", "Si": "silicio", "As": "arsenico", "Hg": "mercurio", "Ag": "argento", "Sb": "antimonio",
    "Mn": "manganese", "Ga": "gallio", "Li": "litio", "Al": "alluminio", "Pt": "platino", "Au": "oro",
    "Bi": "bismuto", "Se": "selenio", "Ba": "bario", "Sr": "stronzio", "Gd": "gadolinio", "Tc": "tecnezio",
    "Cr": "cromo", "Ni": "nichel", "Mo": "molibdeno", "Pb": "piombo", "Cd": "cadmio", "Sn": "stagno",
    "Ti": "titanio", "Xe": "xeno", "He": "elio", "Ne": "neon", "Ar": "argon", "Kr": "kripton", "Tl": "tallio",
}

# Gruppi funzionali che uno studente deve riconoscere: (nome, formula, a cosa serve saperlo, SMARTS).
GRUPPI_FUNZIONALI = [
    ("Anello β-lattamico", "anello di 4 atomi con C=O e N",
     "è il bersaglio delle β-lattamasi: se si apre, l'antibiotico non funziona più", "O=C1CCN1"),
    ("Acido carbossilico", "–COOH", "acido: nel sangue (pH 7,4) perde H⁺ e diventa –COO⁻", "[CX3](=O)[OX2H1,OX1-]"),
    ("Estere", "–COO–", "si rompe con l'acqua (idrolisi), spesso grazie alle esterasi", "[#6][CX3](=O)[OX2][#6]"),
    ("Ammide", "–CO–N<", "legame stabile, lo stesso che unisce gli amminoacidi nelle proteine", "[CX3](=O)[NX3]"),
    ("Ammina", "–NH₂, –NH–, –N<", "basica: nel sangue spesso prende H⁺ e diventa carica positiva",
     "[NX3;!$(N-[C,S,P]=[O,S,N]);!$(N-a);!$(N#*);!$(N=*);!$(N-N);!$(N-O)]"),
    ("Ammina aromatica", "Ar–NH₂ / Ar–N<", "azoto legato a un anello aromatico", "[NX3;H2,H1;$(N-a);!$(N-[C,S]=[O,S,N])]"),
    ("Ossidrile (alcol)", "–OH su C saturo", "rende la molecola più solubile in acqua", "[CX4][OX2H]"),
    ("Fenolo", "–OH su anello aromatico", "debolmente acido, antiossidante", "c[OX2H]"),
    ("Aldeide", "–CHO", "carbonile reattivo, si ossida facilmente ad acido", "[CX3H1](=O)[#6,#1]"),
    ("Chetone", ">C=O tra due carboni", "carbonile, accettore di legami a idrogeno", "[#6][CX3](=O)[#6]"),
    ("Etere", "C–O–C", "poco reattivo", "[OD2;!$(O-C=O);!$(O-[P,S])]([#6])[#6]"),
    ("Tiolo", "–SH", "si ossida formando ponti disolfuro (–S–S–)", "[SX2H]"),
    ("Tioetere", "C–S–C", "zolfo tra due carboni", "[SX2;!$(S-S)]([#6])[#6]"),
    ("Fosfato", "–O–PO₃", "carico negativamente: tipico di ATP, DNA, fosfolipidi", "P(=O)([OX2,OX1-])[OX2,OX1-]"),
    ("Solfonammide", "–SO₂–NH–", "gruppo dei sulfamidici e di alcuni diuretici", "S(=O)(=O)[NX3]"),
    ("Gruppo nitro", "–NO₂", "fortemente elettron-attrattore", "[N+](=O)[O-]"),
    ("Nitrile", "–C≡N", "triplo legame carbonio-azoto", "C#N"),
    ("Alogeno", "–F, –Cl, –Br, –I", "rende la molecola più lipofila e più stabile al metabolismo", "[F,Cl,Br,I;X1]"),
    ("Guanidina", "–NH–C(=NH)–NH₂", "molto basica, sempre carica positiva nel corpo", "[NX3][CX3](=[NX2])[NX3]"),
    ("Doppio legame C=C", "C=C", "insaturazione (non aromatica)", "[CX3;!a]=[CX3;!a]"),
]


def _conta_formula(formula):
    """{"C": 6, "H": 12, "O": 6} dalla formula di PubChem (anche con i sali: «C16H18N3NaO4S»)."""
    conti = {}
    for simbolo, n in re.findall(r"([A-Z][a-z]?)(\d*)", re.sub(r"[+\-]\d*$", "", formula or "")):
        conti[simbolo] = conti.get(simbolo, 0) + int(n or 1)
    return conti


def atomi_della_molecola(info):
    """Gli atomi e i legami della molecola per la scheda: elementi con quanti atomi, colore nel 3D e
    percentuale in massa; numero di legami per tipo, anelli, centri chirali, gruppi funzionali e
    proprietà da farmaco (regola del 5 di Lipinski). Dizionario; {} se la formula non si legge."""
    conti = _conta_formula(info.get("formula", ""))
    if not conti:
        return {}
    try:
        from rdkit import Chem
        from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors
    except ImportError:
        Chem = None
    tabella_periodica = Chem.GetPeriodicTable() if Chem else None
    masse = {s: (tabella_periodica.GetAtomicWeight(s) if tabella_periodica else 0) * n for s, n in conti.items()}
    massa_totale = sum(masse.values()) or 1
    # Prima il carbonio e l'idrogeno, poi gli altri in ordine alfabetico (come nella formula di Hill).
    ordine = sorted(conti, key=lambda s: (s != "C", s != "H", s))
    elementi = [{"simbolo": s, "nome": NOMI_ELEMENTI.get(s, s), "quanti": conti[s],
                 "colore": COLORI_ATOMI.get(s, ("#FF1493", "", "rosa"))[0],
                 "colore_nome": COLORI_ATOMI.get(s, ("", "", "rosa"))[2],
                 "massa": round(100 * masse[s] / massa_totale, 1)} for s in ordine]
    risultato = {"elementi": elementi, "totale": sum(conti.values())}
    molecola = Chem.MolFromMolBlock(info.get("sdf", ""), removeHs=False) if Chem and info.get("sdf") else None
    if molecola is None:
        return risultato
    legami = {"singoli": 0, "doppi": 0, "tripli": 0, "aromatici": 0}
    for legame in molecola.GetBonds():
        tipo = legame.GetBondType()
        chiave = ("aromatici" if legame.GetIsAromatic() else "doppi" if tipo == Chem.BondType.DOUBLE
                  else "tripli" if tipo == Chem.BondType.TRIPLE else "singoli")
        legami[chiave] += 1
    anelli = molecola.GetRingInfo()
    aromatici = sum(1 for anello in anelli.AtomRings() if all(molecola.GetAtomWithIdx(i).GetIsAromatic() for i in anello))
    chirali = Chem.FindMolChiralCenters(molecola, includeUnassigned=True, useLegacyImplementation=False)
    pesante = Chem.RemoveHs(molecola, sanitize=False)
    try:
        Chem.SanitizeMol(pesante)
    except Exception:
        pass
    gruppi = []
    for nome, formula, nota, smarts in GRUPPI_FUNZIONALI:
        schema = Chem.MolFromSmarts(smarts)
        # Un gruppo si conta una volta sola per il suo primo atomo (P del fosfato, C del carbonile).
        n = len({m[0] for m in molecola.GetSubstructMatches(schema)}) if schema is not None else 0
        if n:
            gruppi.append({"nome": nome, "formula": formula, "nota": nota, "quanti": n})
    donatori, accettori = Lipinski.NumHDonors(pesante), Lipinski.NumHAcceptors(pesante)
    logp = Crippen.MolLogP(pesante)
    massa = Descriptors.MolWt(pesante)
    violazioni = sum([massa > 500, logp > 5, donatori > 5, accettori > 10])
    risultato.update(legami=legami, legami_totale=sum(legami.values()), anelli=anelli.NumRings(),
                     anelli_aromatici=aromatici, chirali=[c for i, c in chirali if molecola.GetAtomWithIdx(i).GetSymbol() == "C"],
                     gruppi=gruppi, donatori=donatori, accettori=accettori, logp=round(logp, 1),
                     lipinski=violazioni, rotabili=rdMolDescriptors.CalcNumRotatableBonds(pesante))
    return risultato


# --- Il nome IUPAC in italiano ---------------------------------------------------------------
# PubChem dà il nome IUPAC in inglese; la nomenclatura italiana ne è una traslitterazione quasi
# regolare: hydroxy → idrossi, -ol → -olo, «benzoic acid» → «acido benzoico», «sodium chloride» →
# «cloruro di sodio». Prima le parole intere, poi i pezzi, infine le lettere (ph → f, y → i).
CATIONI = {"sodium": "sodio", "potassium": "potassio", "calcium": "calcio", "magnesium": "magnesio",
           "lithium": "litio", "zinc": "zinco", "iron": "ferro", "copper": "rame", "silver": "argento",
           "aluminum": "alluminio", "barium": "bario", "hydrogen": "idrogeno", "ammonium": "ammonio",
           "bismuth": "bismuto", "mercury": "mercurio", "platinum": "platino", "gold": "oro", "cobalt": "cobalto",
           "manganese": "manganese", "strontium": "stronzio", "gadolinium": "gadolinio", "lead": "piombo",
           "chromium": "cromo", "nickel": "nichel", "cadmium": "cadmio", "tin": "stagno"}
PEZZI_IUPAC = [
    ("sulfonyl", "solfonil"), ("sulfonic", "solfonico"), ("sulfonamide", "solfonammide"), ("sulfinyl", "solfinil"),
    ("sulfate", "solfato"), ("sulfite", "solfito"), ("sulfide", "solfuro"), ("sulfamoyl", "sulfamoil"),
    ("sulfur", "zolfo"), ("chloride", "cloruro"), ("bromide", "bromuro"), ("iodide", "ioduro"),
    ("fluoride", "fluoruro"), ("hydroxide", "idrossido"), ("peroxide", "perossido"), ("oxide", "ossido"),
    ("cyanide", "cianuro"), ("hydride", "idruro"), ("nitride", "nitruro"), ("carbide", "carburo"),
    ("amide", "ammide"), ("amido", "ammido"), ("amino", "ammino"), ("amine", "ammina"), ("aminium", "amminio"),
    ("imide", "immide"), ("imine", "immina"), ("imino", "immino"), ("anilin", "anilin"),
    ("quinolin", "chinolin"), ("quinazolin", "chinazolin"), ("quinone", "chinone"), ("quinoxalin", "chinossalin"),
    ("chlor", "clor"), ("acetyl", "acetil"), ("acid", "acido"), ("oic", "oico"), ("aldehyde", "aldeide"),
    ("hydrogen", "idrogeno"), ("hydr", "idr"), ("hept", "ept"), ("hex", "es"), ("oct", "ott"),
]


def _iupac_parola(parola):
    p = parola
    for inglese, italiano in PEZZI_IUPAC:
        p = p.replace(inglese, italiano)
    p = (p.replace("ph", "f").replace("th", "t").replace("rh", "r").replace("qu", "chi").replace("x", "ss")
          .replace("y", "i").replace("hidr", "idr").replace("hess", "es").replace("kk", "k"))
    p = re.sub(r"(?<![a-z])h(?=[aeiou])", "", p)  # hexa → esa, hydro → idro (h iniziale muta)
    p = re.sub(r"(?<![a-z])ept", "ept", p)
    # Desinenze: -ol → -olo, -ane → -ano, -yne → -ino, -ine → -ina, -ate → -ato, -ium → -io, -al → -ale.
    p = re.sub(r"(?<=[a-z])(ol|ane|ine|ate|ite|ium|ole|one|ene|ide|ic|al|il)(?![a-z])", lambda m: {
        "ol": "olo", "ane": "ano", "ine": "ina", "ate": "ato", "ite": "ito", "ium": "io", "ole": "olo",
        "one": "one", "ene": "ene", "ide": "ide", "ic": "ico", "al": "ale", "il": "il"}[m.group(1)], p)
    return p


def iupac_italiano(nome):
    """Il nome IUPAC inglese di PubChem nella nomenclatura italiana (approssimata ma leggibile)."""
    if not nome:
        return ""
    n = nome.strip()
    parti = [x.strip() for x in n.split(";")]
    # Sali: «sodium;2-[...]acetate» → «2-[...]acetato di sodio».
    cationi = [p for p in parti if re.sub(r"^(di|tri|tetra)", "", p) in CATIONI]
    resto = [p for p in parti if p not in cationi]
    if cationi and resto:
        base = iupac_italiano(";".join(resto))
        return f"{base} di " + " e ".join(CATIONI[re.sub(r'^(di|tri|tetra)', '', c)] for c in cationi)
    if len(parti) > 1:
        return "; ".join(iupac_italiano(p) for p in parti)
    parole = n.split(" ")
    # Acidi: «2-acetyloxybenzoic acid» → «acido 2-acetilossibenzoico».
    if len(parole) >= 2 and parole[-1] == "acid":
        return "acido " + " ".join(_iupac_parola(w) for w in parole[:-1])
    # «sodium chloride» → «cloruro di sodio», «trimagnesium diphosphate» → «difosfato di magnesio».
    catione = re.sub(r"^(di|tri|tetra)", "", parole[0])
    if len(parole) == 2 and catione in CATIONI:
        return f"{_iupac_parola(parole[1])} di {CATIONI[catione]}"
    # Esteri: «methyl 2-hydroxybenzoate» → «2-idrossibenzoato di metile».
    if len(parole) == 2 and parole[0].endswith("yl") and parole[1].endswith("ate"):
        return f"{_iupac_parola(parole[1])} di {_iupac_parola(parole[0])}e"
    return " ".join(_iupac_parola(w) for w in parole)
