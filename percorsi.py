"""I percorsi BIBL-IA: le vie metaboliche spiegate passaggio per passaggio (dal glucosio alla glicolisi,
al ciclo di Krebs...), scritte e controllate a mano, non dall'AI. Sotto ogni molecola e ogni enzima c'è
una scheda breve: che cos'è (monosaccaride, disaccaride, coenzima...) e un consiglio per ricordarlo.
I colori sono sempre gli stessi, spiegati nella legenda: così chi studia non si confonde."""
import html
import json
from functools import lru_cache
from pathlib import Path

CARTELLA = Path(__file__).resolve().parent / "mappe"

# Un colore per ogni tipo di cosa (i colori del sito: fondo inchiostro, accento oro).
COLORI = {
    "zucchero": ("#7FB3FF", "Zuccheri (carboidrati)"),
    "molecola": ("#B79CFF", "Altre molecole del percorso"),
    "enzima": ("#4FD1C5", "Enzimi (chi fa il lavoro)"),
    "energia": ("#E3A857", "Energia (ATP, GTP)"),
    "coenzima": ("#8BD17C", "Coenzimi che portano elettroni (NAD, FAD)"),
    "piccola": ("#9AA0AA", "Acqua, gas, ioni"),
    "struttura": ("#F5A3C7", "Organi, cellule e parti del corpo"),
}
ROSSO = "#F07167"


@lru_cache(maxsize=1)
def percorsi():
    return json.loads((CARTELLA / "percorsi.json").read_text())


@lru_cache(maxsize=1)
def schede():
    return json.loads((CARTELLA / "schede.json").read_text())


def ordine():
    """I percorsi nell'ordine delle mappe pronte (metabolismo, cellula, apparati...)."""
    pronte = [m["argomento"] for m in json.loads((CARTELLA / "mappe_pronte.json").read_text())]
    return sorted(percorsi(), key=lambda n: pronte.index(n) if n in pronte else 99)


def scheda(nome):
    return schede().get(nome) or {"tipo": "molecola"}


# Quanto è approfondita la spiegazione: primaria e medie, superiore, università, università dal
# 4° anno (con le note cliniche).
GRADI = {"base": "primaria e medie", "superiore": "scuola superiore", "universita": "università",
         "clinica": "università, con le note cliniche"}


def grado(livello, classe=1):
    if livello in ("Scuola primaria", "Scuola media"):
        return "base"
    if livello == "Scuola superiore":
        return "superiore"
    try:
        anno = int(str(classe).strip("°ª "))
    except ValueError:
        anno = 1
    return "clinica" if anno >= 4 else "universita"


def spiegazione(nome, livello_grado="universita"):
    """La spiegazione di una molecola o di un enzima per quel livello (e la nota clinica, se c'è)."""
    s = scheda(nome)
    if livello_grado == "clinica":
        return s.get("universita", ""), s.get("clinica", "")
    return s.get(livello_grado) or s.get("superiore", ""), ""


def _disegno(nome, larghezza, altezza, formato):
    smiles = scheda(nome).get("smiles")
    if not smiles or smiles == "O":
        return None
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    molecola = Chem.MolFromSmiles(smiles)
    if molecola is None:
        return None
    disegno = (rdMolDraw2D.MolDraw2DSVG if formato == "svg" else rdMolDraw2D.MolDraw2DCairo)(larghezza, altezza)
    opzioni = disegno.drawOptions()
    rdMolDraw2D.SetDarkMode(opzioni)
    opzioni.setBackgroundColour((0.102, 0.122, 0.161, 1))  # il fondo delle schede del sito
    opzioni.bondLineWidth = 2
    opzioni.padding = 0.08
    opzioni.minFontSize = 11
    rdMolDraw2D.PrepareAndDrawMolecule(disegno, molecola)
    disegno.FinishDrawing()
    return disegno.GetDrawingText()


@lru_cache(maxsize=256)
def formula_svg(nome):
    """La formula di struttura disegnata da RDKit (SVG per il sito)."""
    svg = _disegno(nome, 230, 150, "svg")
    return svg[svg.find("<svg"):] if svg else None


@lru_cache(maxsize=256)
def formula_png(nome):
    """La stessa formula in PNG (per il PDF)."""
    return _disegno(nome, 460, 300, "png")


def trova(argomento):
    """Il nome del percorso per un argomento (o None)."""
    a = (argomento or "").lower().strip()
    for nome in percorsi():
        if nome.lower() in a or a in nome.lower() and len(a) > 4:
            return nome
    return None


def _e(testo):
    return html.escape(testo or "")


