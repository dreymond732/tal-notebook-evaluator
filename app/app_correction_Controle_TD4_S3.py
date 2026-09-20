"""Contrôle cumulatif S3 : mesures privées recalculées sur les corpus fixes."""
from s3_controls import check_control
from s3_controls_quantitative import validate

EVAL_ID = 'controle-td4-s3'
MAX_SCORE_TOTAL = 20.0
CHECKS = [
    {"label": 'Définir les unités du relevé', "validate": lambda value, context: validate(4, 1, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Produire des cooccurrences avec preuves', "validate": lambda value, context: validate(4, 2, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Évaluer une annonce de groupe', "validate": lambda value, context: validate(4, 3, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Définir une fenêtre sur le flux', "validate": lambda value, context: validate(4, 4, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Changer le contexte documentaire', "validate": lambda value, context: validate(4, 5, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Contrôler formes, lemmes et expressions', "validate": lambda value, context: validate(4, 6, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Transférer aux archives sonores', "validate": lambda value, context: validate(4, 7, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
]

def check_notebook(content_str, filename):
    return check_control(content_str, filename, 4, CHECKS)
