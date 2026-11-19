"""Correction inerte du contrôle final S1, contrat v2 (TD1–TD5).

Les sorties enregistrées sont des traces, pas une preuve d'exécution ni de
validité générale du programme. Aucun code déposé n'est exécuté.
"""
import ast
import json
import math
import re
from typing import Any, Dict, List, Optional, Tuple

import outils
from notebook_contract import ContractError, resolve_notebook, validate_cell_metadata

POINTS_IDENTIFICATION = 1.0
CORRECT_ANSWERS = {
    'Q1': 150.0,
    'Q2': {'deb': 19, 'fin': 29, 'mot_extrait': 'extraction'},
    'Q3': True,
    'Q4': 'Terminologie',
    'Q5': False,
    'Q6': ['tokenisation', 'lemme', 'segmentation'],
    'Q7': 3,
    'Q8': ['MACHINE', 'LEARNING', 'NLP'],
    'Q9': [15, 12, 9],
    'Q10': [5, 4, 3, 2, 1],
    'Q11': 'inconnu',
    'Q12': {'le': 2, 'chat': 1},
    'Q13': {'talk': 2, 'is': 1, 'cheap': 1},
    'Q14': 'Vrai',
    'Q15': {'code': 'nom'},
    'Q16': 'Bonjour, David',
    'Q17': 16.0,
    'Q18': 'analyse',
    'Q19': 'nltk',
    'Q20': {'longueur': 7, 'minuscules': 'termino'},
    'Q21': 3,
    'Q22': 15.0,
    'Q23': 10,
    'Q24': [4, 8, 16, 32],
    'Q25': ["l'analyse,", '', 'deux  mots !'],
    'Q26': {'avec': ['Python', 'TAL', 'Nlp'], 'sans': ['code', 'texte']},
    'Q27': {'phrase': 6, 'texte': 5, 'mot': 3},
    'Q28': ['chien', 'cat'],
    'Q29': {'mots_nettoyés': ['le', 'tal', 'est', 'cool'], 'nb_caracteres': 16},
    'Q30': ['bibliothèque', 'livre', ''],
}
POINTS_BREAKDOWN = {f'Q{n}': (1.0 if n <= 25 else 2.0) for n in range(1, 31)}
MAX_SCORE_TOTAL = POINTS_IDENTIFICATION + sum(POINTS_BREAKDOWN.values())


def _recorded_output(index, q_key):
    """Une trace unique dans la cellule désignée, hors exemples et dépôt."""
    cell = index[(q_key, 'answer')]
    chunks = []
    outputs = cell.get('outputs', [])
    if not isinstance(outputs, list):
        return None
    for output in outputs:
        if not isinstance(output, dict):
            continue
        if output.get('output_type') != 'stream' or output.get('name') != 'stdout':
            continue
        value = output.get('text', '')
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            value = ''.join(value)
        if isinstance(value, str):
            chunks.append(value)
    keyword = f'Résultat {q_key} :'
    lines = [line.strip() for line in ''.join(chunks).splitlines()
             if line.strip().startswith(keyword)]
    return lines[0] if len(lines) == 1 else None


def _parse_student_answer(q_key: str, raw_output: Optional[str], keyword: str) -> Any:
    if raw_output is None:
        return None
    value_str = raw_output.split(keyword, 1)[1].strip()
    if q_key == 'Q1':
        match = re.fullmatch(r'Coût total\s*:\s*([-+]?\d+(?:\.\d+)?)\s*€', value_str)
        return float(match.group(1)) if match else None
    if q_key == 'Q2':
        match = re.fullmatch(r"Le mot extrait est '(.*?)' \(Indices (-?\d+):(-?\d+)\)", value_str)
        if match:
            try:
                return {'deb': int(match.group(2)), 'fin': int(match.group(3)),
                        'mot_extrait': match.group(1)}
            except ValueError:
                return value_str
        return value_str
    if q_key == 'Q21':
        match = re.fullmatch(r'Choix\s+([1-4])', value_str)
        return int(match.group(1)) if match else None
    try:
        return ast.literal_eval(value_str)
    except (ValueError, SyntaxError, TypeError, RecursionError):
        return value_str


def _same_answer(student, expected):
    # bool hérite de int en Python : refuser 0 à la place de False, 1 de True.
    if isinstance(expected, bool):
        return type(student) is bool and student is expected
    if isinstance(expected, int):
        return type(student) in (int, float) and student == expected
    if isinstance(expected, float):
        try:
            return (type(student) in (int, float)
                    and math.isclose(student, expected, rel_tol=0.01))
        except OverflowError:
            return False
    if isinstance(expected, list):
        return (isinstance(student, list) and len(student) == len(expected)
                and all(_same_answer(a, b) for a, b in zip(student, expected)))
    if isinstance(expected, dict):
        return (isinstance(student, dict) and student.keys() == expected.keys()
                and all(_same_answer(student[key], value) for key, value in expected.items()))
    return type(student) is type(expected) and student == expected


def check_notebook(notebook_content_str: str, filename: str) -> Tuple[float, List[Dict[str, Any]], float, Dict[str, Any], Optional[str]]:
    """Retourne le score des traces sans exécuter le programme de la copie."""
    try:
        notebook = json.loads(notebook_content_str)
        resolve_notebook(notebook, expected_evaluator='Controletilt-s1')
        index = validate_cell_metadata(notebook)
        student_info = outils.extract_identification_info(notebook['cells'])
    except (json.JSONDecodeError, ContractError, TypeError, ValueError) as exc:
        return (0.0, [], MAX_SCORE_TOTAL,
                {'nom': 'Erreur', 'prenom': 'JSON', 'classe': 'N/A'}, str(exc))

    is_id_ok = all(isinstance(student_info.get(key), str)
                    and student_info[key].strip() not in {'', '...', 'NON_RENSEIGNE'}
                    for key in ('nom', 'prenom'))
    score_id = POINTS_IDENTIFICATION if is_id_ok else 0.0
    details = [{
        'check': '0.1 - Identification',
        'student_answer': f"Nom: {student_info['nom']}, Prénom: {student_info['prenom']}, Classe: {student_info['classe']}",
        'correct_answer': 'Nom et prénom renseignés.',
        'status': '✅' if is_id_ok else '⚠️',
        'points': score_id, 'max_points': POINTS_IDENTIFICATION,
    }]
    for q_key, points in POINTS_BREAKDOWN.items():
        keyword = f'Résultat {q_key} :'
        raw_output = _recorded_output(index, q_key)
        student_val = _parse_student_answer(q_key, raw_output, keyword)
        expected = CORRECT_ANSWERS[q_key]
        if q_key == 'Q2':
            # Trancher une référence connue ne fait pas exécuter le code déposé.
            corpus = "TAL : la clé est l'extraction terminologique."
            valid = (isinstance(student_val, dict)
                     and student_val['mot_extrait'] == 'extraction'
                     and corpus[student_val['deb']:student_val['fin']] == 'extraction')
        else:
            valid = _same_answer(student_val, expected)
        points_awarded = points if valid else 0.0
        details.append({
            'check': f'{q_key} ({points:.1f} pts)',
            'student_answer': (str(student_val) if student_val is not None
                               else 'Réponse non retrouvée par le correcteur'),
            'correct_answer': str(expected),
            'status': '✅' if valid else '❌',
            'points': points_awarded, 'max_points': points,
        })
    final_score = sum(detail['points'] for detail in details)
    student_info.update(score_brut=round(final_score, 1), contract_version=2)
    return final_score, details, MAX_SCORE_TOTAL, student_info, None
