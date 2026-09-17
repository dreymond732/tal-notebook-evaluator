from formative_s3 import check_formative_notebook

EVAL_ID = "td-r2-s3"
MAX_SCORE_TOTAL = 4.0
CHECKS = [
    {"label": "Fonction paramétrée", "source": ["def frequences_lemmas", "stopwords"], "output": "Résultat Q1 :", "points": 1.0, "feedback": "Définir une fonction recevant le texte et une collection de stopwords."},
    {"label": "Lemmes de noms", "source": ["token.lemma_", "token.pos_ == \"NOUN\""], "output": "Résultat Q2 :", "points": 1.0, "feedback": "Ne compter que les lemmes des noms."},
    {"label": "Filtrage", "source": ["not token.is_stop"], "output": "Résultat Q3 :", "points": 1.0, "feedback": "Exclure les mots vides de spaCy."},
    {"label": "Counter et comparaison", "source": ["Counter", "most_common"], "output": "Résultat Q4 :", "points": 1.0, "feedback": "Produire et comparer les fréquences filtrées."},
]
def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
