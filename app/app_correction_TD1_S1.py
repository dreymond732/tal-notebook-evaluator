from formative_s1 import check_formative_notebook

EVAL_ID = 'td1-s1'
MAX_SCORE_TOTAL = 6.0
CHECKS = [{'label': 'Calcul numérique', 'source': ['cout_total', '*'], 'output': 'Résultat Q1 :', 'points': 1.0, 'feedback': 'Reprendre : calcul numérique.'}, {'label': 'Observation de type', 'source': ['type('], 'output': 'Résultat Q2 :', 'points': 1.0, 'feedback': 'Reprendre : observation de type.'}, {'label': 'Comparaison et conjonction', 'source': ['==', 'and'], 'output': 'Résultat Q3 :', 'points': 1.0, 'feedback': 'Reprendre : comparaison et conjonction.'}, {'label': 'f-string', 'source': ['f"'], 'output': 'Résultat Q4 :', 'points': 1.0, 'feedback': 'Reprendre : f-string.'}, {'label': 'Conversion en entier', 'source': ['int('], 'output': 'Résultat Q5 :', 'points': 1.0, 'feedback': 'Reprendre : conversion en entier.'}, {'label': 'Chaîne et appartenance', 'source': ['len(', ' in '], 'output': 'Résultat Q6 :', 'points': 1.0, 'feedback': 'Reprendre : chaîne et appartenance.'}]

def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
