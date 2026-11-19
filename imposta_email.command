#!/bin/zsh
# Imposta la casella da cui BIBL-IA 2 manda i codici ai professori (per esempio un Gmail creato apposta).
# Per Gmail serve la «password per le app» (myaccount.google.com › Sicurezza › Password per le app), non la
# password normale. Tutto resta solo su questo Mac (.streamlit/posta.json); la password non si vede mentre scrivi.
cd "$(dirname "$0")"
read "indirizzo?Indirizzo email da cui mandare (per esempio bibl.ia.codici@gmail.com): "
read "server?Server SMTP [smtp.gmail.com]: "; server=${server:-smtp.gmail.com}
read "porta?Porta [587]: "; porta=${porta:-587}
read -s "parola?Password per le app (non si vede mentre scrivi): "; echo
mkdir -p .streamlit
umask 077
INDIRIZZO="$indirizzo" SERVER="$server" PORTA="$porta" PAROLA="$parola" ./venv/bin/python -c '
import json, os
json.dump({"server": os.environ["SERVER"], "porta": int(os.environ["PORTA"]), "utente": os.environ["INDIRIZZO"],
           "password": os.environ["PAROLA"], "mittente": "BIBL-IA <" + os.environ["INDIRIZZO"] + ">"},
          open(".streamlit/posta.json", "w"))'
chmod 600 .streamlit/posta.json
unset parola
echo "Fatto: da adesso BIBL-IA manda i codici ai professori da $indirizzo."
