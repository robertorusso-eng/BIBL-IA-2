"""Gli account di BIBL-IA 2, solo su invito.

Il proprietario (chi apre l'app sul Mac, da localhost) entra senza password con il suo profilo di sempre.
Chi arriva da fuori deve avere un account; per crearlo serve un codice di invito, che genera il proprietario
nel «Pannello di gestione». Ogni account ha il suo profilo in profili_v2/<nome utente>.json.

Tutto resta sul Mac (account_v2.json e profili_v2/ sono in .gitignore). Le password non si salvano mai:
si salva solo un'impronta (PBKDF2-SHA256 con sale casuale), come fanno i siti seri.
"""
import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_PROVE = bool(__import__("os").environ.get("BIBLIA_PROVE"))   # il server delle prove usa file a parte
ACCOUNT_FILE = ROOT / ("prove/account_prove.json" if _PROVE else "account_v2.json")
PROFILI_DIR = ROOT / ("prove/profili_prove" if _PROVE else "profili_v2")
GIRI = 200_000                      # giri di PBKDF2: rendono lento indovinare le password
DURATA_ACCESSO = 30 * 24 * 3600     # «resta collegato» per 30 giorni
TENTATIVI_MAX = 5                   # dopo 5 password sbagliate si aspetta 5 minuti
ATTESA = 5 * 60
NOME_VALIDO = re.compile(r"^[a-z0-9._-]{3,30}$")
_BLOCCO = threading.Lock()          # più studenti insieme non devono rovinare il file


def _leggi():
    try:
        dati = json.loads(ACCOUNT_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        dati = {}
    except (OSError, ValueError):
        # File rovinato: se ne tiene una copia e ci si ferma, invece di riscriverlo vuoto (si perderebbero gli account).
        copia = ACCOUNT_FILE.with_name(ACCOUNT_FILE.name + f".rotto-{int(time.time())}")
        try:
            copia.write_bytes(ACCOUNT_FILE.read_bytes())
        except OSError:
            pass
        raise RuntimeError("Il file degli account non si legge: ne ho salvato una copia. Ripristinalo da un backup.")
    for k in ("utenti", "inviti", "accessi"):
        dati.setdefault(k, {})
    return dati


def _scrivi(dati):
    temporaneo = ACCOUNT_FILE.with_suffix(".tmp")
    temporaneo.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")
    temporaneo.chmod(0o600)
    temporaneo.replace(ACCOUNT_FILE)


def _impronta(password, sale):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(sale), GIRI).hex()


def _ora():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def file_profilo(utente):
    return PROFILI_DIR / f"{utente}.json"


# --- Inviti ---------------------------------------------------------------------------------------------

def crea_invito(per_chi="", docente=False):
    """Un codice nuovo, da usare una volta sola (per esempio BIBL-7KQ2-M9XA). Con docente=True chi lo usa
    diventa professore: può creare classi e invitare i suoi studenti con il codice della classe."""
    alfabeto = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"   # niente 0/O e 1/I, che si confondono
    codice = "BIBL-" + "".join(secrets.choice(alfabeto) for _ in range(4)) + "-" + \
             "".join(secrets.choice(alfabeto) for _ in range(4))
    with _BLOCCO:
        dati = _leggi()
        dati["inviti"][codice] = {"per": per_chi.strip()[:60], "creato": _ora(), "usato_da": None,
                                  "docente": bool(docente)}
        _scrivi(dati)
    return codice


def elimina_invito(codice):
    with _BLOCCO:
        dati = _leggi()
        if dati["inviti"].get(codice, {}).get("usato_da") is None:
            dati["inviti"].pop(codice, None)
            _scrivi(dati)


def inviti():
    return _leggi()["inviti"]


# --- Account --------------------------------------------------------------------------------------------

def registra(codice, utente, nome, password, codice_di_classe=False):
    """Crea l'account con un invito (o con il codice di una classe aperta: codice_di_classe=True, controllato da
    chi chiama). Restituisce "" se va bene, altrimenti il motivo (da mostrare)."""
    codice = codice.strip().upper()
    utente = utente.strip().lower()
    if not NOME_VALIDO.match(utente):
        return "Il nome utente deve avere da 3 a 30 caratteri: lettere minuscole, numeri, punto, trattino."
    if len(password) < 8:
        return "La password deve avere almeno 8 caratteri."
    with _BLOCCO:
        dati = _leggi()
        invito = dati["inviti"].get(codice)
        if codice_di_classe:
            invito = {"classe": codice}
        elif not invito or invito.get("usato_da"):
            return "Il codice di invito non è valido o è già stato usato."
        if utente in dati["utenti"]:
            return "Questo nome utente esiste già: scegline un altro."
        sale = secrets.token_hex(16)
        dati["utenti"][utente] = {"nome": nome.strip()[:60], "sale": sale, "impronta": _impronta(password, sale),
                                  "creato": _ora(), "ultimo_accesso": None, "attivo": True,
                                  "docente": bool(invito.get("docente")), "invito": codice}
        invito["usato_da"] = utente
        invito["usato_il"] = _ora()
        PROFILI_DIR.mkdir(exist_ok=True)
        f = file_profilo(utente)
        if not f.exists():
            f.write_text(json.dumps({"nome": nome.strip()[:60]}, ensure_ascii=False), encoding="utf-8")
        _scrivi(dati)
    return ""


