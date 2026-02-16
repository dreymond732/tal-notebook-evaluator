# Fichier: app_correction_DevoirMaisonS2.py
from engine import run_evaluation

# --- Configuration ---
EVAL_ID = "devoir-maison-S2"
MAX_SCORE_TOTAL = 40.0

CORRECT_ANSWERS = {
    'Q1': 'bon', 'Q2': [1, 2, 3, 4], 'Q3': 3, 'Q4': 20, 'Q5': {'nom': 'A', 'age': 20, 'ville': 'Paris'},
    'Q6': 6, 'Q7': 'TEST', 'Q8': 'mon chien', 'Q9': 5, 'Q10': {1, 2},
    'Q11': True, 'Q12': ['a', 'b', 'c'], 'Q13': [1, 2], 'Q14': 5, 'Q15': 9,
    'Q16': 42, 'Q17': 3.14, 'Q18': True, 'Q19': ['a'], 'Q20': [1],
    'Q21': [1, 4, 9, 16, 25], 'Q22': {1: 1, 2: 4, 3: 9}, 'Q23': [2, 4],
    'Q24': [1, 2, 3, 4], 'Q25': {'a': 2, 'b': 1, 'c': 1}, 'Q26': {'a': 1, 'b': 2},
    'Q27': {1: 'a', 2: 'b'}, 'Q28': [[1, 3], [2, 4]], 'Q29': [2, 3], 'Q30': 120
}

POINTS_BREAKDOWN = {
    'Q1': 1.0, 'Q2': 1.0, 'Q3': 1.0, 'Q4': 1.0, 'Q5': 1.0,
    'Q6': 1.0, 'Q7': 1.0, 'Q8': 1.0, 'Q9': 1.0, 'Q10': 1.0,
    'Q11': 1.0, 'Q12': 1.0, 'Q13': 1.0, 'Q14': 1.0, 'Q15': 1.0,
    'Q16': 1.0, 'Q17': 1.0, 'Q18': 1.0, 'Q19': 1.0, 'Q20': 1.0,
    'Q21': 2.0, 'Q22': 2.0, 'Q23': 2.0, 'Q24': 2.0, 'Q25': 2.0,
    'Q26': 2.0, 'Q27': 2.0, 'Q28': 2.0, 'Q29': 2.0, 'Q30': 2.0
}

# Fonction appelée par routes.py
def check_notebook(content_str, filename):
    return run_evaluation(
        content_str,
        filename,
        CORRECT_ANSWERS,
        POINTS_BREAKDOWN,
        MAX_SCORE_TOTAL,
        EVAL_ID
    )