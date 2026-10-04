"""Validation de traces JSON enregistrées : jamais d'exécution de code soumis."""
import ast
import json
import math
import re

from notebook_contract import ContractError, evaluation_cells, validate_cell_metadata, s3_contract_identity, CONTRACT_VERSIONS
from s3_review import review_evidence

TRACE_RE = re.compile(r'^S3_TD([0-7])_Q([1-9][0-9]*):\s*(.*)$')
TD_LIMIT_NOTE = (
    "Traces enregistrées uniquement : le serveur n'exécute pas votre programme. "
    "Il ne certifie ni leur authenticité ni leur fraîcheur. Réexécutez votre notebook "
    "dans l'ordre. Les interprétations et les annotations linguistiques relèvent "
    "de votre autoévaluation ; ce score formatif ne mesure pas leur qualité. Une relecture individuelle par l’enseignant n’est pas systématique."
)


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
                    if index.get(('Q' + match[2], 'answer')) is cell:
                        displays.setdefault(int(match[2]), []).append((cell_index, errors))
        stdout = ''.join(text(out.get('text', '')) for out in outputs
                         if out.get('output_type') == 'stream' and out.get('name', 'stdout') == 'stdout')
        for line in stdout.splitlines():
            match = trace_re.fullmatch(line)
            if match and int(match[1]) == td:
                if index.get(('Q' + match[2], 'answer')) is cell:
                    records.setdefault(int(match[2]), []).append((cell_index, match[3]))
    return displays, records


def grade_traces(displays, records, checks, weights, contextual=False):
    """Statuts distincts : mesure fausse, preuve absente, dépendance inutilisable."""
    context, answers, proof_errors = {}, {}, {}
    for number in range(1, len(checks) + 1):
        sources, traces = displays.get(number, []), records.get(number, [])
        if len(sources) != 1 or len(traces) != 1 or sources[0][0] != traces[0][0]:
            proof_errors[number] = 'Un print et une sortie JSON uniques sont attendus dans la même cellule.'
            continue
        raw = traces[0][1]
        answers[number] = raw[:2500]
        if sources[0][1]:
            proof_errors[number] = 'Erreur enregistrée dans la cellule ; réexécutez-la après correction.'
        elif len(raw) > 100000:
            proof_errors[number] = 'Trace trop longue : imprimez la synthèse demandée.'
        else:
            try:
                context[number] = json.loads(raw, parse_constant=_reject_constant, object_pairs_hook=_unique_object)
            except (ValueError, TypeError, RecursionError):
                proof_errors[number] = 'JSON mal formé : la preuve quantitative ne peut pas être lue.'
    details, score, deferred = [], 0.0, 0.0
    for number, (check, weight) in enumerate(zip(checks, weights), 1):
        blocked = []
        for dependency, usable in check.get('dependencies', {}).items():
            try:
                available = dependency in context and usable(context[dependency])
            except (ValueError, TypeError, KeyError, IndexError, AttributeError, RecursionError, OverflowError):
                available = False
            if not available:
                blocked.append('Q' + str(dependency))
        valid = False
        if number in proof_errors:
            state, diagnostic = 'preuve_absente', 'Preuve absente ou inexploitable. ' + proof_errors[number]
        elif blocked:
            state = 'non_verifiable'
            diagnostic = 'Non vérifiable : dépendance ' + ', '.join(blocked) + ' absente ou de structure invalide. À réexaminer après restauration de cette preuve ; aucune erreur de calcul indépendante n’est conclue.'
            deferred += weight
        else:
            try:
                valid = bool(check['validate'](context[number], context) if contextual or check.get('contextual') else check['validate'](context[number]))
            except (ValueError, TypeError, KeyError, IndexError, AttributeError, RecursionError, OverflowError):
                valid = False
            state = 'conforme' if valid else 'incorrect'
            diagnostic = 'Critère technique conforme.' if valid else 'Résultat ou structure non conforme au critère technique.'
        missing_fields = [field for field in check.get('required_text_fields', [])
                          if not isinstance(context.get(number), dict)
                          or not isinstance(context[number].get(field), str)
                          or not context[number][field].strip()]
        if missing_fields:
            diagnostic += ' Production rédigée absente : ' + ', '.join(missing_fields) + '. Présence à compléter ; qualité à relire humainement, sans point automatique.'
        points = float(weight if valid else 0)
        score += points
        details.append({
            'check': 'Q' + str(number) + ' — ' + check['label'],
            'student_answer': answers.get(number, proof_errors.get(number, 'Preuve absente.')),
            'correct_answer': check['feedback'], 'status': '✅' if valid else ('❌' if state == 'incorrect' else '⚠️'),
            'evaluation_status': state, 'diagnostic': diagnostic,
            'dependencies': blocked, 'missing_fields': missing_fields, 'points': points, 'max_points': float(weight),
        })
    return score, details, deferred


def check_audit(content_str, filename, td, checks, *, evaluator=None, trace_re=TRACE_RE, additional_questions=()):
    maximum = float(len(checks))
    evaluator = evaluator or f'td{td}-s3'
    optional_review = evaluator == 'td1b-s3' or evaluator in {f'td{n}-s3' for n in range(1, 8)}
    try:
        notebook = read_notebook(content_str)
        info = s3_contract_identity(notebook, evaluator)
        displays, records = collect(notebook['cells'], td, trace_re=trace_re)
    except ContractError as exc:
        return 0.0, [], maximum, {}, str(exc)
    except (ValueError, TypeError, RecursionError, OverflowError) as exc:
        return 0.0, [], maximum, {}, 'Erreur JSON/notebook : ' + str(exc)
    score, details, deferred = grade_traces(displays, records, checks, [1.0] * len(checks))
    details.append({'check': 'Portée du score', 'student_answer': TD_LIMIT_NOTE if optional_review else LIMIT_NOTE,
                    'correct_answer': '1 point par vérification déclarée dans le sujet ; aucune note automatique sur la qualité de l’argumentation.',
                    'status': 'ℹ️', 'points': 0.0, 'max_points': 0.0})
    info.update(score_brut=score, score_nature='technique_provisoire', score_max=maximum,
                relecture_humaine='facultative' if optional_review else 'requise', contract_version=CONTRACT_VERSIONS[evaluator], points_a_reexaminer=deferred,
                review_evidence=review_evidence(notebook, len(checks), additional_questions=additional_questions))
    return score, details, maximum, info, None
