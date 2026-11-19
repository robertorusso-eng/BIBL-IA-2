"""Controlla i file delle lezioni dei capitoli (mappe/nuove_*_studio.json): capitoli esistenti, due livelli,
parti complete, nessun riferimento ai libri. Uso: ./venv/bin/python prove/controlla_lezioni_nuove.py file ..."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import dati_v2 as D  # noqa: E402

CAPITOLI = {c for capitoli in D.ARGOMENTI.values() for c in capitoli}
ESCLUSE = ROOT / ".parole_escluse.txt"
PROIBITE = re.compile("|".join([r"\blibr[oi] di testo\b", r"secondo il (?:libro|testo)", r"nel (?:libro|testo)\b",
                                r"\bmanuale\b", r"capitolo \d"] + ([r.strip() for r in ESCLUSE.read_text().splitlines()
                                                                    if r.strip()] if ESCLUSE.exists() else [])), re.I)
MISURE = {"spiegazione": (4, 7), "metodo": (4, 8), "ricorda": (3, 5), "errori": (3, 6), "domande": (4, 7)}


def main():
    errori_totali = 0
    for f in sys.argv[1:]:
        errori = []
        try:
            dati = json.loads(Path(f).read_text(encoding="utf-8"))
        except ValueError as e:
            print(f, "JSON non valido:", e)
            errori_totali += 1
            continue
        for capitolo, voce in dati.items():
            if capitolo not in CAPITOLI:
                errori.append(f"{capitolo!r}: non è un capitolo di nessuna materia")
            for livello in ("superiore", "universita"):
                v = voce.get(livello)
                if not isinstance(v, dict):
                    errori.append(f"{capitolo}: manca il livello {livello}")
                    continue
                for parte, (minimo, massimo) in MISURE.items():
                    x = v.get(parte)
                    if not isinstance(x, list) or not minimo <= len(x) <= massimo:
                        errori.append(f"{capitolo}/{livello}: «{parte}» deve avere da {minimo} a {massimo} elementi")
                    elif parte == "domande" and any(not isinstance(q, dict) or not q.get("domanda") or not q.get("risposta") for q in x):
                        errori.append(f"{capitolo}/{livello}: ogni domanda deve avere «domanda» e «risposta»")
                    elif parte != "domande" and any(not isinstance(s, str) or len(s) < 20 for s in x):
                        errori.append(f"{capitolo}/{livello}: elementi di «{parte}» vuoti o troppo corti")
                if sum(len(s) for s in v.get("spiegazione", []) if isinstance(s, str)) < 1500:
                    errori.append(f"{capitolo}/{livello}: spiegazione troppo corta (almeno 1500 caratteri in tutto)")
            m = PROIBITE.search(json.dumps(voce, ensure_ascii=False))
            if m:
                errori.append(f"{capitolo}: parola non ammessa {m.group()!r}")
        errori_totali += len(errori)
        print(Path(f).name, f"{len(dati)} capitoli", "ok" if not errori else f"{len(errori)} ERRORI")
        for e in errori[:40]:
            print("  -", e)
    print("ERRORI", errori_totali)


if __name__ == "__main__":
    main()
