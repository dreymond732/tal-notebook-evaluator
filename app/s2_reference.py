"""Trusted S2 references and question-linked inert evidence checks.

No submitted program is evaluated or executed. A matching saved trace documents
one course case, not all possible inputs or the authenticity of the output.
"""
import ast
import math
import posixpath
from s1_revision import literal, same

REFERENCES = {2: {'Q1': 'nohtyP',
     'Q2': 'chat-chien-souris',
     'Q3': '3.14',
     'Q4': [1, 4, 9, 16],
     'Q5': 4,
     'Q6': {'Français': 'FR', 'Anglais': 'EN'},
     'Q7': 50,
     'Q8': ['Alice', 'Charlie'],
     'Q9': {'b': 2, 'a': 2},
     'Q10': [1, 2, 3, 4, 5, 6],
     'Q11': [0, 1, 1, 2, 3, 5, 8],
     'Q12': True,
     'Q13': [12, 20]},
 3: {'Q1': 300.0,
     'Q2': {'deb': 13, 'fin': 19},
     'Q3': True,
     'Q4': 'python tal',
     'Q5': 2,
     'Q6': ['tal', 'spacy', 'nlp'],
     'Q7': 3,
     'Q8': [0, 4, 16, 36, 64],
     'Q9': {'tal': 2, 'est': 1, 'cool': 1, 'python': 1},
     'Q10': [3, 2, 1],
     'Q11': 'tal',
     'Q12': 17,
     'Q13': [('annotation', 10), ('python', 6), ('tal', 3), ('nlp', 3)],
     'Q14': {'intersection': {3}, 'union': {1, 2, 3, 4}},
     'Q15': None,
     'Q16': 120,
     'Q17': {'max': 10, 'index': 1},
     'Q18': [('tal', 'est'), ('est', 'cool')],
     'Q19': {'a': 1, 'b': 2, 'c': 3},
     'Q20': [1, 2, 4, 5, 7, 8],
     'Q21': 1,
     'Q22': {'moyenne': 5.0, 'ecart_type': 2.0},
     'Q23': 4,
     'Q24': True,
     'Q25': 15,
     'Q26': {'tal': 3, 'python': 6, 'spacy': 5},
     'Q27': [9, 7],
     'Q28': ['tal', 'et', 'python'],
     'Q29': [('analyser', 'corpus'),
             ('analyser', 'termes'),
             ('analyser', 'tokens'),
             ('extraire', 'corpus'),
             ('extraire', 'termes'),
             ('extraire', 'tokens')],
     'Q30': 6},
 4: {'Q1': {'oiseau', 'chat', 'chien'},
     'Q2': {'chat', 'souris', 'chien'},
     'Q3': True,
     'Q4': {'data', 'code'},
     'Q5': {'data', 'python', 'code', 'algo'},
     'Q6': {'pomme', 'poire'},
     'Q7': {'windows', 'linux'},
     'Q8': True,
     'Q9': True,
     'Q10': {'tag1', 'tag3', 'tag2'},
     'Q11': {'est', 'le'},
     'Q12': {'Jean', 'Paul'},
     'Q13': 0.5,
     'Q14': True},
 5: {'Q1': [0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400],
     'Q2': ['arbre', 'ecole', 'igloo', 'orange'],
     'Q3': {'le': 2, 'traitement': 10, 'automatique': 11, 'du': 2, 'langage': 7, 'est': 3, 'passionnant': 11},
     'Q4': 'passionnant est langage du automatique traitement le',
     'Q5': {'nom': 'Dupont', 'prenom': 'Jean', 'age': 25},
     'Q6': True,
     'Q7': True,
     'Q8': 2,
     'Q9': 'TADL',
     'Q10': 'bcd',
     'Q11': [1, 2, 3, 4, 5, 6],
     'Q12': {'a': 10, 'b': 25, 'c': 40, 'd': 40},
     'Q13': {'Maths': ['Alice', 'Bob'], 'Physique': ['Charlie']},
     'Q14': [('Bob', 15), ('Alice', 12), ('Charlie', 10)],
     'Q15': 2,
     'Q16': ['bonjour', 'comment', 'ça', 'va'],
     'Q17': ['chat', 'noir', 'chien', 'dort'],
     'Q18': [('je', 'suis'), ('suis', 'content')],
     'Q19': [('un', 'deux', 'trois'), ('deux', 'trois', 'quatre')],
     'Q20': 0.5,
     'Q21': 0.5,
     'Q22': 32,
     'Q23': 'progr',
     'Q24': {'chat': 1, 'chien': 1},
     'Q25': ['python', 'est', 'super']},
 6: {'Q1': 'Le chat, mange la souris.\n'
           'Le chien; aboie fort!!\n'
           "L'oiseau vole... dans le ciel.\n"
           'La souris (petite) court vite.\n'
           'CHAT et chien sont des amis?\n'
           '123 souris mangent 456 graines.',
     'Q2': ['Le chat, mange la souris.\n',
            'Le chien; aboie fort!!\n',
            "L'oiseau vole... dans le ciel.\n",
            'La souris (petite) court vite.\n',
            'CHAT et chien sont des amis?\n',
            '123 souris mangent 456 graines.'],
     'Q3': 'le chien  aboie fort  ',
     'Q4': ['le', 'chien', 'aboie', 'fort'],
     'Q5': ['souris', 'mangent', 'graines'],
     'Q6': ['chat', 'souris'],
     'Q7': ['chat',
            'mange',
            'souris',
            'chien',
            'aboie',
            'fort',
            'oiseau',
            'vole',
            'ciel',
            'souris',
            'petite',
            'court',
            'vite',
            'chat',
            'chien',
            'amis',
            'souris',
            'mangent',
            'graines'],
     'Q8': {'chat': 2,
            'mange': 1,
            'souris': 3,
            'chien': 2,
            'aboie': 1,
            'fort': 1,
            'oiseau': 1,
            'vole': 1,
            'ciel': 1,
            'petite': 1,
            'court': 1,
            'vite': 1,
            'amis': 1,
            'mangent': 1,
            'graines': 1},
     'Q9': ['Mot;Frequence', 'chat;2', 'mange;1'],
     'Q10': [('souris', 3),
             ('chat', 2),
             ('chien', 2),
             ('mange', 1),
             ('aboie', 1),
             ('fort', 1),
             ('oiseau', 1),
             ('vole', 1),
             ('ciel', 1),
             ('petite', 1),
             ('court', 1),
             ('vite', 1),
             ('amis', 1),
             ('mangent', 1),
             ('graines', 1)]},
 'dm': {'Q1': 'bon',
        'Q2': [1, 2, 3, 4],
        'Q3': 3,
        'Q4': 20,
        'Q5': {'nom': 'A', 'age': 20, 'ville': 'Paris'},
        'Q6': 6,
        'Q7': 'TEST',
        'Q8': 'mon chien',
        'Q9': 5,
        'Q10': {1, 2},
        'Q11': True,
        'Q12': ['a', 'b', 'c'],
        'Q13': [1, 2],
        'Q14': 5,
        'Q15': 9,
        'Q16': 42,
        'Q17': 3.14,
        'Q18': True,
        'Q19': ['a'],
        'Q20': [1],
        'Q21': [1, 4, 9, 16, 25],
        'Q22': {1: 1, 2: 4, 3: 9},
        'Q23': [2, 4],
        'Q24': [1, 2, 3, 4],
        'Q25': {'a': 2, 'b': 1, 'c': 1},
        'Q26': {'a': 1, 'b': 2},
        'Q27': {1: 'a', 2: 'b'},
        'Q28': [[1, 3], [2, 4]],
        'Q29': [2, 3],
        'Q30': 120}}

