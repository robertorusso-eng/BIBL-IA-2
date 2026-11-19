"""Le email di BIBL-IA 2 (il codice per i professori), mandate dalla casella scelta dal proprietario.

La casella si imposta con imposta_email.command: server, indirizzo e password (per Gmail una «password per le
app»). Restano solo sul Mac, in .streamlit/posta.json (in .gitignore). Senza casella le email non partono e le
richieste dei professori le controlla a mano il proprietario.
"""
import json
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

CONFIG = Path(__file__).resolve().parent / ".streamlit" / "posta.json"


def attiva():
    try:
        c = json.loads(CONFIG.read_text(encoding="utf-8"))
        return all(c.get(k) for k in ("server", "porta", "utente", "password"))
    except (OSError, ValueError):
        return False


def manda(a, oggetto, testo):
    """Manda l'email. Restituisce "" se è partita, altrimenti il motivo (senza dati riservati)."""
    try:
        c = json.loads(CONFIG.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "La casella email di BIBL-IA non è impostata."
    m = EmailMessage()
    m["From"] = c.get("mittente") or c["utente"]
    m["To"] = a
    m["Subject"] = oggetto
    m.set_content(testo)
    try:
        if int(c["porta"]) == 465:
            with smtplib.SMTP_SSL(c["server"], 465, context=ssl.create_default_context(), timeout=30) as s:
                s.login(c["utente"], c["password"])
                s.send_message(m)
        else:
            with smtplib.SMTP(c["server"], int(c["porta"]), timeout=30) as s:
                s.starttls(context=ssl.create_default_context())
                s.login(c["utente"], c["password"])
                s.send_message(m)
    except (OSError, smtplib.SMTPException):
        return "L'email non è partita: riprova tra poco."
    return ""
