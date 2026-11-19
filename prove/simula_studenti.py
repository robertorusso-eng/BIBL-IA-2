"""Studenti virtuali per provare BIBL-IA 2 dall'inizio alla fine, con le vere funzioni dell'app.

Ogni studente ha una bravura (probabilità di rispondere giusto), che cambia un po' da materia a materia e cresce
quando studia un argomento. Fa il test di livello, riceve il piano, poi studia giorno per giorno: ripasso degli
errori, lezioni del piano (si va avanti solo con il quiz al 100%), Flash Review e verifiche del recupero
intelligente, «Rifai gli errori» e una simulazione del test ogni settimana.

Per ogni studente scrive una cartella sulla Scrivania («Prove studenti BIBL-IA/<numero nome>») con il piano, il
diario giorno per giorno e il resoconto, e il profilo in prove/studenti/<id>.json (per le foto con il server
delle prove: http://localhost:8768/?studente=<id>). Il profilo vero non si tocca.

Uso: ./venv/bin/python prove/simula_studenti.py [quanti] [inizio]"""
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import streamlit as st  # noqa: E402

sorgente = (ROOT / "bibl_ia_2.py").read_text().replace("\nmain()\n", "\n")
g = {"__name__": "simula", "__file__": str(ROOT / "bibl_ia_2.py")}
exec(compile(sorgente, "bibl_ia_2.py", "exec"), g)
D = g["D"]

SCRIVANIA = Path.home() / "Desktop" / "Prove studenti BIBL-IA"
STUDENTI = ROOT / "prove" / "studenti"
STUDENTI.mkdir(parents=True, exist_ok=True)

NOMI = ["Luca", "Giulia", "Marco", "Sofia", "Matteo", "Chiara", "Andrea", "Sara", "Davide", "Martina", "Lorenzo",
        "Alessia", "Simone", "Elena", "Federico", "Aurora", "Gabriele", "Francesca", "Tommaso", "Beatrice", "Riccardo",
        "Ginevra", "Pietro", "Noemi", "Edoardo", "Camilla", "Filippo", "Arianna", "Nicolò", "Anna"]
TEST_CORSO = [("Medicina e Chirurgia", "Semestre filtro"), ("Professioni sanitarie", "Test delle professioni sanitarie"),
              ("Ingegneria", "TOLC-I"), ("Farmacia e CTF", "TOLC-F"), ("Scienze biologiche", "TOLC-B"),
              ("Chimica", "TOLC-S"), ("Economia", "TOLC-E"), ("Psicologia", "TOLC-PSI"),
              ("Medicina Veterinaria", "Semestre filtro"), ("Architettura", "Test di Architettura")]
# I tre profili chiesti per primi, poi livelli diversi a rotazione.
BRAVURE = [("Bravissimo", 0.88), ("Medio-scarso", 0.47), ("Debole", 0.25), ("Buono", 0.72), ("Medio", 0.58),
           ("Scarso", 0.36), ("Eccellente", 0.94), ("Discreto", 0.65), ("Molto debole", 0.18), ("Medio-alto", 0.80)]


