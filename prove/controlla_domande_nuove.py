"""Controlla i file di domande scritte per BIBL-IA (contenuti_v2/domande/*.json): formato, capitoli esistenti,
cinque opzioni, risposta giusta, spiegazione, passaggi del ragionamento, nessun riferimento ai libri, id unici.
Uso: ./venv/bin/python prove/controlla_domande_nuove.py [file ...]   (senza file: tutti)"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import dati_v2 as D  # noqa: E402

ESCLUSE = ROOT / ".parole_escluse.txt"
PROIBITE = re.compile("|".join([r"\blibr[oi] di testo\b", r"secondo il (?:libro|testo)", r"nel (?:libro|testo)\b",
                                r"\bmanuale\b", r"capitolo \d"] + ([r.strip() for r in ESCLUSE.read_text().splitlines()
                                                                    if r.strip()] if ESCLUSE.exists() else [])), re.I)


def controlla(file, ids_altri):
    errori = []
    try:
        dati = json.loads(Path(file).read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"JSON non valido: {e}"]
    if not isinstance(dati, list):
        return ["il file deve essere una lista di domande"]
    viste = set()
    for n, d in enumerate(dati, 1):
        dove = f"#{n} {d.get('id', '?')}"
        for campo in ("id", "materia", "argomento", "livello", "domanda", "opzioni", "giusta", "perche", "semplice",
                      "passaggi", "concetto"):
            if campo not in d:
                errori.append(f"{dove}: manca il campo {campo}")
        if d.get("materia") not in D.ARGOMENTI:
            errori.append(f"{dove}: materia sconosciuta {d.get('materia')!r}")
        elif d.get("argomento") not in D.ARGOMENTI[d["materia"]]:
            errori.append(f"{dove}: capitolo {d.get('argomento')!r} non è tra quelli di {d['materia']}")
        if d.get("livello") not in ("superiori", "università", "test"):
            errori.append(f"{dove}: livello deve essere superiori, università o test")
        op = d.get("opzioni") or {}
        if sorted(op) != ["A", "B", "C", "D", "E"] or any(not str(v).strip() for v in op.values()):
            errori.append(f"{dove}: servono 5 opzioni A-E non vuote")
        if len({str(v).strip().casefold() for v in op.values()}) < len(op):
            errori.append(f"{dove}: due opzioni uguali")
        if d.get("giusta") not in op:
            errori.append(f"{dove}: «giusta» deve essere una lettera A-E")
        if len(str(d.get("perche", ""))) < 120:
            errori.append(f"{dove}: «perche» troppo corto (almeno 120 caratteri)")
        if len(str(d.get("semplice", ""))) < 60:
            errori.append(f"{dove}: «semplice» troppo corto")
        passi = d.get("passaggi")
        if not isinstance(passi, list) or not 3 <= len(passi) <= 7:
            errori.append(f"{dove}: «passaggi» deve essere una lista di 3-7 passi del ragionamento")
        testo = json.dumps(d, ensure_ascii=False)
        m = PROIBITE.search(testo)
        if m:
            errori.append(f"{dove}: parola non ammessa {m.group()!r}")
        if d.get("id") in viste or d.get("id") in ids_altri:
            errori.append(f"{dove}: id ripetuto")
        viste.add(d.get("id"))
    return errori


def main():
    tutti = sorted(glob.glob(str(ROOT / "contenuti_v2" / "domande" / "*.json")))
    scelti = sys.argv[1:] or tutti
    totale = 0
    for f in scelti:
        altri = set()
        for g in tutti:
            if Path(g).resolve() != Path(f).resolve():
                try:
                    altri |= {x.get("id") for x in json.loads(Path(g).read_text(encoding="utf-8")) if isinstance(x, dict)}
                except ValueError:
                    pass
        errori = controlla(f, altri)
        totale += len(errori)
        print(Path(f).name, "ok" if not errori else f"{len(errori)} ERRORI")
        for e in errori[:40]:
            print("  -", e)
    print("ERRORI", totale)


if __name__ == "__main__":
    main()
