#!/usr/bin/env bash
# Publicación nocturna (cron, tras sync_work_blog):
#   1. traduce al inglés solo los capítulos publicados que aún no tienen versión en inglés,
#   2. bloquea si la auditoría encuentra información sensible,
#   3. exporta la web estática y la sube a GitHub Pages solo si ha cambiado algo.
set -euo pipefail

SITE_DIR="$HOME/miWeb"
PAGES_DIR="$HOME/Ocultwolf.github.io"
PY="$SITE_DIR/.venv_host/bin/python"
export PATH="$HOME/.local/bin:$PATH"   # cron no incluye ~/.local/bin (claude)

cd "$SITE_DIR"
echo "[$(date -Is)] publish_site"
"$PY" manage.py translate_posts || echo "translate_posts falló; se publica lo que ya está traducido"
"$PY" manage.py audit_posts       # sale con 1 si hay algo sensible sin censurar: no se publica
"$PY" manage.py export_site --out "$PAGES_DIR"

cd "$PAGES_DIR"
git add -A
if git diff --cached --quiet; then
    echo "sin cambios en la web"
else
    git commit -q -m "Update site ($(date +%Y-%m-%d))"
    git push -q origin main
    echo "publicado en https://ocultwolf.github.io"
fi
