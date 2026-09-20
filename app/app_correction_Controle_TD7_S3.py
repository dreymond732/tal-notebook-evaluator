"""Contrôle cumulatif S3 : mesures privées recalculées sur les corpus fixes."""
from s3_controls import check_control
from s3_controls_quantitative import validate

EVAL_ID = 'controle-td7-s3'
MAX_SCORE_TOTAL = 20.0
CHECKS = [
    {"label": 'Qualifier les annonces du rapport', "validate": lambda value, context: validate(7, 1, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Construire un moteur paramétrable de mesure', "validate": lambda value, context: validate(7, 2, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Vérifier la fidélité des citations', "validate": lambda value, context: validate(7, 3, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Comparer des nombres dans leur protocole', "validate": lambda value, context: validate(7, 4, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Éprouver groupes, expressions et représentations', "validate": lambda value, context: validate(7, 5, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Valider sur un autre domaine', "validate": lambda value, context: validate(7, 6, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Livrer un dossier complet de vérification', "validate": lambda value, context: validate(7, 7, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
]

def check_notebook(content_str, filename):
    return check_control(content_str, filename, 7, CHECKS)