WEIGHTS = {2: {'Q1': 1.0,
     'Q2': 1.0,
     'Q3': 1.0,
     'Q4': 1.0,
     'Q5': 1.0,
     'Q6': 1.0,
     'Q7': 1.0,
     'Q8': 2.0,
     'Q9': 2.0,
     'Q10': 2.0,
     'Q11': 2.0,
     'Q12': 2.0,
     'Q13': 3.0},
 3: {'Q1': 1.0,
     'Q2': 1.0,
     'Q3': 1.0,
     'Q4': 1.0,
     'Q5': 1.0,
     'Q6': 1.0,
     'Q7': 1.0,
     'Q8': 1.0,
     'Q9': 1.0,
     'Q10': 1.0,
     'Q11': 1.0,
     'Q12': 1.0,
     'Q13': 1.0,
     'Q14': 1.0,
     'Q15': 1.0,
     'Q16': 1.0,
     'Q17': 1.0,
     'Q18': 1.0,
     'Q19': 1.0,
     'Q20': 1.0,
     'Q21': 1.0,
     'Q22': 1.0,
     'Q23': 1.0,
     'Q24': 1.0,
     'Q25': 1.0,
     'Q26': 1.0,
     'Q27': 1.0,
     'Q28': 1.0,
     'Q29': 1.0,
     'Q30': 1.0},
 4: {'Q1': 2.0,
     'Q2': 2.0,
     'Q3': 2.0,
     'Q4': 3.0,
     'Q5': 3.0,
     'Q6': 3.0,
     'Q7': 3.0,
     'Q8': 2.0,
     'Q9': 3.0,
     'Q10': 3.0,
     'Q11': 3.0,
     'Q12': 3.0,
     'Q13': 4.0,
     'Q14': 4.0},
 5: {'Q1': 1.0,
     'Q2': 1.0,
     'Q3': 1.0,
     'Q4': 1.0,
     'Q5': 1.0,
     'Q6': 1.0,
     'Q7': 1.0,
     'Q8': 1.0,
     'Q9': 1.0,
     'Q10': 1.0,
     'Q11': 1.0,
     'Q12': 1.0,
     'Q13': 1.0,
     'Q14': 1.0,
     'Q15': 1.0,
     'Q16': 1.0,
     'Q17': 1.0,
     'Q18': 1.0,
     'Q19': 1.0,
     'Q20': 1.0,
     'Q21': 1.0,
     'Q22': 1.0,
     'Q23': 1.0,
     'Q24': 1.0,
     'Q25': 1.0},
 6: {'Q1': 1.0,
     'Q2': 1.0,
     'Q3': 2.0,
     'Q4': 2.0,
     'Q5': 2.0,
     'Q6': 2.0,
     'Q7': 3.0,
     'Q8': 3.0,
     'Q9': 2.0,
     'Q10': 2.0},
 'dm': {'Q1': 1.0,
        'Q2': 1.0,
        'Q3': 1.0,
        'Q4': 1.0,
        'Q5': 1.0,
        'Q6': 1.0,
        'Q7': 1.0,
        'Q8': 1.0,
        'Q9': 1.0,
        'Q10': 1.0,
        'Q11': 1.0,
        'Q12': 1.0,
        'Q13': 1.0,
        'Q14': 1.0,
        'Q15': 1.0,
        'Q16': 1.0,
        'Q17': 1.0,
        'Q18': 1.0,
        'Q19': 1.0,
        'Q20': 1.0,
        'Q21': 2.0,
        'Q22': 2.0,
        'Q23': 2.0,
        'Q24': 2.0,
        'Q25': 2.0,
        'Q26': 2.0,
        'Q27': 2.0,
        'Q28': 2.0,
        'Q29': 2.0,
        'Q30': 2.0}}

