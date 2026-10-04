"""TD1B v3: recorded technical evidence only; student code is never executed."""
import math
import re
from s3_audit import check_audit, keys, same

EVAL_ID = 'td1b-s3'
MAX_SCORE_TOTAL = 4.0
TRACE_RE = re.compile(r'^S3_TD(1)B_Q([1-9][0-9]*):\s*(.*)$')
TEXT1 = 'Apple a annoncé un investissement de 2 milliards d’euros en Allemagne en 2024.'
TEXT2 = 'Emmanuel Macron a rencontré Elon Musk à Paris hier. Ils ont parlé de Google et de Tesla'
TEXT4 = "J'étudie à l'Université de Toulon."
PHRASES = ['Le chat est sur le tapis.', 'Le chien est sur le canapé.']
# Teacher reference measured with spaCy 3.8.7 / fr_core_news_md 3.8.0.
# In particular Tesla=PER is the model output, not a linguistic endorsement.
ENTITIES1 = [['Apple', 'ORG'], ['Allemagne', 'LOC']]
ENTITIES2 = [['Emmanuel Macron', 'PER'], ['Elon Musk', 'PER'], ['Paris', 'LOC'], ['Google', 'ORG'], ['Tesla', 'PER']]
ENTITIES4 = [['Université de Toulon', 'ORG']]
SCORES = {'chien_chat': 0.6840823292732239, 'chien_voiture': 0.3173190653324127,
          'phrases': 0.9808356761932373}


def entity_rows(value, source, labels=('PER', 'ORG', 'LOC', 'MISC')):
    """Only provenance, label vocabulary and mention order for student texts."""
    if not isinstance(value, list) or not isinstance(source, str):
        return False
    position = 0
    for row in value:
        if (not isinstance(row, list) or len(row) != 2
                or not isinstance(row[0], str) or not row[0]
                or row[1] not in labels):
            return False
        start = source.find(row[0], position)
        if start < 0:
            return False
        position = start + len(row[0])
    return True


def selection(rows):
    return [row for row in rows if row[1] in ('PER', 'ORG')]


def q1(value):
    return (keys(value, ['texte', 'entites']) and value['texte'] == TEXT1
            and same(value['entites'], ENTITIES1))


def q2(value):
    if not (keys(value, ['texte', 'entites', 'selection', 'essai'])
            and value['texte'] == TEXT2 and same(value['entites'], ENTITIES2)
            and same(value['selection'], selection(ENTITIES2))):
        return False
    trial = value['essai']
    return (keys(trial, ['texte', 'entites', 'selection'])
            and isinstance(trial['texte'], str) and trial['texte'].strip()
            and trial['texte'] != TEXT2 and entity_rows(trial['entites'], trial['texte'])
            and same(trial['selection'], selection(trial['entites'])))


def finite_score(value):
    return type(value) in (int, float) and math.isfinite(value) and -1 <= value <= 1


def q3(value):
    if not (keys(value, ['vecteurs', 'scores', 'variation'])
            and same(value['vecteurs'], {'chien': True, 'chat': True, 'voiture': True})
            and keys(value['scores'], SCORES)):
        return False
    if not all(finite_score(value['scores'][key]) and math.isclose(value['scores'][key], score,
               rel_tol=0, abs_tol=1e-5) for key, score in SCORES.items()):
        return False
    trial = value['variation']
    return (keys(trial, ['original', 'modifie', 'score']) and trial['original'] in PHRASES
            and isinstance(trial['modifie'], str) and trial['modifie'].strip()
            and trial['modifie'] != trial['original'] and finite_score(trial['score']))


def q4(value):
    if not (keys(value, ['texte', 'avant', 'apres', 'pipeline', 'regles', 'essais'])
            and value['texte'] == TEXT4 and same(value['avant'], ENTITIES4)
            and same(value['apres'], ENTITIES4)):
        return False
    pipeline, rules, trials = value['pipeline'], value['regles'], value['essais']
    if (not isinstance(pipeline, list) or not all(isinstance(s, str) for s in pipeline)
            or pipeline.count('entity_ruler') != 1 or pipeline.count('ner') != 1
            or pipeline.index('entity_ruler') >= pipeline.index('ner')
            or not isinstance(rules, list) or len(rules) < 4):
        return False
    if not all(keys(rule, ['label', 'pattern']) and rule['label'] in ('PER', 'ORG', 'LOC', 'MISC', 'DATE')
               and isinstance(rule['pattern'], str) and rule['pattern'].strip() for rule in rules):
        return False
    patterns = [rule['pattern'] for rule in rules]
    if (len(set(patterns)) != len(patterns)
            or {'label': 'ORG', 'pattern': 'Université de Toulon'} not in rules
            or sum(rule['label'] == 'ORG' for rule in rules) < 2
            or not {'ORG', 'LOC', 'DATE'} <= {rule['label'] for rule in rules}
            or not isinstance(trials, list) or len(trials) < 5):
        return False
    for trial in trials:
        if (not keys(trial, ['texte', 'sans_regles', 'avec_regles'])
                or not isinstance(trial['texte'], str) or not trial['texte'].strip()
                or not entity_rows(trial['sans_regles'], trial['texte'])
                or not entity_rows(trial['avec_regles'], trial['texte'], labels=('PER', 'ORG', 'LOC', 'MISC', 'DATE'))):
            return False
    texts = [trial['texte'] for trial in trials]
    witnessed = [rule for rule in rules if any(
        rule['pattern'] in trial['texte']
        and [rule['pattern'], rule['label']] in trial['avec_regles'] for trial in trials)]
    return (len(set(texts)) == len(texts)
            and {'label': 'ORG', 'pattern': 'Université de Toulon'} in witnessed
            and any(rule['label'] == 'ORG' and rule['pattern'] != 'Université de Toulon' for rule in witnessed)
            and {'LOC', 'DATE'} <= {rule['label'] for rule in witnessed})


CHECKS = [
    {'label': 'Prédictions du modèle sur le texte fixé', 'validate': q1,
     'feedback': 'Texte exact et liste complète des entités, dans leur ordre, conformes au modèle md fixé. Le score ne juge pas votre comparaison linguistique.'},
    {'label': 'Filtrage PER/ORG et réemploi', 'validate': q2,
     'feedback': 'Prédictions du texte fixé et filtrage exact ; sur le texte personnel, provenance et cohérence du filtre seulement. Une liste vide peut être une prédiction réelle : le score ne certifie pas la qualité du modèle.'},
    {'label': 'Scores fixes et essai de variation', 'validate': q3,
     'feedback': 'Vecteurs présents et trois scores conformes au modèle md fixé (tolérance absolue 0,00001). Pour la variation, seule la présence de deux textes distincts et d’un score fini entre −1 et 1 est vérifiée ; sa justesse n’est pas recalculée.'},
    {'label': 'Règles et traces des cinq essais', 'validate': q4,
     'feedback': 'Comparaison Toulon, ordre du pipeline, règles ORG/LOC/DATE et au moins cinq textes distincts couvrant les expressions. Les quatre règles requises doivent apparaître avec leur label dans au moins un essai exact, y compris DATE qui n’est pas proposé par le modèle seul. Les autres mentions sont vérifiées pour leur provenance ; les variantes, ambiguïtés et l’exécution effective ne sont pas certifiées.'},
]


def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 1, CHECKS, evaluator=EVAL_ID, trace_re=TRACE_RE, additional_questions=('bilan',))
