import os
import json
import ast 
import re
import math
import sys
from flask import Flask, request, render_template_string, flash, redirect, url_for
from werkzeug.utils import secure_filename
from typing import List, Dict, Any, Tuple, Optional

# --- Importation de vos outils ---
import outils
# --- Constantes de Correction (Total 35.0 pts) ---

POINTS_IDENTIFICATION = 1.0
MAX_SCORE_TOTAL = 35.0 # 34 pts de Q + 1 pt ID

# Réponses attendues (basées sur le corrigé DevoirS1_TILT_corrigé.ipynb)
CORRECT_ANSWERS = {
    'Q1': 150.0,
    'Q2': {'deb': 19, 'fin': 29}, # Indices pour 'extraction '
    'Q3': True,
    'Q4': 'terminologie', # Le corrigé produit 'terminologie'
    'Q5': 3,
    'Q6': ['tokenisation', 'lemme', 'segmentation'],
    'Q7': 3,
    'Q8': ['MACHINE', 'LEARNING', 'NLP'],
    'Q9': [15, 12, 9],
    'Q10': [5, 4, 3, 2, 1],
    'Q11': 'inconnu',
    'Q12': {'le': 2, 'chat': 1},
    'Q13': {'talk': 2, 'is': 1, 'cheap': 1},
    'Q14': 'Vrai',
    'Q15': {'TAL': 'nom', 'mot': 'nom', 'code': 'nom'}, # Le corrigé utilise >= 3
    'Q16': 'Bonjour, David',
    'Q17': 16.0, # Le corrigé retourne nombre ** 2
    'Q18': 'analyse',
    'Q19': 'nltk',
    'Q20': {'longueur': 7, 'minuscules': 'termino'},
    'Q21': 3,
    'Q22': 20.0, # Le corrigé appelle addition(10) avec b=10
    'Q23': 10,
    'Q24': 5.0,
    'Q25': "l'analyse", 
    'Q26': {'avec': ['Python', 'TAL', 'Nlp'], 'sans': ['code', 'texte']},
    'Q27': {'phrase': 6, 'texte': 5, 'mot': 3},
    'Q28': ['chien', 'cat'],
    'Q29': {'mots_nettoyés': ['le', 'tal', 'est', 'cool'], 'nb_caracteres': 16},
    'Q30': {'lignes': 3, 'mots': 8}, # Le corrigé a 8 mots
}

# Barème des questions (Total 34 points)
POINTS_BREAKDOWN = {
    'Q1': 1.0, 'Q2': 1.0, 'Q3': 1.0, 'Q4': 1.0, 'Q5': 1.0, 
    'Q6': 1.0, 'Q7': 1.0, 'Q8': 1.0, 'Q9': 1.0, 'Q10': 1.0,
    'Q11': 1.0, 'Q12': 1.0, 'Q13': 1.0, 'Q14': 1.0, 'Q15': 1.0,
    'Q16': 1.0, 'Q17': 1.0, 'Q18': 1.0, 'Q19': 1.0, 'Q20': 1.0,
    'Q21': 1.0, 'Q22': 1.0, 'Q23': 1.0, 'Q24': 1.0, 'Q25': 1.0,
    'Q26': 2.0, 'Q27': 2.0, 'Q28': 2.0, 'Q29': 2.0, 'Q30': 2.0, # Q30 = 2.0 pts
}

# --- Logique d'extraction (interne) ---

def _parse_student_answer(q_key: str, raw_output: Optional[str], keyword: str) -> Any:
    """Tente d'extraire la valeur de la sortie brute d'un print()."""
    if not raw_output:
        return None
    
    try:
        # Isole la partie après le mot-clé (Ex: 'Résultat Q1 : ')
        value_str = raw_output.split(keyword, 1)[-1].strip()
        
        # Cas Q1 (avec '€')
        if q_key == 'Q1':
            match = re.search(r"([\d\.]+)", value_str)
            return float(match.group(1)) if match else None

        # Cas Q5 et Q21 (avec 'Choix ')
        if q_key in ['Q5', 'Q21']:
            match = re.search(r"(\d+)$", value_str)
            return int(match.group(1)) if match else None

        # Tente d'évaluer la chaîne pour les listes, dicts, bool, int, float
        try:
            return ast.literal_eval(value_str)
        except (ValueError, SyntaxError):
            # Si c'est une chaîne simple (Q4, Q11, Q14, Q16, Q18, Q19, Q25)
            return value_str.strip("'\"") # Nettoie les guillemets résiduels
            
    except Exception:
        return None

# --- Logique de Correction (check_notebook) ---

