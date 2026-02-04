# Fichier: app_correction_TD4_S2.py
import math
from engine import run_evaluation

EVAL_ID = "td4-S2"
MAX_SCORE_TOTAL = 40.0

CORRECT_ANSWERS = {
    'Q1': {'chat', 'chien', 'oiseau'},
    'Q2': {'chat', 'chien', 'souris'},
    'Q3': True,
    'Q4': {'data', 'code'},
    'Q5': {'data', 'code', 'python', 'algo'},
    'Q6': {'pomme', 'poire'},
    'Q7': {'linux', 'windows'},
    'Q8': True,
    'Q9': True,
    'Q10': {'tag1', 'tag2', 'tag3'},
    'Q11': {'le', 'est'},
    'Q12': {'Paul', 'Jean'},
    'Q13': 0.5,
    'Q14': True
}

POINTS_BREAKDOWN = {
    'Q1': 2.0, 'Q2': 2.0, 'Q3': 2.0, 'Q4': 3.0,
    'Q5': 3.0, 'Q6': 3.0, 'Q7': 3.0, 'Q8': 2.0,
    'Q9': 3.0, 'Q10': 3.0, 'Q11': 3.0,
    'Q12': 3.0, 'Q13': 4.0, 'Q14': 4.0
}

def check_notebook(content_str, filename):
    return run_evaluation(
        content_str,
        filename,
        CORRECT_ANSWERS,
        POINTS_BREAKDOWN,
        MAX_SCORE_TOTAL,
        EVAL_ID
    )