STILE = """<style>
.pc{font-family:-apple-system,Helvetica,Arial,sans-serif;color:#E8E6E1;background:#11141B;border:1px solid #2B3240;
 border-radius:14px;padding:18px 16px;max-width:760px;margin:0 auto}
.pc h3{color:#E3A857;margin:0 0 4px;font-family:Georgia,serif;font-size:1.35rem}
.pc .dove{color:#9AA0AA;font-size:.85rem;margin-bottom:8px}
.pc .intro{font-size:.92rem;line-height:1.45;margin:8px 0 12px}
.pc .leg{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:.75rem;color:#C9C5BD;margin-bottom:14px}
.pc .leg span{display:inline-flex;align-items:center;gap:5px}
.pc .leg i{width:11px;height:11px;border-radius:3px;display:inline-block}
.pc .fase{margin:16px 0 8px;padding:6px 10px;border-left:3px solid #E3A857;background:#1A1F29;color:#E3A857;
 font-weight:600;font-size:.88rem;border-radius:0 6px 6px 0}
.pc .riga{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.pc .card{background:#1A1F29;border:1px solid #2B3240;border-left:5px solid var(--c);border-radius:10px;
 padding:9px 12px;flex:1 1 300px;max-width:560px;display:flex;gap:10px;align-items:flex-start}
.pc .card .txt{flex:1}
.pc .card .formula{flex:0 0 auto;width:170px}
.pc .card .formula img{width:170px;height:auto;border-radius:6px;display:block}
.pc .clin{font-size:.78rem;margin-top:5px;padding:4px 7px;border-radius:5px;background:#F0716714;
 border-left:3px solid #F07167;line-height:1.35}
@media (max-width:560px){.pc .card{flex-direction:column}.pc .card .formula{width:100%}.pc .card .formula img{width:100%}}
.pc .card b{color:var(--c);font-size:1.02rem}
.pc .cosa{font-size:.82rem;margin-top:3px;line-height:1.35}
.pc .cons{font-size:.78rem;color:#C9C5BD;margin-top:4px;line-height:1.35}
.pc .passo{display:grid;grid-template-columns:44px 1fr;gap:8px;margin:6px 0 6px 18px;
 border-left:2px dashed #4FD1C5;padding-left:10px}
.pc .num{width:30px;height:30px;border-radius:50%;background:#E3A857;color:#11141B;font-weight:700;
 display:flex;align-items:center;justify-content:center;margin-left:-27px;margin-top:4px}
.pc .enz{display:inline-block;border:1px solid #4FD1C5;color:#4FD1C5;border-radius:999px;padding:2px 10px;
 font-weight:600;font-size:.86rem}
.pc .chip{display:inline-block;border-radius:6px;padding:1px 7px;font-size:.78rem;margin:2px 3px 0 0;
 border:1px solid var(--c);color:var(--c)}
.pc .ent{font-size:.78rem;color:#9AA0AA;margin-top:4px}
.pc .nota{font-size:.84rem;line-height:1.4;margin-top:5px}
.pc .bad{display:inline-block;font-size:.72rem;border-radius:4px;padding:1px 6px;margin-left:6px;
 background:#F0716722;color:#F07167;border:1px solid #F07167}
.pc .x2{display:inline-block;font-size:.72rem;border-radius:4px;padding:1px 6px;margin-left:6px;
 color:#E3A857;border:1px solid #E3A857}
.pc .box{background:#1A1F29;border:1px solid #E3A857;border-radius:10px;padding:10px 12px;margin-top:14px}
.pc .box h4{margin:0 0 6px;color:#E3A857;font-size:.95rem}
.pc .box li{font-size:.86rem;margin:2px 0}
.pc .strade{display:flex;gap:10px;flex-wrap:wrap}
.pc .strada{flex:1 1 280px;background:#11141B;border:1px solid #2B3240;border-radius:8px;padding:8px 10px}
.pc .cond{color:#E3A857;font-weight:600;font-size:.85rem}
.pc .prox{margin-top:6px;font-size:.84rem;color:#4FD1C5}
.pc .firma{text-align:right;font-size:.72rem;color:#E3A857;margin-top:10px;letter-spacing:.04em}
</style>"""


def _card(nome, livello_grado):
    s = scheda(nome)
    colore = COLORI.get(s["tipo"], COLORI["molecola"])[0]
    testo, clinica = spiegazione(nome, livello_grado)
    corpo = f'<b>{_e(nome)}</b>'
    if testo:
        corpo += f'<div class="cosa">{_e(testo)}</div>'
    if clinica:
        corpo += f'<div class="clin">🩺 {_e(clinica)}</div>'
    formula = formula_svg(nome)
    if formula:
        import base64
        sorgente = "data:image/svg+xml;base64," + base64.b64encode(formula.encode()).decode()
        disegno = f'<div class="formula"><img src="{sorgente}" alt="formula di struttura: {_e(nome)}"></div>'
    else:
        disegno = ""
    return f'<div class="card" style="--c:{colore}"><div class="txt">{corpo}</div>{disegno}</div>'


