"""Controlla una parte: ./venv/bin/python mappe/parti/controlla.py N"""
import json, sys
from pathlib import Path
from rdkit import Chem
cart = Path(__file__).resolve().parent
n = sys.argv[1]
per = json.loads((cart / f"percorsi_{n}.json").read_text())
sch = json.loads((cart / f"schede_{n}.json").read_text())
tutte = {**json.loads((cart.parent / "schede.json").read_text()), **sch}
pronte = {m["argomento"] for m in json.loads((cart.parent / "mappe_pronte.json").read_text())}
errori = []
# Argomenti nuovi: la mappa pronta e la mappa semplice stanno nella parte (pronte_N.json, base_N.json).
if (cart / f"pronte_{n}.json").exists():
    nuove = json.loads((cart / f"pronte_{n}.json").read_text())
    pronte |= {m["argomento"] for m in nuove}
    base = json.loads((cart / f"base_{n}.json").read_text()) if (cart / f"base_{n}.json").exists() else {}
    for m in nuove:
        for c in ("argomento", "categoria", "parole", "relazioni", "fonti"):
            if c not in m: errori.append(f"mappa pronta {m.get('argomento')}: manca {c}")
        if not 10 <= len(m.get("relazioni", [])) <= 25: errori.append(f"mappa pronta {m['argomento']}: servono 10-25 relazioni")
        for x in m.get("relazioni", []):
            if set(x) != {"da", "relazione", "a"}: errori.append(f"mappa pronta {m['argomento']}: relazione malformata")
        righe = base.get(m["argomento"].lower())
        if not righe or not 9 <= len(righe) <= 14 or any(len(r) != 3 for r in righe):
            errori.append(f"mappa semplice {m['argomento'].lower()}: servono 9-14 righe [da, relazione, a]")
        if m["argomento"] not in per: errori.append(f"mappa pronta {m['argomento']}: manca il percorso")
for k in per:
    if k not in pronte: errori.append(f"argomento non tra le mappe pronte: {k}")
for k, v in sch.items():
    for c in ("tipo", "base", "superiore", "universita", "clinica"):
        if c not in v: errori.append(f"scheda {k}: manca {c}")
    if v.get("tipo") not in ("zucchero", "molecola", "enzima", "energia", "coenzima", "piccola", "struttura"):
        errori.append(f"scheda {k}: tipo sbagliato")
    if v.get("smiles") and Chem.MolFromSmiles(v["smiles"]) is None: errori.append(f"smiles non valido: {k}")
for k, p in per.items():
    for c in ("titolo", "dove", "inizio", "intro", "passaggi", "bilancio"):
        if c not in p: errori.append(f"{k}: manca {c}")
    nomi = [p.get("inizio")]
    for x in p.get("passaggi", []) + (p.get("dopo") or {}).get("strade", []):
        for c in ("da", "a", "enzima", "entra", "esce", "nota"):
            if c not in x: errori.append(f"{k}: passaggio senza {c}")
        da = x.get("da"); a = x.get("a")
        nomi += (da if isinstance(da, list) else [da]) + (a if isinstance(a, list) else [a]) + [x.get("enzima")] + x.get("entra", []) + x.get("esce", [])
    for b in p.get("da_sapere", []):
        for _, ns in b["voci"]: nomi += ns
    for nome in nomi:
        if nome and nome not in tutte: errori.append(f"{k}: «{nome}» non ha una scheda")
print("\n".join(sorted(set(errori))) or "OK")
