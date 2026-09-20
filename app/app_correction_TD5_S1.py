from formative_s1 import check_formative_notebook

EVAL_ID = 'td5-s1'
MAX_SCORE_TOTAL = 6.0
CHECKS = [{'label': 'Fonction et retour', 'source': ['def longueur_texte', 'return'], 'output': 'Résultat Q1 :', 'points': 1.0, 'feedback': 'Reprendre : fonction et retour.'}, {'label': 'Normalisation réutilisable', 'source': ['def normaliser', '.strip(', '.lower('], 'output': 'Résultat Q2 :', 'points': 1.0, 'feedback': 'Reprendre : normalisation réutilisable.'}, {'label': 'Composition', 'source': ['def nombre_mots', 'normaliser('], 'output': 'Résultat Q3 :', 'points': 1.0, 'feedback': 'Reprendre : composition.'}, {'label': 'Traduction sécurisée', 'source': ['def traduire_mot', 'if ', 'return'], 'output': 'Résultat Q4 :', 'points': 1.0, 'feedback': 'Reprendre : traduction sécurisée.'}, {'label': 'Traduction de phrase', 'source': ['def traduire_phrase', '.join('], 'output': 'Résultat Q5 :', 'points': 1.0, 'feedback': 'Reprendre : traduction de phrase.'}, {'label': 'Dictionnaire de synthèse', 'source': ['def resume_texte', 'nombre_mots('], 'output': 'Résultat Q6 :', 'points': 1.0, 'feedback': 'Reprendre : dictionnaire de synthèse.'}]

def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
