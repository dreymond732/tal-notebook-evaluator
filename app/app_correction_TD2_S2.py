# Fichier: app_correction_TD2_S2.py
from engine import run_evaluation

# --- Configuration ---
EVAL_ID = "td2-S2"
MAX_SCORE_TOTAL = 20.0

CORRECT_ANSWERS = {
    'Q1': 'nohtyP',
    'Q2': 'chat-chien-souris',
    'Q3': '3.14',
    'Q4': [1, 4, 9, 16],
    'Q5': 4,
    'Q6': {'Français': 'FR', 'Anglais': 'EN'},
    'Q7': 50,
    'Q8': ['Alice', 'Charlie'],
    'Q9': {'b': 2, 'a': 2},
    'Q10': [1, 2, 3, 4, 5, 6],
    'Q11': [0, 1, 1, 2, 3, 5, 8],
    'Q12': True,
    'Q13': [12, 20]
}

POINTS_BREAKDOWN = {
    'Q1': 1.0, 'Q2': 1.0, 'Q3': 1.0, 'Q4': 1.0, 'Q5': 1.0,
    'Q6': 1.0, 'Q7': 1.0, 'Q8': 2.0, 'Q9': 2.0,
    'Q10': 2.0, 'Q11': 2.0, 'Q12': 2.0, 'Q13': 3.0
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