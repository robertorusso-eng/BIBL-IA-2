"""Le classi di BIBL-IA 2: un professore crea la classe, i ragazzi entrano con il codice della classe, il
professore assegna compiti (lezioni da studiare e domande, anche scritte da lui) e vede come va ognuno.

Il professore lo invita il proprietario (invito «da professore»). Il codice della classe vale anche come invito:
i ragazzi senza account lo usano per crearsi l'account ed entrano subito nella classe.
Tutto resta sul Mac (classi_v2.json è in .gitignore).
"""
import json
import os
import re
import secrets
import threading
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLASSI_FILE = ROOT / ("prove/classi_prove.json" if os.environ.get("BIBLIA_PROVE") else "classi_v2.json")
_BLOCCO = threading.Lock()
ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _leggi():
    try:
        return json.loads(CLASSI_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _scrivi(dati):
    temporaneo = CLASSI_FILE.with_suffix(".tmp")
    temporaneo.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")
    temporaneo.replace(CLASSI_FILE)


def _modifica(funzione):
    """Legge, modifica e riscrive il file sotto il blocco (più persone insieme non si rovinano i dati)."""
    with _BLOCCO:
        dati = _leggi()
        risultato = funzione(dati)
        _scrivi(dati)
        return risultato


def pulito(testo, massimo=2000):
    """Il testo scritto da un professore, senza immagini o HTML nascosti: chi lo legge non deve caricare niente da
    siti esterni. I link restano solo come testo."""
    testo = str(testo or "")[:massimo]
    testo = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", testo)        # immagini markdown
    testo = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", testo)         # link markdown: solo il testo
    testo = re.sub(r"<[^>]*>", "", testo)                              # HTML
    return testo.replace("<", "‹").replace(">", "›")


def _ora():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def tutte():
    return _leggi()


def classe(codice):
    return _leggi().get((codice or "").strip().upper())


def e_codice_classe(codice):
    c = classe(codice)
    return bool(c and c.get("aperta", True))


def nome_completo(c):
    parti = [c.get("nome")] + [x for x in (c.get("anno"), c.get("indirizzo"), c.get("sezione") and f"sezione {c['sezione']}") if x]
    return " · ".join(p for p in parti if p)


def del_docente(docente):
    """Le classi di un professore ("" = il proprietario sul Mac)."""
    return {k: v for k, v in _leggi().items() if v.get("docente", "") == docente}


def dello_studente(studente):
    return {k: v for k, v in _leggi().items() if studente in v.get("studenti", {})}


def crea(docente, docente_nome, nome, tipo, anno, indirizzo, sezione, materia):
    codice = "CL-" + "".join(secrets.choice(ALFABETO) for _ in range(6))

    def f(dati):
        dati[codice] = {"nome": pulito(nome.strip(), 60), "tipo": tipo, "anno": anno,
                        "indirizzo": pulito(indirizzo.strip(), 60), "sezione": pulito(sezione.strip(), 10), "materia": materia, "docente": docente,
                        "docente_nome": docente_nome, "creata": _ora(), "aperta": True, "studenti": {}, "compiti": []}
    _modifica(f)
    return codice


def aggiungi_studente(codice, studente, nome):
    """Mette lo studente nella classe. Restituisce "" se va bene, altrimenti il motivo."""
    codice = (codice or "").strip().upper()

    def f(dati):
        c = dati.get(codice)
        if not c:
            return "Il codice della classe non esiste."
        if not c.get("aperta", True) and studente not in c["studenti"]:
            return "Questa classe non accetta più iscrizioni: chiedi al professore."
        c["studenti"].setdefault(studente, {"nome": nome, "entrato": _ora()})
        return ""
    return _modifica(f)


def togli_studente(codice, studente):
    _modifica(lambda dati: dati.get(codice, {}).get("studenti", {}).pop(studente, None))


def imposta(codice, **campi):
    _modifica(lambda dati: dati.get(codice, {}).update({k: v for k, v in campi.items() if k in ("aperta",)}))


def elimina(codice):
    _modifica(lambda dati: dati.pop(codice, None))


def aggiungi_compito(codice, titolo, argomenti, domande_banca, scadenza, nota):
    """Un compito: capitoli da studiare (materia|argomento) e un quiz (domande della banca, per id)."""
    ident = secrets.token_hex(4)

    def f(dati):
        dati[codice]["compiti"].append({"id": ident, "titolo": pulito(titolo.strip(), 80), "argomenti": argomenti,
                                        "banca": domande_banca, "proprie": [], "scadenza": scadenza,
                                        "nota": pulito(nota.strip(), 400), "creato": _ora(), "esiti": {}})
    _modifica(f)
    return ident


def aggiungi_domanda(codice, compito, domanda):
    """Una domanda scritta dal professore (stesso formato delle domande di BIBL-IA)."""
    for campo in ("domanda", "spiegazione", "materia", "argomento"):
        if isinstance(domanda.get(campo), str):
            domanda[campo] = pulito(domanda[campo])
    if isinstance(domanda.get("opzioni"), dict):
        domanda["opzioni"] = {k: pulito(v, 500) for k, v in domanda["opzioni"].items()}

    def f(dati):
        for x in dati[codice]["compiti"]:
            if x["id"] == compito:
                domanda["id"] = f"CLS-{codice}-{compito}-{len(x['proprie']) + 1}"
                x["proprie"].append(domanda)
    _modifica(f)


def togli_compito(codice, compito):
    def f(dati):
        dati[codice]["compiti"] = [x for x in dati[codice]["compiti"] if x["id"] != compito]
    _modifica(f)


def segna_esito(codice, compito, studente, giuste, totale):
    def f(dati):
        for x in dati.get(codice, {}).get("compiti", []):
            if x["id"] == compito:
                x["esiti"][studente] = {"data": _ora(), "giuste": giuste, "totale": totale}
    _modifica(f)
