"""Contrôle cumulatif S3 : mesures privées recalculées sur les corpus fixes."""
from s3_controls import check_control
from s3_controls_quantitative import validate

EVAL_ID = 'controle-td5-s3'
MAX_SCORE_TOTAL = 20.0
CHECKS = [
    {"label": 'Reconstruire les effectifs de base', "validate": lambda value, context: validate(5, 1, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Construire les deux populations de référence', "validate": lambda value, context: validate(5, 2, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Distinguer fréquence et concentration', "validate": lambda value, context: validate(5, 3, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Comparer deux tailles de texte', "validate": lambda value, context: validate(5, 4, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Distinguer zéro, absence de base et rareté', "validate": lambda value, context: validate(5, 5, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Mesurer une couverture de positions', "validate": lambda value, context: validate(5, 6, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Transférer aux bulletins du littoral', "validate": lambda value, context: validate(5, 7, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
]

def check_notebook(content_str, filename):
    return check_control(content_str, filename, 5, CHECKS)
