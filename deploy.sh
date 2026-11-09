#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
ENV_FILE="${1:-./.env}"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Fichier d'environnement introuvable." >&2
  exit 1
fi
# Aucun source/eval du fichier d'environnement : le script Python lit une seule clé.
python3 app/prepare_student_notebooks.py check
python3 app/prepare_student_notebooks.py render --env-file "$ENV_FILE"
python3 app/prepare_student_notebooks.py verify --env-file "$ENV_FILE"
# Certaines installations NAS ne disposent pas du plugin "docker compose"
# (V2) et utilisent encore la commande autonome "docker-compose" (V1).
# Vérifier la commande effective plutôt que supposer la présence du plugin.
if docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1 && docker-compose version >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
else
  echo "Docker Compose indisponible : installer docker compose (V2) ou docker-compose (V1)." >&2
  exit 1
fi

# Les anciennes versions de docker-compose ne reconnaissent pas --env-file.
# Avec .env à la racine du projet, Compose lit déjà ce fichier automatiquement.
COMPOSE_ARGS=()
if "${COMPOSE[@]}" --help 2>&1 | grep -q -- '--env-file'; then
  COMPOSE_ARGS=(--env-file "$ENV_FILE")
elif [[ "$ENV_FILE" != "./.env" && "$ENV_FILE" != ".env" ]]; then
  echo "Ce Docker Compose ne prend pas en charge --env-file ; utiliser ./.env ou mettre à jour Compose." >&2
  exit 1
fi
echo "Déploiement avec : ${COMPOSE[*]}"
"${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" up -d --build
"${COMPOSE[@]}" "${COMPOSE_ARGS[@]}" exec -T corrector-tal python -c '
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
