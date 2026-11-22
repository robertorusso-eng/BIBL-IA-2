"""Ripara le molecole 3D di BIBL-IA (modelli_3d/molecole): non tocca lo strumento dei Modelli 3D (modelli3d.py), ne
usa solo le funzioni per scaricare da PubChem e per calcolare il 3D.

1. Le molecole «vuote» (nome trovato nei testi ma non su PubChem): ricostruisce il nome chimico dal nome del file
   («1_2_dicloroetano» → «1,2-dicloroetano»), lo traduce in inglese con le regole della nomenclatura (e, se non basta,
   con l'AI del Mac) e lo cerca su PubChem. Si tiene solo se la formula è coerente con il nome (se il nome dice
   «cloro» ci deve essere Cl, ecc.): così non si salvano molecole sbagliate.
2. Le molecole grandi arrivate solo in 2D (piatte nel 3D): prova a calcolare la forma 3D con RDKit.
3. L'oro, che aveva preso l'acido orotico: diventa l'oro (Au).

A PubChem si inviano solo i nomi delle molecole. Si può fermare e rilanciare.
Uso: ./venv/bin/python -I ripara_molecole_v2.py
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import modelli3d  # noqa: E402

CARTELLA = ROOT / "modelli_3d" / "molecole"
REGISTRO = ROOT / "modelli_3d" / "riparazioni_v2.json"
PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"

METALLI = {"sodio": "sodium", "potassio": "potassium", "calcio": "calcium", "magnesio": "magnesium", "ferro": "iron",
           "rame": "copper", "zinco": "zinc", "argento": "silver", "ammonio": "ammonium", "alluminio": "aluminum",
           "bario": "barium", "litio": "lithium", "piombo": "lead", "mercurio": "mercury", "manganese": "manganese",
           "cromo": "chromium", "nichel": "nickel", "cobalto": "cobalt", "stagno": "tin", "idrogeno": "hydrogen",
           "oro": "gold", "platino": "platinum", "cesio": "cesium", "stronzio": "strontium", "rubidio": "rubidium"}
ANIONI = {"cloruro": "chloride", "bromuro": "bromide", "ioduro": "iodide", "fluoruro": "fluoride", "solfuro": "sulfide",
          "ossido": "oxide", "perossido": "peroxide", "idrossido": "hydroxide", "nitrato": "nitrate", "nitrito": "nitrite",
          "solfato": "sulfate", "solfito": "sulfite", "carbonato": "carbonate", "bicarbonato": "bicarbonate",
          "idrogenocarbonato": "hydrogen carbonate", "fosfato": "phosphate", "acetato": "acetate",
          "permanganato": "permanganate", "cromato": "chromate", "dicromato": "dichromate", "ipoclorito": "hypochlorite",
          "clorato": "chlorate", "perclorato": "perchlorate", "cianuro": "cyanide", "idruro": "hydride",
          "tiosolfato": "thiosulfate", "ossalato": "oxalate", "citrato": "citrate", "lattato": "lactate"}
ACIDI = {"solforico": "sulfuric acid", "cloridrico": "hydrochloric acid", "nitrico": "nitric acid",
         "fosforico": "phosphoric acid", "carbonico": "carbonic acid", "bromidrico": "hydrobromic acid",
         "fluoridrico": "hydrofluoric acid", "iodidrico": "hydroiodic acid", "cianidrico": "hydrogen cyanide",
         "solfidrico": "hydrogen sulfide", "ipocloroso": "hypochlorous acid", "nitroso": "nitrous acid",
         "solforoso": "sulfurous acid", "perclorico": "perchloric acid", "clorico": "chloric acid",
         "glutammico": "glutamic acid", "aspartico": "aspartic acid", "salicilico": "salicylic acid",
         "acetilsalicilico": "acetylsalicylic acid", "fosfatidico": "phosphatidic acid", "urico": "uric acid"}
PAROLE = [  # dalla più lunga alla più corta: sostituzioni di pezzi di parola
    ("cicloesa", "cyclohexa"), ("cicloes", "cyclohex"), ("ciclopenta", "cyclopenta"), ("ciclobuta", "cyclobuta"),
    ("ciclopropa", "cyclopropa"), ("ciclo", "cyclo"), ("metan", "methan"), ("metil", "methyl"), ("etan", "ethan"),
    ("eten", "ethen"), ("etin", "ethyn"), ("cloro", "chloro"), ("metil", "methyl"), ("etil", "ethyl"),
    ("fenil", "phenyl"), ("idrossi", "hydroxy"), ("ammino", "amino"), ("ammina", "amine"), ("ammide", "amide"),
    ("immide", "imide"), ("naftalene", "naphthalene"), ("fenolo", "phenol"), ("anilina", "aniline"),
    ("diossano", "dioxane"), ("etere", "ether"), ("estere", "ester"), ("acetofenone", "acetophenone"),
    ("tiofene", "thiophene"), ("furano", "furan"), ("piridina", "pyridine"), ("pirrolo", "pyrrole"),
    ("eptil", "heptyl"), ("ottil", "octyl"), ("esil", "hexyl"), ("epta", "hepta"), ("otta", "octa"), ("esa", "hexa"),
    ("tetradeca", "tetradeca"), ("dodeca", "dodeca"), ("solfonico", "sulfonic"), ("solf", "sulf"), ("fosf", "phosph"),
    ("ossi", "oxy"), ("idro", "hydro"), ("acrilato", "acrylate"), ("benzoato", "benzoate"),
]
FINALI = [("triolo", "triol"), ("diolo", "diol"), ("olo", "ol"), ("ano", "ane"), ("ino", "yne"), ("ale", "al"),
          ("ato", "ate"), ("ito", "ite"), ("uro", "ide")]
CONTROLLI = [  # (parola nel nome italiano, elementi che la formula deve contenere)
    (r"clor", "Cl"), (r"brom", "Br"), (r"fluor", "F"), (r"iod", "I"), (r"solf|tio|zolfo|mercapt", "S"),
    (r"fosf", "P"), (r"azot|ammin|ammid|ammon|nitr|ciano|cian|imid|piridin|pirrol|anilin|urea|ammino", "N"),
    (r"sodio", "Na"), (r"potassio", "K"), (r"calcio", "Ca"), (r"magnesio", "Mg"), (r"ferro", "Fe"), (r"rame", "Cu"),
    (r"zinco", "Zn"), (r"argento", "Ag"), (r"bario", "Ba"), (r"litio", "Li"), (r"alluminio", "Al"),
    (r"(?<!b)ossid|idross|olo\b|diolo|triolo|acido|ato\b|one\b|ale\b|etere|estere|fenolo|ossi", "O"),
    (r"metil|etil|propil|butil|ano\b|ene\b|benzen|ciclo|acetic|acetat|carbon|toluen|fenil", "C"),
]


def nome_dal_file(stem):
    """«1_2_dicloroetano» → «1,2-dicloroetano»; «acido_acetico» → «acido acetico»."""
    pezzi = stem.split("_")
    out, numeri = "", []
    for p in pezzi:
        if p.isdigit():
            numeri.append(p)
            continue
        if numeri:
            out += ("-" if out and not out.endswith(" ") else "") + ",".join(numeri) + "-"
            numeri = []
            out += p
        else:
            out += (" " if out and not out.endswith("-") else "") + p
    if numeri:
        out += "-" + ",".join(numeri)
    return out.strip()


def traduci_regole(nome):
    """La traduzione inglese con le regole della nomenclatura (può sbagliare: poi si controlla la formula)."""
    n = nome.lower().strip()
    m = re.match(r"^acido (\S+)$", n)
    if m and m.group(1) in ACIDI:
        return ACIDI[m.group(1)]
    m = re.match(r"^acido (\S+)ico$", n)
    if m:
        return f"{_radice(m.group(1))}ic acid"
    m = re.match(r"^acido (\S+)oso$", n)
    if m:
        return f"{_radice(m.group(1))}ous acid"
    m = re.match(r"^(\w+) di (\w+)$", n)
    if m and m.group(1) in ANIONI and m.group(2) in METALLI:
        return f"{METALLI[m.group(2)]} {ANIONI[m.group(1)]}"
    return " ".join(_parola(w) for w in n.split(" "))


def _radice(w):
    """Solo i pezzi di parola tradotti, senza cambiare la fine (per gli acidi: propano-ico → propano-ic)."""
    for a, b in PAROLE:
        w = w.replace(a, b)
    return w


def _parola(w):
    w = re.sub(r"an(?=(?:di|tri|tetra)(?:olo|one|ale|oico|ammina|ene|ino))", "ane", w)   # propantriolo → propanetriolo
    for a, b in PAROLE:
        w = w.replace(a, b)
    for a, b in FINALI:
        if w.endswith(a):
            return w[: -len(a)] + b
    return w


def traduci_ai(nome):
    """L'AI del Mac traduce il nome chimico (solo se le regole non bastano)."""
    dati = json.dumps({"model": "gemma3:4b", "stream": False, "options": {"temperature": 0, "num_predict": 30},
                       "prompt": "Translate this Italian chemical compound name into its standard English (IUPAC or common) "
                                 f"name. Answer with the name only.\n\n{nome}"}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/generate", data=dati,
                                                          headers={"Content-Type": "application/json"}), timeout=60)
        testo = json.load(r).get("response", "").strip().splitlines()[0].strip(" .\"'*")
        return testo if 2 < len(testo) < 80 else ""
    except Exception:
        return ""


