from formative_s3 import check_formative_notebook

EVAL_ID = "td0-s3"
MAX_SCORE_TOTAL = 4.0
CHECKS = [
    {"label": "Lecture du fichier", "source": ["open(", "encoding="], "output": "Résultat Q1 :", "points": 1.0, "feedback": "Lire le fichier en UTF-8 et afficher le nombre de caractères."},
    {"label": "Découpage brut", "source": [".split()"], "output": "Résultat Q2 :", "points": 1.0, "feedback": "Créer une liste obtenue avec split()."},
    {"label": "Comptage", "source": ["len("], "output": "Résultat Q3 :", "points": 1.0, "feedback": "Afficher la taille de la liste de mots."},
    {"label": "Observation critique", "source": [], "output": "Résultat Q4 :", "points": 1.0, "feedback": "Expliquer au moins une limite de split() : ponctuation, casse, contraction ou morphologie."},
]
def check_notebook(content_str, filename):
    score, details, max_score, info, error = check_formative_notebook(
        content_str, CHECKS, MAX_SCORE_TOTAL
    )
    if score == max_score:
        verdict = "PRÊT : les prérequis minimaux pour TD1 sont présents."
    elif score >= 2:
        verdict = "À CONSOLIDER : réalisez R0 avant TD1."
    else:
        verdict = "ACCOMPAGNEMENT RECOMMANDÉ : réalisez R0 et reprenez les bases avec l'enseignant."
    details.insert(0, {
        "check": "Diagnostic TD0",
        "student_answer": verdict,
        "correct_answer": "Diagnostic formatif ; pas de note certificative.",
        "status": "ℹ️",
        "points": score,
        "max_points": max_score,
    })
    return score, details, max_score, info, error