def check_notebook(notebook_content_str: str, filename: str) -> Tuple[float, List[Dict[str, Any]], float, Dict[str, str], Optional[str]]:
    """Logique principale de correction du Notebook."""
    
    try:
        notebook_content = json.loads(notebook_content_str)
        cells = notebook_content.get('cells', [])
    except json.JSONDecodeError as e:
        error_msg = f"Erreur de décodage JSON: {e}"
        return 0.0, [], MAX_SCORE_TOTAL, {'nom': 'Erreur', 'prenom': 'JSON', 'classe': 'N/A'}, error_msg

    # Utilisation de outils.py pour l'identification
    student_info = outils.extract_identification_info(cells)
    
    details = []
    score = 0.0
    
    # 1. Identification
    # CORRECTION : On ignore la validation de la classe (qui est spécifique au BUT dans outils.py)
    is_name_present = student_info['nom'] != 'NON_RENSEIGNE' and student_info['prenom'] != 'NON_RENSEIGNE'
    is_id_ok = is_name_present
    score_id = POINTS_IDENTIFICATION if is_id_ok else 0.0
    
    # Rétablit la classe si elle a été trouvée, même si non validée, pour l'affichage
    student_info['classe'] = "M1-TILT"
    student_info['encouragement'] = "Évaluation de la rigueur et des bases de Python terminée. Voir les détails ci-dessous."
    
    details.append({
        'check': "0.1 - Identification",
        'student_answer': f"Nom: {student_info['nom']}, Prénom: {student_info['prenom']}, Classe: {student_info['classe']}",
        'correct_answer': "Nom et Prénom renseignés.",
        'status': '✅' if is_id_ok else '⚠️', 'points': score_id, 'max_points': POINTS_IDENTIFICATION,
    })
    score += score_id

    # --- Évaluation des 30 Questions de Code ---
    
    for q_num in range(1, 31):
        q_key = f'Q{q_num}'
        points = POINTS_BREAKDOWN.get(q_key, 0.0)
        correct_val = CORRECT_ANSWERS.get(q_key)
        keyword = f"Résultat {q_key} :"
        
        student_val = None
        status = '❌'
        pts = 0.0

        try:
            # --- CAS SPÉCIAL Q2 : Vérification des variables d'index ---
            if q_key == 'Q2':
                deb = outils.extract_code_variable(notebook_content, 'valeur_Q2_deb', mode='numeric')
                fin = outils.extract_code_variable(notebook_content, 'valeur_Q2_fin', mode='numeric')
                student_val = {'deb': deb, 'fin': fin}

                if deb == correct_val['deb'] and fin == correct_val['fin']:
                    pts = points
                    status = '✅'
            
            # --- CAS Q5, Q21, Q23 : Lecture de la variable 'reponse_Qx' ---
            elif q_key in [5, 21, 23]:
                var_name = f'reponse_Q{q_key}'
                student_val = outils.extract_code_variable(notebook_content, var_name, mode='numeric')
                if student_val is not None and math.isclose(student_val, correct_val):
                    pts = points
                    status = '✅'

            # --- CAS STANDARD : Lecture de la sortie 'print()' ---
            else:
                raw_output = outils.get_ipynb_raw_output(notebook_content, keyword)
                student_val = _parse_student_answer(q_key, raw_output, keyword)

                # Comparaison
                if isinstance(correct_val, (int, float)):
                    if student_val is not None and isinstance(student_val, (int, float)) and math.isclose(float(student_val), float(correct_val), rel_tol=0.01):
                        pts = points
                        status = '✅'
                elif isinstance(correct_val, str):
                    student_val_cleaned = str(student_val).strip("'\"").strip() if student_val is not None else None
                    correct_val_cleaned = correct_val.strip("'\"").strip()
                    
                    # Tolérance pour Q4 (casse)
                    if q_key == 4 and student_val_cleaned is not None and student_val_cleaned.lower() == correct_val_cleaned.lower():
                         pts = points
                         status = '✅'
                    elif student_val_cleaned is not None and student_val_cleaned == correct_val_cleaned:
                        pts = points
                        status = '✅'
                        
                elif isinstance(correct_val, (list, dict, bool)):
                    if student_val is not None and student_val == correct_val:
                        pts = points
                        status = '✅'
                
        except Exception:
            student_val = "Erreur d'extraction"

        # Formatage pour affichage
        correct_answer_display = str(correct_val)
        student_answer_display = str(student_val) if student_val is not None else "Non trouvé / Erreur d'exécution"
        
        details.append({
            'check': f"{q_key} ({points:.1f} pts)",
            'student_answer': student_answer_display,
            'correct_answer': correct_answer_display,
            'status': status, 'points': pts, 'max_points': points,
        })
        score += pts

    # Recalcul du score final
    final_score = sum(d['points'] for d in details)
    student_info['score_brut'] = round(final_score, 1)

    return final_score, details, MAX_SCORE_TOTAL, student_info, None
