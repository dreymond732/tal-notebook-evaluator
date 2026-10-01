"""Versioned R0/R1/R2 formative checks, without running uploaded Python.

Only explicitly tagged answer cells and their declared prerequisites contribute.
The score checks source structure and saved traces, not execution authenticity.
"""
import ast
import json

from notebook_contract import (ContractError, WRONG_VERSION, resolve_notebook,
                               validate_cell_metadata, s3_contract_identity)

TEXT_R0 = 'Python est utile. Python sert au TAL et le TAL sert à analyser des textes.'
# These tables are reference annotations for the pinned fr_core_news_sm 3.8.0 model.
R1_TOKENS = [('Les', 'le', 'DET'), ('traducteurs', 'traducteur', 'NOUN'),
             ('analysent', 'analyser', 'ADV'), ('rapidement', 'rapidement', 'ADV'),
             ('les', 'le', 'DET'), ('nouveaux', 'nouveau', 'ADJ'),
             ('documents', 'document', 'NOUN'), ('.', '.', 'PUNCT')]
R2_TOKENS = [('Les', 'le', 'DET'), ('corpus', 'corpus', 'PRON'),
             ('contiennent', 'contenir', 'VERB'), ('des', 'de', 'ADP'),
             ('textes', 'texte', 'NOUN'), ('.', '.', 'PUNCT'), ('Les', 'le', 'DET'),
             ('textes', 'texte', 'NOUN'), ('contiennent', 'contenir', 'VERB'),
             ('des', 'de', 'ADP'), ('termes', 'terme', 'NOUN'), ('et', 'et', 'CCONJ'),
             ('des', 'un', 'DET'), ('répétitions', 'répétition', 'NOUN'), ('.', '.', 'PUNCT')]


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(part, str) for part in value):
        return ''.join(value)
    raise ValueError('Texte de cellule ou de sortie invalide.')


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Clé JSON dupliquée.')
        result[key] = value
    return result


def _tree(cell):
    if cell.get('cell_type') != 'code':
        raise ValueError('Une réponse doit être une cellule de code.')
    source = _text(cell.get('source', ''))
    if len(source) > 100000:
        raise ValueError('Réponse trop volumineuse.')
    return ast.parse(source)


def _literal(source):
    if len(source) > 30000:
        raise ValueError('Sortie trop volumineuse.')
    tree = ast.parse(source, mode='eval')
    if sum(1 for _ in ast.walk(tree)) > 5000:
        raise ValueError('Sortie trop complexe.')
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [ast.literal_eval(key) for key in node.keys]
            if len(keys) != len(set(keys)):
                raise ValueError('Clé de résultat dupliquée.')
    return ast.literal_eval(tree)


def _trace(cell, number):
    outputs = cell.get('outputs', [])
    if not isinstance(outputs, list):
        raise ValueError('Sorties invalides.')
    chunks = []
    for output in outputs:
        if not isinstance(output, dict):
            raise ValueError('Sortie invalide.')
        if output.get('output_type') == 'error':
            raise ValueError('La cellule contient une erreur enregistrée.')
        if output.get('output_type') == 'stream' and output.get('name', 'stdout') == 'stdout':
            chunks.append(_text(output.get('text', '')))
    prefix = f'Résultat Q{number} :'
    rows = [line[len(prefix):].strip() for line in ''.join(chunks).splitlines()
            if line.startswith(prefix)]
    if len(rows) != 1:
        raise ValueError('Une seule sortie marquée est attendue dans cette réponse.')
    return _literal(rows[0])


def _equal(actual, expected):
    # bool is an int subclass: exact numeric types are deliberate here.
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and actual.keys() == expected.keys()
                and all(_equal(actual[k], v) for k, v in expected.items()))
    if isinstance(expected, (tuple, list)):
        return (isinstance(actual, (tuple, list)) and len(actual) == len(expected)
                and all(_equal(a, b) for a, b in zip(actual, expected)))
    return type(actual) is type(expected) and actual == expected


def _names(tree):
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}


def _has_call(tree, name):
    return any(isinstance(n, ast.Call) and
               ((isinstance(n.func, ast.Name) and n.func.id == name) or
                (isinstance(n.func, ast.Attribute) and n.func.attr == name))
               for n in ast.walk(tree))


def _attrs(tree):
    return {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}


def _strings(tree):
    return {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant)
            and isinstance(n.value, str)}


def _function(tree, name, params):
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(functions) != 1:
        return None
    function = _return_slice(functions[0])
    actual = [a.arg for a in function.args.args]
    if len(actual) != len(params) or actual[1:] != params[1:]:
        return None
    if not any(isinstance(n, ast.Return) and n.value is not None for n in ast.walk(function)):
        return None
    # A parameter appearing only in the signature is not a computed answer.
    if not set(actual[:1]) <= _names(function):
        return None
    return function


def _loads(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}


def _writes(statement):
    result = {n.id for n in ast.walk(statement) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    for node in ast.walk(statement):
        if isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Store):
            result |= _names(node.value)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {'append', 'extend', 'update', 'add'}:
            result |= _names(node.func.value)
    if isinstance(statement, ast.FunctionDef):
        result = {statement.name}
    return result