# References corrected against the notebook data and approved coverage matrix.


def nodes(proofs):
    return tuple(node for proof in proofs.values() for node in proof.nodes)


def has(proofs, kind):
    return any(isinstance(node, kind) for node in nodes(proofs))


def calls(proofs, name):
    return any(proof.calls(name) for proof in proofs.values())


def construct(*kinds, names=(), any_names=()):
    return lambda proofs, context: (all(has(proofs, kind) for kind in kinds)
        and all(calls(proofs, name) for name in names)
        and (not any_names or any(calls(proofs, name) for name in any_names)))


def computed(proofs, context):
    """Literal answers alone cannot attest an algorithm; MCQs are exempted."""
    return any(isinstance(node, ast.Assign) and any(isinstance(t, ast.Subscript) for t in node.targets) for node in nodes(proofs)) or any(has(proofs, kind) for kind in (ast.Call, ast.Subscript, ast.BinOp,
        ast.Compare, ast.BoolOp, ast.ListComp, ast.DictComp, ast.SetComp,
        ast.For, ast.While, ast.AugAssign))


def set_construct(proofs, context):
    return calls(proofs, 'set') or has(proofs, ast.SetComp)


def operation(kind, method):
    return lambda proofs, context: has(proofs, kind) or calls(proofs, method)


