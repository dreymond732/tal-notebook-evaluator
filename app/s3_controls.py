"""Mesures techniques privées des contrôles S3, sans exécution des copies."""
import json
import re

import outils
from s3_audit import collect, read_notebook, _reject_constant, _unique_object

TRACE_RE = re.compile(r'^S3_C([1-7])_Q([1-9][0-9]*):\s*(.*)$')
WEIGHTS = (2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0)
SCORE_KIND = 'technique_provisoire'
HUMAN_REVIEW = (
    'Relecture humaine requise : raisonnement, validité des annotations linguistiques, '
    'interprétation, qualité des figures, autonomie et respect du protocole. '
    'Le score technique sur 20 ne constitue pas une note globale. '
    'Le serveur analyse uniquement les traces enregistrées, sans exécuter le code ; '
    'il ne certifie ni leur authenticité ni leur fraîcheur.'
)


def check_control(content_str, filename, number, checks):
    """Contrat commun ; aucune mesure de qualité par longueur ou mots-clés."""
    if len(checks) != len(WEIGHTS):
        raise ValueError('Un contrôle S3 comporte exactement sept vérifications.')
    maximum = sum(WEIGHTS)
    try:
        nb = read_notebook(content_str)
        displays, records = collect(nb['cells'], number, trace_re=TRACE_RE)
    except (ValueError, TypeError, RecursionError, OverflowError) as exc:
        return 0.0, [], maximum, {}, 'Erreur JSON/notebook : ' + str(exc)
    context, raw_answers = {}, {}
    for q, entries in records.items():
        sources = displays.get(q, [])
        if len(entries) != 1 or len(sources) != 1 or entries[0][0] != sources[0][0] or sources[0][1]:
            continue
        raw = entries[0][1]
        raw_answers[q] = raw[:2500]
        if len(raw) > 100000:
            continue
        try:
            context[q] = json.loads(raw, parse_constant=_reject_constant, object_pairs_hook=_unique_object)
        except (ValueError, TypeError, RecursionError):
            continue
    details, score = [], 0.0
    for q, (check, weight) in enumerate(zip(checks, WEIGHTS), 1):
        valid = False
        if q in context:
            try:
                valid = bool(check['validate'](context[q], context))
            except (ValueError, TypeError, KeyError, IndexError, AttributeError, RecursionError, OverflowError):
                valid = False
        points = weight if valid else 0.0
        score += points
        details.append({
            'check': f'Q{q} — ' + check['label'],
            'student_answer': raw_answers.get(q, 'Trace absente, répétée, erronée ou sans affichage correspondant.'),
            'correct_answer': check['feedback'], 'status': '✅' if valid else '❌',
            'points': points, 'max_points': weight,
        })
    info = outils.extract_identification_info(nb['cells'])
    info.update(score_brut=score, score_nature=SCORE_KIND,
                relecture_humaine='requise', score_max=maximum)
    return score, details, maximum, info, None
