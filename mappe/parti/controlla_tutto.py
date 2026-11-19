"""Controllo di tutte le mappe unite: ./venv/bin/python mappe/parti/controlla_tutto.py [R ...]
Con i numeri R controlla le mappe come sarebbero dopo le revisioni mappe/parti/revisione_R.json."""
import json
import sys
from pathlib import Path
cart = Path(__file__).resolve().parent.parent
per = json.loads((cart / "percorsi.json").read_text())
sch = json.loads((cart / "schede.json").read_text())
pronte = {m["argomento"]: m for m in json.loads((cart / "mappe_pronte.json").read_text())}
for n in sys.argv[1:]:
    rev = json.loads((cart / "parti" / f"revisione_{n}.json").read_text())
    per.update({k: v for k, v in rev.get("percorsi", {}).items() if k in per})
    sch.update(rev.get("schede", {}))
errori = []
for k, p in per.items():
    if k not in pronte: errori.append(f"{k}: manca la mappa pronta")
    nomi = [p.get("inizio")]
    for x in p.get("passaggi", []) + (p.get("dopo") or {}).get("strade", []):
        for c in ("da", "a", "enzima", "entra", "esce"):
            v = x.get(c) or []
            nomi += v if isinstance(v, list) else [v]
    for b in p.get("da_sapere", []):
        for _, ns in b["voci"]: nomi += ns
    errori += [f"{k}: «{n}» non ha una scheda" for n in nomi if n and n not in sch]
for k, v in sch.items():
    for c in ("tipo", "base", "superiore", "universita", "clinica"):
        if c not in v: errori.append(f"scheda {k}: manca {c}")
print("\n".join(sorted(set(errori))) or f"OK: {len(per)} percorsi, {len(sch)} schede")