def function(name):
    return construct(ast.FunctionDef, ast.Return, names=(name,))


def loops(proofs, context):
    return has(proofs, ast.For) or has(proofs, ast.While)


def nested_loops(proofs, context):
    return any(isinstance(node, ast.For) and any(isinstance(child, ast.For)
        for statement in node.body for child in ast.walk(statement)) for node in nodes(proofs))


def no_membership(proofs, context):
    return function('contient_liste')(proofs, context) and has(proofs, ast.For) and not has(proofs, (ast.In, ast.NotIn))


def read_file(proofs, context):
    return calls(proofs, 'open') and (calls(proofs, 'read') or calls(proofs, 'readlines') or calls(proofs, 'list'))


def file_roundtrip(expected_path):
    def compare(proofs, context):
        # The shared dependency graph retains earlier writes. They cannot stand
        # in for writing the second CSV: require this question's destination.
        destinations = []
        for proof in proofs.values():
            for node in proof.nodes:
                if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id == 'open'):
                    continue
                keywords = {item.arg:item.value for item in node.keywords}
                path = node.args[0] if node.args else keywords.get('file')
                mode = node.args[1] if len(node.args)>1 else keywords.get('mode')
                def known(expr):
                    if isinstance(expr, ast.Constant):
                        return expr.value
                    if isinstance(expr, ast.Name):
                        return proof.literal(expr.id)
                    return None
                if known(mode) in {'w', 'wt', 'w+', 'w+t', 'wt+', 'a', 'at', 'a+'}:
                    filename = known(path)
                    if isinstance(filename, str):
                        destinations.append(posixpath.normpath(filename.replace('\\', '/')))
        return (expected_path in destinations and calls(proofs, 'open')
                and any(calls(proofs, name) for name in ('read', 'readlines', 'readline'))
                and any(calls(proofs, name) for name in ('write', 'writelines', 'writerow', 'writerows')))
    return compare


def slice_indices(raw, proof, context):
    value = literal(raw)
    return (proof.argc == 1 and type(value) is dict and set(value) == {'deb', 'fin'}
        and all(type(index) is int for index in value.values())
        and "initiation à python pour le tal"[value['deb']:value['fin']] == 'python')


def interval_condition(proofs, context):
    """Recognise the requested interval and equivalent Boolean spellings.

    This checks the syntax of bounds, never evaluates submitted expressions.
    In particular the original `>= 10 or < 16` is not a bounded interval.
    """
    inverse = {ast.Lt: ast.GtE, ast.LtE: ast.Gt, ast.Gt: ast.LtE, ast.GtE: ast.Lt}
    reverse = {ast.Lt: ast.Gt, ast.LtE: ast.GtE, ast.Gt: ast.Lt, ast.GtE: ast.LtE}

    def bounds(expr, negate=False):
        if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.Not):
            return bounds(expr.operand, not negate)
        if isinstance(expr, ast.BoolOp) and ((isinstance(expr.op, ast.And) and not negate)
                or (isinstance(expr.op, ast.Or) and negate)):
            parts = [bounds(value, negate) for value in expr.values]
            if all(part is not None for part in parts):
                return set().union(*parts)
            return None
        if not isinstance(expr, ast.Compare) or (negate and len(expr.ops) != 1):
            return None
        found = set()
        for left, op, right in zip([expr.left, *expr.comparators[:-1]], expr.ops, expr.comparators):
            kind = type(op)
            if isinstance(left, ast.Constant) and isinstance(right, ast.Name):
                left, right = right, left
                kind = reverse.get(kind)
            if not (isinstance(left, ast.Name) and left.id == 'note'
                    and isinstance(right, ast.Constant) and type(right.value) in (int, float)):
                return None
            if negate:
                kind = inverse.get(kind)
            if kind is ast.GtE and right.value == 10:
                found.add('lower')
            elif kind is ast.Lt and right.value == 16:
                found.add('upper')
            else:
                return None
        return found

    for node in nodes(proofs):
        if bounds(node) == {'lower', 'upper'}:
            return True
        if isinstance(node, ast.If):
            # Equivalent exclusion with explicit False/True branches.
            if len(node.body) == len(node.orelse) == 1:
                a, b = node.body[0], node.orelse[0]
                if (isinstance(a, ast.Assign) and isinstance(b, ast.Assign)
                        and len(a.targets) == len(b.targets) == 1
                        and isinstance(a.targets[0], ast.Name) and isinstance(b.targets[0], ast.Name)
                        and a.targets[0].id == b.targets[0].id
                        and isinstance(a.value, ast.Constant) and a.value.value is False
                        and isinstance(b.value, ast.Constant) and b.value.value is True
                        and bounds(node.test, True) == {'lower', 'upper'}):
                    return True
    return False