def _slice(statements, required):
    """Conservative backward data slice, never an evaluator/interpreter."""
    selected, required = [], set(required)
    for statement in reversed(statements):
        writes = _writes(statement)
        if not writes & required:
            continue
        if isinstance(statement, ast.FunctionDef):
            statement = _return_slice(statement)
        selected.append(statement)
        if isinstance(statement, (ast.Assign, ast.AnnAssign, ast.FunctionDef)):
            required -= writes
        required |= _loads(statement)
    return list(reversed(selected))


def _return_slice(function):
    # A normal top-level return is the teaching contract. Nested returns remain
    # inspectable, with their conditionals, rather than being executed here.
    returns = [n for n in function.body if isinstance(n, ast.Return)]
    if not returns:
        return function
    ret = returns[-1]
    prefix = function.body[:function.body.index(ret)]
    body = _slice(prefix, _loads(ret)) + [ret]
    return ast.FunctionDef(name=function.name, args=function.args, body=body,
                           decorator_list=[], returns=function.returns, type_comment=None)


def _printed_tree(tree, number):
    """Keep the marked print and preceding definitions used to compute it."""
    marker = f'Résultat Q{number} :'
    prints = [n for n in tree.body if isinstance(n, ast.Expr)
              and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
              and n.value.func.id == 'print' and n.value.args
              and isinstance(n.value.args[0], ast.Constant) and n.value.args[0].value == marker]
    if len(prints) != 1 or len(prints[0].value.args) != 2:
        raise ValueError('Affichez le marqueur et la valeur calculée avec print.')
    expression = prints[0].value.args[1]
    names = _loads(expression)
    if not names:
        raise ValueError('La sortie doit provenir du calcul demandé, pas d’un littéral recopié.')
    prefix = tree.body[:tree.body.index(prints[0])]
    return ast.Module(body=_slice(prefix, names) + [prints[0]], type_ignores=[])


def _freq(words):
    result = {}
    for word in words:
        result[word] = result.get(word, 0) + 1
    return result


def _noun_freq(tokens):
    return _freq(lemma for _, lemma, pos in tokens if pos == 'NOUN')


def _tokens_shape(tree):
    return {'text', 'lemma_', 'pos_'} <= _attrs(tree) and any(
        isinstance(n, (ast.For, ast.comprehension)) for n in ast.walk(tree))


def _lemma_reference(node, function):
    if 'lemma_' in _attrs(node):
        return True
    aliases = {target.id for assignment in ast.walk(function) if isinstance(assignment, ast.Assign)
               and 'lemma_' in _attrs(assignment.value)
               for target in assignment.targets if isinstance(target, ast.Name)}
    return bool(_names(node) & aliases)


def _noun_function(tree, filtered=False):
    fn = _function(tree, 'frequences_lemmas', ['texte', 'stopwords'])
    if fn is None or not fn.args.defaults or not isinstance(fn.args.defaults[-1], ast.Constant) or fn.args.defaults[-1].value is not None:
        return False
    ok = (_has_call(fn, 'nlp') and _has_call(fn, 'Counter')
          and {'lemma_', 'pos_'} <= _attrs(fn) and 'NOUN' in _strings(fn))
    if filtered:
        ok = ok and 'is_stop' in _attrs(fn) and 'stopwords' in _names(fn)
        ok = ok and any(isinstance(n, ast.Compare) and any(isinstance(op, ast.NotIn) for op in n.ops)
                       and 'stopwords' in _names(n) and _lemma_reference(n.left, fn) for n in ast.walk(fn))
        ok = ok and any((isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not)
                        and 'is_stop' in _attrs(n)) or
                       (isinstance(n, ast.Compare) and 'is_stop' in _attrs(n)
                        and len(n.ops) == 1 and isinstance(n.ops[0], (ast.Eq, ast.Is))
                        and any(isinstance(v, ast.Constant) and v.value is False
                                for v in [n.left] + n.comparators)) for n in ast.walk(fn))
    return bool(ok)