def _chip(nome):
    colore = COLORI.get(scheda(nome)["tipo"], COLORI["molecola"])[0]
    return f'<span class="chip" style="--c:{colore}">{_e(nome)}</span>'


def _passo(numero, p, livello_grado):
    icona = "⚙️" if scheda(p["enzima"]).get("tipo") == "enzima" else "📍"
    testa = f'<span class="enz">{icona} {_e(p["enzima"])}</span>'
    if p.get("irreversibile"):
        testa += '<span class="bad">⛔ irreversibile</span>'
    if p.get("limitante"):
        testa += '<span class="bad">🚦 tappa che regola la velocità</span>'
    if p.get("volte") == 2:
        testa += '<span class="x2">×2</span>'
    corpo = testa
    testo, clinica = spiegazione(p["enzima"], livello_grado)
    if testo:
        corpo += f'<div class="cons">{_e(testo)}</div>'
    if clinica:
        corpo += f'<div class="clin">🩺 {_e(clinica)}</div>'
    if p.get("entra") or p.get("esce"):
        corpo += ('<div class="ent">entra: ' + ("".join(map(_chip, p.get("entra", []))) or "—")
                  + ' &nbsp;→&nbsp; esce: ' + ("".join(map(_chip, p.get("esce", []))) or "—") + '</div>')
    corpo += f'<div class="nota">{_e(p["nota"])}</div>'
    return f'<div class="passo"><div class="num">{numero}</div><div>{corpo}</div></div>'


def html_percorso(nome, livello_grado="universita"):
    """Il percorso disegnato come pagina HTML (per st.html)."""
    dati = percorsi()[nome]
    parti = [STILE, '<div class="pc">', f'<h3>{_e(dati["titolo"])}</h3>', f'<div class="dove">📍 {_e(dati["dove"])} · spiegazioni per: <b>{_e(GRADI[livello_grado])}</b></div>',
             f'<div class="intro">{_e(dati["intro"])}</div>', '<div class="leg">']
    parti += [f'<span><i style="background:{c}"></i>{_e(t)}</span>' for c, t in COLORI.values()]
    parti.append(f'<span><i style="background:{ROSSO}"></i>Passaggio a senso unico</span></div>')
    fasi = {f["da"]: f["nome"] for f in dati.get("fasi", [])}
    parti.append(f'<div class="riga">{_card(dati["inizio"], livello_grado)}</div>')
    ultimi = [dati["inizio"]]
    for i, p in enumerate(dati["passaggi"], 1):
        if i in fasi:
            parti.append(f'<div class="fase">{_e(fasi[i])}</div>')
        nuovi = [d for d in p["da"] if d not in ultimi]
        if nuovi:
            parti.append('<div class="riga">' + "".join(_card(d, livello_grado) for d in nuovi) + '</div>')
        parti.append(_passo(i, p, livello_grado))
        parti.append('<div class="riga">' + "".join(_card(a, livello_grado) for a in p["a"]) + '</div>')
        ultimi = p["a"]
    parti.append(f'<div class="box"><h4>📊 {_e(dati.get("titolo_bilancio", "Il bilancio"))}</h4><ul>' + "".join(f"<li>{_e(b)}</li>" for b in dati["bilancio"]) + '</ul></div>')
    dopo = dati.get("dopo")
    if dopo:
        strade = []
        for s in dopo["strade"]:
            strade.append('<div class="strada">' f'<div class="cond">{_e(s["condizione"])}</div>'
                          + _passo("→", s, livello_grado) + _card(s["a"], livello_grado)
                          + (f'<div class="prox">➡️ Continua: <b>{_e(s["prossimo"])}</b></div>' if s.get("prossimo") else "")
                          + '</div>')
        parti.append(f'<div class="box"><h4>🔀 {_e(dopo["titolo"])}</h4><div class="strade">' + "".join(strade) + '</div></div>')
    for box in dati.get("da_sapere", []):
        righe = []
        for titolo, nomi in box["voci"]:
            righe.append(f'<li><b>{_e(titolo)}</b>: ' + "; ".join(
                f'{_chip(n)} {_e(spiegazione(n, "superiore")[0])}' for n in nomi) + '</li>')
        parti.append(f'<div class="box"><h4>📌 Da sapere: {_e(box["titolo"])}</h4><ul>' + "".join(righe) + '</ul></div>')
    parti.append('<div class="firma">★ BIBL-IA · percorso controllato</div></div>')
    return "".join(parti)