def configurazione(n):
    caso = random.Random(1000 + n)
    etichetta, bravura = BRAVURE[n % len(BRAVURE)]
    if n >= len(BRAVURE):                       # dal secondo giro: bravura un po' diversa e altri corsi
        bravura = round(min(0.97, max(0.12, bravura + caso.uniform(-0.05, 0.05))), 2)
    corso, test = TEST_CORSO[(n * 3 + n // len(TEST_CORSO)) % len(TEST_CORSO)]
    tipo = "test"
    if n % 7 == 5:
        tipo = "superiori"
    elif n >= 30 and n % 5 == 2:
        tipo = "migliorare"                       # superiori: migliorare una sola materia
    if n >= 46 and n % 2 == 0:
        tipo = "universita"                       # sesto giro: chi frequenta già l'università
    nome = NOMI[n % len(NOMI)]
    import unicodedata
    semplice = unicodedata.normalize("NFKD", nome.lower()).encode("ascii", "ignore").decode()
    return {"n": n + 1, "id": f"s{n + 1:02d}_{semplice}", "nome": nome, "etichetta": etichetta,
            "bravura": bravura, "corso": corso, "test": test, "tipo": tipo, "giorni": 21 if n < 10 else 28,
            "ore": caso.choice([0.5, 1, 1.5]) if n >= 30 else caso.choice([1, 1.5, 2, 3]),
            # dal terzo giro: esame vicino (10-21 giorni), per vedere come il recupero stringe i tempi
            "esame_fra": caso.choice([10, 14, 21]) if n >= 20 else caso.choice([30, 45, 60]),
            "costanza": 0.95 if bravura > 0.7 else (0.85 if bravura > 0.4 else 0.75)}


class Studente:
    def __init__(self, cfg):
        self.cfg = cfg
        self.caso = random.Random(cfg["n"] * 7919)
        # Ogni materia un po' diversa: chi è bravo non lo è uguale ovunque.
        self.bonus_materia = {}
        self.studiato = {}            # (materia, argomento) -> volte studiato: la bravura cresce
        self.risposte_sbagliate = {}  # id -> la risposta sbagliata che tende a ripetere (errore di concetto)

    def probabilita(self, d, ripasso=False):
        m, a = d.get("materia", ""), d.get("argomento", "")
        if m not in self.bonus_materia:
            self.bonus_materia[m] = self.caso.uniform(-0.12, 0.12)
        base = self.cfg["bravura"] + self.bonus_materia[m]
        crescita = min(0.25, 0.04 * self.studiato.get((m, a), 0)) * (1 - base)
        return max(0.03, min(0.98, base + crescita + (0.06 if ripasso else 0)))

    def rispondi(self, elenco, ripasso=False):
        risposte = {}
        for d in elenco:
            giusta = self.caso.random() < self.probabilita(d, ripasso)
            if d.get("tipo") == "completamento":
                risposte[d["id"]] = str(d.get("risposta", "")) if giusta else "boh"
                continue
            lettere = sorted(d.get("opzioni", {}))
            if giusta:
                risposte[d["id"]] = d["giusta"]
            else:
                sbagliate = [x for x in lettere if x != d.get("giusta")] or lettere
                # 60% delle volte ripete lo stesso errore (idea sbagliata), se l'aveva già fatto.
                prima = self.risposte_sbagliate.get(d["id"])
                scelta = prima if prima in sbagliate and self.caso.random() < 0.6 else self.caso.choice(sbagliate)
                self.risposte_sbagliate[d["id"]] = scelta
                risposte[d["id"]] = scelta
        return risposte


def simula(cfg):
    cfg["giorni"] = min(cfg["giorni"], cfg["esame_fra"])       # si studia fino al giorno dell'esame
    inizio = date.today() - timedelta(days=cfg["giorni"])   # le settimane appena passate: l'ultimo giorno è oggi
    p = {"nome": cfg["nome"], "punti": 0, "lingua": "it", "passo": 3, "ore_giorno": cfg["ore"],
         "data_esame": (date.today() + timedelta(days=cfg["esame_fra"])).isoformat(), "bisogni": []}
    if cfg["tipo"] == "superiori":
        p.update(stato="superiori", corso="Liceo scientifico", scuola="Liceo scientifico", anno=4,
                 obiettivo="maturita", materie_scuola=["Matematica", "Fisica", "Chimica", "Biologia"])
        cfg["corso"], cfg["test"] = "Liceo scientifico (4ª)", "Maturità"
    elif cfg["tipo"] == "universita":
        corso = ["Medicina e Chirurgia", "Ingegneria", "Scienze biologiche", "Chimica", "Farmacia e CTF"][cfg["n"] % 5]
        anno = 1 + cfg["n"] % 3
        p.update(stato="frequento", corso=corso, anno=anno)
        if D.CORSI.get(corso, {}).get("indirizzi"):
            p["indirizzo"] = next(iter(D.CORSI[corso]["indirizzi"]))
        cfg["corso"], cfg["test"] = f"{corso}, {anno}° anno", "Esami universitari"
    elif cfg["tipo"] == "migliorare":
        materia = ["Chimica", "Matematica", "Fisica", "Biologia"][cfg["n"] % 4]
        p.update(stato="superiori", corso="Liceo scientifico", scuola="Liceo scientifico", anno=3,
                 obiettivo="migliorare", materia_obiettivo=materia, materie_scuola=[materia])
        cfg["corso"], cfg["test"] = f"Liceo scientifico (3ª) — migliorare {materia}", "Migliorare una materia"
    else:
        p.update(stato="test", corso=cfg["corso"], test=cfg["test"])
    if cfg["n"] > 40 and cfg["n"] % 3 == 0:
        p["lingua"] = "en"                          # quinto giro: anche in inglese
    if cfg["n"] > 40 and cfg["n"] % 3 == 1:
        p["bisogni"] = ["Dislessia"]                # e con la dislessia (carattere leggibile, mappe facili)
    g["profilo"] = lambda: p
    g["salva"] = lambda: None
    s = Studente(cfg)
    oggi_vero = g["oggi"]
    diario = []

    def in_data(giorno):
        """Le risposte registrate «oggi» vanno nel giorno simulato."""
        iso = giorno.isoformat()
        for r in p.get("storico", []):
            if r["g"] == oggi_vero():
                r["g"] = iso
        giorni = p.setdefault("giorni_studio", [])
        if oggi_vero() in giorni:
            giorni.remove(oggi_vero())
            if iso not in giorni:
                giorni.append(iso)
        for a in p.get("attivita", []):
            if a["quando"].startswith(date.today().strftime("%d/%m")):
                a["quando"] = giorno.strftime("%d/%m") + a["quando"][5:]

    # --- Giorno 0: test di livello e piano ---
    materie = g["materie_percorso"]()
    elenco, usate = [], set()
    for i in range(g["DOMANDE_LIVELLO"]):
        m = materie[i % len(materie)]
        argomento = None
        if p.get("stato") == "superiori":
            fatti = g["argomenti_obiettivo"](m) or [None]
            argomento = fatti[(i // len(materie)) % len(fatti)]
        trovate = g["domande"](m, argomento, quante=1, escluse=usate, seme=cfg["n"] * 100 + i)
        if trovate:
            elenco.append(trovate[0])
            usate.add(trovate[0]["id"])
    risposte = s.rispondi(elenco)
    per_materia = {}
    for d in elenco:
        ok = g["e_giusta"](d, risposte[d["id"]])
        x = per_materia.setdefault(d["materia"], [0, 0])
        x[0] += ok
        x[1] += 1
    totale = 100 * sum(v[0] for v in per_materia.values()) / max(1, len(elenco))
    p["livello"] = "basso" if totale < 50 else "intermedio" if totale < 75 else "alto"
    p["percentuali"] = {m: round(100 * a / b) for m, (a, b) in per_materia.items()}
    g["registra_risposte"](elenco, risposte, "Test di livello")
    in_data(inizio)
    # Il piano si crea il primo giorno: l'esame è fra «esame_fra» giorni da quel giorno.
    p["data_esame"] = (date.today() + timedelta(days=cfg["esame_fra"])).isoformat()
    p["piano"] = g["crea_piano"](p["percentuali"], p["livello"])
    p["data_esame"] = (inizio + timedelta(days=cfg["esame_fra"])).isoformat()
    piano_iniziale = json.loads(json.dumps(p["piano"]))
    test_livello = {"totale": round(totale), "livello": p["livello"], "percentuali": dict(p["percentuali"]),
                    "domande": len(elenco)}

    # --- I giorni di studio ---
    sim_esiti = []
    recuperi = []
    for k in range(1, cfg["giorni"] + 1):
        giorno = inizio + timedelta(days=k)
        if s.caso.random() > cfg["costanza"]:
            diario.append({"giorno": k, "data": giorno.isoformat(), "studiato": False})
            continue
        fatto = {"giorno": k, "data": giorno.isoformat(), "studiato": True, "domande": 0, "giuste": 0,
                 "sessioni": [], "note": []}
        budget = int(cfg["ore"] * 60)
        prima_del_giorno = {i: v["prossima"] for i, v in p.get("ripasso", {}).items()}

        def quiz_registrato(el, fonte, ripasso=False):
            r = s.rispondi(el, ripasso)
            g["registra_risposte"](el, r, fonte)
            giuste = sum(1 for d in el if g["e_giusta"](d, r[d["id"]]))
            fatto["domande"] += len(el)
            fatto["giuste"] += giuste
            return giuste, r

        # Le voci del ripasso sono «dovute» se la data è passata: si spostano le date al giorno simulato.
        per_id = g["domanda_per_id"]()
        dovute = [per_id[i] for i, v in p.get("ripasso", {}).items() if v["prossima"] <= giorno.isoformat() and i in per_id]
        quanti_rip, quante_ver = g["carico_giornaliero"](p)
        if dovute:
            giuste, _ = quiz_registrato(dovute[:quanti_rip], "Ripasso di oggi", ripasso=True)
            fatto["sessioni"].append(f"Ripasso degli errori: {giuste}/{len(dovute[:quanti_rip])}")
            budget -= max(5, quanti_rip // 3)
        # Verifiche programmate dal recupero (3 e 7 giorni dopo).
        for v in [v for v in p.get("verifiche_programmate", []) if not v["fatta"] and v["data"] <= giorno.isoformat()][:quante_ver]:
            el = g["domande"](v["materia"], v["argomento"], quante=8, seme=k * 31 + len(v["argomento"]))
            if el:
                giuste, _ = quiz_registrato(el, f"Verifica: {v['argomento']}", ripasso=True)
                v["fatta"] = True
                esito = "superata" if giuste >= 0.7 * len(el) else "da ripetere domani"
                if esito != "superata":
                    p["verifiche_programmate"].append({"materia": v["materia"], "argomento": v["argomento"], "fatta": False,
                                                      "data": (giorno + timedelta(days=1)).isoformat()})
                fatto["sessioni"].append(f"Verifica di memoria «{v['argomento']}»: {giuste}/{len(el)} ({esito})")
                budget -= 10
        # Il recupero intelligente dopo i primi giorni e poi ogni 5 giorni.
        if k in (3, 8, 13, 18):
            lacune, aggiunte = g["pianifica_recupero"]()
            recuperi.append({"giorno": k, "aggiunte": aggiunte,
                             "lacune": [(r["argomento"], r["materia"], r["pc"], r["punteggio"]) for r in lacune]})
            if aggiunte:
                fatto["note"].append(f"Recupero intelligente: {aggiunte} Flash Review nel piano")
        # Le sessioni del piano, finché c'è tempo.
        tentativi_oggi = 0
        while budget > 0 and tentativi_oggi < 6:
            prossima = g["prossima_sessione"](p["piano"])
            if prossima is None:
                break
            si, ii = prossima
            sess = p["piano"][si][ii]
            durata = g["DURATE_SESSIONI"].get(sess["tipo"], 30)
            tentativi_oggi += 1
            m, a = sess["materia"], sess["argomento"]
            s.studiato[(m, a)] = s.studiato.get((m, a), 0) + 1
            if sess["tipo"] == "simulazione":
                sess["fatta"] = True
                fatto["sessioni"].append("Simulazione del piano (segnata come fatta)")
            elif sess["tipo"] == "flash":
                el = g["domande"](m if m in g["MATERIE_BANCA"] else None, a, quante=10, seme=k * 13 + ii)
                giuste, _ = quiz_registrato(el, f"Flash Review: {a}")
                sess["fatta"] = True
                g["programma_verifiche"](m, a)
                # le date delle verifiche partono dal giorno simulato, non da oggi
                p["verifiche_programmate"] = [v for v in p["verifiche_programmate"] if not (
                    v["argomento"] == a and not v["fatta"] and v["data"] in (
                        (date.today() + timedelta(days=3)).isoformat(), (date.today() + timedelta(days=7)).isoformat()))]
                for gg in (3, 7):
                    p["verifiche_programmate"].append({"materia": m, "argomento": a, "fatta": False,
                                                       "data": (giorno + timedelta(days=gg)).isoformat()})
                fatto["sessioni"].append(f"⚡ Flash Review «{a}» ({sess.get('motivo', '')}): {giuste}/{len(el)}")
            elif sess["tipo"] == "verifica":
                el = g["domande_verifica"](p["piano"][si], g["seme_di"](f"verifica{si}"))
                giuste, _ = quiz_registrato(el, f"Verifica della settimana {si + 1}")
                sess["fatta"] = True        # nell'app la verifica si chiude comunque, con il voto
                fatto["sessioni"].append(f"📝 Verifica della settimana {si + 1}: {giuste}/{len(el)}")
            elif sess["tipo"] in ("materia", "video", "impianto"):
                if sess["tipo"] == "materia":
                    lez = g["lezione"](sess["tema"], sess["numero"])
                    el = g["quiz_lezione"](lez, 10) if lez else []
                else:
                    el = g["domande_esame"](m, 10, k * 7 + ii)
                giuste, _ = quiz_registrato(el, f"{sess['tipo'].capitalize()}: {a}") if el else (0, {})
                ok = not el or giuste >= 0.8 * len(el)
                sess["fatta"] = ok or sess.get("tentativo", 0) >= 2
                sess["tentativo"] = sess.get("tentativo", 0) + (0 if ok else 1)
                fatto["sessioni"].append(f"🎓 {sess['tipo']} «{a[:60]}»: {giuste}/{len(el)}"
                                         + (" ✅" if sess["fatta"] else " ✗ da rifare"))
            elif sess["tipo"] == "ripasso":
                el = g["domande"](m if m in g["MATERIE_BANCA"] else None, quante=g["DOMANDE_RIPASSO"], seme=k * 17 + ii)
                giuste, _ = quiz_registrato(el, f"Ripasso: {a}")
                sess["fatta"] = True
                fatto["sessioni"].append(f"Ripasso «{a}»: {giuste}/{len(el)}")
            else:
                n = g["DOMANDE_LEZIONE"]
                rifare = [per_id[x] for x in sess.get("da_rifare", []) if x in per_id]
                nuove = g["domande"](m, a, quante=n, seme=g["seme_di"](a) + sess.get("tentativo", 0),
                                     escluse={d["id"] for d in rifare})
                el = (rifare + nuove)[:n]
                giuste, r = quiz_registrato(el, f"Lezione: {a}")
                tentativo = sess.get("tentativo", 0)
                if giuste == len(el) or giuste >= g["soglia_lezione"](tentativo) * len(el):
                    sess["fatta"] = True
                    sess.pop("da_rifare", None)
                    consolidare = giuste < len(el)
                    if consolidare:
                        sess["da_consolidare"] = True
                        for gg in (3, 7):
                            p.setdefault("verifiche_programmate", []).append(
                                {"materia": m, "argomento": a, "fatta": False,
                                 "data": (giorno + timedelta(days=gg)).isoformat()})
                    fatto["sessioni"].append(f"📘 Lezione «{a}» ({m}): quiz {giuste}/{len(el)} ✅ superata"
                                             + (" (da consolidare)" if consolidare else ""))
                elif tentativo >= 4:
                    # Dal 5° tentativo lo studente usa «Vai avanti»: la lezione entra nel recupero.
                    sess["fatta"] = True
                    sess["da_consolidare"] = True
                    g["inserisci_flash"](m, a, "Lezione superata con «Vai avanti»: da consolidare")
                    for gg in (3, 7):
                        p.setdefault("verifiche_programmate", []).append(
                            {"materia": m, "argomento": a, "fatta": False, "data": (giorno + timedelta(days=gg)).isoformat()})
                    fatto["sessioni"].append(f"📘 Lezione «{a}» ({m}): quiz {giuste}/{len(el)} ➡️ «Vai avanti» "
                                             "(da consolidare con Flash Review)")
                else:
                    sess["tentativo"] = sess.get("tentativo", 0) + 1
                    sess["da_rifare"] = [d["id"] for d in el if not g["e_giusta"](d, r[d["id"]])]
                    fatto["sessioni"].append(f"📘 Lezione «{a}» ({m}): quiz {giuste}/{len(el)} ✗ da rifare "
                                             f"(tentativo {sess['tentativo']})")
            budget -= durata
        # «Rifai gli errori» ogni domenica simulata.
        if giorno.weekday() == 6:
            errori = g["errori_da_rifare"]()[:20]
            if errori:
                prima = {d["id"]: (p.get("ripasso", {}).get(d["id"]) or {}).get("ultima") for d in errori}
                giuste, r = quiz_registrato(errori, "Rifai gli errori", ripasso=True)
                stesse = sum(1 for d in errori if not g["e_giusta"](d, r[d["id"]]) and prima.get(d["id"])
                             and r[d["id"]] == prima[d["id"]])
                p.setdefault("rifai_storico", []).append({"data": giorno.isoformat(), "totale": len(errori),
                                                          "recuperate": giuste,
                                                          "percento": round(100 * giuste / len(errori))})
                fatto["sessioni"].append(f"🔁 Rifai gli errori: recuperate {giuste}/{len(errori)}, "
                                         f"{stesse} errori di concetto (stessa risposta sbagliata)")
        # Una simulazione del test ogni 7 giorni.
        if k % 7 == 0 and cfg["test"] in D.TEST:
            t = D.TEST[cfg["test"]]
            el = []
            for nome_s, q, mins, materia in t["sezioni"]:
                if materia:
                    el += g["domande"](materia, quante=q, seme=k * 101 + q)
            r = s.rispondi(el)
            g["registra_risposte"](el, r, f"Simulazione {cfg['test']}")
            giuste = sum(1 for d in el if g["e_giusta"](d, r[d["id"]]))
            vuote = 0
            punteggio = giuste * t["punti"]["giusta"] + (len(el) - giuste - vuote) * t["punti"]["sbagliata"]
            massimo = len(el) * t["punti"]["giusta"]
            p.setdefault("esiti_sim", []).append({"data": giorno.strftime("%d/%m/%Y"), "test": cfg["test"], "tipo": "ufficiale",
                                                  "percento": round(100 * giuste / max(1, len(el))),
                                                  "punteggio": round(punteggio, 2), "domande": len(el), "minuti": 0})
            sim_esiti.append((k, giuste, len(el), round(punteggio, 1), massimo))
            fatto["domande"] += len(el)
            fatto["giuste"] += giuste
            fatto["sessioni"].append(f"🏁 Simulazione {cfg['test']}: {giuste}/{len(el)} giuste, punteggio "
                                     f"{punteggio:.1f}/{massimo:g}")
        in_data(giorno)
        # Le date del ripasso decise «oggi» partono dal giorno simulato.
        spostamento = (giorno - date.today()).days
        for i, v in p.get("ripasso", {}).items():
            if prima_del_giorno.get(i) != v["prossima"]:
                v["prossima"] = (date.fromisoformat(v["prossima"]) + timedelta(days=spostamento)).isoformat()
        fatto["preparazione"] = g["preparazione"]()
        diario.append(fatto)
    return p, piano_iniziale, test_livello, diario, sim_esiti, recuperi


def scrivi_cartella(cfg, p, piano_iniziale, test_livello, diario, sim_esiti, recuperi):
    cartella = SCRIVANIA / f"{cfg['n']:02d} {cfg['nome']} - {cfg['etichetta']} ({round(cfg['bravura'] * 100)}%)"
    cartella.mkdir(parents=True, exist_ok=True)
    (STUDENTI / f"{cfg['id']}.json").write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
    unita = p.get("piano_unita", "Settimana")
    icone = {"lezione": "📘", "ripasso": "🔁", "simulazione": "🏁", "verifica": "📝", "flash": "⚡", "materia": "📘",
             "video": "▶️", "impianto": "🏭"}
    # --- Il piano ---
    righe = [f"# Il piano di studio di {cfg['nome']}", "",
             f"- Profilo: **{cfg['etichetta']}** (risponde giusto a circa il {round(cfg['bravura'] * 100)}% delle domande)",
             f"- Corso: {cfg['corso']} · test: **{cfg['test']}** · {cfg['ore']} ore al giorno · esame fra {cfg['esame_fra']} giorni (dal giorno del piano)",
             (f"- ⏱️ Piano accorciato per l'esame vicino: tenute {p['piano_compresso']['tenute']} sessioni, tolte "
              f"{p['piano_compresso']['tolte']}" if p.get("piano_compresso") else "- Piano completo (c'è tempo per tutto)"),
             f"- Test di livello: **{test_livello['totale']}%** su {test_livello['domande']} domande → livello **{test_livello['livello']}**",
             "- Per materia: " + ", ".join(f"{m} {v}%" for m, v in test_livello["percentuali"].items()), "",
             f"## Il piano iniziale ({len(piano_iniziale)} {'giorni' if unita == 'Giorno' else 'settimane'}, {sum(len(w) for w in piano_iniziale)} sessioni)",
             "Le materie più deboli vengono prima; quelle sotto il 60% hanno un ripasso in più; alla fine la simulazione.", ""]
    for n, w in enumerate(piano_iniziale, 1):
        righe.append(f"**{unita} {n}**")
        righe += [f"- {icone.get(x['tipo'], '📘')} {x['argomento']} · {x['materia']}" for x in w]
        righe.append("")
    fatte = sum(x["fatta"] for w in p["piano"] for x in w)
    totale = sum(len(w) for w in p["piano"])
    righe += [f"## Il piano dopo {cfg['giorni']} giorni: {fatte} sessioni fatte su {totale}", ""]
    for n, w in enumerate(p["piano"], 1):
        righe.append(f"**{unita} {n}** — {sum(x['fatta'] for x in w)}/{len(w)} fatte")
        for x in w:
            extra = f" ({x.get('motivo')})" if x.get("motivo") else ""
            tent = f" · tentativi {x['tentativo']}" if x.get("tentativo") else ""
            righe.append(f"- {'✅' if x['fatta'] else '⬜'} {icone.get(x['tipo'], '📘')} {x['argomento']} · {x['materia']}{extra}{tent}")
        righe.append("")
    righe += ["## Il recupero intelligente (Flash Review aggiunte)", ""]
    for rc in recuperi:
        righe.append(f"- Giorno {rc['giorno']}: {rc['aggiunte']} aggiunte. Priorità: "
                     + "; ".join(f"{a} ({m}) {pc}% → priorità {pu}" for a, m, pc, pu in rc["lacune"]) if rc["lacune"]
                     else f"- Giorno {rc['giorno']}: nessuna lacuna da recuperare")
    verifiche = p.get("verifiche_programmate", [])
    righe += ["", f"## Verifiche di memoria programmate: {sum(v['fatta'] for v in verifiche)} fatte, "
              f"{sum(not v['fatta'] for v in verifiche)} ancora da fare", ""]
    (cartella / "piano.md").write_text("\n".join(righe), encoding="utf-8")
    # --- Il diario ---
    righe = [f"# Diario di {cfg['nome']} ({cfg['etichetta']})", "",
             "| Giorno | Data | Domande | Giuste | Preparazione | Che cosa ha fatto |", "|---|---|---|---|---|---|"]
    for f in diario:
        if not f["studiato"]:
            righe.append(f"| {f['giorno']} | {f['data']} | — | — | — | non ha studiato |")
            continue
        pc = round(100 * f["giuste"] / f["domande"]) if f["domande"] else 0
        righe.append(f"| {f['giorno']} | {f['data']} | {f['domande']} | {pc}% | {f.get('preparazione') or '—'}% | "
                     + "<br>".join(f["sessioni"] + f["note"]).replace("|", "/") + " |")
    (cartella / "diario.md").write_text("\n".join(righe), encoding="utf-8")
    # --- Il resoconto ---
    prep = [f.get("preparazione") for f in diario if f.get("studiato") and f.get("preparazione") is not None]
    rifai = p.get("rifai_storico", [])
    giorni_studio = sum(1 for f in diario if f["studiato"])
    righe = [f"# Resoconto: {cfg['nome']} — {cfg['etichetta']} ({round(cfg['bravura'] * 100)}%)", "",
             f"- Ha studiato **{giorni_studio} giorni su {cfg['giorni']}**, {sum(f.get('domande', 0) for f in diario)} domande.",
             f"- Preparazione: dal test di livello {test_livello['totale']}% → **{prep[-1] if prep else '—'}%** dopo {cfg['giorni']} giorni "
             f"(obiettivo 85%).",
             f"- Sessioni del piano fatte: **{fatte}/{totale}**.",
             "- Simulazioni: " + (", ".join(f"giorno {k}: {gi}/{to} ({pu}/{ma:g})" for k, gi, to, pu, ma in sim_esiti)
                                  or "nessuna"),
             "- Rifai gli errori: " + (" → ".join(f"{x['percento']}%" for x in rifai) or "mai") + " di recuperate",
             f"- Errori ancora nel ripasso: {len(p.get('ripasso', {}))} · imparate: {p.get('imparate', 0)}", ""]
    lacune = g["priorita_lacune"]()[:5]
    righe += ["## Le lacune più urgenti alla fine (algoritmo di priorità)", ""]
    righe += [f"- {r['argomento']} ({r['materia']}): {r['pc']}% su {r['risposte']} risposte · errori ripetuti "
              f"{r['ripetuti']} · {'nel test' if r.get('nel_test') else 'non nel test'} · priorità {r['punteggio']}"
              for r in lacune] or ["- nessuna"]
    righe += ["", "## Come si è comportata l'app", ""] + osservazioni(cfg, p, test_livello, diario, fatte, totale, prep)
    (cartella / "resoconto.md").write_text("\n".join(righe), encoding="utf-8")
    return cartella


def osservazioni(cfg, p, test_livello, diario, fatte, totale, prep):
    """Le cose notate, in automatico: quello che funziona e quello che non va."""
    note = []
    livello_atteso = "alto" if cfg["bravura"] >= 0.75 else ("intermedio" if cfg["bravura"] >= 0.5 else "basso")
    note.append(f"- Livello assegnato **{test_livello['livello']}** (atteso circa «{livello_atteso}»): "
                + ("✅ coerente." if test_livello["livello"] == livello_atteso else "⚠️ diverso: il test di livello ha "
                   f"solo {test_livello['domande']} domande, quindi è sensibile alla fortuna."))
    settimane = len(p["piano"])
    note.append(f"- Piano di {settimane} {'giorni' if p.get('piano_unita') == 'Giorno' else 'settimane'} "
                f"({'più corto' if settimane <= 4 else 'più lungo'} per il livello {test_livello['livello']}).")
    consolidare = [x for w in p["piano"] for x in w if x.get("da_consolidare")]
    if consolidare:
        note.append(f"- {len(consolidare)} lezioni superate con la soglia ridotta o con «Vai avanti» (da consolidare): "
                    + ", ".join(x["argomento"] for x in consolidare[:5]) + ".")
    bloccate = [x for w in p["piano"] for x in w if not x["fatta"] and x.get("tentativo", 0) >= 3]
    if bloccate:
        note.append(f"- ⚠️ {len(bloccate)} lezioni ferme dopo 3 o più tentativi (serve il 100% al quiz): "
                    + ", ".join(x["argomento"] for x in bloccate[:4]) + ". Per uno studente "
                    + ("bravo" if cfg["bravura"] > 0.7 else "debole") + " la regola del 100% può rallentare molto.")
    if prep and len(prep) > 2:
        note.append(f"- Preparazione {'cresciuta' if prep[-1] > prep[0] else 'non cresciuta'}: {prep[0]}% → {prep[-1]}%.")
    if fatte == 0:
        note.append("- ⚠️ Nessuna sessione del piano completata: lo studente resta fermo sulla prima lezione.")
    return note


def main():
    quanti = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    inizio = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    SCRIVANIA.mkdir(parents=True, exist_ok=True)
    for n in range(inizio, inizio + quanti):
        cfg = configurazione(n)
        st.session_state.clear()
        risultato = simula(cfg)
        cartella = scrivi_cartella(cfg, *risultato)
        print("FATTO", cfg["id"], cfg["etichetta"], cfg["test"], "→", cartella, flush=True)


if __name__ == "__main__":
    main()