def accedi(utente, password):
    """Controlla nome utente e password. Restituisce (True, "") oppure (False, motivo)."""
    utente = utente.strip().lower()
    with _BLOCCO:
        dati = _leggi()
        u = dati["utenti"].get(utente)
        if u and u.get("bloccato_fino", 0) > time.time():
            return False, "Troppe password sbagliate: riprova tra qualche minuto."
        if not u or not u.get("attivo", True):
            _impronta(password, "00" * 16)     # stesso tempo di risposta: non si capisce se l'utente esiste
            return False, "Nome utente o password sbagliati."
        if not hmac.compare_digest(_impronta(password, u["sale"]), u["impronta"]):
            u["sbagliate"] = u.get("sbagliate", 0) + 1
            if u["sbagliate"] >= TENTATIVI_MAX:
                u["bloccato_fino"] = time.time() + ATTESA
                u["sbagliate"] = 0
            _scrivi(dati)
            return False, "Nome utente o password sbagliati."
        u["sbagliate"] = 0
        u["ultimo_accesso"] = _ora()
        _scrivi(dati)
    return True, ""


def cambia_password(utente, vecchia, nuova):
    ok, motivo = accedi(utente, vecchia)
    if not ok:
        return motivo
    if len(nuova) < 8:
        return "La password nuova deve avere almeno 8 caratteri."
    with _BLOCCO:
        dati = _leggi()
        sale = secrets.token_hex(16)
        dati["utenti"][utente].update(sale=sale, impronta=_impronta(nuova, sale))
        # Cambiata la password, si esce da tutti gli altri dispositivi.
        dati["accessi"] = {k: v for k, v in dati["accessi"].items() if v["utente"] != utente}
        _scrivi(dati)
    return ""


def utenti():
    return {k: {c: v for c, v in u.items() if c not in ("sale", "impronta")} for k, u in _leggi()["utenti"].items()}


def utente(nome):
    return utenti().get(nome)


def imposta(utente, **campi):
    """Per il proprietario: attiva/disattiva un account o lo segna come docente."""
    with _BLOCCO:
        dati = _leggi()
        if utente in dati["utenti"]:
            dati["utenti"][utente].update({k: v for k, v in campi.items() if k in ("attivo", "docente")})
            if campi.get("attivo") is False:
                dati["accessi"] = {k: v for k, v in dati["accessi"].items() if v["utente"] != utente}
            _scrivi(dati)


# --- «Resta collegato»: un gettone casuale nel browser, sul Mac solo la sua impronta --------------------

def nuovo_gettone(utente):
    gettone = secrets.token_urlsafe(32)
    with _BLOCCO:
        dati = _leggi()
        adesso = time.time()
        dati["accessi"] = {k: v for k, v in dati["accessi"].items() if v["scade"] > adesso}
        dati["accessi"][hashlib.sha256(gettone.encode()).hexdigest()] = {"utente": utente,
                                                                         "scade": adesso + DURATA_ACCESSO}
        _scrivi(dati)
    return gettone


def utente_del_gettone(gettone):
    if not gettone:
        return None
    dati = _leggi()
    voce = dati["accessi"].get(hashlib.sha256(gettone.encode()).hexdigest())
    if not voce or voce["scade"] < time.time():
        return None
    u = dati["utenti"].get(voce["utente"])
    return voce["utente"] if u and u.get("attivo", True) else None


def esci(gettone):
    if not gettone:
        return
    with _BLOCCO:
        dati = _leggi()
        if dati["accessi"].pop(hashlib.sha256(gettone.encode()).hexdigest(), None):
            _scrivi(dati)


# --- Professori che si presentano da soli: email della scuola, codice via email, controllo dell'AI ---------
# Il professore dichiara chi è (scuola, città, classi) e scrive l'email della scuola. Riceve un'email con la sua
# dichiarazione e un codice: scrivendo il codice dimostra che quell'email è sua. Poi l'AI del Mac guarda se
# l'email è coerente con la scuola dichiarata. Se l'email è di un dominio scolastico ufficiale e l'AI è d'accordo,
# l'account da professore si attiva da solo; negli altri casi decide il proprietario nel Pannello di gestione.

