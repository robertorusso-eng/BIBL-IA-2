"""Unisce le parti controllate nei file principali: ./venv/bin/python mappe/parti/unisci.py 1 2 ..."""
import json, sys
from pathlib import Path
cart = Path(__file__).resolve().parent
P, S = cart.parent / "percorsi.json", cart.parent / "schede.json"
per, sch = json.loads(P.read_text()), json.loads(S.read_text())
for n in sys.argv[1:]:
    nuovi_p = json.loads((cart / f"percorsi_{n}.json").read_text())
    nuove_s = json.loads((cart / f"schede_{n}.json").read_text())
    per.update(nuovi_p)
    aggiunte = {k: v for k, v in nuove_s.items() if k not in sch}
    sch.update(aggiunte)
    print(f"parte {n}: {len(nuovi_p)} percorsi, {len(aggiunte)} schede nuove ({len(nuove_s) - len(aggiunte)} già presenti, lasciate com'erano)")
    # Argomenti nuovi: mappe pronte e mappe semplici della parte.
    if (cart / f"pronte_{n}.json").exists():
        R, B = cart.parent / "mappe_pronte.json", cart.parent / "mappe_base.json"
        pronte, base = json.loads(R.read_text()), json.loads(B.read_text())
        presenti = {m["argomento"] for m in pronte}
        nuove = [m for m in json.loads((cart / f"pronte_{n}.json").read_text()) if m["argomento"] not in presenti]
        base.update(json.loads((cart / f"base_{n}.json").read_text()))
        R.write_text(json.dumps(pronte + nuove, ensure_ascii=False, indent=1))
        B.write_text(json.dumps(base, ensure_ascii=False, indent=1))
        print(f"parte {n}: {len(nuove)} mappe pronte nuove")
P.write_text(json.dumps(per, ensure_ascii=False, indent=1))
S.write_text(json.dumps(sch, ensure_ascii=False, indent=1))
