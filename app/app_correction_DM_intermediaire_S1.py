"""Private, provisional checks for the S1 intermediate assignment.

Only JSON, Python syntax trees and saved literal outputs are inspected. No student
code is executed. Static evidence cannot authenticate saved outputs or establish
correctness on untested inputs; the teacher must review the program and prose.
"""
import ast
import json
import math
import re

from notebook_contract import resolve_notebook, validate_cell_metadata

EVAL_ID = 'dm-intermediaire-s1'
MAX_SCORE_TOTAL = 20.0
HUMAN_REVIEW = (
    'Relecture humaine requise : raisonnement, explications, généralité des fonctions, '
    'tests, lisibilité et respect des notions vues jusqu’au TD5. '
    'Le score technique sur 20 ne constitue pas une note globale. '
    'Le serveur lit le code et les sorties enregistrées sans les exécuter ; '
    'il ne certifie ni leur authenticité ni leur fraîcheur. '
    'Une solution valable non reconnue par les vérifications statiques doit être réexaminée.'
)
HUMAN_REVIEW_DIMENSIONS = (
    'Raisonnement et justification des calculs, conditions et bornes',
    'Explications demandées : types, chaînes, collections, paramètres et retours',
    'Généralité des fonctions, tests et gestion des cas limites',
    'Lisibilité du programme, autonomie et notions des TD1 à TD5',
)
TRACE = re.compile(r'^Résultat Q([1-9][0-9]*)\s*:\s*(.*)$')


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        return ''.join(value)
    raise ValueError('Texte de cellule ou de sortie invalide.')


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Champ JSON dupliqué.')
        result[key] = value
    return result


def _literal(raw):
    if len(raw) > 50000:
        raise ValueError('Trace trop longue.')
    node = ast.parse(raw, mode='eval')
    for item in ast.walk(node):
        if isinstance(item, ast.Dict):
            keys = [ast.literal_eval(key) for key in item.keys]
            if len(keys) != len(set(keys)):
                raise ValueError('Clé de dictionnaire répétée.')
    return ast.literal_eval(node)


def _same(actual, expected):
    # bool is deliberately not accepted as a numerical answer.
    if isinstance(expected, bool):
        return type(actual) is bool and actual == expected
    if isinstance(expected, (float, int)):
        return (type(actual) in (int, float) and math.isfinite(actual)
                and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9))
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and actual.keys() == expected.keys()
                and all(_same(actual[key], value) for key, value in expected.items()))
    if isinstance(expected, (list, tuple)):
        return (type(actual) is type(expected) and len(actual) == len(expected)
                and all(_same(a, b) for a, b in zip(actual, expected)))
    return type(actual) is type(expected) and actual == expected


def _names(node):
    return {item.id for item in ast.walk(node) if isinstance(item, ast.Name)}


def _writes(node):
    names = {item.id for item in ast.walk(node)
             if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Store)}
    # Mutation through append/update/subscripts also defines an accumulator.
    for item in ast.walk(node):
        if isinstance(item, ast.Call) and isinstance(item.func, ast.Attribute):
            names.update(_names(item.func.value))
        elif isinstance(item, ast.Subscript) and isinstance(item.ctx, ast.Store):
            names.update(_names(item.value))
    return names


def _relevant(expression, statements):
    """Conservative dependency slice of a displayed expression, never an interpreter."""
    selected, needed = [expression], _names(expression)
    while True:
        added = False
        for statement in statements:
            if statement in selected:
                continue
            defined = ({statement.name} if isinstance(statement, ast.FunctionDef)
                       else _writes(statement))
            if defined & needed:
                selected.append(statement)
                needed.update(_names(statement))
                added = True
        if not added:
            return selected


def _nodes(roots):
    return [node for root in roots for node in ast.walk(root)]


def _calls(nodes, name):
    return [node for node in nodes if isinstance(node, ast.Call)
            and ((isinstance(node.func, ast.Name) and node.func.id == name)
                 or (isinstance(node.func, ast.Attribute) and node.func.attr == name))]


def _has(nodes, kind):
    return any(isinstance(node, kind) for node in nodes)