def coerente(nome, formula):
    """La formula contiene gli elementi che il nome italiano promette."""
    elementi = set(re.findall(r"[A-Z][a-z]?", formula or ""))
    n = nome.lower()
    simboli = {"oro": "Au", "argento": "Ag", "rame": "Cu", "ferro": "Fe", "sodio": "Na", "potassio": "K", "calcio": "Ca",
               "magnesio": "Mg", "zinco": "Zn", "piombo": "Pb", "mercurio": "Hg", "alluminio": "Al", "litio": "Li",
               "idrogeno": "H", "ossigeno": "O", "azoto": "N", "cloro": "Cl", "carbonio": "C", "zolfo": "S", "iodio": "I"}
    if n in simboli:
        return elementi == {simboli[n]}
    for regola, el in CONTROLLI:
        if re.search(regola, n) and el not in elementi:
            return False
    return bool(elementi)


def cerca_pubchem(inglese):
    try:
        dati = json.loads(modelli3d._richiesta(PUG + "name/" + urllib.parse.quote(inglese) +
                                               "/property/MolecularFormula,MolecularWeight,IUPACName/JSON"))
        return dati["PropertyTable"]["Properties"][0]
    except Exception:
        return None


def scarica_struttura(cid):
    for tipo in ("3d", "2d"):
        try:
            sdf = modelli3d._richiesta(f"{PUG}cid/{cid}/SDF?record_type={tipo}").decode()
            if tipo == "2d":
                tre = modelli3d.forma_3d(sdf)
                return (tre, True) if tre else (sdf, False)
            return sdf, True
        except Exception:
            continue
    return "", False


