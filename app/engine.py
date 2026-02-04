import json
import ast
import math
import re
from typing import List, Dict, Any, Tuple, Optional
import outils


def get_cell_output_text(cell: Dict[str, Any]) -> str:
    """Récupère tout le texte affiché (stdout) par une cellule."""
    text_output = []
    if 'outputs' in cell:
        for output in cell['outputs']:
            if output.get('output_type') == 'stream' and output.get('name') == 'stdout':
                text_list = output.get('text', [])
                if isinstance(text_list, list):
                    text_output.append("".join(text_list))
                else:
                    text_output.append(str(text_list))
            elif output.get('output_type') == 'execute_result':
                data = output.get('data', {})
                if 'text/plain' in data:
                    text_list = data['text/plain']
                    text_output.append("".join(text_list) if isinstance(text_list, list) else str(text_list))
    return "\n".join(text_output)


def parse_student_answer(raw_output: Optional[str], keyword: str, expected_type: Any = None) -> Any:
    """Extrait la réponse depuis stdout."""
    if not raw_output or keyword not in raw_output:
        return None

    # On coupe après "Résultat Qx :"
    value_str = raw_output.split(keyword, 1)[-1].strip()

    # On prend la première ligne non vide qui suit
    lines = [l.strip() for l in value_str.splitlines() if l.strip()]
    if lines:
        value_str = lines[0]
    else:
        return None

    # 1. Tentative d'extraction numérique (ex: "300 €" -> 300)
    if isinstance(expected_type, (int, float)):
        # Cherche un nombre (entier ou flottant) isolé
        match = re.search(r'-?\d+(\.\d+)?', value_str)
        if match:
            try:
                num_str = match.group()
                return float(num_str) if '.' in num_str else int(num_str)
            except:
                pass

    # 2. Tentative d'évaluation littérale (Listes, Dicts, Bool)
    try:
        # ast.literal_eval est sûr pour parser des structures Python
        return ast.literal_eval(value_str)
    except (ValueError, SyntaxError):
        pass

    # 3. Fallback : Chaîne nettoyée
    cleaned = value_str.strip("'\"")
    # Gestion booléens textuels
    if cleaned.lower() == 'true': return True
    if cleaned.lower() == 'false': return False
    return cleaned


def compare_answers(student_val: Any, correct_val: Any) -> bool:
    """Comparaison flexible (Types et Structures)."""
    if correct_val is None: return student_val is None

    # Comparaison Numérique (avec tolérance)
    if isinstance(correct_val, (int, float)):
        if isinstance(student_val, (int, float)):
            return math.isclose(float(student_val), float(correct_val), rel_tol=0.01, abs_tol=1e-6)
        try:  # Si c'est une string qui contient un nombre
            return math.isclose(float(student_val), float(correct_val), rel_tol=0.01, abs_tol=1e-6)
        except:
            pass

    # Comparaison Structures (List, Tuple, Set)
    if isinstance(correct_val, (list, tuple)):
        if isinstance(student_val, (list, tuple)):
            return list(student_val) == list(correct_val)

    if isinstance(correct_val, set):
        if isinstance(student_val, (list, set, tuple)):
            return set(student_val) == correct_val

    if isinstance(correct_val, dict):
        if isinstance(student_val, dict):
            return student_val == correct_val

    # Comparaison Chaînes
    if isinstance(correct_val, str):
        return str(student_val).strip().lower() == correct_val.strip().lower()

    return student_val == correct_val


def run_evaluation(
        notebook_content_str: str,
        filename: str,
        correct_answers: Dict[str, Any],
        points_breakdown: Dict[str, float],
        max_score_total: float,
        eval_id: str
) -> Tuple[float, List[Dict[str, Any]], float, Dict[str, str], Optional[str]]:
    try:
        nb_json = json.loads(notebook_content_str)
        cells = nb_json.get('cells', [])
    except json.JSONDecodeError as e:
        return 0.0, [], max_score_total, {'nom': 'Erreur', 'prenom': 'JSON'}, f"Erreur JSON: {e}"

    student_info = outils.extract_identification_info(cells)

    details = []
    score = 0.0

    # Ordre naturel des questions
    sorted_keys = sorted(points_breakdown.keys(),
                         key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)

    for q_key in sorted_keys:
        max_pts = points_breakdown.get(q_key, 0.0)
        correct_val = correct_answers.get(q_key)

        student_val = None
        source_found = "Aucune"

        # --- ÉTAPE 1 : EXCEPTION SPÉCIFIQUE (Variables Q2 TD3) ---
        # On ne le fait QUE pour ce cas précis où l'AST est fiable (valeurs constantes)
        # et où le print peut être ambigu.
        if q_key == 'Q2' and isinstance(correct_val, dict) and 'deb' in correct_val:
            deb = outils.extract_code_variable(nb_json, 'valeur_Q2_deb', mode='numeric')
            fin = outils.extract_code_variable(nb_json, 'valeur_Q2_fin', mode='numeric')
            # Si on trouve au moins le début, on considère que l'étudiant a utilisé cette méthode
            if deb is not None:
                student_val = {'deb': int(deb), 'fin': int(fin) if fin is not None else None}
                source_found = "Variable (Exception Q2)"

        # --- ÉTAPE 2 : SORTIE STANDARD (Priorité Absolue pour le reste) ---
        # C'est la seule façon d'avoir le résultat d'une boucle (Q10) ou d'un if/else (Q3)
        if source_found == "Aucune":
            keyword = f"Résultat {q_key} :"
            for cell in cells:
                output_text = get_cell_output_text(cell)
                if keyword in output_text:
                    parsed = parse_student_answer(output_text, keyword, expected_type=correct_val)
                    if parsed is not None:
                        student_val = parsed
                        source_found = "Sortie (Print)"
                        break

        # --- ÉTAPE 3 : FALLBACK VARIABLES (Si print absent) ---
        # Utile si l'étudiant a oublié le print mais a fait une assignation simple (ex: Q21, Q5)
        if source_found == "Aucune":
            potential_vars = [f"reponse_{q_key}", f"valeur_{q_key}", f"resultat_{q_key}"]
            for var_name in potential_vars:
                val = outils.extract_code_variable(nb_json, var_name, mode='auto')
                if val is not None:
                    # Fix pour éviter de capturer un dict partiel si Q2 échoue en étape 1
                    if q_key == 'Q2' and not isinstance(val, dict):
                        continue
                    student_val = val
                    source_found = f"Variable ({var_name})"
                    break

        # --- Comparaison ---
        is_correct = compare_answers(student_val, correct_val)
        status = '✅' if is_correct else '❌'
        pts = max_pts if is_correct else 0.0

        details.append({
            'check': f"{q_key}",
            'student_answer': str(student_val),
            'correct_answer': str(correct_val),
            'status': status,
            'points': pts,
            'max_points': max_pts
        })
        score += pts

    student_info['score_brut'] = round(score, 2)
    return score, details, max_score_total, student_info, None