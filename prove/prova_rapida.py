"""Prova rapida di BIBL-IA 2: esegue le funzioni principali senza aprire il sito e dice che cosa non va.
Si lancia con: ./venv/bin/python prove/prova_rapida.py   (qualche minuto; stampa ERRORI 0 se va tutto bene)"""
import random
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import streamlit as st  # noqa: E402

sorgente = (ROOT / "bibl_ia_2.py").read_text().replace("\nmain()\n", "\n")
g = {"__name__": "prova", "__file__": str(ROOT / "bibl_ia_2.py")}
exec(compile(sorgente, "bibl_ia_2.py", "exec"), g)
errori = []


def prova(nome, f):
    try:
        f()
    except Exception:
        errori.append((nome, traceback.format_exc()[-600:]))


def controlla(cond, messaggio):
    if not cond:
        errori.append((messaggio, ""))


# Profilo di prova (in memoria: il profilo vero non si tocca).
g["profilo"] = lambda: st.session_state.setdefault("p_prova", {"stato": "test", "corso": "Medicina e Chirurgia",
                                                                 "test": "Semestre filtro", "punti": 0})
g["salva"] = lambda: None

banca = g["banca"]()
print("domande nella banca:", len(banca))
materie = {m: sum(d["materia"] == m for d in banca) for m in g["MATERIE_BANCA"]}
print("per materia:", materie)
for m, n in materie.items():
    controlla(n >= 40, f"poche domande di {m}: {n}")
pronte = g["spiegazioni_pronte"]()
senza = [d["id"] for d in banca if d["id"] not in pronte]
print("domande senza spiegazione:", len(senza), senza[:3])
controlla(len(senza) == 0, "domande senza spiegazione")

# Correzione: risposta multipla e completamento.
for d in banca:
    if d.get("tipo") == "completamento":
        controlla(g["e_giusta"](d, d["risposta"]), f"completamento non accetta la sua risposta: {d['id']}")
        controlla(not g["e_giusta"](d, "zzzz"), f"completamento accetta qualsiasi cosa: {d['id']}")
    else:
        controlla(d["giusta"] in d["opzioni"], f"lettera giusta non tra le opzioni: {d['id']}")
        controlla(g["e_giusta"](d, d["giusta"]), f"risposta giusta non riconosciuta: {d['id']}")

# Simulazioni: ogni test ha abbastanza domande per sezione.
for nome, t in g["D"].TEST.items():
    for sez, q, minuti, materia in t["sezioni"]:
        if materia:
            trovate = g["domande"](materia, quante=q, seme=1)
            controlla(len(trovate) == q, f"{nome} › {sez}: {len(trovate)} domande su {q}")
    if t.get("completamento"):
        for sez, q, minuti, materia in t["sezioni"]:
            n = len(g["domande"](materia, quante=t["completamento"], seme=1, tipo="completamento"))
            controlla(n == t["completamento"], f"{nome} › {sez}: completamento {n} su {t['completamento']}")

# Lezioni: testo nostro, quiz da 10.
riscritte = g["lezioni_riscritte"]()
lezioni = g["lezioni_materie"]()
print("lezioni riscritte:", len(riscritte), "su", len(lezioni))
for lez in random.Random(1).sample(lezioni, 15):
    prova(f"quiz {lez['titolo']}", lambda lez=lez: controlla(len(g["quiz_lezione"](lez, 10)) >= 5,
                                                              f"quiz corto: {lez['titolo']}"))

# Esami universitari.
print("domande d'esame:", len(g["banca_esami"]()))
for esame in ["Anatomia umana I", "Analisi matematica I", "Farmacologia", "Scienza delle costruzioni", "Fisiologia"]:
    prova(f"esame {esame}", lambda e=esame: controlla(len(g["domande_esame"](e, 10, 1)) == 10, f"esame corto: {e}"))

# Biblioteca: risposte solo dai testi di BIBL-IA, mai dai libri.
LIBRI = re.compile(r"\b(pagina|pag\.|capitolo \d|paragrafo \d|\.pdf|edizione|editore)\b", re.I)
for domanda in ["che cos'è l'emoglobina?", "come funziona la glicolisi?", "che cos'è il pH?", "legge di Ohm",
                "che cos'è la mitosi?"]:
    def chiedi(domanda=domanda):
        trovati = g["risposta_con_fonti"](domanda)
        controlla(trovati, f"nessuna risposta: {domanda}")
        for testo, fonte in trovati:
            controlla(not LIBRI.search(testo + fonte), f"riferimento a un libro nella risposta: {domanda}")
        print("  ", domanda, "→", trovati[0][1] if trovati else "—")
    prova(f"biblioteca {domanda}", chiedi)

# Laboratorio e 3D.
C = g["C"]
for a in C.tutti_i_reagenti():
    controlla(C.cerca(a), f"reagente senza reazione: {a}")
for n in C.IMPIANTI:
    prova(f"impianto {n}", lambda n=n: g["dot_impianto"](C.IMPIANTI[n]["unita"], C.IMPIANTI[n]["correnti"]))
prova("organi", lambda: [g["modelli3d"].html_organo(o["nome"]) for o in g["modelli3d"].elenco_organi()[:5]])

print("ERRORI", len(errori))
for nome, testo in errori[:40]:
    print("==", nome, testo)
