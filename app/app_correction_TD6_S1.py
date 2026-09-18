from formative_s1 import check_formative_notebook

EVAL_ID = 'td6-s1'
MAX_SCORE_TOTAL = 6.0
CHECKS = [{'label': 'Lecture UTF-8 contextualisée', 'source': ['with open(', 'encoding='], 'output': 'Résultat Q1 :', 'points': 1.0, 'feedback': 'Reprendre : lecture utf-8 contextualisée.'}, {'label': 'Découpage en lignes', 'source': ['.splitlines('], 'output': 'Résultat Q2 :', 'points': 1.0, 'feedback': 'Reprendre : découpage en lignes.'}, {'label': 'Séparation structurée', 'source': ['split(";", 1)'], 'output': 'Résultat Q3 :', 'points': 1.0, 'feedback': 'Reprendre : séparation structurée.'}, {'label': 'Fonction de normalisation', 'source': ['def normaliser_personne', '.title('], 'output': 'Résultat Q4 :', 'points': 1.0, 'feedback': 'Reprendre : fonction de normalisation.'}, {'label': 'Dédoublonnage', 'source': ['set('], 'output': 'Résultat Q5 :', 'points': 1.0, 'feedback': 'Reprendre : dédoublonnage.'}, {'label': 'Écriture CSV', 'source': ['csv.', 'open(', 'newline='], 'output': 'Résultat Q6 :', 'points': 1.0, 'feedback': 'Reprendre : écriture csv.'}]

def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
