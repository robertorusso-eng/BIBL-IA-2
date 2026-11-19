#!/bin/zsh
# Sceglie le password del Pannello di gestione di BIBL-IA 2 (almeno due: per entrare servono tutte).
# Le password non si vedono mentre le scrivi e restano solo su questo Mac (.streamlit/accesso_gestione.txt).
cd "$(dirname "$0")"
echo "Password del Pannello di gestione di BIBL-IA 2"
echo "Per entrare nel Pannello serviranno tutte le password che scegli (almeno due)."
echo "Usa password diverse da quella dell'Area docenti. Mentre scrivi non compare niente: è normale."
echo
read "quante?Quante password vuoi? (almeno 2) [2]: "
quante=${quante:-2}
if ! [[ "$quante" =~ ^[0-9]+$ ]] || (( quante < 2 )); then quante=2; fi
righe=()
for (( n = 1; n <= quante; n++ )); do
  while true; do
    read -s "p1?Password $n (almeno 8 caratteri): "; echo
    read -s "p2?Ripeti la password $n: "; echo
    if [[ "$p1" != "$p2" ]]; then echo "Non sono uguali: riprova."; continue; fi
    if (( ${#p1} < 8 )); then echo "Troppo corta: almeno 8 caratteri."; continue; fi
    if (( ${righe[(Ie)$p1]} )); then echo "Deve essere diversa dalle altre."; continue; fi
    righe+=("$p1"); break
  done
done
mkdir -p .streamlit
umask 077
printf '%s\n' "${righe[@]}" > .streamlit/accesso_gestione.txt
chmod 600 .streamlit/accesso_gestione.txt
unset p1 p2 righe
echo
echo "Fatto: da adesso il Pannello di gestione chiede $quante password. Ricaricare la pagina di BIBL-IA basta."
