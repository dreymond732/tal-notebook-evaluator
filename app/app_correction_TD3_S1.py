from formative_s1 import check_formative_notebook

EVAL_ID = 'td3-s1'
MAX_SCORE_TOTAL = 6.0
CHECKS = [{'label': 'Modification de liste', 'source': ['.append(', '.pop('], 'output': 'Résultat Q1 :', 'points': 1.0, 'feedback': 'Reprendre : modification de liste.'}, {'label': 'Tuple', 'source': ['tuple'], 'output': 'Résultat Q2 :', 'points': 1.0, 'feedback': 'Reprendre : tuple.'}, {'label': 'Dictionnaire', 'source': ['lexique', '{'], 'output': 'Résultat Q3 :', 'points': 1.0, 'feedback': 'Reprendre : dictionnaire.'}, {'label': 'Parcours clé-valeur', 'source': ['.items('], 'output': 'Résultat Q4 :', 'points': 1.0, 'feedback': 'Reprendre : parcours clé-valeur.'}, {'label': 'Ensemble', 'source': ['set('], 'output': 'Résultat Q5 :', 'points': 1.0, 'feedback': 'Reprendre : ensemble.'}, {'label': 'Comparaison d’ensembles', 'source': ['&', '-'], 'output': 'Résultat Q6 :', 'points': 1.0, 'feedback': 'Reprendre : comparaison d’ensembles.'}]

def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
