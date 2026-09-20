"""Contrôle cumulatif S3 : mesures privées recalculées sur les corpus fixes."""
from s3_controls import check_control
from s3_controls_quantitative import validate

EVAL_ID = 'controle-td6-s3'
MAX_SCORE_TOTAL = 20.0
CHECKS = [
    {"label": 'Situer les occurrences sans changer le flux', "validate": lambda value, context: validate(6, 1, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Segmenter et conserver les frontières', "validate": lambda value, context: validate(6, 2, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Relier la carte de chaleur aux dénominateurs', "validate": lambda value, context: validate(6, 3, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Visualiser la sensibilité aux fenêtres', "validate": lambda value, context: validate(6, 4, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Revenir du graphique au texte original', "validate": lambda value, context: validate(6, 5, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Rendre une matrice de cooccurrences lisible', "validate": lambda value, context: validate(6, 6, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
    {"label": 'Transférer aux retours d’ateliers', "validate": lambda value, context: validate(6, 7, value), "feedback": 'Valeurs calculées sur les données et selon les conventions du sujet. Les preuves quantitatives sont contrôlées ; le code, les arguments, les annotations et les figures restent à relire humainement.'},
]

def check_notebook(content_str, filename):
    return check_control(content_str, filename, 6, CHECKS)