EMAIL_PERSONALI = {"gmail.com", "googlemail.com", "libero.it", "hotmail.com", "hotmail.it", "outlook.com",
                   "outlook.it", "live.com", "live.it", "yahoo.com", "yahoo.it", "icloud.com", "me.com", "alice.it",
                   "tiscali.it", "virgilio.it", "tim.it", "fastwebnet.it", "email.it", "inwind.it", "aol.com",
                   "proton.me", "protonmail.com", "gmx.com", "gmx.it", "pec.it", "legalmail.it"}
UNIVERSITA_SENZA_UNI = {"polimi.it", "polito.it", "sns.it", "sissa.it", "iuss.it", "luiss.it", "unibocconi.it",
                        "santannapisa.it", "imtlucca.it", "gssi.it", "iulm.it", "lumsa.it", "hunimed.eu", "humanitas.it",
                        "uniroma1.it", "iusspavia.it", "ucsc.it"}
# Solo i domini veri delle università italiane: un nome come «unixyz.it» lo può comprare chiunque, quindi non basta
# che cominci con «uni» (gli altri vanno controllati dal proprietario).
UNIVERSITA = UNIVERSITA_SENZA_UNI | {
    "unibo.it", "unipd.it", "unimi.it", "unito.it", "unina.it", "unipi.it", "unifi.it", "unige.it", "unipv.it",
    "unimib.it", "unitn.it", "univr.it", "unive.it", "units.it", "uniud.it", "unimore.it", "unipr.it", "unife.it",
    "uniba.it", "poliba.it", "unisalento.it", "unifg.it", "unict.it", "unipa.it", "unime.it", "unical.it",
    "unicz.it", "unirc.it", "unisa.it", "unicampania.it", "uniparthenope.it", "unior.it", "unisob.na.it",
    "unicas.it", "uniroma2.it", "uniroma3.it", "uniroma4.it", "unitus.it", "univaq.it", "unite.it", "unich.it",
    "unimol.it", "unibas.it", "uniss.it", "unica.it", "unipg.it", "unistrapg.it", "unicam.it", "univpm.it",
    "uniurb.it", "unimc.it", "unisi.it", "unistrasi.it", "unibs.it", "unibg.it", "uninsubria.it", "unipmn.it",
    "uniupo.it", "unisr.it", "unimib.it", "unicatt.it", "unibz.it", "unikore.it", "unicusano.it", "uniroma5.it",
    "unicampus.it", "unimercatorum.it", "unipegaso.it", "uninettunouniversity.net"}
EMAIL_VALIDA = re.compile(r"^[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$")
CODICE_DURATA = 30 * 60


def dominio(email):
    return email.rsplit("@", 1)[-1].lower().strip()


def tipo_dominio(email):
    """«ufficiale» (scuola statale o università), «personale» (gmail, libero...) oppure «da controllare»."""
    d = dominio(email)
    if d in EMAIL_PERSONALI:
        return "personale"
    if re.search(r"(^|\.)stud(enti|ent|ents)?\.", d) or d.startswith("studenti"):
        return "personale"                       # le email degli studenti universitari non valgono
    if d in ("istruzione.it", "posta.istruzione.it") or d.endswith(".edu.it") or d.endswith(".istruzione.it"):
        return "ufficiale"
    if d in UNIVERSITA or any(d.endswith("." + u) for u in UNIVERSITA):
        return "ufficiale"
    return "da controllare"


def nuova_richiesta(nome, scuola, citta, classi, email, utente, password):
    """Salva la richiesta del professore (la password solo come impronta) e prepara il codice da mandare via
    email. Restituisce (id, codice, "") oppure (None, None, motivo)."""
    utente, email = utente.strip().lower(), email.strip().lower()
    if not all(x.strip() for x in (nome, scuola, citta, classi)):
        return None, None, "Scrivi nome, scuola, città e classi."
    if not EMAIL_VALIDA.match(email):
        return None, None, "L'email non è scritta bene."
    if tipo_dominio(email) == "personale":
        return None, None, "Serve l'email della tua scuola o università, non quella personale."
    if not NOME_VALIDO.match(utente):
        return None, None, "Il nome utente deve avere da 3 a 30 caratteri: lettere minuscole, numeri, punto, trattino."
    if len(password) < 8:
        return None, None, "La password deve avere almeno 8 caratteri."
    with _BLOCCO:
        dati = _leggi()
        richieste = dati.setdefault("richieste", {})
        if utente in dati["utenti"] or any(r["utente"] == utente and r["stato"] in ("da confermare", "in attesa")
                                           for r in richieste.values()):
            return None, None, "Questo nome utente esiste già: scegline un altro."
        ora = time.time()
        recenti = [r for r in richieste.values() if r["email"] == email and ora - r.get("t", 0) < 3600]
        if len(recenti) >= 3:
            return None, None, "Troppe richieste con questa email: riprova tra un'ora."
        # In tutto al massimo 15 richieste all'ora: BIBL-IA non deve diventare un modo per mandare email a chiunque.
        if sum(1 for r in richieste.values() if ora - r.get("t", 0) < 3600) >= 15:
            return None, None, "Troppe richieste in questo momento: riprova tra un'ora."
        # Le richieste mai confermate e scadute da più di un giorno si cancellano (il file non cresce all'infinito).
        for k in [k for k, r in richieste.items() if r["stato"] == "da confermare" and ora - r.get("t", 0) > 86400]:
            del richieste[k]
        ident = secrets.token_hex(6)
        codice = f"{secrets.randbelow(10 ** 6):06d}"
        sale = secrets.token_hex(16)
        richieste[ident] = {"nome": nome.strip()[:80], "scuola": scuola.strip()[:120], "citta": citta.strip()[:60],
                            "classi": classi.strip()[:200], "email": email, "utente": utente, "sale": sale,
                            "impronta": _impronta(password, sale), "codice": hashlib.sha256(codice.encode()).hexdigest(),
                            "scade": ora + CODICE_DURATA, "tentativi": 0, "t": ora, "creata": _ora(),
                            "stato": "da confermare", "dominio": tipo_dominio(email), "ai": None}
        _scrivi(dati)
    return ident, codice, ""