def default_parameter(proofs, context):
    return function('addition')(proofs, context) and any(
        isinstance(node, ast.FunctionDef) and node.name == 'addition'
        and any(isinstance(default, ast.Constant) and type(default.value) is int and default.value == 10
                for default in node.args.defaults) for node in nodes(proofs))


def recursive_sum(proofs, context):
    if not function('somme_n')(proofs, context):
        return False
    return any(isinstance(fn, ast.FunctionDef) and fn.name == 'somme_n'
        and any(isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            and call.func.id == 'somme_n' and fn.lineno < call.lineno <= fn.end_lineno
            for call in nodes(proofs)) for fn in nodes(proofs))


def division_handler(proofs, context):
    return has(proofs, ast.Div) and any(isinstance(node, ast.Try)
        and any(handler.type is None or (isinstance(handler.type, ast.Name)
            and handler.type.id in {'ZeroDivisionError', 'ArithmeticError', 'Exception'})
            for handler in node.handlers) for node in nodes(proofs))


def numeric_price(raw, proof, context):
    if proof.argc not in (1, 2):
        return False
    # The historical display includes a euro unit; both preserved and normalized
    # prints are accepted, without searching for any number elsewhere in text.
    value = literal(raw[:-2] if raw.endswith(' €') else raw)
    return type(value) in (int, float) and math.isfinite(value) and abs(value - 300) < 1e-9


def represented(expected):
    def compare(raw, proof, context):
        return proof.argc == 1 and same(literal(raw), expected)
    return compare


def list_without_order(expected):
    def compare(raw, proof, context):
        value = literal(raw)
        return (proof.argc == 1 and type(value) is list and len(value) == len(expected)
                and all(any(same(item, ref) for ref in expected) for item in value)
                and all(sum(same(item, ref) for item in value) == 1 for ref in expected))
    return compare


def length_order(raw, proof, context):
    value = literal(raw)
    expected = REFERENCES[3]['Q13']
    return (list_without_order(expected)(raw, proof, context)
            and all(value[i][1] >= value[i + 1][1] for i in range(len(value) - 1)))


def grouped_students(raw, proof, context):
    value = literal(raw)
    return (proof.argc == 1 and type(value) is dict and set(value) == {'Maths', 'Physique'}
        and type(value['Maths']) is list and sorted(value['Maths']) == ['Alice', 'Bob']
        and type(value['Physique']) is list and value['Physique'] == ['Charlie'])


def common_elements(raw, proof, context):
    value = literal(raw)
    return (proof.argc == 1 and type(value) in (list, tuple, set) and len(value) == 2
        and all(type(item) is int for item in value) and set(value) == {2, 3})


def csv_records(raw, proof, context):
    lines = literal(raw)
    expected = REFERENCES[6]['Q8']
    if proof.argc != 1 or type(lines) is not list or len(lines) != len(expected) + 1:
        return False
    if lines[0] != 'Mot;Frequence' or any(type(line) is not str for line in lines):
        return False
    observed = {}
    for line in lines[1:]:
        parts = line.split(';')
        if len(parts) != 2 or parts[0] in observed or not parts[1].isdigit():
            return False
        observed[parts[0]] = int(parts[1])
    return same(observed, expected)


