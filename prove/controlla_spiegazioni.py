"""Controlla che ogni spiegazione stia sotto la domanda giusta: confronta il significato della domanda con quello
della spiegazione (modello locale) e segnala le coppie troppo lontane. Uso: ./venv/bin/python prove/controlla_spiegazioni.py"""
import glob
import json
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
domande = {}
for f in glob.glob(str(ROOT / "prove_passate" / "*.json")) + glob.glob(str(ROOT / "contenuti_v2/domande/*.json")) + \
        [str(ROOT / "banca_domande.json")]:
    dati = json.loads(Path(f).read_text())
    for d in (dati.get("domande", []) if isinstance(dati, dict) else dati if isinstance(dati, list) else []):
        if isinstance(d, dict) and d.get("id"):
            domande[d["id"]] = d
spieg = {}
for f in glob.glob(str(ROOT / "prove_passate/spiegazioni_*.json")) + glob.glob(str(ROOT / "spiegazioni_pronte/lotto_*.json")):
    spieg.update(json.loads(Path(f).read_text()))
ids = [i for i in spieg if i in domande]
modello = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", device="cpu")
a = modello.encode([domande[i]["domanda"] + " " + " ".join((domande[i].get("opzioni") or {}).values()) for i in ids],
                   normalize_embeddings=True, batch_size=64)
b = modello.encode([spieg[i].get("perche", "") for i in ids], normalize_embeddings=True, batch_size=64)
sim = (a * b).sum(1)
# Confronto con la spiegazione della domanda vicina: se quella è più simile, la spiegazione è probabilmente spostata.
sospette = []
for k, i in enumerate(ids):
    if sim[k] < 0.25:
        sospette.append((float(sim[k]), i, domande[i]["domanda"][:80], spieg[i].get("concetto", "")))
print(f"spiegazioni controllate: {len(ids)} — senza domanda: {len(spieg) - len(ids)} — sospette: {len(sospette)}")
for s in sorted(sospette)[:40]:
    print(f"  {s[0]:.2f} {s[1]} | {s[2]} | {s[3]}")
