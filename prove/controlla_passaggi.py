"""Controlla che nei file indicati sia stato aggiunto SOLO il campo «passaggi» (3-6 passi senza numeri davanti)
rispetto alla versione salvata in git, e conta le domande che non li hanno ancora.
Uso: ./venv/bin/python prove/controlla_passaggi.py file1.json [file2.json ...]"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUMERO = re.compile(r"^\s*\d+[.)]\s")
PROIBITE = re.compile(r"secondo il (?:libro|testo)|nel (?:libro|testo)\b|\bmanuale\b|capitolo \d", re.I)


def voci(dati):
    if isinstance(dati, dict):
        return dati.items()
    return ((d.get("id"), d) for d in dati if isinstance(d, dict))


def main():
    totale_errori = 0
    for f in sys.argv[1:]:
        p = Path(f).resolve()
        rel = p.relative_to(ROOT)
        prima = json.loads(subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True,
                                          check=True).stdout)
        dopo = json.loads(p.read_text(encoding="utf-8"))
        errori, mancano = [], 0
        vecchie = dict(voci(prima))
        nuove = dict(voci(dopo))
        if set(vecchie) != set(nuove):
            errori.append("l'elenco delle domande è cambiato (aggiunte o tolte)")
        for k, v in nuove.items():
            w = vecchie.get(k, {})
            for campo in set(v) | set(w):
                if campo != "passaggi" and v.get(campo) != w.get(campo):
                    errori.append(f"{k}: cambiato il campo {campo}")
            passi = v.get("passaggi") or []
            if not passi:
                mancano += 1
                continue
            if passi == w.get("passaggi"):
                continue        # c'erano già: non si ricontrollano
            if not isinstance(passi, list) or not 3 <= len(passi) <= 6 or any(not isinstance(x, str) or len(x) < 6 for x in passi):
                errori.append(f"{k}: «passaggi» deve avere 3-6 passi")
            elif any(NUMERO.match(x) for x in passi) and not w.get("passaggi"):
                errori.append(f"{k}: niente numeri davanti ai passi")
            elif PROIBITE.search(" ".join(passi)):
                errori.append(f"{k}: parola non ammessa nei passaggi")
        totale_errori += len(errori)
        print(rel, f"senza passaggi: {mancano}", "ok" if not errori else f"{len(errori)} ERRORI")
        for e in errori[:30]:
            print("  -", e)
    print("ERRORI", totale_errori)


if __name__ == "__main__":
    main()
