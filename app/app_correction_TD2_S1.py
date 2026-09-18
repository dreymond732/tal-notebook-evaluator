from formative_s1 import check_formative_notebook

EVAL_ID = 'td2-s1'
MAX_SCORE_TOTAL = 7.0
CHECKS = [{'label': 'Nettoyage de bord', 'source': ['.strip('], 'output': 'Résultat Q1 :', 'points': 1.0, 'feedback': 'Reprendre : nettoyage de bord.'}, {'label': 'Transformation de chaîne', 'source': ['.lower(', '.replace('], 'output': 'Résultat Q2 :', 'points': 1.0, 'feedback': 'Reprendre : transformation de chaîne.'}, {'label': 'Indexation et tranche', 'source': ['mot[0]', 'mot[-1]', 'mot[0:4]'], 'output': 'Résultat Q3 :', 'points': 1.0, 'feedback': 'Reprendre : indexation et tranche.'}, {'label': 'Découpage', 'source': ['.split('], 'output': 'Résultat Q4 :', 'points': 1.0, 'feedback': 'Reprendre : découpage.'}, {'label': 'Recomposition', 'source': ['.join('], 'output': 'Résultat Q5 :', 'points': 1.0, 'feedback': 'Reprendre : recomposition.'}, {'label': 'Parcours de plusieurs chaînes', 'source': ['for '], 'output': 'Résultat Q6 :', 'points': 1.0, 'feedback': 'Reprendre : parcours de plusieurs chaînes.'}, {'label': 'Limite explicitée', 'source': [], 'output': 'Résultat Q7 :', 'points': 1.0, 'feedback': 'Reprendre : limite explicitée.'}]

def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
