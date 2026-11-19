"""Applica una revisione delle mappe: ./venv/bin/python mappe/parti/applica_revisione.py R ...
mappe/parti/revisione_R.json = {"percorsi": {nome: percorso intero}, "schede": {nome: scheda intera},
"pronte": {argomento: mappa pronta intera}, "base": {argomento in minuscolo: righe}}: ogni voce
sostituisce quella che c'è (o si aggiunge, per le schede nuove)."""
import json, sys
from pathlib import Path
cart = Path(__file__).resolve().parent
P, S, R, B = (cart.parent / f for f in ("percorsi.json", "schede.json", "mappe_pronte.json", "mappe_base.json"))
per, sch, pronte, base = (json.loads(f.read_text()) for f in (P, S, R, B))
for n in sys.argv[1:]:
    rev = json.loads((cart / f"revisione_{n}.json").read_text())
    ignoti = [k for k in rev.get("percorsi", {}) if k not in per]
    per.update({k: v for k, v in rev.get("percorsi", {}).items() if k in per})
    sch.update(rev.get("schede", {}))
    for m in pronte:
        if m["argomento"] in rev.get("pronte", {}):
            m.update(rev["pronte"][m["argomento"]], argomento=m["argomento"])
    base.update({k: v for k, v in rev.get("base", {}).items() if k in base})
    print(f"revisione {n}: {len(rev.get('percorsi', {})) - len(ignoti)} percorsi, {len(rev.get('schede', {}))} schede, "
          f"{len(rev.get('pronte', {}))} mappe pronte, {len(rev.get('base', {}))} mappe semplici"
          + (f"; percorsi sconosciuti ignorati: {ignoti}" if ignoti else ""))
P.write_text(json.dumps(per, ensure_ascii=False, indent=1))
S.write_text(json.dumps(sch, ensure_ascii=False, indent=1))
R.write_text(json.dumps(pronte, ensure_ascii=False, indent=1))
B.write_text(json.dumps(base, ensure_ascii=False, indent=1))