def salva(f, nome, inglese, prop, sdf, tre_d, come):
    info = {"nome": nome, "inglese": inglese, "cid": prop["CID"], "formula": prop.get("MolecularFormula", ""),
            "peso": prop.get("MolecularWeight", ""), "iupac": prop.get("IUPACName", ""), "sdf": sdf,
            "tridimensionale": tre_d, "riparata": come}
    f.write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")


def main():
    registro = json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else {}
    fatte = {"trovate": 0, "scartate": 0, "non_trovate": 0, "3d": 0}
    # 3. L'oro
    oro = CARTELLA / "oro.json"
    if "oro" not in registro:
        prop = json.loads(modelli3d._richiesta(PUG + "cid/23985/property/MolecularFormula,MolecularWeight,IUPACName/JSON"))
        prop = prop["PropertyTable"]["Properties"][0]
        sdf, tre = scarica_struttura(23985)
        if sdf:
            salva(oro, "oro", "gold", prop, sdf, tre, "corretta: prima era l'acido orotico")
            registro["oro"] = "corretta (Au)"
            print("oro: corretto →", prop.get("MolecularFormula"), flush=True)
    # 2. Le molecole grandi piatte: la forma 3D con RDKit
    from rdkit import Chem
    for f in sorted(CARTELLA.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not d.get("sdf") or f.stem in registro:
            continue
        m = Chem.MolFromMolBlock(d["sdf"], removeHs=False, sanitize=False)
        if m is None or m.GetNumAtoms() < 8 or not m.GetNumConformers():
            continue
        c = m.GetConformer()
        if all(abs(c.GetAtomPosition(i).z) < 1e-4 for i in range(m.GetNumAtoms())):
            tre = modelli3d.forma_3d(d["sdf"], massimo_atomi=400)
            registro[f.stem] = "3d calcolato" if tre else "resta piatta (troppo grande o non calcolabile)"
            if tre:
                d["sdf"], d["tridimensionale"] = tre, True
                f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
                fatte["3d"] += 1
                print("3D calcolato:", f.stem, flush=True)
    REGISTRO.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    # 1. Le molecole vuote
    vuote = []
    for f in sorted(CARTELLA.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            d = {}
        if not (isinstance(d, dict) and d.get("sdf")) and f.stem not in registro:
            vuote.append(f)
    print(f"{len(vuote)} molecole vuote da riparare", flush=True)
    for k, f in enumerate(vuote, 1):
        nome = nome_dal_file(f.stem)
        tentativi = list(dict.fromkeys([traduci_regole(nome), nome]))
        prop = inglese = None
        for t in tentativi:
            prop = cerca_pubchem(t)
            if prop:
                inglese = t
                break
            time.sleep(0.25)
        if not prop:
            t = traduci_ai(nome)
            if t and t.lower() not in [x.lower() for x in tentativi]:
                prop = cerca_pubchem(t)
                inglese = t if prop else None
        if prop and coerente(nome, prop.get("MolecularFormula")):
            sdf, tre = scarica_struttura(prop["CID"])
            if sdf:
                salva(f, nome, inglese, prop, sdf, tre, "riparata con ripara_molecole_v2.py")
                registro[f.stem] = f"trovata: {inglese} → {prop.get('MolecularFormula')}"
                fatte["trovate"] += 1
                print("trovata:", nome, "→", inglese, prop.get("MolecularFormula"), flush=True)
        elif prop:
            registro[f.stem] = f"scartata: {inglese} → {prop.get('MolecularFormula')} non coerente con il nome"
            fatte["scartate"] += 1
            print("SCARTATA:", nome, "→", inglese, prop.get("MolecularFormula"), flush=True)
        else:
            registro[f.stem] = "non trovata"
            fatte["non_trovate"] += 1
        if k % 50 == 0:
            REGISTRO.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[{time.strftime('%H:%M')}] {k}/{len(vuote)} {fatte}", flush=True)
        time.sleep(0.25)
    REGISTRO.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Fatto.", fatte, flush=True)


if __name__ == "__main__":
    main()
