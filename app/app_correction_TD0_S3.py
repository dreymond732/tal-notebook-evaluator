from formative_s3 import check_formative_notebook

EVAL_ID = "td0-s3"
MAX_SCORE_TOTAL = 7.0
CHECKS = [
    {"label": "Lecture UTF-8", "source": ["with open(", "encoding="], "output": "Résultat Q1 :", "points": 1.0, "feedback": "Lire le corpus fourni en UTF-8 avec un contexte with."},
    {"label": "Découpage brut", "source": [".split()"], "output": "Résultat Q2 :", "points": 1.0, "feedback": "Créer et afficher une liste issue de split()."},
    {"label": "Comptage", "source": ["len("], "output": "Résultat Q3 :", "points": 1.0, "feedback": "Compter les éléments de la liste."},
    {"label": "Formes distinctes", "source": ["set("], "output": "Résultat Q4 :", "points": 1.0, "feedback": "Construire un ensemble de formes distinctes."},
    {"label": "Fonction de fréquences", "source": ["def frequences_brutes", "return", ".get("], "output": "Résultat Q5 :", "points": 1.0, "feedback": "Définir une fonction qui retourne un dictionnaire de fréquences."},
    {"label": "Normalisation", "source": ["def frequences_minuscules", ".lower()"], "output": "Résultat Q6 :", "points": 1.0, "feedback": "Comparer le comptage brut avec une normalisation en minuscules."},
    {"label": "Limites du découpage", "source": [], "output": "Résultat Q7 :", "points": 1.0, "feedback": "Expliquer une limite de split() et l'apport d'une annotation linguistique."},
]

def check_notebook(content_str, filename):
    score, details, max_score, info, error = check_formative_notebook(
        content_str, CHECKS, MAX_SCORE_TOTAL
    )
    if score >= 6:
        verdict = "PRÊT : les prérequis minimaux pour TD1 sont présents."
    elif score >= 4:
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
