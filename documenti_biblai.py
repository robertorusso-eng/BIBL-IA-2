"""I documenti BIBL-IA da salvare e condividere (ricerche e mappe concettuali): PDF con il simbolo e la
scritta BIBL-IA, il numero identificativo, la filigrana su ogni pagina e la protezione che impedisce di
modificare il testo (si può solo leggere e stampare). Così le idee salvate o girate ad altri restano
come sono state scritte e si riconosce da dove vengono."""
import datetime
import hashlib
import io
import re
import secrets
from pathlib import Path

CARTELLA = Path(__file__).resolve().parent
LOGO = CARTELLA / "immagini" / "simbolo_bibl_ai_oro.png"
CARATTERI = Path("/System/Library/Fonts/Supplemental")
# I colori del sito (.streamlit/config.toml): fondo inchiostro e un solo accento oro.
INCHIOSTRO = (17, 20, 27)
FONDO = (26, 31, 41)
BORDO = (43, 50, 64)
ORO = (227, 168, 87)
TESTO = (232, 230, 225)
GRIGIO = (150, 156, 168)
BLU = INCHIOSTRO  # il vecchio nome, per chi lo usa ancora
# I recapiti scritti in fondo a ogni documento (telefono, email, sito): si cambiano in questo file,
# che resta solo sul Mac. Se manca, al loro posto c'è un trattino.
CONTATTI = CARTELLA / ".streamlit" / "contatti_biblai.json"


