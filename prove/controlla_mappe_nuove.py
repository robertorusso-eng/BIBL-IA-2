"""Controlla i file delle mappe dei capitoli (mappe/nuove_*_mappe.json): capitoli esistenti, due livelli, collegamenti
completi, mappa tutta collegata al concetto centrale (il nome del capitolo), nessun riferimento ai libri.
Uso: ./venv/bin/python prove/controlla_mappe_nuove.py file ..."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import dati_v2 as D  # noqa: E402

CAPITOLI = {c for capitoli in D.ARGOMENTI.values() for c in capitoli}
PROIBITE = re.compile(r"\blibr[oi] di testo\b|secondo il (?:libro|testo)|nel (?:libro|testo)\b|\bmanuale\b|capitolo \d", re.I)
MISURE = {"superiore": (12, 30), "universita": (16, 40)}


def main():
    totale = 0
    for f in sys.argv[1:]:
        errori = []
        dati = json.loads(Path(f).read_text(encoding="utf-8"))
        for capitolo, voce in dati.items():
            if capitolo not in CAPITOLI:
                errori.append(f"{capitolo!r}: non è un capitolo di nessuna materia")
            for livello, (minimo, massimo) in MISURE.items():
                rel = voce.get(livello)
                if not isinstance(rel, list) or not minimo <= len(rel) <= massimo:
                    errori.append(f"{capitolo}/{livello}: servono da {minimo} a {massimo} collegamenti")
                    continue
                if any(not isinstance(r, dict) or not all(str(r.get(k, "")).strip() for k in ("da", "relazione", "a"))
                       for r in rel):
                    errori.append(f"{capitolo}/{livello}: ogni collegamento vuole «da», «relazione» e «a»")
                    continue
                lungo = lambda c: len(c) > 80 and c != capitolo   # il nome del capitolo può essere lungo
                if any(lungo(r["da"]) or lungo(r["a"]) or len(r["relazione"]) > 45 for r in rel):
                    errori.append(f"{capitolo}/{livello}: concetti (max 80) o frasi sulle frecce (max 45) troppo lunghi")
                if rel[0]["da"] != capitolo:
                    errori.append(f"{capitolo}/{livello}: il primo collegamento deve partire dal nome del capitolo")
                raggiunti, cambiato = {capitolo}, True
                while cambiato:
                    cambiato = False
                    for r in rel:
                        if r["da"] in raggiunti and r["a"] not in raggiunti:
                            raggiunti.add(r["a"])
                            cambiato = True
                staccati = {r["da"] for r in rel} - raggiunti
                if staccati:
                    errori.append(f"{capitolo}/{livello}: concetti non collegati al centro: {sorted(staccati)[:3]}")
            m = PROIBITE.search(json.dumps(voce, ensure_ascii=False))
            if m:
                errori.append(f"{capitolo}: parola non ammessa {m.group()!r}")
        totale += len(errori)
        print(Path(f).name, f"{len(dati)} capitoli", "ok" if not errori else f"{len(errori)} ERRORI")
        for e in errori[:40]:
            print("  -", e)
    print("ERRORI", totale)


if __name__ == "__main__":
    main()
