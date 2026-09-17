from formative_s3 import check_formative_notebook

EVAL_ID = "td-r1-s3"
MAX_SCORE_TOTAL = 4.0
CHECKS = [
    {"label": "Traitement spaCy", "source": ["nlp(", "doc ="], "output": "Résultat Q1 :", "points": 1.0, "feedback": "Créer un Doc spaCy à partir du texte fourni."},
    {"label": "Parcours des tokens", "source": ["for token in doc"], "output": "Résultat Q2 :", "points": 1.0, "feedback": "Parcourir les tokens du Doc."},
    {"label": "Filtrage morpho-syntaxique", "source": ["token.pos_", "NOUN"], "output": "Résultat Q3 :", "points": 1.0, "feedback": "Extraire les noms en utilisant token.pos_."},
    {"label": "Verbes et lemmes", "source": ["VERB", "token.lemma_"], "output": "Résultat Q4 :", "points": 1.0, "feedback": "Extraire les lemmes des verbes."},
]
def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
