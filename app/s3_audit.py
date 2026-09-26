"""Validation de traces JSON enregistrées : jamais d'exécution de code soumis."""
import ast
import json
import math
import re

import outils
from notebook_contract import evaluation_cells, validate_cell_metadata

TRACE_RE = re.compile(r'^S3_TD([0-7])_Q([1-9][0-9]*):\s*(.*)$')
LIMIT_NOTE = (
    "Traces enregistrées uniquement : le serveur n'exécute pas votre programme. "
    "Il ne certifie ni leur authenticité ni leur fraîcheur. Réexécutez votre notebook "
    "dans l'ordre. Les interprétations et les annotations linguistiques relèvent "
    "d'une relecture humaine ; ce score formatif ne mesure pas leur qualité."
)


def text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(part, str) for part in value):
        return ''.join(value)
    raise ValueError('Texte de cellule ou de sortie mal formé.')


def same(value, expected):
    """Égalité JSON typée ; bool n'est pas un entier et NaN n'est pas une mesure."""
    if isinstance(expected, float):
        return type(value) in (int, float) and math.isfinite(value) and math.isclose(value, expected, rel_tol=1e-8, abs_tol=1e-8)
    if type(value) is not type(expected):
        return False
    if isinstance(expected, dict):
        return value.keys() == expected.keys() and all(same(value[key], item) for key, item in expected.items())
    if isinstance(expected, list):
        return len(value) == len(expected) and all(same(left, right) for left, right in zip(value, expected))
    return value == expected


def integer(value, minimum=0):
    return type(value) is int and value >= minimum


def string(value):
    return isinstance(value, str) and len(value.strip()) >= 3 and value.strip() not in {'...', 'À compléter', 'A compléter', 'TODO'}


def keys(value, required):
    return isinstance(value, dict) and set(required) <= value.keys()


def _reject_constant(value):
    raise ValueError('Valeur JSON non finie interdite.')


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Clé JSON répétée.')
        result[key] = value
    return result


def read_notebook(content):
    notebook = json.loads(content, parse_constant=_reject_constant)
    if not isinstance(notebook, dict) or not isinstance(notebook.get('cells'), list):
        raise ValueError('Liste de cellules absente.')
    for cell in notebook['cells']:
        if not isinstance(cell, dict):
            raise ValueError('Cellule mal formée.')
        text(cell.get('source', ''))
        outputs = cell.get('outputs', [])
        if not isinstance(outputs, list) or not all(isinstance(out, dict) for out in outputs):
            raise ValueError('Sorties mal formées.')
        for out in outputs:
            if out.get('output_type') == 'stream':
                text(out.get('text', ''))
    return notebook


def collect(cells, td, trace_re=TRACE_RE):
    notebook = {'cells': cells}
    index = validate_cell_metadata(notebook)
    explicit = any(role not in {'submission', 'infrastructure'} for _, role in index)
    displays, records = {}, {}
    for cell_index, cell in enumerate(evaluation_cells(notebook)):
        if cell.get('cell_type') != 'code':
            continue
        source = text(cell.get('source', ''))
        outputs = cell.get('outputs', [])
        errors = any(out.get('output_type') == 'error' for out in outputs)
        try:
            tree = ast.parse(source)
        except (SyntaxError, ValueError, RecursionError):
            tree = None
        if tree:
            # Le contrat utilise un print explicite au niveau de la cellule.
            # Les commentaires, fonctions non appelées et affichages Markdown ne comptent pas.
            for statement in tree.body:
                call = statement.value if isinstance(statement, ast.Expr) else None
                if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                        and call.func.id == 'print' and len(call.args) == 2):
                    continue
                first = call.args[0]
                if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
                    continue
                match = trace_re.fullmatch(first.value)
                if match and int(match[1]) == td and not match[3]:
                    if not explicit or index.get(('Q' + match[2], 'answer')) is cell:
                        displays.setdefault(int(match[2]), []).append((cell_index, errors))
        stdout = ''.join(text(out.get('text', '')) for out in outputs
                         if out.get('output_type') == 'stream' and out.get('name', 'stdout') == 'stdout')
        for line in stdout.splitlines():
            match = trace_re.fullmatch(line)
            if match and int(match[1]) == td:
                if not explicit or index.get(('Q' + match[2], 'answer')) is cell:
                    records.setdefault(int(match[2]), []).append((cell_index, match[3]))
    return displays, records


def check_audit(content_str, filename, td, checks):
    maximum = float(len(checks))
    try:
        notebook = read_notebook(content_str)
        displays, records = collect(notebook['cells'], td)
    except (ValueError, TypeError, RecursionError, OverflowError) as exc:
        return 0.0, [], maximum, {}, 'Erreur JSON/notebook : ' + str(exc)
    context = {}
    for question, entries in records.items():
        sources = displays.get(question, [])
        if len(entries) == len(sources) == 1 and entries[0][0] == sources[0][0] and not sources[0][1] and len(entries[0][1]) <= 100000:
            try:
                context[question] = json.loads(entries[0][1], parse_constant=_reject_constant, object_pairs_hook=_unique_object)
            except (ValueError, TypeError, RecursionError):
                pass
    details, score = [], 0.0
    for number, check in enumerate(checks, 1):
        sources, traces = displays.get(number, []), records.get(number, [])
        valid, answer = False, 'Un print et une sortie JSON uniques sont attendus dans la même cellule.'
        if len(sources) == len(traces) == 1 and sources[0][0] == traces[0][0]:
            raw = traces[0][1]
            answer = raw[:2500]
            if sources[0][1]:
                answer = 'Erreur enregistrée dans la cellule ; réexécutez-la après correction.'
            elif len(raw) > 100000:
                answer = 'Trace trop longue : imprimez la synthèse demandée, pas le corpus complet.'
            else:
                try:
                    value = json.loads(raw, parse_constant=_reject_constant, object_pairs_hook=_unique_object)
                    valid = check['validate'](value, context) if check.get('contextual') else check['validate'](value)
                except (ValueError, TypeError, KeyError, IndexError, AttributeError, RecursionError, OverflowError):
                    answer = 'JSON mal formé ou structure non conforme. ' + raw[:1000]
        score += float(bool(valid))
        details.append({
            'check': 'Q' + str(number) + ' — ' + check['label'],
            'student_answer': answer,
            'correct_answer': check['feedback'],
            'status': '✅' if valid else '❌', 'points': float(bool(valid)), 'max_points': 1.0,
        })
    details.append({'check': 'Portée du score', 'student_answer': LIMIT_NOTE,
                    'correct_answer': '1 point par vérification déclarée dans le sujet ; aucune note automatique sur la qualité de l’argumentation.',
                    'status': 'ℹ️', 'points': 0.0, 'max_points': 0.0})
    info = outils.extract_identification_info(notebook['cells'])
    info['score_brut'] = score
    return score, details, maximum, info, None