def conferma_codice(ident, codice):
    """Il professore scrive il codice ricevuto via email. Restituisce "" se è giusto, altrimenti il motivo."""
    with _BLOCCO:
        dati = _leggi()
        r = dati.get("richieste", {}).get(ident)
        if not r or r["stato"] != "da confermare":
            return "Richiesta non trovata: ricomincia."
        if time.time() > r["scade"]:
            return "Il codice è scaduto: ricomincia."
        if r["tentativi"] >= 5:
            return "Troppi codici sbagliati: ricomincia."
        if not hmac.compare_digest(hashlib.sha256(codice.strip().encode()).hexdigest(), r["codice"]):
            r["tentativi"] += 1
            _scrivi(dati)
            return "Il codice non è giusto."
        r["stato"] = "in attesa"
        r["email_confermata"] = _ora()
        _scrivi(dati)
    return ""


def richieste(stato=None):
    tutte = _leggi().get("richieste", {})
    return {k: {c: v for c, v in r.items() if c not in ("sale", "impronta", "codice")}
            for k, r in tutte.items() if stato is None or r["stato"] == stato}


def segna_parere_ai(ident, parere):
    with _BLOCCO:
        dati = _leggi()
        if ident in dati.get("richieste", {}):
            dati["richieste"][ident]["ai"] = parere
            _scrivi(dati)


def approva(ident):
    """Crea l'account da professore dalla richiesta (con la password che aveva scelto)."""
    with _BLOCCO:
        dati = _leggi()
        r = dati.get("richieste", {}).get(ident)
        if not r or r["stato"] != "in attesa" or r["utente"] in dati["utenti"]:
            return False
        dati["utenti"][r["utente"]] = {"nome": r["nome"], "sale": r["sale"], "impronta": r["impronta"],
                                       "creato": _ora(), "ultimo_accesso": None, "attivo": True, "docente": True,
                                       "invito": f"richiesta {ident}", "email_scuola": r["email"],
                                       "scuola": r["scuola"], "citta": r["citta"], "classi": r["classi"]}
        r["stato"] = "approvata"
        r["decisa"] = _ora()
        PROFILI_DIR.mkdir(exist_ok=True)
        f = file_profilo(r["utente"])
        if not f.exists():
            f.write_text(json.dumps({"nome": r["nome"], "ruolo": "docente"}, ensure_ascii=False), encoding="utf-8")
        _scrivi(dati)
    return True


def rifiuta(ident):
    with _BLOCCO:
        dati = _leggi()
        r = dati.get("richieste", {}).get(ident)
        if r:
            r["stato"] = "rifiutata"
            r["decisa"] = _ora()
            _scrivi(dati)


def stato_richiesta(ident):
    return (_leggi().get("richieste", {}).get(ident) or {}).get("stato")


def in_attesa_senza_email(ident):
    """Quando la casella email di BIBL-IA non è impostata: la richiesta va subito al proprietario (email non
    confermata, lo vede scritto)."""
    with _BLOCCO:
        dati = _leggi()
        r = dati.get("richieste", {}).get(ident)
        if r and r["stato"] == "da confermare":
            r["stato"] = "in attesa"
            r["email_confermata"] = None
            _scrivi(dati)


def richiesta_di(utente):
    for r in _leggi().get("richieste", {}).values():
        if r["utente"] == utente.strip().lower() and r["stato"] in ("in attesa", "rifiutata"):
            return r["stato"]
    return None