def _function(nodes, name, argument_count):
    defs = [node for node in nodes if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(defs) != 1:
        return None
    function = defs[0]
    parameters = {arg.arg for arg in function.args.posonlyargs + function.args.args}
    if len(parameters) != argument_count:
        return None
    returns = [node for node in ast.walk(function) if isinstance(node, ast.Return) and node.value is not None]
    # A constant return with an unrelated use of a parameter earns no evidence.
    returned_dependencies = set().union(*(_names(root) for ret in returns
                                          for root in _relevant(ret.value, function.body)))
    if not returns or not parameters <= returned_dependencies:
        return None
    return function


def _read_answer(cell, q):
    if not cell or cell.get('cell_type') != 'code':
        return None
    tree = ast.parse(_text(cell.get('source', '')))
    outputs = cell.get('outputs', [])
    if not isinstance(outputs, list) or any(not isinstance(out, dict) or out.get('output_type') == 'error' for out in outputs):
        return None
    matching = []
    for statement in tree.body:
        if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
            continue
        call = statement.value
        if not (isinstance(call.func, ast.Name) and call.func.id == 'print' and len(call.args) == 2):
            continue
        if isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
            match = TRACE.fullmatch(call.args[0].value.strip())
            if match and int(match.group(1)) == q:
                matching.append(call)
    if len(matching) != 1:
        return None
    saved = []
    for output in outputs:
        if output.get('output_type') == 'stream' and output.get('name', 'stdout') == 'stdout':
            # One stream may be split into several chunks by the notebook runtime.
            saved.append(_text(output.get('text', '')))
    lines = [m for line in ''.join(saved).splitlines() if (m := TRACE.fullmatch(line.strip()))
             and int(m.group(1)) == q]
    if len(lines) != 1:
        return None
    raw = lines[0].group(2)
    expression = matching[0].args[1]
    roots = _relevant(expression, [stmt for stmt in tree.body if stmt is not matching[0]])
    return _literal(raw), _nodes(roots), tree, raw

# Reference data are server-owned, not read from the uploaded notebook.
EXPECTED = [
    [12, 90.0, 108.0, 9.0, True],
    [57.0, 12.0],
    [True, False, True, 'Atelier italien : 0 place(s).'],
    ['ATELIER de LIVRES', 'atelier de livres', 'atelier de récits', '  ATELIER de LIVRES  '],
    ['B', '6', 'BIB', 'FR', '2026'],
    [['Lire,', 'c’est', 'partager', 'des', 'récits', '!'], 6, 'partager', '!'],
    ['lecture | traduction | échange', ['lecture', 'traduction', 'échange'], True],
    [['accueil', 'lecture', 'échange'], ('français', 'italien', 'espagnol'), True],
    [{'book': 'livre', 'story': 'récit', 'reader': 'lecteur', 'library': 'bibliothèque'}, 'récit',
     ['book -> livre', 'story -> récit', 'reader -> lecteur', 'library -> bibliothèque']],
    [5, 4, {'langue', 'lecture'}, {'récit', 'mémoire'}],
    [['livre', 'art', 'langue', 'récit', 'image'], ['livre', 'langue', 'récit', 'image'], [5, 6, 5, 5]],
    [[2, 4, 6, 8, 10, 12], [3, 6, 12, 24, 48, 96], 189],
    [{'lecture': 3, 'traduction': 2, 'échange': 1}, ['lecture', 'traduction'], 6, True],
    [['trop petit', 'trop grand', 'trouvé'], 3, True, 2],
    ['livre', '', 'deux  mots !'],
    [{'livre': 2, 'récit': 1}, {}, {'Livre': 1, 'livre': 1}],
    ['livre', 'map', 'livre récit map', '', 'ouvrage'],
    [{'texte_normalise': 'livre récit livre', 'nb_caracteres': 17, 'nb_fragments': 3,
      'nb_formes': 2, 'frequences': {'livre': 2, 'récit': 1}},
     {'texte_normalise': '', 'nb_caracteres': 0, 'nb_fragments': 0, 'nb_formes': 0, 'frequences': {}},
     {'texte_normalise': 'livre livre, livre', 'nb_caracteres': 18, 'nb_fragments': 3,
      'nb_formes': 2, 'frequences': {'livre': 2, 'livre,': 1}}],
]
LABELS = [
    'Budget et conversion', 'Priorités des opérations', 'Conditions et message',
    'Transformation et conservation de la source', 'Indices et tranches',
    'Découpage et unités', 'Reconstruction et séparateur', 'Liste et tuple',
    'Lexique et parcours', 'Ensembles et différences', 'Filtre et compréhension',
    'Séries bornées', 'Fréquences et vérification', 'Recherche bornée',
    'Fonction de normalisation', 'Fonction de comptage', 'Traduction paramétrée', 'Composition du bilan',
]


def _test_cases(nodes, name, cases, literals):
    observed = []
    for call in _calls(nodes, name):
        try:
            args = [literals[arg.id] if isinstance(arg, ast.Name) else ast.literal_eval(arg) for arg in call.args]
            observed.append(args)
        except (ValueError, KeyError, TypeError):
            continue
    return all(any(_same(args, list(case)) for args in observed) for case in cases)


def _evidence(q, nodes, tree, literals):
    """Per-result structural criteria; names of temporary variables are unrestricted."""
    has = lambda kind: _has(nodes, kind)
    call = lambda name: bool(_calls(nodes, name))
    arithmetic = lambda kind: has(kind) and has(ast.BinOp)
    loop_count = has(ast.For) and has(ast.Subscript) and (has(ast.Add) or call('get'))
    if q == 1:
        return [call('int'), arithmetic(ast.Mult), arithmetic(ast.Add), arithmetic(ast.Div), call('type')]
    if q == 2:
        return [arithmetic(ast.Sub) and arithmetic(ast.Div)] * 2
    if q == 3:
        return [has(ast.In), has(ast.And) and has(ast.Compare), has(ast.Compare), has(ast.JoinedStr)]
    if q == 4:
        return [call('strip'), call('lower'), call('replace'), call('strip') and call('lower')]
    if q == 5:
        return [has(ast.Subscript)] * 2 + [has(ast.Slice)] * 3
    if q == 6:
        return [call('split'), call('len'), has(ast.Subscript), has(ast.Subscript)]
    if q == 7:
        return [call('join'), call('split'), has(ast.Compare)]
    if q == 8:
        return [(call('pop') or call('remove') or has(ast.Delete)) and (call('append') or call('extend')),
                has(ast.Tuple) or call('tuple'), call('type') and (has(ast.Tuple) or call('tuple'))]
    if q == 9:
        return [has(ast.Dict) and has(ast.Subscript), has(ast.Subscript), has(ast.For) and call('items')]
    if q == 10:
        return [call('len'), call('set') and call('len'), call('set') and (has(ast.BitAnd) or call('intersection')),
                call('set') and (has(ast.Sub) or call('difference'))]
    if q == 11:
        return [has(ast.For) and call('strip') and call('lower'),
                has(ast.Compare) and call('len') and (has(ast.If) or has(ast.ListComp)),
                has(ast.ListComp) and call('len')]
    if q == 12:
        return [has(ast.For) and call('range'), has(ast.While) and (has(ast.Mult) or has(ast.Add)),
                has(ast.While) and has(ast.Add) and not call('sum')]
    if q == 13:
        return [loop_count, has(ast.For) and call('items') and has(ast.Compare),
                has(ast.For) and has(ast.Add) and call('items'), has(ast.Compare) and call('len')]
    if q == 14:
        return [has(ast.While) and has(ast.If) and has(ast.Compare), has(ast.While) and has(ast.Add),
                has(ast.While) and has(ast.Compare), has(ast.While) and has(ast.Sub)]
    function_names = {15: [('normaliser_notice', 1)], 16: [('compter_elements', 1)],
                      17: [('traduire_etiquette', 2), ('traduire_annonce', 2)], 18: [('bilan_notice', 1)]}
    definitions = {name: _function(nodes, name, arity) for name, arity in function_names[q]}
    top = _nodes([statement for statement in tree.body if not isinstance(statement, ast.FunctionDef)])
    if q == 15:
        ok = bool(definitions['normaliser_notice']) and call('strip') and call('lower')
        return [ok and _test_cases(top, 'normaliser_notice', [case], literals) for case in [('  LIVRE  ',), ('',), ('  Deux  MOTS !  ',)]]
    if q == 16:
        ok = bool(definitions['compter_elements']) and loop_count
        return [ok and _test_cases(top, 'compter_elements', [case], literals) for case in [(['livre', 'récit', 'livre'],), ([],), (['Livre', 'livre'],)]]
    if q == 17:
        word = bool(definitions['traduire_etiquette']) and call('normaliser_notice') and (has(ast.If) or has(ast.IfExp) or call('get'))
        sentence = bool(definitions['traduire_annonce']) and word and call('split') and call('join') and call('traduire_etiquette') and (has(ast.For) or has(ast.ListComp))
        lexicon = {'book': 'livre', 'story': 'récit'}
        cases = [('traduire_etiquette', (' BOOK ', lexicon), word),
                 ('traduire_etiquette', (' MAP ', lexicon), word),
                 ('traduire_annonce', ('BOOK story MAP', lexicon), sentence),
                 ('traduire_annonce', ('', lexicon), sentence),
                 ('traduire_etiquette', ('BOOK', {'book': 'ouvrage'}), word)]
        return [valid and _test_cases(top, name, [args], literals) for name, args, valid in cases]
    ok = bool(definitions['bilan_notice']) and call('normaliser_notice') and call('compter_elements') and call('split') and call('len')
    return [ok and _test_cases(top, 'bilan_notice', [case], literals) for case in [('  LIVRE récit livre  ',), ('',), ('Livre livre, LIVRE',)]]


def _fraction(actual, expected):
    # Independent keys in a structured answer earn independent credit.
    if isinstance(expected, dict) and expected and isinstance(actual, dict):
        if actual.keys() - expected.keys():
            return 0.0
        return sum(_fraction(actual.get(key), value) for key, value in expected.items()) / len(expected)
    return float(_same(actual, expected))


def _identification(index):
    cell = index.get(('identity', 'identification'))
    if not cell or cell.get('cell_type') != 'code':
        raise ValueError('Cellule d’identification absente.')
    info = {}
    for statement in ast.parse(_text(cell.get('source', ''))).body:
        if isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Constant):
            for target in statement.targets:
                if isinstance(target, ast.Name) and target.id in {'nom', 'prenom', 'classe', 'numero_etudiant'}:
                    value = statement.value.value
                    if isinstance(value, str):
                        info[target.id] = value.strip()
    if any(not info.get(key) or info[key] in {'...', 'À compléter', 'NON_RENSEIGNE'}
           for key in ('nom', 'prenom', 'classe', 'numero_etudiant')):
        raise ValueError('Nom, prénom, classe et numéro étudiant sont obligatoires.')
    return info


