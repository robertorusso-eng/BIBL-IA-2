"""Le lezioni di BIBL-IA 2 per tutte le materie e i temi di BIBL-IA 1.

Per ogni tema si prendono le domande guida che hanno già la risposta pronta dei libri e si raggruppano per
significato (circa 6 domande per lezione): ogni gruppo diventa una lezione, con il titolo fatto dai
concetti che contiene. Il risultato va in lezioni_v2.json. Si lancia con:
./venv/bin/python prepara_lezioni_v2.py
"""
import json
import math
import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parent


def concetto(domanda):
    """«Che cos'è il glicogeno?» → «glicogeno»; altrimenti la domanda accorciata."""
    m = re.match(r"^(?:che cos['’]è|cos['’]è|cosa (?:si intende per|è)|che cosa sono|cosa sono|chi (?:è|era)|"
                 r"a cosa serve|come (?:funziona|si)|qual è|quali sono)\s+(?:(?:il|lo|la|l['’]|i|gli|le|un|una|uno)\s*)?"
                 r"(.+?)\?*$", domanda.strip(), re.I)
    testo = (m.group(1) if m else domanda).strip(" ?\"'«»")
    return testo if len(testo) <= 40 else testo[:38].rsplit(" ", 1)[0] + "…"


def prima_frase(voce, traduzioni):
    """La prima frase della risposta dei libri (in italiano se è già tradotta): dice di cosa parla davvero."""
    import hashlib
    m = re.search(r"«([^»]{25,})»", voce["risposta"])
    if not m:
        return ""
    return traduzioni.get(f"it:{hashlib.sha1(m.group(1).encode()).hexdigest()}", m.group(1))[:300]


def e_definizione(domanda):
    return bool(re.match(r"^(?:che cos['’]è|cos['’]è|cosa (?:si intende per|è)|che cosa sono|cosa sono)\s", domanda, re.I))


def main():
    guida = json.loads((ROOT / "domande_guida.json").read_text(encoding="utf-8"))
    risposte = {v["domanda"]: v for v in json.loads((ROOT / "risposte_pronte.json").read_text(encoding="utf-8"))}
    pronte = set(risposte)
    traduzioni = json.loads((ROOT / "traduzioni.json").read_text(encoding="utf-8"))
    modello = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", device="cpu")
    materie = {}
    for voce in guida:
        if voce["domanda"] in pronte:
            materie.setdefault(voce["materia"], {}).setdefault(voce["tema"], []).append(voce["domanda"])
    lezioni = []
    for materia, temi in materie.items():
        for tema, domande in temi.items():
            domande = list(dict.fromkeys(domande))
            gruppi = max(1, round(len(domande) / 6))
            if gruppi == 1:
                etichette = [0] * len(domande)
            else:
                # Si raggruppa per quello che dicono le risposte, non per la forma della domanda
                # («Che cos'è…?» si somigliano tutte).
                testi = [f"{concetto(d)}: {prima_frase(risposte[d], traduzioni)}" for d in domande]
                vettori = modello.encode(testi, normalize_embeddings=True)
                etichette = KMeans(n_clusters=gruppi, n_init=10, random_state=0).fit_predict(vettori).tolist()
            ordine = sorted(set(etichette), key=lambda g: etichette.index(g))
            blocchi = []
            for g in ordine:
                elenco = [d for d, e in zip(domande, etichette) if e == g]
                # Lezioni di al massimo 8 domande.
                blocchi += [elenco[i:i + 8] for i in range(0, len(elenco), 8)]
            for n, elenco in enumerate(blocchi, 1):
                concetti = list(dict.fromkeys(concetto(d) for d in elenco if e_definizione(d)))
                if concetti:
                    titolo = ", ".join(concetti[:3]) + ("…" if len(concetti) > 3 else "")
                    titolo = titolo[:1].upper() + titolo[1:]
                else:
                    titolo = f"Approfondimento {n}"
                lezioni.append({"materia": materia, "tema": tema, "numero": n, "titolo": titolo, "domande": elenco})
            print(f"{materia} › {tema}: {len(domande)} domande, {len(ordine)} lezioni", flush=True)
    (ROOT / "lezioni_v2.json").write_text(json.dumps(lezioni, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(lezioni)} lezioni in lezioni_v2.json")


if __name__ == "__main__":
    main()
