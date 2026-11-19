"""Pubblicazioni scientifiche per BIBL-IA: articoli di rassegna da Europe PMC (che comprende
PubMed), con titolo, rivista, anno, link e riassunto (abstract). Le ricerche restano salvate su
disco, così la stessa domanda non richiede internet una seconda volta."""
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

FILE_SALVATE = Path(__file__).resolve().parent / "pubblicazioni_salvate.json"
INDIRIZZO = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
AGENTE = {"User-Agent": "BIBL-IA (uso didattico)"}
# Parole delle domande che non servono a cercare un articolo.
PAROLE_VUOTE = set("""what which who whom whose why how when where is are was were be been being do does did
the a an of in on at to for from by with about and or as into than that this these those it its can could
should would will may might must tell me explain describe list give show please difference between role
main mean means meaning definition define happen happens occur occurs used use mechanism mechanisms action
actions function functions work works effect effects important""".split())

_salvate = None


def _leggi():
    global _salvate
    if _salvate is None:
        try:
            _salvate = json.loads(FILE_SALVATE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _salvate = {}
    return _salvate


def _scrivi():
    try:
        FILE_SALVATE.write_text(json.dumps(_salvate, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def parole_di_ricerca(domanda_inglese):
    """Le parole utili della domanda inglese: «How is tuberculosis transmitted?» → tuberculosis transmitted."""
    parole = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", domanda_inglese)
    return [p for p in parole if p.casefold() not in PAROLE_VUOTE and len(p) > 1][:8]


def testo_semplice(testo):
    testo = re.sub(r"<h4>([^<]*)</h4>", r" \1: ", testo or "")
    testo = html.unescape(re.sub(r"<[^>]+>", "", testo))
    return re.sub(r"\s+", " ", testo).strip()


def _richiesta(query, quante):
    # Le rassegne più citate sono quelle più solide; l'ordine per pertinenza di Europe PMC premia
    # invece gli articoli più recenti anche se parlano d'altro (fermentazione delle olive...).
    parametri = urllib.parse.urlencode({"query": query, "format": "json", "resultType": "core",
                                        "pageSize": quante, "sort": "CITED desc"})
    with urllib.request.urlopen(urllib.request.Request(f"{INDIRIZZO}?{parametri}", headers=AGENTE),
                                timeout=20) as risposta:
        return json.load(risposta).get("resultList", {}).get("result", [])


def cerca(domanda_inglese, quante=6):
    """Gli articoli più pertinenti: rassegne (review) degli ultimi 15 anni con il riassunto e le
    parole della domanda nel titolo; se non bastano, con le parole nel riassunto.
    Lista di dizionari; vuota senza internet."""
    parole = parole_di_ricerca(domanda_inglese)
    if not parole:
        return []
    chiave = " ".join(p.casefold() for p in parole) + f"|{quante}"
    salvate = _leggi()
    if chiave in salvate:
        return salvate[chiave]
    filtri = 'PUB_TYPE:"review" AND HAS_ABSTRACT:y AND PUB_YEAR:[2011 TO 2030] AND LANG:"eng"'
    # «transmitted» deve trovare anche «transmission»: ogni parola si cerca con le sue forme
    # (l'asterisco di Europe PMC nei campi TITLE e ABSTRACT trova pochissimo).
    def forme(campo, parola):
        radice = re.sub(r"(?:ted|ed|ing|ions?|s)$", "", parola) if len(parola) >= 7 else parola
        if radice == parola or len(radice) < 5:
            return f"{campo}:{parola}"
        varianti = {parola, radice, radice + "s", radice + "ed", radice + "ing", radice + "ion", radice + "ions"}
        if radice.endswith("t"):
            varianti |= {radice + "ted", radice[:-1] + "ssion"}
        return "(" + " OR ".join(f"{campo}:{v}" for v in sorted(varianti)) + ")"

    nel_titolo = " AND ".join(forme("TITLE", p) for p in parole)
    tentativi = [f"{nel_titolo} AND {filtri}"]
    if len(parole) > 2:
        # Le due parole più lunghe (di solito le più specifiche) nel titolo, le altre nel riassunto.
        principali = sorted(parole, key=len, reverse=True)[:2]
        tentativi.append(" AND ".join([forme("TITLE", p) for p in principali]
                                      + [forme("ABSTRACT", p) for p in parole if p not in principali]) + f" AND {filtri}")
    tentativi.append(" AND ".join(forme("ABSTRACT", p) for p in parole) + f" AND {filtri}")
    risultati = []
    try:
        for query in tentativi:
            visti = {r["id"] for r in risultati}
            risultati += [r for r in _richiesta(query, quante) if r.get("id") not in visti]
            if len(risultati) >= 3:
                break
    except (OSError, ValueError):
        return []
    articoli = []
    for r in risultati[:quante]:
        pmid, pmcid, doi = r.get("pmid"), r.get("pmcid"), r.get("doi")
        url = (f"https://europepmc.org/article/PMC/{pmcid}" if pmcid else
               f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else
               f"https://doi.org/{doi}" if doi else f"https://europepmc.org/article/{r.get('source')}/{r.get('id')}")
        autori = (r.get("authorString") or "").rstrip(".")
        if autori.count(",") >= 3:
            autori = autori.split(",")[0] + " et al."
        rivista = (r.get("journalInfo") or {}).get("journal", {}).get("title") or r.get("bookOrReportDetails", {}).get("publisher", "")
        articoli.append({"titolo": testo_semplice(r.get("title", "")).rstrip("."), "autori": autori,
                         "rivista": rivista, "anno": r.get("pubYear", ""), "url": url, "pmid": pmid or "",
                         "accesso_libero": r.get("isOpenAccess") == "Y",
                         "rassegna": any("review" in t.casefold() for t in (r.get("pubTypeList") or {}).get("pubType", [])),
                         "citazioni": r.get("citedByCount", 0),
                         "riassunto": testo_semplice(r.get("abstractText", ""))})
    salvate[chiave] = articoli
    _scrivi()
    return articoli


def frasi_dei_riassunti(articoli):
    """Le frasi dei riassunti come (frase, numero dell'articolo), senza le frasi di metodo
    («We searched...», «Methods:») che non spiegano l'argomento."""
    frasi = []
    for n, a in enumerate(articoli):
        for f in re.split(r"(?<=[.!?])\s+(?=[A-Z])", a["riassunto"]):
            f = re.sub(r"^(?:Background|Introduction|Purpose|Objectives?|Aims?|Conclusions?|Results|Summary|"
                       r"Context|Rationale|Significance|Recent findings|Purpose of review)\s*:\s*", "", f.strip())
            if (60 <= len(f) <= 400 and f[0].isupper() and not re.search(
                    r"\b(?:we (?:searched|conducted|performed|reviewed|included|identified|aimed|analy[sz]ed)|this (?:review|article|study|paper)|"
                    r"in this (?:review|article|paper)|PubMed|Embase|PRISMA|databases?|systematic(?:ally)? search|"
                    r"Methods?:|meta-analysis of|were included|eligible)\b", f, re.I)):
                frasi.append((f, n))
    return frasi
