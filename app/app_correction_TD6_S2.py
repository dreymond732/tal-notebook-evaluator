# Fichier: app_correction_TD6_S2.py
from engine import run_evaluation

EVAL_ID = "td6-S2"
MAX_SCORE_TOTAL = 20.0

CORRECT_ANSWERS = {
    'Q1': "Le chat, mange la souris.\nLe chien; aboie fort!!\nL'oiseau vole... dans le ciel.\nLa souris (petite) court vite.\nCHAT et chien sont des amis?\n123 souris mangent 456 graines.",
    'Q2': ["Le chat, mange la souris.\n", "Le chien; aboie fort!!\n", "L'oiseau vole... dans le ciel.\n", "La souris (petite) court vite.\n", "CHAT et chien sont des amis?\n", "123 souris mangent 456 graines.\n"], # Note: readlines garde souvent le \n
    'Q3': "le chien  aboie fort  ", # Ponctuation remplacée par espace
    'Q4': ['le', 'chien', 'aboie', 'fort'],
    'Q5': ['souris', 'mangent', 'graines'],
    'Q6': ['chat', 'souris'],
    'Q7': ['chat', 'mange', 'souris', 'chien', 'aboie', 'fort', 'oiseau', 'vole', 'ciel', 'souris', 'petite', 'court', 'vite', 'chat', 'chien', 'amis', 'souris', 'mangent', 'graines'],
    'Q8': {'chat': 2, 'mange': 1, 'souris': 3, 'chien': 2, 'aboie': 1, 'fort': 1, 'oiseau': 1, 'vole': 1, 'ciel': 1, 'petite': 1, 'court': 1, 'vite': 1, 'amis': 1, 'mangent': 1, 'graines': 1},
    'Q9': ['Mot;Frequence', 'chat;2', 'mange;1'], # On checke juste le début
    'Q10': [('souris', 3), ('chat', 2), ('chien', 2), ('mange', 1), ('aboie', 1), ('fort', 1), ('oiseau', 1), ('vole', 1), ('ciel', 1), ('petite', 1), ('court', 1), ('vite', 1), ('amis', 1), ('mangent', 1), ('graines', 1)]
}

# Note pour Q2 : on accepte avec ou sans le dernier \n selon comment l'étudiant a lu
# Pour simplifier, vous pourriez nettoyer Q2 dans engine.py ou ici être tolérant.

POINTS_BREAKDOWN = {
    'Q1': 1.0, 'Q2': 1.0, 'Q3': 2.0, 'Q4': 2.0, 'Q5': 2.0,
    'Q6': 2.0, 'Q7': 3.0, 'Q8': 3.0, 'Q9': 2.0, 'Q10': 2.0
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