def _check(r, q, tree, relevant, prior, value):
    """Return source and saved-result agreement for one pedagogical criterion."""
    if r == 0:
        if q == 1:
            fn = _function(relevant, 'compter_mots', ['texte'])
            return bool(fn and _has_call(fn, 'len') and _has_call(fn, 'split')
                        and _has_call(relevant, 'compter_mots')
                        and {'', 'Un essai'} <= _strings(relevant)
                        and _equal(value, {'principal': len(TEXT_R0.split()), 'vide': 0, 'essai': 2}))
        if q == 2:
            return (_has_call(relevant, 'lower') and _has_call(relevant, 'split')
                    and 'texte' in _names(relevant) and _equal(value, TEXT_R0.lower().split()))
        if q == 3:
            fn = _function(relevant, 'frequences', ['texte'])
            return bool(fn and _has_call(fn, 'get') and _has_call(fn, 'split')
                        and _has_call(fn, 'lower') and _has_call(relevant, 'frequences')
                        and 'Mot mot autre' in _strings(relevant)
                        and _equal(value, {'principal': _freq(TEXT_R0.lower().split()),
                                          'essai': {'mot': 2, 'autre': 1}}))
        if q == 4:
            return (3 in prior and _function(prior[3], 'frequences', ['texte']) is not None
                    and _has_call(relevant, 'frequences') and 'Python Python.' in _strings(relevant)
                    and isinstance(value, dict) and value.keys() == {'comptes', 'limite'}
                    and _equal(value['comptes'], {'python': 1, 'python.': 1})
                    and isinstance(value['limite'], str))
    if r == 1:
        if q == 1:
            return (_has_call(relevant, 'nlp') and _has_call(relevant, 'len')
                    and {'doc', 'texte'} <= _names(relevant) and _equal(value, len(R1_TOKENS)))
        if 1 not in prior or not _has_call(prior[1], 'nlp'):
            return False
        if q == 2:
            return _tokens_shape(relevant) and 'doc' in _names(relevant) and _equal(value, R1_TOKENS)
        target = 'NOUN' if q == 3 else 'VERB'
        return ({'lemma_', 'pos_'} <= _attrs(relevant) and 'doc' in _names(relevant)
                and target in _strings(relevant)
                and _equal(value, [lemma for _, lemma, pos in R1_TOKENS if pos == target]))
    if r == 2:
        expected = _noun_freq(R2_TOKENS)
        filtered = {k: v for k, v in expected.items() if k != 'texte'}
        if q == 1:
            return _noun_function(relevant) and _has_call(relevant, 'frequences_lemmas') and _equal(value, expected)
        if q == 2:
            return (1 in prior and _noun_function(prior[1]) and _tokens_shape(relevant)
                    and _equal(value, R2_TOKENS))
        if q == 3:
            return (_noun_function(relevant, filtered=True) and _has_call(relevant, 'frequences_lemmas')
                    and 'texte' in _strings(relevant)
                    and _equal(value, {'sans_exclusions': expected, 'avec_exclusions': filtered}))
        if q == 4:
            if 3 not in prior or not _noun_function(prior[3], filtered=True) or not _has_call(relevant, 'most_common') or not _has_call(relevant, 'frequences_lemmas'):
                return False
            if not isinstance(value, dict) or value.keys() != {'avant', 'apres'}:
                return False
            # Counter.most_common tie order is not itself a linguistic criterion.
            for key, target in [('avant', expected), ('apres', filtered)]:
                rows = value[key]
                if not isinstance(rows, (tuple, list)) or len(rows) != len(target):
                    return False
                if any(not isinstance(row, (tuple, list)) or len(row) != 2 or not isinstance(row[0], str)
                       or type(row[1]) is not int for row in rows):
                    return False
                if len({row[0] for row in rows}) != len(rows) or dict(rows) != target:
                    return False
                if [row[1] for row in rows] != sorted(target.values(), reverse=True):
                    return False
            return True
    return False


def check_revision(content_str, evaluator):
    maximum = 4.0
    try:
        notebook = json.loads(content_str, object_pairs_hook=_unique)
        resolve_notebook(notebook, expected_evaluator=evaluator, require_metadata=True)
        index = validate_cell_metadata(notebook)
        if any((f'Q{q}', 'answer') not in index for q in range(1, 5)):
            raise ContractError(WRONG_VERSION)
        info = s3_contract_identity(notebook, evaluator)
    except (ValueError, TypeError, SyntaxError, RecursionError) as exc:
        return 0.0, [], maximum, {}, str(exc)
    revision = int(evaluator[4])
    details, trees, score = [], {}, 0.0
    for q in range(1, 5):
        cell = index[(f'Q{q}', 'answer')]
        try:
            tree = _tree(cell)
            trees[q] = tree
            relevant = _printed_tree(tree, q)
            value = _trace(cell, q)
            ok = _check(revision, q, tree, relevant, trees, value)
            feedback = ('Structure du calcul et résultats enregistrés concordants.' if ok else
                        'Vérifiez le calcul demandé, ses essais et les valeurs affichées dans cette cellule.')
        except (ValueError, TypeError, SyntaxError, RecursionError, KeyError) as exc:
            ok, feedback = False, str(exc)
        score += float(ok)
        details.append({'check': f'Question {q}', 'student_answer': feedback,
                        'correct_answer': 'Concordance technique du code et des traces attendues.',
                        'status': '✅' if ok else '❌', 'points': float(ok), 'max_points': 1.0})
    if revision in {0, 1, 2}:
        try:
            observation = _text(index[('Q4', 'answer')].get('source', ''))
        except ValueError:
            observation = 'Source Q4 invalide.'
        details.append({'check': 'Observation Q4 — relecture', 'student_answer':
                        'Le point Q4 porte sur le calcul, pas sur la qualité de l’explication. '
                        'La pertinence linguistique de cette explication reste à relire.\n'
                        + observation, 
                        'correct_answer': '', 'status': 'ℹ️', 'points': 0, 'max_points': 0})
    info.update(score_brut=score, score_nature='technique_provisoire', score_max=maximum,
                contract_version=2, relecture_humaine='Interprétation et reproductibilité à relire.')
    return score, details, maximum, info, None