def check_notebook(content_str, filename):
    try:
        notebook = json.loads(content_str, object_pairs_hook=_unique)
        resolve_notebook(notebook, expected_evaluator=EVAL_ID)
        index = validate_cell_metadata(notebook)
        info = _identification(index)
    except (ValueError, TypeError, KeyError, SyntaxError, RecursionError) as exc:
        return 0.0, [], MAX_SCORE_TOTAL, {}, 'Notebook/identification invalide : ' + str(exc)
    literals = {}
    for cell in notebook['cells']:
        if cell.get('cell_type') == 'code':
            try:
                for statement in ast.parse(_text(cell.get('source', ''))).body:
                    if isinstance(statement, ast.Assign):
                        for target in statement.targets:
                            if isinstance(target, ast.Name):
                                try:
                                    literals[target.id] = ast.literal_eval(statement.value)
                                except (ValueError, TypeError):
                                    literals.pop(target.id, None)
            except (SyntaxError, ValueError, TypeError, RecursionError):
                pass
    details, score = [], 0.0
    for q, expected in enumerate(EXPECTED, 1):
        weight = 1.0 if q <= 14 else 1.5
        points, raw, evidence = 0.0, 'Trace absente, invalide ou ambiguë.', []
        cell = index.get((f'Q{q}', 'answer'))
        try:
            answer = _read_answer(cell, q)
            if answer:
                value, nodes, tree, raw = answer
                evidence = _evidence(q, nodes, tree, literals)
                if isinstance(value, list) and len(value) <= len(expected):
                    parts = [(_fraction(value[i], expected[i]) if i < len(value) and evidence[i] else 0.0)
                             for i in range(len(expected))]
                    points = weight * sum(parts) / len(expected)
        except (ValueError, TypeError, SyntaxError, KeyError, IndexError, OverflowError, RecursionError):
            pass
        score += points
        details.append({'check': f'Q{q} — {LABELS[q - 1]}', 'student_answer': raw[:3000],
                        'correct_answer': 'Sorties de référence et indices AST des opérations demandées ; '
                                          'points partiels par résultat. Raisonnement à relire. '
                                          + ('Critères AST : ' + ', '.join('oui' if x else 'non' for x in evidence) if evidence else ''),
                        'points': round(points, 3), 'max_points': weight,
                        'status': '✅' if math.isclose(points, weight) else ('◐' if points else '❌')})
        if q in (2, 6, 12, 14, 17):
            try:
                source = _text(cell.get('source', '')) if cell else ''
                # Verbatim code/comments, escaped by the private template, avoid keyword grading.
                comments = '\n'.join(line for line in source.splitlines() if line.lstrip().startswith('#'))
                if q == 14:
                    comments += '\nEssais complémentaires et algorithme à examiner :\n' + source
                    if cell:
                        comments += '\nSorties enregistrées :\n' + '\n'.join(_text(out.get('text', '')) for out in cell.get('outputs', [])
                                                                           if isinstance(out, dict) and out.get('output_type') == 'stream')
            except (ValueError, TypeError):
                comments = 'Commentaires ou sorties mal formés ; consulter la copie.'
            details.append({'check': f'Q{q} — Relecture ciblée', 'student_answer': comments[:12000] or 'Explication absente.',
                            'correct_answer': 'Apprécier le raisonnement ; aucun point automatique pour la présence d’un commentaire.',
                            'points': 0, 'max_points': 0, 'status': 'À relire'})
    score = round(score, 3)
    info.update(score_brut=score, score_nature='technique_provisoire', relecture_humaine='requise', score_max=MAX_SCORE_TOTAL)
    return score, details, MAX_SCORE_TOTAL, info, None
