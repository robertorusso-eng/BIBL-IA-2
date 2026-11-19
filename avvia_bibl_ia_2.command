#!/bin/zsh
# Avvia BIBL-IA 2 con il suo tema chiaro (BIBL-IA 1 resta con il suo tema scuro).
# Solo su questo Mac (localhost): dagli altri computer della rete Wi-Fi non si apre.
cd "$(dirname "$0")"
exec ./venv/bin/python -m streamlit run bibl_ia_2.py --server.port 8767 --server.address localhost \
  --theme.base light --theme.primaryColor "#2563EB" --theme.backgroundColor "#F5F7FB" \
  --theme.secondaryBackgroundColor "#EEF2F7" --theme.textColor "#0F1B3D" --theme.linkColor "#2563EB" \
  --theme.borderColor "#E2E8F0" --theme.headingFont sans-serif --theme.font sans-serif \
  --theme.baseRadius 0.75rem --theme.buttonRadius 0.75rem
