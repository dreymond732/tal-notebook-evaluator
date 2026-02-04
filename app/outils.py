# Fichier: outils.py
import re
import ast
import os
import csv
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union
from werkzeug.utils import secure_filename

# --- Constantes ---
BASE_DIR = "soumissions"


def extract_code_variable(notebook_content: Dict[str, Any], var_name: str, mode: str = 'string') -> Optional[Any]:
    """
    Extrait la valeur d'une variable (nom, reponse_Qx_x, etc.) définie dans une cellule de code.
    Utilise l'AST pour l'extraction la plus fiable.
    """
    last_value = None

    for cell in notebook_content.get('cells', []):
        if cell.get('cell_type') == 'code':
            source_code = ''.join(cell.get('source', []))

            try:
                tree = ast.parse(source_code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == var_name:
                                # Extrait la valeur de la variable
                                try:
                                    extracted_value = ast.literal_eval(node.value)
                                    last_value = extracted_value
                                except (ValueError, TypeError):
                                    pass

            except SyntaxError:
                pass

            # Fallback textuel simple pour la phrase si AST a échoué ou pour les vieux formats
            if last_value is None:
                match = re.search(rf'^{re.escape(var_name)}\s*=\s*["\'](.*?)["\']', source_code,
                                  re.MULTILINE | re.IGNORECASE)
                if match:
                    last_value = match.group(1).strip()

    if last_value is None:
        return None

    # Conversion selon le mode
    if mode == 'string':
        # Normalisation pour la comparaison (minuscules, sans point final, sans espace insécable)
        return str(last_value).strip().lower().strip('.')
    elif mode == 'numeric':
        try:
            # Tente de convertir en float
            return float(str(last_value).strip())
        except (ValueError, TypeError):
            return None

    return last_value


def create_seed_from_name(nom: str, prenom: str) -> int:
    """Graine numérique unique (Source de vérité pour la génération)."""
    if not nom or not prenom or nom in ["NON_RENSEIGNE", "..."]:
        return 42
    full_name = f"{nom}{prenom}".lower().replace(' ', '')
    return sum(ord(c) * (i + 1) for i, c in enumerate(full_name)) % 1000000


# --- Chemins ---
def get_nb_path(eval_id, group, filename):
    return os.path.join(BASE_DIR, secure_filename(eval_id), secure_filename(group), "nb", filename)


def get_rapport_path(eval_id, group, filename):
    return os.path.join(BASE_DIR, secure_filename(eval_id), secure_filename(group), "rapport", filename)


def get_csv_path(eval_id, group):
    e, g = secure_filename(eval_id), secure_filename(group)
    return os.path.join(BASE_DIR, e, g, f"notes_{e}_{g}.csv")


# --- Utilitaires de conversion ---
def safe_float(val: Any) -> Optional[float]:
    if val is None: return None
    if isinstance(val, bool): return 1.0 if val else 0.0
    try:
        clean = str(val).strip().replace(',', '.').replace(' ', '').replace('€', '').replace('%', '')
        match = re.search(r"[-+]?\d*\.?\d+", clean)
        return float(match.group()) if match else None
    except:
        return None


def check_close(val_stud: Any, val_true: Union[float, int], tol: float = 0.01) -> bool:
    s_val = safe_float(val_stud)
    if s_val is None: return False
    return abs(s_val - float(val_true)) <= tol


# --- Moteur d'extraction Jupyter ---
def extract_identification_info(cells):
    info = {'nom': 'NON_RENSEIGNE', 'prenom': 'NON_RENSEIGNE', 'classe': 'NON_RENSEIGNEE'}
    marker = "# Complétez les informations entre les guillemets."
    for cell in cells:
        if cell.get('cell_type') == 'code':
            src = "".join(cell.get('source', []))
            if marker in src:
                for k in ['nom', 'prenom', 'classe']:
                    m = re.search(rf'{k}\s*=\s*["\'“](.*?)["\'”]', src, re.I)
                    if m: info[k] = m.group(1).strip()
    return info


def check_identification(info):
    inv = ["NON_RENSEIGNE", "NON_RENSEIGNEE", "..."]
    return all(info.get(k) not in inv for k in ['nom', 'prenom', 'classe'])


def extract_variable_from_notebook(nb_json: Dict[str, Any], var_name: str) -> Any:
    """Extrait les valeurs littérales en ignorant les expressions complexes."""
    for cell in nb_json.get('cells', []):
        if cell.get('cell_type') == 'code':
            src = "".join(cell.get('source', []))
            # On cherche une assignation simple suivie d'un nombre et d'une fin de ligne (ou commentaire)
            # Cela évite de capturer le '1' dans 'var = 1 - stats...'
            pattern = rf"^{var_name}\s*=\s*([-+]?\d*\.?\d+)\s*(?:#.*)?$"
            match = re.search(pattern, src, re.M)
            if match:
                return safe_float(match.group(1))

            # Support des listes de booléens (Heatmap)
            list_match = re.search(rf"^{var_name}\s*=\s*(\[.*?\])\s*(?:#.*)?$", src, re.M)
            if list_match:
                try:
                    return ast.literal_eval(list_match.group(1))
                except:
                    pass
    return None

def get_ipynb_raw_output(nb_json, keyword):
    """Cherche le mot-clé dans les flux stdout ou les résultats d'exécution."""
    for cell in nb_json.get('cells', []):
        if cell.get('cell_type') == 'code':
            for out in cell.get('outputs', []):
                text = "".join(out.get('text', [])) if out.get('output_type') == 'stream' else ""
                if not text and out.get('output_type') == 'execute_result':
                    text = out.get('data', {}).get('text/plain', "")
                if keyword.lower() in text.lower(): return text
    return ""


def extract_numeric_result(text: str, keyword: str) -> Optional[float]:
    """Extrait un nombre après un mot-clé avec flexibilité sur le texte intermédiaire."""
    if not text: return None
    # On rend la recherche flexible sur les accents et la présence d'un 'Q' optionnel
    kw_clean = re.escape(keyword).replace('é', '[é e]')
    # Pattern : Mot-clé + n'importe quoi (non avide) + Nombre
    pattern = rf"{kw_clean}.*?([-+]?\d+[\.,]\d+|-?\d+)"
    match = re.search(pattern, text, re.S | re.I)
    return safe_float(match.group(1)) if match else None


def log_grade_to_csv(eval_id, info, score, bonus=0.0):
    csv_path = get_csv_path(eval_id, info.get('classe', 'SANS_CLASSE'))
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    write_h = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        if write_h: w.writerow(['Date', 'Nom', 'Prénom', 'Classe', 'Note', 'Bonus'])
        w.writerow([datetime.now().strftime("%d/%m/%Y %H:%M"), info.get('nom', '').upper(),
                    info.get('prenom', '').capitalize(), info.get('classe', ''),
                    f"{score:.2f}".replace('.', ','), f"{bonus:.2f}".replace('.', ',')])