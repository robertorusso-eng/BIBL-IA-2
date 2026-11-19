"""Prepara in anticipo le risposte della Biblioteca di BIBL-IA 2 (risposte_pronte_v2.json), con le ricerche di
università e centri di ricerca: quando uno studente fa una di queste domande (o una quasi uguale) la risposta
arriva subito. Gira sul Mac con l'AI del Mac (Ollama); per le ricerche serve internet (si inviano solo le parole
dell'argomento a Europe PMC). Si può fermare e rilanciare: le domande già pronte si saltano.

Uso: ./venv/bin/python -I prepara_risposte_v2.py [quante domande al massimo]
"""
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "prove"))

import dati_v2 as D  # noqa: E402
import prova_pagine_studenti as P  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

PRONTE = ROOT / "risposte_pronte_v2.json"
GRUPPO = 10          # domande per ogni giro (se un giro si blocca, si perde poco)


def domande_da_preparare():
    """Le domande già fatte a BIBL-IA, quelle del collaudo e una per ogni capitolo di ogni materia."""
    domande = []
    for f in ("domande_biblioteca_v2.json", "domande_frequenti_esempi.json"):
        try:
            domande += [v["domanda"] for v in json.loads((ROOT / f).read_text(encoding="utf-8"))
                        if v.get("frasi", 1) and len(v["domanda"].split()) >= 2]
        except (OSError, ValueError):
            pass
    for capitoli in D.ARGOMENTI.values():
        for c in capitoli:
            domande.append(f"Spiegami {c[0].lower() + c[1:]}")
    visti, uniche = set(), []
    for d in domande:
        k = " ".join(d.casefold().split())
        if k not in visti:
            visti.add(k)
            uniche.append(d.strip())
    return uniche


def gia_pronte():
    try:
        return {v.get("domanda", "").casefold() for v in json.loads(PRONTE.read_text(encoding="utf-8")).values()
                if v.get("risposta") and "ricerche" in v}
    except (OSError, ValueError):
        return set()


def main():
    massimo = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
    da_fare = [d for d in domande_da_preparare() if d.casefold() not in gia_pronte()][:massimo]
    print(f"Da preparare: {len(da_fare)} domande", flush=True)
    studente = sorted((ROOT / "prove" / "studenti").glob("s*.json"))[0]
    copia = Path(tempfile.mkdtemp()) / "profilo.json"
    shutil.copy(studente, copia)          # un profilo di prova su una copia: nessun profilo vero cambia
    fatte = 0
    for inizio in range(0, len(da_fare), GRUPPO):
        gruppo = da_fare[inizio:inizio + GRUPPO]
        codice = P.script(copia, "prepara_gruppo").replace("prepara_gruppo()", f'''
def prepara_gruppo():
    import time as _t
    for d in {gruppo!r}:
        spiegata, trovati = prepara_risposta(d, "it")
        if not spiegata:
            print("  (niente nei testi)", d, flush=True)
            continue
        articoli = ricerche_per_domanda(d)
        salva_risposta_pronta(d, lingua="it", risposta=spiegata, fonti=[list(x) for x in trovati], ricerche=articoli,
                              dalle_ricerche=sintesi_ricerche(d, articoli) if articoli else "")
        print("  ok", len(articoli), "ricerche ·", d, flush=True)
        _t.sleep(1)
prepara_gruppo()''')
        try:
            prova = AppTest.from_string(codice, default_timeout=3600).run()
            for e in prova.exception:
                print("  ERRORE:", e.value, flush=True)
        except Exception as errore:            # un giro bloccato non ferma tutto
            print("  ERRORE nel giro:", errore, flush=True)
        fatte += len(gruppo)
        print(f"[{time.strftime('%H:%M')}] {fatte}/{len(da_fare)}", flush=True)
    shutil.rmtree(copia.parent, ignore_errors=True)
    print("Fatto.", flush=True)


if __name__ == "__main__":
    main()
