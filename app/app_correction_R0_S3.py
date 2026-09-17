from formative_s3 import check_formative_notebook

EVAL_ID = "td-r0-s3"
MAX_SCORE_TOTAL = 4.0
CHECKS = [
    {"label": "Fonction de comptage", "source": ["def compter_mots", "return"], "output": "Résultat Q1 :", "points": 1.0, "feedback": "Définir compter_mots(texte) et l'essayer."},
    {"label": "Normalisation minimale", "source": [".lower()"], "output": "Résultat Q2 :", "points": 1.0, "feedback": "Passer en minuscules avant de compter."},
    {"label": "Dictionnaire de fréquences", "source": ["frequences", "get("], "output": "Résultat Q3 :", "points": 1.0, "feedback": "Construire un dictionnaire de fréquences sans bibliothèque supplémentaire."},
    {"label": "Interprétation", "source": [], "output": "Résultat Q4 :", "points": 1.0, "feedback": "Commenter une limite du comptage brut."},
]
def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
