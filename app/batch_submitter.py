import requests
import os
import argparse
import time
from werkzeug.utils import secure_filename
from typing import Tuple, Optional

# --- Configuration par variables d'environnement ---
# On évite d'écrire l'adresse DNS en dur pour plus de sécurité.
DEFAULT_URL = os.environ.get('EVALUATION_URL', 'http://localhost:5000')
# Dossiers par défaut
SUBMISSION_FOLDER = 'pool_devoirs'
REPORT_BASE_FOLDER = 'rapports_evaluation'


def submit_notebook(filepath: str, evaluator_slug: str, server_url: str) -> Tuple[bool, str]:
    """
    Envoie un fichier au serveur d'évaluation sur la route spécifique.
    """
    filename = os.path.basename(filepath)
    # Construction de l'URL propre à l'évaluateur (ex: /eval/td2-S2)
    url = f"{server_url.rstrip('/')}/eval/{evaluator_slug}"

    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filename, f, 'application/x-ipynb+json')}
            # Timeout de 120s car l'analyse de gros notebooks peut être longue
            response = requests.post(url, files=files, timeout=120)

        if response.status_code == 200:
            return True, response.text
        else:
            return False, f"Erreur HTTP {response.status_code} : {response.text[:200]}"

    except Exception as e:
        return False, f"Erreur de connexion : {e}"


def run_batch_evaluation(evaluator_slug: str, input_folder: str, server_url: str):
    """
    Parcourt un dossier et traite chaque notebook.
    Le logging (CSV) est géré côté serveur par la fonction 'process_submission'.
    """
    if not os.path.exists(input_folder):
        print(f"❌ Erreur : Le dossier source '{input_folder}' n'existe pas.")
        return

    # Création d'un sous-dossier de rapports spécifique à cet évaluateur
    report_folder = os.path.join(REPORT_BASE_FOLDER, evaluator_slug)
    os.makedirs(report_folder, exist_ok=True)

    notebooks = [f for f in os.listdir(input_folder) if f.endswith('.ipynb')]

    if not notebooks:
        print(f"⚠️ Aucun fichier .ipynb trouvé dans {input_folder}")
        return

    print(f"--- Début du lot : {evaluator_slug} ---")
    print(f"Serveur : {server_url}")
    print(f"Nombre de fichiers : {len(notebooks)}")
    print("-" * 30)

    success_count = 0
    for i, filename in enumerate(notebooks):
        filepath = os.path.join(input_folder, filename)
        print(f"[{i + 1}/{len(notebooks)}] Traitement de {filename}...", end="", flush=True)

        success, result = submit_notebook(filepath, evaluator_slug, server_url)

        if success:
            # Sauvegarde du rapport HTML localement pour consultation prof
            report_name = f"Rapport_{secure_filename(filename)}.html"
            with open(os.path.join(report_folder, report_name), 'w', encoding='utf-8') as f:
                f.write(result)
            print(" [✅ OK]")
            success_count += 1
        else:
            print(f" [❌ ERREUR] -> {result}")

        # Pause de courtoisie pour le serveur
        time.sleep(0.5)

    print("-" * 30)
    print(f"Terminé : {success_count}/{len(notebooks)} copies traitées.")
    print(f"Rapports disponibles dans : {report_folder}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Batch Submitter pour l'Évaluateur TAL.")
    parser.add_argument("evaluator", help="Slug de l'évaluateur (ex: td3-S2, td6-S2)")
    parser.add_argument("--folder", default=SUBMISSION_FOLDER, help="Dossier contenant les .ipynb")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL racine du serveur Flask")

    args = parser.parse_args()
    run_batch_evaluation(args.evaluator, args.folder, args.url)