def testo_percorso(nome):
    """Il percorso come testo semplice (per WhatsApp, email, appunti)."""
    dati = percorsi()[nome]
    righe = [dati["titolo"], f"Dove: {dati['dove']}", ""]
    for i, p in enumerate(dati["passaggi"], 1):
        extra = " (×2)" if p.get("volte") == 2 else ""
        righe.append(f"{i}. {' + '.join(p['da'])} → {' + '.join(p['a'])}{extra}")
        righe.append(f"   enzima: {p['enzima']}" + (f"; entra {', '.join(p['entra'])}" if p.get("entra") else "")
                     + (f"; esce {', '.join(p['esce'])}" if p.get("esce") else ""))
    righe += ["", "Bilancio: " + "; ".join(dati["bilancio"])]
    return "\n".join(righe)


def nomi_del_percorso(nome):
    """Le molecole e gli enzimi del percorso, nell'ordine in cui compaiono (per le flashcard)."""
    p = percorsi()[nome]
    visti = []
    for passo in p.get("passaggi", []):
        for n in (*passo.get("da", []), passo.get("enzima") or "", *passo.get("a", []),
                  *passo.get("entra", []), *passo.get("esce", [])):
            if n and n not in visti and n in schede():
                visti.append(n)
    return visti


def flashcard(nome, livello_grado="universita"):
    """Le flashcard del percorso: «Che cos'è X?» con la spiegazione controllata per quel livello."""
    carte = []
    for n in nomi_del_percorso(nome):
        testo, clinica = spiegazione(n, livello_grado)
        if testo:
            carte.append((n, scheda(n).get("tipo", "molecola"), testo, clinica))
    return carte


def domande(nome, quante=12):
    """Domande a scelta multipla su tutto il percorso, costruite dai passaggi controllati (non dall'AI):
    quale enzima fa un passaggio, che cosa si forma, che cosa entra o esce, quale tappa è irreversibile."""
    import random
    p = percorsi()[nome]
    passi = p.get("passaggi", [])
    caso = random.Random(nome)
    enzimi = list(dict.fromkeys(x["enzima"] for x in passi if x.get("enzima")))
    prodotti = list(dict.fromkeys(a for x in passi for a in x.get("a", [])))
    entrano = list(dict.fromkeys(e for x in passi for e in x.get("entra", []) + x.get("esce", [])))
    fatte = []

    def aggiungi(testo, giusta, altre, spiega):
        altre = [a for a in dict.fromkeys(altre) if a != giusta]
        if len(altre) < 3:
            return
        opzioni = caso.sample(altre, 3) + [giusta]
        caso.shuffle(opzioni)
        lettere = "ABCD"
        fatte.append({"domanda": testo, "opzioni": dict(zip(lettere, opzioni)),
                      "giusta": lettere[opzioni.index(giusta)], "spiegazione": spiega})

    for n, x in enumerate(passi, 1):
        da, a = " + ".join(x.get("da", [])), " + ".join(x.get("a", []))
        if not da or not a:
            continue
        nota = x.get("nota", "")
        if x.get("enzima") and len(enzimi) >= 4:
            chi = "quale enzima" if scheda(x["enzima"]).get("tipo") == "enzima" else "chi o che cosa"
            aggiungi(f"Passaggio {n}: {chi} trasforma {da} in {a}?", x["enzima"], enzimi, nota)
        gia = set(x.get("a", [])) | set(x.get("esce", [])) | set(x.get("da", [])) | set(x.get("entra", []))
        if x.get("a"):
            aggiungi(f"Passaggio {n}: da {da}" + (f" (grazie a {x['enzima']})" if x.get("enzima") else "")
                     + " che cosa si forma?", x["a"][0], [c for c in prodotti + [d for y in passi for d in y.get("da", [])] if c not in gia], nota)
        if x.get("esce") and len(entrano) >= 4:
            aggiungi(f"Passaggio {n} ({da} → {a}): che cosa viene prodotto o liberato insieme?",
                     x["esce"][0], [c for c in entrano if c not in gia], nota)
    irreversibili = [x for x in passi if x.get("irreversibile") and x.get("enzima")]
    if irreversibili and len(enzimi) >= 4:
        x = caso.choice(irreversibili)
        aggiungi("Quale di questi enzimi catalizza una tappa irreversibile?", x["enzima"],
                 [e for e in enzimi if e not in {y["enzima"] for y in irreversibili}],
                 "Le tappe irreversibili sono quelle che la cellula usa per regolare il percorso.")
    # Un po' da tutto il percorso: le domande si scelgono distribuite dall'inizio alla fine.
    if len(fatte) > quante:
        passo = len(fatte) / quante
        fatte = [fatte[int(i * passo)] for i in range(quante)]
    return fatte
