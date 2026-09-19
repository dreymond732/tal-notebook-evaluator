from formative_s1 import check_formative_notebook

EVAL_ID = 'td4-s1'
MAX_SCORE_TOTAL = 7.0
CHECKS = [{'label': 'Boucle de parcours', 'source': ['for ', '.upper('], 'output': 'Résultat Q1 :', 'points': 1.0, 'feedback': 'Reprendre : boucle de parcours.'}, {'label': 'Filtrage par longueur', 'source': ['for ', 'if ', 'len('], 'output': 'Résultat Q2 :', 'points': 1.0, 'feedback': 'Reprendre : filtrage par longueur.'}, {'label': 'Filtrage par appartenance', 'source': ['for ', '.lower(', ' in '], 'output': 'Résultat Q3 :', 'points': 1.0, 'feedback': 'Reprendre : filtrage par appartenance.'}, {'label': 'Positions avec range', 'source': ['range('], 'output': 'Résultat Q4 :', 'points': 1.0, 'feedback': 'Reprendre : positions avec range.'}, {'label': 'Boucle while bornée', 'source': ['while ', '+='], 'output': 'Résultat Q5 :', 'points': 1.0, 'feedback': 'Reprendre : boucle while bornée.'}, {'label': 'Fréquences', 'source': ['for ', '.get('], 'output': 'Résultat Q6 :', 'points': 1.0, 'feedback': 'Reprendre : fréquences.'}, {'label': 'Compréhension', 'source': ['[', 'for ', 'if '], 'output': 'Résultat Q7 :', 'points': 1.0, 'feedback': 'Reprendre : compréhension.'}]

def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
