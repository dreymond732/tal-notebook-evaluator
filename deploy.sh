#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
ENV_FILE="${1:-./.env}"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Fichier d'environnement introuvable." >&2
  exit 1
fi
# Aucun source/eval du fichier d'environnement : le script Python lit une seule clé.
python3 app/prepare_student_notebooks.py render --env-file "$ENV_FILE"
python3 app/prepare_student_notebooks.py verify --env-file "$ENV_FILE"
docker compose --env-file "$ENV_FILE" up -d --build
docker compose --env-file "$ENV_FILE" exec -T corrector-tal python -c '
import json, time, urllib.request
for attempt in range(15):
    try:
        with urllib.request.urlopen("http://127.0.0.1:5001/health", timeout=2) as response:
            result = json.load(response)
        if result.get("status") == "ok":
            print("TAL disponible ; copies distribuables dans dist/.")
            break
    except (OSError, ValueError):
        pass
    time.sleep(1)
else:
    raise SystemExit("Le serveur ne répond pas correctement sur /health.")
'
