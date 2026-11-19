"""Apre tutte le pagine di BIBL-IA 2 con il profilo di ogni studente virtuale (prove/studenti/*.json) e controlla
che nessuna vada in errore. Il profilo si usa su una copia temporanea: né quello vero né quelli degli studenti
cambiano. Uso: ./venv/bin/python prove/prova_pagine_studenti.py [quanti studenti]"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
STUDENTI = sorted((ROOT / "prove" / "studenti").glob("s*.json"))
# Due studenti nuovi senza piano (profilo vuoto e solo il nome): aprono anche gli strumenti e le pagine informative.
NUOVI = {"zz_vuoto": {}, "zz_libero": {"nome": "Libero", "lingua": "it"}}
ALTRE_PAGINE = ["pagina_biblioteca", "modelli_3d", "reazioni_chimiche", "laboratorio", "mini_giochi", "aiuto", "guida",
                "abbonamenti", "valuta_sito", "area_docenti", "pagina_malattie", "pagina_ricerche"]
PAGINE = ["dashboard", "statistiche", "ripasso_intelligente", "pagina_mappe", "pagina_impostazioni", "esercitati",
          "simulazione", "documenti_ai", "pagina_materie", "pagina_traguardi", "pagina_segnalibri", "tutor_ai",
          "_percorso:3", "_percorso:4", "pagina_strumenti"]

sorgente = (ROOT / "bibl_ia_2.py").read_text(encoding="utf-8").replace("\nmain()\n", "\n")


def script(file_profilo, pagina):
    funzione, _, passo = pagina.partition(":")
    testa = (f"import sys as _sys\n_sys.path.insert(0, {str(ROOT)!r})\n"
             f"__file__ = {str(ROOT / 'bibl_ia_2.py')!r}\n")
    return testa + sorgente + f'''
import json as _json
if "p" not in st.session_state:
    st.session_state["_file_profilo"] = {str(file_profilo)!r}
    st.session_state["p"] = _json.load(open({str(file_profilo)!r}, encoding="utf-8"))
    st.session_state["lingua"] = st.session_state["p"].get("lingua", "it")
    if {passo!r}:
        st.session_state["p"]["passo"] = int({passo!r})
        _prossima = prossima_sessione(st.session_state["p"].get("piano") or [])
        if _prossima:
            st.session_state["p"]["sessione"] = list(_prossima)
for _nome in ["dashboard", "percorso", "ripasso", "tutor", "materie", "mappe", "esercitati", "segnalibri", "docenti",
              "simulazione", "statistiche", "traguardi", "documenti", "valuta", "impostazioni", "abbonamenti",
              "strumenti", "giochi", "biblioteca", "modelli3d", "reazioni", "laboratorio", "aiuto", "malattie", "ricerche", "classe"]:
    PAGINE[_nome] = st.Page(lambda: None, title=_nome, url_path=_nome)
st.navigation(list(PAGINE.values()), position="hidden")
# I componenti speciali (mappa da toccare, voce) non si possono creare nella prova: qui restituiscono il valore vuoto.
componenti.declare_component = lambda *_a, **_k: (lambda *_a2, **_k2: _k2.get("default"))
{funzione}()
'''


def main():
    quanti = int(sys.argv[1]) if len(sys.argv) > 1 else len(STUDENTI)
    errori = []
    cartella = Path(tempfile.mkdtemp())
    for nome, dati in NUOVI.items():
        (cartella / f"{nome}.json").write_text(json.dumps(dati), encoding="utf-8")
    elenco = [(f, PAGINE) for f in STUDENTI[:quanti]] + [(cartella / f"{n}.json", PAGINE + ALTRE_PAGINE) for n in NUOVI]
    for f, pagine in elenco:
        for pagina in pagine:
            copia = cartella / f"copia_{f.stem}.json"
            shutil.copy(f, copia)
            at = AppTest.from_string(script(copia, pagina), default_timeout=120)
            try:
                at.run()
            except Exception as e:  # anche un errore del motore di prova conta
                errori.append((f.stem, pagina, repr(e)[:300]))
                continue
            for e in at.exception:
                errori.append((f.stem, pagina, (e.message or "")[:300] + " | " + " / ".join(e.stack_trace[-2:])[:400]))
        print(f.stem, "ok" if not [x for x in errori if x[0] == f.stem] else "ERRORI", flush=True)
    print("\nERRORI", len(errori))
    for x in errori:
        print(" -", x)


if __name__ == "__main__":
    main()
