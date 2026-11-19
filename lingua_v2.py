"""Il cambio di lingua di BIBL-IA 2 (italiano / inglese).

Le scritte dell'interfaccia si traducono quando si mostrano: le funzioni di Streamlit (markdown, button, radio…)
passano dal traduttore, che usa i dizionari in traduzioni_ui/en_*.json (italiano esatto → inglese). Le parti fisse
delle frasi composte (f-string) si traducono come frammenti. I valori restituiti dai widget non cambiano mai, quindi
la logica dell'app resta in italiano. Le lezioni e le domande (contenuti) restano in italiano: si traducono a richiesta.
"""
import functools
import json
import re
from pathlib import Path

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

CARTELLA = Path(__file__).resolve().parent / "traduzioni_ui"
_DIZIONARIO = {}
_FRAMMENTI = []
_CARICATO = []
TAG = re.compile(r"<[^>]+>")
# Le emoji decorative si tolgono da tutte le scritte: restano solo quelle che dicono qualcosa (giusto, sbagliato,
# attenzione, le bandiere della lingua, l'accessibilità). Al posto delle emoji: parole e icone semplici.
EMOJI_UTILI = {"✅", "❌", "⚠", "✓", "✔", "✗", "✕", "✖", "♂", "♀", "★", "☆", "🇮🇹", "🇬🇧"}
_TASTI = re.compile("([0-9#*])\uFE0F?\u20E3")
_EMOJI = re.compile("(?:[\U0001F1E6-\U0001F1FF]{2}|[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u23E9-\u23FA"
                    "\u231A\u231B\u2328\u2139\u24C2\u3030\u303D\u3297\u3299](?:\uFE0F|\u200D|[\U0001F3FB-\U0001F3FF])*"
                    "(?:\u200D[\U0001F000-\U0001FAFF\u2600-\u27BF](?:\uFE0F)?)*|\u20E3)[ \u00A0]?")


# Le emoji usate da sole come icona (dentro un cerchio o un riquadro) diventano icone a linea, come quelle del menu.
ICONE_LINEA = {"🩺": "stethoscope", "🧬": "genetics", "⚗": "science", "⚛": "bolt", "📐": "straighten", "🌋": "volcano", "💻": "computer",
               "🧪": "science", "🔬": "biotech", "🏭": "factory", "🧫": "biotech", "🫀": "cardiology", "🦠": "coronavirus",
               "🌿": "eco", "🔭": "travel_explore", "🔌": "electrical_services", "☢": "flare", "📊": "bar_chart",
               "🧮": "calculate", "🔥": "local_fire_department", "🌱": "potted_plant", "💊": "medication",
               "🧱": "grid_view", "🧩": "extension", "📖": "menu_book", "📘": "menu_book", "📚": "library_books",
               "🕒": "schedule", "⏰": "alarm", "💬": "chat", "🔎": "search", "🔍": "search", "🗺": "map",
               "🎓": "school", "🤖": "smart_toy", "❓": "help", "📄": "description", "🎮": "sports_esports",
               "🗂": "folder", "⏱": "timer", "🏆": "emoji_events", "🎯": "flag", "📈": "trending_up", "📝": "edit_note",
               "🔁": "replay", "🔄": "replay", "🗓": "calendar_month", "📅": "calendar_month", "🧭": "explore",
               "👩‍🏫": "co_present", "🧑‍🎓": "school", "🆘": "support", "⭐": "star", "💳": "credit_card",
               "🔖": "bookmark", "⚙": "settings", "🧰": "construction", "🔔": "notifications", "🧠": "psychology",
               "💡": "lightbulb", "🎉": "celebration", "👍": "thumb_up", "📌": "push_pin", "📦": "inventory_2"}
_DA_SOLA = re.compile(r">(\s*)([^<>\sA-Za-z0-9]{1,12})(\s*)<")


def _icona(m):
    nucleo = m.group(2).replace("\uFE0F", "")
    if nucleo in ICONE_LINEA:
        return f'>{m.group(1)}<span class="ico">{ICONE_LINEA[nucleo]}</span>{m.group(3)}<'
    if _EMOJI.fullmatch(m.group(2)) and nucleo not in EMOJI_UTILI:
        return f'>{m.group(1)}<span class="ico">school</span>{m.group(3)}<'
    return m.group(0)


def senza_emoji(testo):
    """La scritta senza le emoji decorative (e senza lo spazio che le seguiva)."""
    if not isinstance(testo, str) or not testo:
        return testo
    def via(m):
        e = m.group(0)
        return e if e.strip().replace("\uFE0F", "") in EMOJI_UTILI else ""
    if "<" in testo:
        testo = _DA_SOLA.sub(_icona, testo)
    # La spunta verde a colori diventa un segno semplice: in elenchi lunghi le emoji verdi erano troppe.
    return _EMOJI.sub(via, _TASTI.sub(r"\1.", testo)).replace("\u2705", "\u2713")