def crea_simbolo(lato=512):
    """Il simbolo BIBL-IA nei colori del sito: un libro aperto chiaro su un quadrato color inchiostro con
    gli angoli arrotondati e il bordo oro, e una stella oro (l'intelligenza artificiale) sopra le pagine."""
    from PIL import Image, ImageDraw
    if LOGO.exists():
        return LOGO
    LOGO.parent.mkdir(exist_ok=True)
    immagine = Image.new("RGBA", (lato, lato), (0, 0, 0, 0))
    d = ImageDraw.Draw(immagine)
    d.rounded_rectangle((0, 0, lato - 1, lato - 1), radius=lato // 6, fill=INCHIOSTRO,
                        outline=ORO, width=max(3, lato // 40))
    c, base, alto = lato / 2, lato * 0.78, lato * 0.40
    # Le due pagine del libro, un po' inclinate verso il dorso.
    for verso in (-1, 1):
        esterno = c + verso * lato * 0.34
        d.polygon([(c, alto + lato * 0.06), (esterno, alto), (esterno, base - lato * 0.04), (c, base)],
                  fill=TESTO)
        for k in range(3):  # le righe del testo
            y = alto + lato * (0.11 + 0.09 * k)
            d.line([(c + verso * lato * 0.06, y + lato * 0.03), (c + verso * lato * 0.27, y)],
                   fill=(190, 175, 150), width=max(2, lato // 64))
    d.line([(c, alto + lato * 0.06), (c, base)], fill=ORO, width=max(2, lato // 80))
    # La stella a quattro punte.
    sx, sy, r = c, lato * 0.22, lato * 0.12
    d.polygon([(sx, sy - r), (sx + r * 0.28, sy - r * 0.28), (sx + r, sy), (sx + r * 0.28, sy + r * 0.28),
               (sx, sy + r), (sx - r * 0.28, sy + r * 0.28), (sx - r, sy), (sx - r * 0.28, sy - r * 0.28)],
              fill=ORO)
    immagine.save(LOGO)
    return LOGO


def codice_documento(*parti):
    """Il numero del documento: la data e sei caratteri che dipendono dal contenuto."""
    impronta = hashlib.sha256("|".join(map(str, parti)).encode()).hexdigest()[:6].upper()
    return f"BIBL-IA-{datetime.date.today():%Y%m%d}-{impronta}"


def senza_emoji(testo):
    testo = re.sub(r"[\U00010000-\U0010FFFF☀-➿️‍]", "", testo or "")
    return re.sub(r"\*\*|__", "", testo).strip()


def recapiti():
    """Telefono, email e sito da scrivere in fondo ai documenti (dal file CONTATTI)."""
    import json
    dati = {}
    try:
        dati = json.loads(CONTATTI.read_text())
    except (OSError, ValueError):
        pass
    return {"Telefono": dati.get("telefono") or "—", "Email": dati.get("email") or "—",
            "Sito": dati.get("sito") or "—"}


def _documento(codice, titolo, orientamento="P"):
    from fpdf import FPDF
    salvato = datetime.datetime.now()

    class Documento(FPDF):
        def multi_cell(self, *args, **kwargs):
            kwargs.setdefault("new_x", "LMARGIN")
            kwargs.setdefault("new_y", "NEXT")
            return super().multi_cell(*args, **kwargs)

        def header(self):
            larghezza = self.w
            # Tutta la pagina nel colore inchiostro del sito, la fascia in alto un po' più chiara
            # con la riga oro sotto.
            self.set_fill_color(*INCHIOSTRO)
            self.rect(0, 0, larghezza, self.h, "F")
            self.set_fill_color(*FONDO)
            self.rect(0, 0, larghezza, 30, "F")
            self.set_fill_color(*ORO)
            self.rect(0, 30, larghezza, 0.8, "F")
            self.image(str(crea_simbolo()), x=10, y=5, w=20, h=20)
            self.set_xy(33, 6)
            self.set_text_color(*ORO)
            self.set_font(self.carattere, "B", 24)
            self.cell(60, 11, "BIBL-IA")
            self.set_xy(33, 18)
            self.set_text_color(*TESTO)
            self.set_font(self.carattere, "", 9)
            self.cell(90, 5, titolo)
            self.set_xy(larghezza - 86, 7)
            self.set_font(self.carattere, "", 8.5)
            self.multi_cell(76, 4.6, f"DOCUMENTO IDENTIFICATIVO\nn. {codice}\n"
                                     f"{salvato:%d/%m/%Y %H:%M}", align="R", new_x="LEFT")
            self.set_text_color(*TESTO)
            self.set_xy(self.l_margin, 38)

        def footer(self):
            # In fondo, come nei documenti salvati: quando e con cosa è stato salvato, i recapiti e
            # la protezione.
            self.set_fill_color(*ORO)
            self.rect(self.l_margin, self.h - 21, self.w - self.l_margin - self.r_margin, 0.4, "F")
            self.set_y(-19)
            self.set_font(self.carattere, "B", 8)
            self.set_text_color(*ORO)
            self.multi_cell(0, 4, f"Salvato con BIBL-IA il {salvato:%d/%m/%Y} alle {salvato:%H:%M} · "
                                  f"documento n. {codice} · pagina {self.page_no()}/{{nb}}", align="C")
            self.set_font(self.carattere, "", 7.5)
            self.set_text_color(*GRIGIO)
            self.multi_cell(0, 3.8, "   ·   ".join(f"{k}: {v}" for k, v in recapiti().items()), align="C")
            self.multi_cell(0, 3.8, "Documento protetto: il testo non si può modificare. Informazioni a scopo "
                                    "di studio, consultativo e non curativo.", align="C")

    pdf = Documento(orientation=orientamento, format="A4")
    pdf.carattere = "Helvetica"
    if (CARATTERI / "Arial Unicode.ttf").exists():
        pdf.add_font("Testo", "", str(CARATTERI / "Arial Unicode.ttf"))
        pdf.add_font("Testo", "B", str(CARATTERI / "Arial Bold.ttf"))
        pdf.add_font("Riserva", "", str(CARATTERI / "Arial Unicode.ttf"))
        pdf.set_fallback_fonts(["Riserva"], exact_match=False)
        pdf.carattere = "Testo"
    pdf.set_auto_page_break(True, margin=26)
    pdf.set_title(f"BIBL-IA · {titolo} · {codice}")
    pdf.set_author("BIBL-IA")
    pdf.set_creator("BIBL-IA")
    return pdf


def _pulisci(pdf, testo):
    testo = senza_emoji(testo)
    return testo if pdf.carattere == "Testo" else testo.encode("latin-1", "replace").decode("latin-1")


def _chiudi(pdf):
    """Il PDF protetto: si apre e si stampa senza password, ma non si può modificare (né la scritta
    BIBL-IA né il testo). La password del proprietario è casuale e non si conserva."""
    from fpdf.enums import AccessPermission, EncryptionMethod
    pdf.set_encryption(owner_password=secrets.token_urlsafe(24), encryption_method=EncryptionMethod.RC4,
                       permissions=AccessPermission.PRINT_LOW_RES | AccessPermission.PRINT_HIGH_RES
                       | AccessPermission.COPY_FOR_ACCESSIBILITY)
    return bytes(pdf.output())


def _titolo(pdf, testo):
    pdf.ln(2)
    pdf.set_font(pdf.carattere, "B", 13)
    pdf.set_text_color(*ORO)
    pdf.multi_cell(0, 7, testo)
    pdf.set_text_color(*TESTO)
    pdf.set_font(pdf.carattere, "", 11)


def documento_ricerca(codice, domanda, risposta, pagine, consigliate):
    pdf = _documento(codice, "La biblioteca che risponde con le pagine dei libri")
    pdf.add_page()
    _titolo(pdf, "Domanda")
    pdf.multi_cell(0, 6, _pulisci(pdf, domanda))
    _titolo(pdf, "Risposta (frasi dei libri)")
    for riga in _pulisci(pdf, risposta).splitlines():
        if riga.strip():
            pdf.multi_cell(0, 6, riga.strip())
            pdf.ln(1)
    if pagine:
        _titolo(pdf, "Pagine dei libri")
        pdf.multi_cell(0, 6, _pulisci(pdf, " · ".join(f"{Path(l).stem}, p. {n}" for l, n in pagine)))
    if consigliate:
        _titolo(pdf, "Per studiare meglio: le pagine consigliate")
        for libro, numero, spiegazione in consigliate:
            pdf.set_font(pdf.carattere, "B", 10)
            pdf.multi_cell(0, 5, _pulisci(pdf, f"{Path(libro).stem}, pagina {numero}"))
            pdf.set_font(pdf.carattere, "", 10)
            if spiegazione:
                pdf.multi_cell(0, 5, _pulisci(pdf, spiegazione))
            pdf.ln(1)
    return _chiudi(pdf)


def documento_mappa(codice, argomento, relazioni, sottotitolo=""):
    """La mappa disegnata a livelli (il concetto centrale in alto, poi i concetti collegati, riga per
    riga) con i colori di BIBL-IA, e sotto l'elenco dei collegamenti."""
    pdf = _documento(codice, "Mappa concettuale", "L")
    pdf.add_page()
    _titolo(pdf, _pulisci(pdf, argomento[:1].upper() + argomento[1:]))
    if sottotitolo:
        pdf.set_font(pdf.carattere, "", 9)
        pdf.multi_cell(0, 5, _pulisci(pdf, sottotitolo))
    # I livelli: la distanza di ogni concetto dal centro.
    vicini = {}
    for r in relazioni:
        vicini.setdefault(r["da"], []).append(r["a"])
        vicini.setdefault(r["a"], []).append(r["da"])
    livello, coda = {argomento: 0}, [argomento]
    while coda:
        n = coda.pop(0)
        for v in vicini.get(n, []):
            if v not in livello:
                livello[v] = livello[n] + 1
                coda.append(v)
    for n in vicini:
        livello.setdefault(n, max(livello.values()) + 1)
    righe = {}
    for n, l in livello.items():
        righe.setdefault(l, []).append(n)
    # Al massimo 7 concetti per riga (la pagina è orizzontale).
    file_ = []
    for l in sorted(righe):
        for i in range(0, len(righe[l]), 7):
            file_.append((l, righe[l][i:i + 7]))
    colori = [ORO, (58, 48, 32), (32, 46, 54), (44, 38, 58), (34, 50, 40)]
    sinistra, larghezza = 12, pdf.w - 24
    y, alto_riga = pdf.get_y() + 4, min(24, (pdf.h - pdf.get_y() - 30) / max(1, len(file_)))
    posizioni = {}
    for l, nodi in file_:
        passo = larghezza / len(nodi)
        for i, n in enumerate(nodi):
            posizioni[n] = (sinistra + passo * (i + 0.5), y, min(36, passo - 3))
        y += alto_riga
    # Prima le frecce (sotto i riquadri), con il verbo a metà.
    pdf.set_draw_color(110, 116, 128)
    pdf.set_line_width(0.3)
    for r in relazioni:
        if r["da"] in posizioni and r["a"] in posizioni:
            x1, y1, _ = posizioni[r["da"]]
            x2, y2, _ = posizioni[r["a"]]
            pdf.line(x1, y1 + 5, x2, y2 + 5)
            pdf.set_font(pdf.carattere, "", 6)
            pdf.set_text_color(190, 185, 175)
            etichetta = _pulisci(pdf, r["relazione"])[:28]
            pdf.text((x1 + x2) / 2 - pdf.get_string_width(etichetta) / 2, (y1 + y2) / 2 + 5, etichetta)
    for n, (x, yy, w) in posizioni.items():
        colore = colori[min(livello[n], len(colori) - 1)]
        pdf.set_fill_color(*colore)
        pdf.set_draw_color(*(ORO if livello[n] <= 1 else BORDO))
        pdf.rect(x - w / 2, yy, w, 10, "DF", round_corners=True)
        pdf.set_text_color(*(INCHIOSTRO if livello[n] == 0 else TESTO))
        pdf.set_font(pdf.carattere, "B" if livello[n] == 0 else "", 7)
        pdf.set_xy(x - w / 2, yy + 1)
        pdf.multi_cell(w, 3.4, _pulisci(pdf, n)[:60], align="C", new_x="LEFT", new_y="TOP", max_line_height=3.4)
    pdf.set_text_color(*TESTO)
    pdf.add_page()
    _titolo(pdf, "I collegamenti della mappa")
    pdf.set_font(pdf.carattere, "", 10)
    for r in relazioni:
        pdf.multi_cell(0, 5.5, _pulisci(pdf, f"• {r['da']} → {r['relazione']} → {r['a']}"))
    return _chiudi(pdf)


def _rgb(esadecimale):
    esadecimale = esadecimale.lstrip("#")
    return tuple(int(esadecimale[i:i + 2], 16) for i in (0, 2, 4))


def documento_percorso(codice, nome, livello_grado="universita"):
    """Il percorso (glicolisi, ciclo di Krebs...) passaggio per passaggio, con i colori della legenda
    e la scheda sotto ogni molecola, come nel sito."""
    import percorsi
    dati = percorsi.percorsi()[nome]
    pdf = _documento(codice, "Percorso passo per passo")
    pdf.add_page()
    larghezza = pdf.w - pdf.l_margin - pdf.r_margin

    def spazio(alto):
        if pdf.get_y() + alto > pdf.h - 28:
            pdf.add_page()

    def righe(testo, w, dimensione):
        pdf.set_font(pdf.carattere, "", dimensione)
        return len(pdf.multi_cell(w, 4, _pulisci(pdf, testo), dry_run=True, output="LINES")) if testo else 0

    def misura(nome_m, w):
        testo, clinica = percorsi.spiegazione(nome_m, livello_grado)
        formula = percorsi.formula_png(nome_m)
        wt = w - 8 - (36 if formula else 0)
        alto = 8 + 4 * (righe(testo, wt, 8.5) + righe(clinica and "Clinica: " + clinica, wt, 8)) + 2
        return max(alto, 30 if formula else 0), wt, testo, clinica, formula

    def card(nome_m, x, w, alto):
        s = percorsi.scheda(nome_m)
        colore = _rgb(percorsi.COLORI.get(s["tipo"], percorsi.COLORI["molecola"])[0])
        _, wt, testo, clinica, formula = misura(nome_m, w)
        y = pdf.get_y()
        pdf.set_fill_color(*FONDO)
        pdf.set_draw_color(*BORDO)
        pdf.rect(x, y, w, alto, "DF", round_corners=True)
        pdf.set_fill_color(*colore)
        pdf.rect(x, y, 1.6, alto, "F")
        if formula:
            pdf.image(io.BytesIO(formula), x=x + w - 37, y=y + (alto - 23) / 2, w=35, h=23)
        pdf.set_xy(x + 5, y + 2)
        pdf.set_font(pdf.carattere, "B", 10.5)
        pdf.set_text_color(*colore)
        pdf.cell(wt, 5, _pulisci(pdf, nome_m))
        pdf.set_xy(x + 5, y + 7.5)
        if testo:
            pdf.set_font(pdf.carattere, "", 8.5)
            pdf.set_text_color(*TESTO)
            pdf.multi_cell(wt, 4, _pulisci(pdf, testo), new_x="LEFT")
        if clinica:
            pdf.set_font(pdf.carattere, "", 8)
            pdf.set_text_color(*_rgb(percorsi.ROSSO))
            pdf.multi_cell(wt, 4, _pulisci(pdf, "Clinica: " + clinica), new_x="LEFT")

    def fila(nomi):
        w = (larghezza - 4 * (len(nomi) - 1)) / len(nomi)
        alto = max(misura(n, w)[0] for n in nomi)
        spazio(alto)
        y = pdf.get_y()
        for i, n in enumerate(nomi):
            pdf.set_y(y)
            card(n, pdf.l_margin + i * (w + 4), w, alto)
        pdf.set_y(y + alto + 1)

    def passo(numero, p):
        x = pdf.l_margin + 14
        w = larghezza - 14
        spiega, clinica = percorsi.spiegazione(p["enzima"], livello_grado)
        segni = ("  [senso unico]" if p.get("irreversibile") else "") + \
                ("  [regola la velocità]" if p.get("limitante") else "") + ("  ×2" if p.get("volte") == 2 else "")
        scambio = ""
        if p.get("entra") or p.get("esce"):
            scambio = f"entra: {', '.join(p.get('entra', [])) or '—'}   →   esce: {', '.join(p.get('esce', [])) or '—'}"
        alto = 6 + 4 * (righe(spiega, w, 8) + righe(clinica and "Clinica: " + clinica, w, 8)
                         + (1 if scambio else 0) + righe(p["nota"], w, 9)) + 3
        spazio(alto)
        y = pdf.get_y()
        pdf.set_draw_color(*_rgb(percorsi.COLORI["enzima"][0]))
        pdf.set_line_width(0.5)
        pdf.dashed_line(pdf.l_margin + 6, y, pdf.l_margin + 6, y + alto, 1.2, 1)
        pdf.set_line_width(0.2)
        pdf.set_fill_color(*ORO)
        pdf.ellipse(pdf.l_margin + 2, y + 0.5, 8, 8, "F")
        pdf.set_text_color(*INCHIOSTRO)
        pdf.set_font(pdf.carattere, "B", 9)
        pdf.set_xy(pdf.l_margin + 2, y + 2.3)
        pdf.cell(8, 4, str(numero), align="C")
        pdf.set_xy(x, y + 1)
        pdf.set_font(pdf.carattere, "B", 10)
        pdf.set_text_color(*_rgb(percorsi.COLORI["enzima"][0]))
        chi = ("Enzima: " if percorsi.scheda(p["enzima"]).get("tipo") == "enzima" else "Chi lo fa: ") + p["enzima"]
        pdf.cell(pdf.get_string_width(_pulisci(pdf, chi)) + 2, 5, _pulisci(pdf, chi))
        if segni:
            pdf.set_text_color(*_rgb(percorsi.ROSSO))
            pdf.set_font(pdf.carattere, "B", 8)
            pdf.cell(0, 5, _pulisci(pdf, segni))
        pdf.set_xy(x, y + 6.5)
        if spiega:
            pdf.set_font(pdf.carattere, "", 8)
            pdf.set_text_color(*GRIGIO)
            pdf.multi_cell(w, 4, _pulisci(pdf, spiega), new_x="LEFT")
        if clinica:
            pdf.set_font(pdf.carattere, "", 8)
            pdf.set_text_color(*_rgb(percorsi.ROSSO))
            pdf.multi_cell(w, 4, _pulisci(pdf, "Clinica: " + clinica), new_x="LEFT")
        if scambio:
            pdf.set_font(pdf.carattere, "B", 8.5)
            pdf.set_text_color(*ORO)
            pdf.multi_cell(w, 4, _pulisci(pdf, scambio), new_x="LEFT")
        pdf.set_font(pdf.carattere, "", 9)
        pdf.set_text_color(*TESTO)
        pdf.multi_cell(w, 4, _pulisci(pdf, p["nota"]), new_x="LEFT")
        pdf.set_y(y + alto)

    _titolo(pdf, dati["titolo"])
    pdf.set_font(pdf.carattere, "", 9)
    pdf.set_text_color(*GRIGIO)
    pdf.multi_cell(0, 4.5, _pulisci(pdf, "Dove: " + dati["dove"] + " · spiegazioni per: " + percorsi.GRADI[livello_grado]))
    pdf.set_text_color(*TESTO)
    pdf.multi_cell(0, 4.5, _pulisci(pdf, dati["intro"]))
    pdf.ln(2)
    # La legenda dei colori.
    pdf.set_font(pdf.carattere, "", 7.5)
    for colore, testo in list(percorsi.COLORI.values()) + [(percorsi.ROSSO, "Passaggio a senso unico")]:
        w = pdf.get_string_width(testo) + 9
        if pdf.get_x() + w > pdf.w - pdf.r_margin:
            pdf.ln(5)
        pdf.set_fill_color(*_rgb(colore))
        pdf.rect(pdf.get_x(), pdf.get_y() + 1, 3, 3, "F")
        pdf.set_x(pdf.get_x() + 4)
        pdf.set_text_color(*TESTO)
        pdf.cell(w - 4, 5, testo)
    pdf.ln(8)
    fasi = {f["da"]: f["nome"] for f in dati.get("fasi", [])}
    fila([dati["inizio"]])
    ultimi = [dati["inizio"]]
    for i, p in enumerate(dati["passaggi"], 1):
        if i in fasi:
            spazio(30)
            pdf.ln(1)
            pdf.set_font(pdf.carattere, "B", 10)
            pdf.set_text_color(*ORO)
            pdf.multi_cell(0, 6, _pulisci(pdf, fasi[i]))
        nuovi = [d for d in p["da"] if d not in ultimi]
        if nuovi:
            fila(nuovi)
        passo(i, p)
        fila(p["a"])
        ultimi = p["a"]
    spazio(30)
    _titolo(pdf, dati.get("titolo_bilancio", "Il bilancio"))
    pdf.set_font(pdf.carattere, "", 10)
    for b in dati["bilancio"]:
        pdf.multi_cell(0, 5.5, _pulisci(pdf, "• " + b))
    dopo = dati.get("dopo")
    if dopo:
        spazio(50)
        _titolo(pdf, dopo["titolo"])
        for s in dopo["strade"]:
            spazio(45)
            pdf.set_font(pdf.carattere, "B", 10)
            pdf.set_text_color(*ORO)
            pdf.multi_cell(0, 6, _pulisci(pdf, s["condizione"]))
            passo("→", s)
            fila([s["a"]])
            if s.get("prossimo"):
                pdf.set_font(pdf.carattere, "B", 9)
                pdf.set_text_color(*_rgb(percorsi.COLORI["enzima"][0]))
                pdf.multi_cell(0, 5, _pulisci(pdf, "Continua: " + s["prossimo"]))
            pdf.ln(2)
    for box in dati.get("da_sapere", []):
        spazio(40)
        _titolo(pdf, "Da sapere: " + box["titolo"])
        for titolo, nomi in box["voci"]:
            pdf.set_font(pdf.carattere, "B", 9.5)
            pdf.set_text_color(*ORO)
            pdf.multi_cell(0, 5, _pulisci(pdf, titolo))
            pdf.set_font(pdf.carattere, "", 9)
            pdf.set_text_color(*TESTO)
            for n in nomi:
                pdf.multi_cell(0, 4.6, _pulisci(pdf, f"• {n}: {percorsi.spiegazione(n, 'superiore')[0]}"))
    return _chiudi(pdf)


def documento_quaderno(codice, gruppi):
    """Il quaderno intero in PDF: per ogni argomento le voci salvate (ricerche, percorsi, mappe,
    documenti, errori da rivedere, note), con data e fonti. `gruppi` = [(argomento, [voce, ...])]."""
    pdf = _documento(codice, "Il tuo quaderno di studio")
    pdf.add_page()
    for argomento, voci in gruppi:
        pdf.ln(2)
        pdf.set_font(pdf.carattere, "B", 15)
        pdf.set_text_color(*ORO)
        pdf.multi_cell(0, 8, _pulisci(pdf, argomento))
        pdf.set_text_color(*TESTO)
        for voce in voci:
            _titolo(pdf, _pulisci(pdf, f"{voce['etichetta']} · {voce['titolo']}"))
            pdf.set_font(pdf.carattere, "", 9)
            pdf.multi_cell(0, 5, _pulisci(pdf, f"Salvato il {voce['data']}"))
            pdf.set_font(pdf.carattere, "", 11)
            for riga in _pulisci(pdf, voce.get("testo", "")).splitlines():
                if riga.strip():
                    pdf.multi_cell(0, 6, riga.replace("**", "").strip().lstrip("-• ").strip())
            if voce.get("fonti"):
                pdf.set_font(pdf.carattere, "", 9)
                pdf.multi_cell(0, 5, _pulisci(pdf, "Fonti: " + " · ".join(voce["fonti"])))
                pdf.set_font(pdf.carattere, "", 11)
            pdf.ln(2)
    return _chiudi(pdf)