def csv_preview(raw, proof, context):
    if 'Q9b' not in context:
        return False
    value = literal(raw)
    complete = literal(context['Q9b']['raw'])
    return proof.argc == 1 and type(value) is list and same(value, complete[:3])


def frequency_order(raw, proof, context):
    value = literal(raw)
    expected = list(REFERENCES[6]['Q8'].items())
    return (list_without_order(expected)(raw, proof, context)
            and all(value[i][1] >= value[i + 1][1] for i in range(len(value) - 1)))


SYNTAX = {
    2: {
        1: construct(ast.Slice), 2: construct(names=('join',)),
        3: construct(ast.JoinedStr, ast.FormattedValue), 4: construct(ast.ListComp),
        5: set_construct,
        6: lambda p, c: calls(p, 'zip') or has(p, ast.For),
        10: lambda p, c: nested_loops(p,c) or any(isinstance(n, ast.ListComp) and len(n.generators)>1 for n in nodes(p)),
        11: loops, 12: function('est_anagramme'), 13: construct(ast.ListComp),
    },
    3: {
        2: None, 3: interval_condition, 5: None, 6: construct(names=('insert', 'pop')),
        7: construct(ast.For, names=('enumerate',)),
        8: construct(ast.ListComp), 10: construct(ast.While),
        11: function('normaliser_token'), 12: default_parameter,
        15: division_handler,
        16: construct(ast.For), 18: construct(ast.For), 19: construct(names=('zip',)),
        20: construct(ast.ListComp), 21: None, 23: None,
        24: no_membership, 25: recursive_sum, 26: construct(ast.DictComp),
        29: nested_loops, 30: construct(ast.While),
    },
    4: {
        1: set_construct, 4: operation(ast.BitAnd, 'intersection'),
        5: operation(ast.BitOr, 'union'), 6: operation(ast.Sub, 'difference'),
        7: operation(ast.BitXor, 'symmetric_difference'),
        8: lambda p,c: operation(ast.LtE, 'issubset')(p,c) or has(p,ast.GtE),
        9: set_construct, 10: set_construct,
        11: operation(ast.BitAnd, 'intersection'), 12: operation(ast.Sub, 'difference'),
        14: lambda p,c: operation(ast.GtE, 'issuperset')(p,c) or has(p,ast.LtE) or calls(p,'issubset'),
    },
    5: {1: construct(ast.ListComp), 2: construct(ast.ListComp)},
    6: {
        1: lambda p,c: read_file(p,c) and has(p,ast.With),
        2: read_file, 3: function('nettoyer_ligne'),
        8: lambda p,c: computed(p,c) and not calls(p,'Counter'),
        9: file_roundtrip('lexique.csv'), 10: file_roundtrip('lexique_trie.csv'),
    },
    'dm': {
        21: construct(ast.ListComp), 22: construct(ast.DictComp),
        23: construct(ast.ListComp), 24: nested_loops,
        26: construct(names=('zip',)), 30: loops,
    },
}

SPECIAL_VALUES = {
    (3, 1): numeric_price, (3, 2): slice_indices, (3, 13): length_order,
    (5, 13): grouped_students,
    (6, 1): represented(REFERENCES[6]['Q1']),
    (6, 9): csv_preview, (6, 10): frequency_order,
    ('dm', 29): common_elements,
}

CHECKS = {}
for course, answers in REFERENCES.items():
    checks = []
    for marker, expected in answers.items():
        number = int(marker[1:])
        traces = {marker: SPECIAL_VALUES.get((course, number), (expected,))}
        if (course, number) == (6, 9):
            traces['Q9b'] = csv_records
        if (course, number) == (6, 10):
            traces['Q10b'] = ('Mot;Frequence',)
        checks.append({'label': f'Exercice {number}', 'points': WEIGHTS[course][marker],
            'traces': traces, 'syntax': SYNTAX.get(course, {}).get(number, computed),
            'feedback': 'Vérifiez les données, le type, le traitement demandé et les traces de cette question.'})
    CHECKS[course] = checks