def _carica():
    firma = tuple((f.name, f.stat().st_mtime_ns) for f in sorted(CARTELLA.glob("en_*.json")))
    if _CARICATO and _CARICATO[0] == firma:
        return
    _CARICATO[:] = [firma]
    _DIZIONARIO.clear()
    _FRAMMENTI.clear()
    for f in sorted(CARTELLA.glob("en_*.json")):
        try:
            _DIZIONARIO.update({k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items()
                                if isinstance(v, str) and v})
        except (OSError, ValueError):
            pass
    # I frammenti: pezzi di almeno 6 caratteri con uno spazio, dal più lungo (così non si spezzano le frasi).
    _FRAMMENTI.extend(sorted(((k, v) for k, v in _DIZIONARIO.items()
                              if k != v and 5 <= len(k.strip()) <= 2500
                              and (" " in k.strip() or k != k.strip())),
                             key=lambda x: -len(x[0])))


def inglese():
    try:
        return st.session_state.get("lingua", "it") == "en"
    except Exception:  # fuori da una sessione Streamlit (prove automatiche)
        return False


def tr(testo):
    """La scritta nella lingua scelta (in italiano resta com'è)."""
    if not isinstance(testo, str) or not testo or not inglese():
        return testo
    _carica()
    if testo in _DIZIONARIO:
        return _DIZIONARIO[testo]
    nudo = testo.strip()
    if nudo in _DIZIONARIO:
        return testo.replace(nudo, _DIZIONARIO[nudo])
    # Testi lunghi senza HTML sono contenuti (lezioni, spiegazioni): non si toccano.
    if len(testo) > 700 and not TAG.search(testo):
        return testo
    risultato = testo
    for italiano, english in _FRAMMENTI:
        if italiano in risultato:
            risultato = risultato.replace(italiano, english)
    return risultato


def _formato(kwargs):
    originale = kwargs.get("format_func") or str
    kwargs["format_func"] = lambda x, f=originale: senza_emoji(tr(f(x)))


def scritta(testo):
    """Traduzione (se serve) e via le emoji decorative."""
    return senza_emoji(tr(testo))


def _avvolgi(funzione, primo=True, opzioni=False, elenco=False, tutti=False):
    @functools.wraps(funzione)
    def nuova(*args, **kwargs):
        args = list(args)
        # I metodi della classe ricevono «self» per primo; le funzioni del modulo no.
        inizio = 1 if args and isinstance(args[0], DeltaGenerator) else 0
        if tutti:
            args = [scritta(a) if isinstance(a, str) else a for a in args]
        elif elenco and len(args) > inizio and isinstance(args[inizio], (list, tuple)):
            args[inizio] = [scritta(a) for a in args[inizio]]
        elif primo and len(args) > inizio and isinstance(args[inizio], str):
            args[inizio] = scritta(args[inizio])
        for chiave in ("label", "placeholder", "help", "text", "body", "title"):
            if isinstance(kwargs.get(chiave), str):
                kwargs[chiave] = scritta(kwargs[chiave])
        # Le icone emoji dei pulsanti e dei collegamenti si tolgono; quelle a linea (:material/…:) restano.
        if isinstance(kwargs.get("icon"), str) and not kwargs["icon"].startswith(":material/") \
                and not senza_emoji(kwargs["icon"]).strip():
            kwargs["icon"] = None
        if opzioni:
            _formato(kwargs)
        return funzione(*args, **kwargs)
    nuova._tradotta = True
    return nuova


TESTO = ["markdown", "header", "subheader", "title", "caption", "info", "success", "warning", "error", "button",
         "link_button", "download_button", "form_submit_button", "expander", "popover", "toggle", "checkbox",
         "text_input", "text_area", "number_input", "date_input", "file_uploader", "page_link", "metric", "progress",
         "chat_input", "audio_input"]
# st.feedback non accetta format_func (le stelle non hanno testo da tradurre): non va nell'elenco.
OPZIONI = ["radio", "selectbox", "multiselect", "select_slider", "pills", "segmented_control"]


def attiva():
    """Mette il traduttore davanti alle funzioni di Streamlit (una volta sola)."""
    if getattr(st.markdown, "_tradotta", False):
        return
    for nome in TESTO + OPZIONI + ["tabs", "write"]:
        kwargs = {"opzioni": nome in OPZIONI, "elenco": nome == "tabs", "tutti": nome == "write"}
        if nome in ("progress", "chat_input"):
            kwargs["primo"] = nome == "chat_input"
        if hasattr(DeltaGenerator, nome):
            setattr(DeltaGenerator, nome, _avvolgi(getattr(DeltaGenerator, nome), **kwargs))
        if hasattr(st, nome):
            setattr(st, nome, _avvolgi(getattr(st, nome), **kwargs))
    st.spinner = _avvolgi(st.spinner)
    pagina = st.Page

    def pagina_tradotta(*args, **kwargs):
        if isinstance(kwargs.get("title"), str):
            kwargs["title"] = scritta(kwargs["title"])
        return pagina(*args, **kwargs)
    pagina_tradotta._tradotta = True
    st.Page = pagina_tradotta
