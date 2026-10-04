"""S1 v2 : traces et dépendances syntaxiques inertes, jamais de code exécuté.

Une trace enregistrée n'est pas une preuve d'exécution fraîche ni d'auteur.
L'analyse relie les constructions demandées aux variables effectivement imprimées.
"""
import ast
import io
import math
import re
import tokenize
from dataclasses import dataclass

from notebook_contract import ContractError, strict_contract_identity, validate_cell_metadata
from s3_audit import read_notebook, text
from s3_review import review_evidence

MARKER = re.compile(r'^Résultat (Q[1-9][0-9]*[a-z]?)\s*:\s?(.*)$')
LIMIT_NOTE = ('Score technique provisoire sur les traces enregistrées. Le serveur ne lance pas votre code '
              'et ne certifie ni l’authenticité ni la fraîcheur des sorties. Réexécutez les cellules dans '
              'l’ordre. Les explications et interprétations restent à relire humainement.')


def same(value, expected):
    """Égalité récursive typée : bool est distinct de int, ensembles non ordonnés."""
    if type(value) is not type(expected):
        return False
    if isinstance(value, float):
        return math.isfinite(value) and math.isfinite(expected) and math.isclose(value, expected, rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(value, dict):
        return len(value) == len(expected) and all(any(same(k, ek) and same(v, ev) for ek, ev in expected.items()) for k, v in value.items())
    if isinstance(value, (set, frozenset)):
        return len(value) == len(expected) and all(any(same(v, ev) for ev in expected) for v in value)
    if isinstance(value, (list, tuple)):
        return len(value) == len(expected) and all(same(v, ev) for v, ev in zip(value, expected))
    return value == expected


def literal(raw):
    if len(raw) > 16000:
        raise ValueError('Trace littérale trop longue.')
    tree = ast.parse(raw, mode='eval')
    if sum(1 for _ in ast.walk(tree)) > 2000:
        raise ValueError('Trace littérale trop complexe.')
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [ast.literal_eval(key) for key in node.keys]
            if len(keys) != len(set(keys)):
                raise ValueError('Clé répétée dans une trace littérale.')
    return ast.literal_eval(tree)


def matches(raw, expected):
    """Compare les arguments d'un print, sans exécuter d'expression soumise."""
    if len(raw) > 16000 or not isinstance(expected, tuple):
        return False
    # Les chaînes sont imprimées sans quotes : les longueurs attendues lèvent
    # leur ambiguïté. Pour les conteneurs, le tokenizer délimite le littéral.
    rest = raw
    for i, wanted in enumerate(expected):
        if isinstance(wanted, str):
            piece = wanted
            if not rest.startswith(piece):
                return False
        else:
            piece = None
            try:
                tokens = list(tokenize.generate_tokens(io.StringIO(rest).readline))
                depth = 0
                for token in tokens:
                    if token.type == tokenize.OP:
                        if token.string in '([{': depth += 1
                        elif token.string in ')]}': depth -= 1
                    end = token.end[1]
                    candidate = rest[:end]
                    if depth == 0 and token.type not in {tokenize.ENDMARKER, tokenize.NEWLINE, tokenize.NL}:
                        try:
                            value = literal(candidate)
                        except (SyntaxError, ValueError, TypeError, RecursionError):
                            continue
                        if same(value, wanted):
                            piece = candidate
                            break
                if piece is None:
                    return False
            except (tokenize.TokenError, IndentationError, SyntaxError, ValueError, RecursionError):
                return False
        rest = rest[len(piece):]
        if i < len(expected) - 1:
            if not rest.startswith(' '):
                return False
            rest = rest[1:]
    return rest == ''


def _dedup(nodes):
    return tuple({id(node): node for node in nodes}.values())


def _root(expr):
    while isinstance(expr, (ast.Subscript, ast.Attribute)):
        expr = expr.value
    return expr.id if isinstance(expr, ast.Name) else None


def _dead_loop(statement):
    if isinstance(statement, ast.While):
        return isinstance(statement.test, ast.Constant) and not statement.test.value
    if isinstance(statement, ast.For):
        try:
            value = ast.literal_eval(statement.iter)
            return isinstance(value, (str, bytes, list, tuple, set, dict)) and not value
        except (ValueError, TypeError, RecursionError):
            return False
    return False


@dataclass
class Proof:
    nodes: tuple
    args: tuple
    source: str
    aliases: dict
    missing: tuple = ()

    @property
    def argc(self):
        return len(self.args)

    def has_node(self, cls):
        return any(isinstance(node, cls) for node in self.nodes)

    def calls(self, name):
        def qualified(node):
            if isinstance(node, ast.Name):
                return self.aliases.get(node.id, node.id)
            if isinstance(node, ast.Attribute):
                prefix = qualified(node.value)
                return prefix + '.' + node.attr if prefix else node.attr
            return ''
        return any(isinstance(node, ast.Call) and (qualified(node.func) == name or
                   ('.' not in name and qualified(node.func).split('.')[-1] == name)) for node in self.nodes)

    def literal(self, name):
        for node in reversed(self.nodes):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                try:
                    return ast.literal_eval(node.value)
                except (ValueError, TypeError, RecursionError):
                    pass
        return None


class Slicer:
    """Graphe de dépendances borné ; fonctions incluses seulement si appelées."""
    def __init__(self):
        self.bindings = {}
        self.functions = {}
        self.aliases = {}
        self.files = ()

    def dependencies(self, expr, seen=()):
        nodes = list(ast.walk(expr))
        for node in tuple(nodes):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                nodes.extend(self.bindings.get(node.id, ()))
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else None
                if name in self.functions and name not in seen:
                    function = self.functions[name]
                    local = Slicer()
                    local.bindings = dict(self.bindings)
                    local.functions = {key: value for key, value in self.functions.items() if key not in (*seen, name)}
                    local.aliases = dict(self.aliases)
                    for parameter, argument in zip(function.args.args, node.args):
                        local.bindings[parameter.arg] = self.dependencies(argument, (*seen, name))
                    def returns(body, controls=()):
                        result = []
                        for statement in body:
                            if isinstance(statement, ast.Return):
                                if statement.value is not None:
                                    result.extend((statement, *controls, *local.dependencies(statement.value, (*seen, name))))
                                break
                            elif isinstance(statement, ast.Raise):
                                break
                            elif _dead_loop(statement):
                                result.extend(returns(statement.orelse, controls))
                            elif isinstance(statement, (ast.If, ast.For, ast.While, ast.With)):
                                if isinstance(statement, ast.If) and isinstance(statement.test, ast.Constant):
                                    result.extend(returns(statement.body if statement.test.value else statement.orelse, controls))
                                else:
                                    local.update(statement, controls)
                                    condition = getattr(statement, 'test', getattr(statement, 'iter', None))
                                    extra = local.dependencies(condition, (*seen, name)) if condition is not None else ()
                                    result.extend(returns(statement.body, (*controls, statement, *extra)))
                                    result.extend(returns(getattr(statement, 'orelse', []), (*controls, statement, *extra)))
                            else:
                                local.update(statement, controls)
                        return result
                    nodes.extend(returns(function.body))
                    nodes.append(function)
                if isinstance(node.func, ast.Attribute) and node.func.attr in {'read_text', 'read', 'readlines'}:
                    nodes.extend(self.files)
        return _dedup(nodes)

    def update(self, statement, controls=()):
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.functions[statement.name] = statement
            self.bindings.pop(statement.name, None)
            self.aliases.pop(statement.name, None)
            return
        if isinstance(statement, ast.Import):
            for alias in statement.names:
                name = alias.asname or alias.name
                self.bindings.pop(name, None)
                self.functions.pop(name, None)
                self.aliases[name] = alias.name
            return
        if isinstance(statement, ast.ImportFrom):
            for alias in statement.names:
                name = alias.asname or alias.name
                self.bindings.pop(name, None)
                self.functions.pop(name, None)
                self.aliases[name] = (statement.module or '') + '.' + alias.name
            return
        if isinstance(statement, ast.Try):
            # Saved non-error output can support the nominal path. Exception
            # handlers are alternatives, not evidence that a file was read.
            # Never run the submitted try block or inspect student files.
            for child in statement.body:
                if isinstance(child, ast.Raise):
                    break
                self.update(child, (*controls, statement))
            else:
                for child in statement.orelse:
                    self.update(child, (*controls, statement))
            for child in statement.finalbody:
                self.update(child, (*controls, statement))
            return
        # Ignore statically dead branches rather than awarding their keywords.
        if _dead_loop(statement):
            for child in statement.orelse:
                self.update(child, controls)
            return
        if isinstance(statement, ast.If) and isinstance(statement.test, ast.Constant):
            for child in statement.body if statement.test.value else statement.orelse:
                self.update(child, controls)
            return
        if isinstance(statement, (ast.For, ast.While, ast.If, ast.With)):
            if isinstance(statement, ast.For):
                deps = self.dependencies(statement.iter)
                for node in ast.walk(statement.target):
                    if isinstance(node, ast.Name): self.bindings[node.id] = deps
                control_nodes = (statement, *deps)
            elif isinstance(statement, (ast.While, ast.If)):
                control_nodes = (statement, *self.dependencies(statement.test))
            else:
                control_nodes = (statement,)
                for item in statement.items:
                    deps = self.dependencies(item.context_expr)
                    control_nodes += deps
                    if isinstance(item.optional_vars, ast.Name): self.bindings[item.optional_vars.id] = deps
            before = dict(self.bindings)
            for child in statement.body:
                self.update(child, (*controls, *control_nodes))
            for child in getattr(statement, 'orelse', []): self.update(child, (*controls, *control_nodes))
            if isinstance(statement, (ast.For, ast.While)):
                # A list append precedes the counter update in a conventional
                # while loop. Carry that update into the next iteration's
                # controlling/data dependencies, without unrelated assignments.
                changed = {name: deps for name, deps in self.bindings.items()
                           if deps is not before.get(name)}
                for name, deps in changed.items():
                    reads = {node.id for node in deps if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
                    carried = tuple(node for read in reads for node in changed.get(read, ()))
                    self.bindings[name] = _dedup((*deps, *carried))
            return
        value = getattr(statement, 'value', None)
        if isinstance(statement, (ast.Assign, ast.AnnAssign, ast.AugAssign)) and value is not None:
            deps = _dedup((statement, *controls, *self.dependencies(value)))
            targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
            for target in targets:
                name = _root(target)
                if name:
                    if isinstance(target, ast.Name):
                        self.functions.pop(name, None)
                        if isinstance(value, ast.Name) and value.id in self.aliases:
                            self.aliases[name] = self.aliases[value.id]
                        else:
                            self.aliases.pop(name, None)
                    old = self.bindings.get(name, ()) if not isinstance(target, ast.Name) or isinstance(statement, ast.AugAssign) else ()
                    self.bindings[name] = _dedup((*old, *deps))
                elif isinstance(target, (ast.Tuple, ast.List)):
                    for node in ast.walk(target):
                        if isinstance(node, ast.Name): self.bindings[node.id] = deps
            return
        if isinstance(statement, ast.Expr) and isinstance(value, ast.Call):
            if isinstance(value.func, ast.Attribute):
                name = _root(value.func.value)
                deps = _dedup((*controls, *self.dependencies(value)))
                if name:
                    self.bindings[name] = _dedup((*self.bindings.get(name, ()), *deps))
                if value.func.attr in {'write', 'writerow', 'writerows'}:
                    self.files = _dedup((*self.files, *deps))


def collect(notebook):
    index = validate_cell_metadata(notebook)
    sources, records = {}, {}
    slicer = Slicer()
    # Execution convention is notebook order. Additional practice/example cells
    # cannot provide syntax credit for an assessed answer.
    for cell_index, cell in enumerate(notebook['cells']):
        tal = cell.get('metadata', {}).get('tal', {})
        if cell.get('cell_type') != 'code':
            continue
        if tal.get('role') != 'answer':
            # Library aliases are context, never pedagogical evidence.
            if tal.get('role') == 'provided':
                try:
                    for statement in ast.parse(text(cell.get('source', ''))).body:
                        if isinstance(statement, (ast.Import, ast.ImportFrom)):
                            slicer.update(statement)
                except (SyntaxError, ValueError, RecursionError):
                    pass
            continue
        source = text(cell.get('source', ''))
        errors = any(out.get('output_type') == 'error' for out in cell.get('outputs', []))
        try:
            tree = ast.parse(source) if len(source) <= 100000 else None
            if tree is not None and sum(1 for _ in ast.walk(tree)) > 10000: tree = None
        except (SyntaxError, ValueError, RecursionError):
            tree = None
        if tree:
            for statement in tree.body:
                call = statement.value if isinstance(statement, ast.Expr) else None
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == 'print' and call.args:
                    first = call.args[0]
                    match = MARKER.fullmatch(first.value) if isinstance(first, ast.Constant) and isinstance(first.value, str) else None
                    if match and not match[2] and index.get((re.sub('[a-z]$', '', match[1]), 'answer')) is cell:
                        nodes = _dedup(n for arg in call.args[1:] for n in slicer.dependencies(arg))
                        proof = Proof(nodes, tuple(call.args[1:]), source, dict(slicer.aliases))
                        sources.setdefault(match[1], []).append((cell_index, proof, errors))
                slicer.update(statement)
        stdout = ''.join(text(out.get('text', '')) for out in cell.get('outputs', [])
                         if out.get('output_type') == 'stream' and out.get('name', 'stdout') == 'stdout')
        for line in stdout.splitlines():
            match = MARKER.fullmatch(line)
            if match and index.get((re.sub('[a-z]$', '', match[1]), 'answer')) is cell:
                records.setdefault(match[1], []).append((cell_index, match[2]))
    return sources, records


def check_s1(content_str, filename, td, checks):
    """Stable S1 entry point, sharing the inert evaluator with S2."""
    return check_saved_notebook(content_str, filename, f'td{td}-s1', checks)


def check_saved_notebook(content_str, filename, evaluator, checks):
    """Grade explicitly identified saved traces with a trusted weighted rubric.

    `checks` is application-owned; neither callbacks nor weights come from the
    submitted notebook. No submitted statement or function is executed.
    """
    weights = [float(check.get('points', 1.0)) for check in checks]
    if any(not math.isfinite(weight) or weight < 0 for weight in weights):
        raise ValueError('Barème applicatif invalide.')
    maximum = sum(weights)
    try:
        notebook = read_notebook(content_str)
        info = strict_contract_identity(notebook, evaluator)
        sources, records = collect(notebook)
    except ContractError as exc:
        return 0.0, [], maximum, {}, str(exc)
    except (ValueError, TypeError, RecursionError, OverflowError) as exc:
        return 0.0, [], maximum, {}, 'Erreur notebook : ' + str(exc)
    context = {}
    for marker, displays in sources.items():
        saved = records.get(marker, [])
        if len(displays) == len(saved) == 1 and displays[0][0] == saved[0][0] and not displays[0][2] and len(saved[0][1]) <= 16000:
            context[marker] = {'raw': saved[0][1], 'proof': displays[0][1], 'value_ok': False}
    score, details = 0.0, []
    for number, check in enumerate(checks, 1):
        traces = check['traces']
        absent = [m for m in traces if m not in context]
        proofs = {m: context[m]['proof'] for m in traces if m in context}
        valid = not absent
        for marker, expected in traces.items():
            if marker not in context: continue
            item = context[marker]
            try:
                if expected is None:
                    ok = bool(item['raw'].strip()) and item['raw'].strip() not in {'...', 'À compléter', 'A compléter', 'TODO'}
                elif callable(expected):
                    ok = bool(expected(item['raw'], item['proof'], context))
                else:
                    ok = item['proof'].argc == len(expected) and matches(item['raw'], expected)
                item['value_ok'] = ok
                valid &= ok
            except (ValueError, TypeError, KeyError, IndexError, SyntaxError, RecursionError, OverflowError, AttributeError):
                valid = False
        values_ok = valid
        syntax_ok = True
        if not absent and check.get('syntax'):
            try:
                syntax_ok = bool(check['syntax'](proofs, context))
            except (ValueError, TypeError, KeyError, IndexError, RecursionError, AttributeError):
                syntax_ok = False
        valid = values_ok and syntax_ok
        missing_dependencies = [dependency for dependency in check.get('dependencies', [])
                                if dependency not in context]
        if absent:
            state = 'preuve_absente'
            diagnostic = 'Preuve absente ou inexploitable : ' + ', '.join(absent) + '.'
        elif not values_ok:
            state = 'incorrect'
            diagnostic = 'Résultat ou type enregistré non conforme à la référence de cette question.'
        elif not syntax_ok and missing_dependencies:
            state = 'non_verifiable'
            diagnostic = ('Construction non vérifiable : dépendance ' + ', '.join(missing_dependencies)
                          + ' absente. Aucune erreur de calcul indépendante n’est conclue ; restaurer les étapes précédentes.')
        elif not syntax_ok:
            state = 'construction_absente'
            diagnostic = 'Valeur enregistrée conforme, mais construction demandée non repérée dans ses dépendances syntaxiques.'
        else:
            state = 'conforme'
            diagnostic = 'Critère technique conforme.'
        points = weights[number - 1]
        score += points if valid else 0.0
        details.append({'check': f'Q{number} — ' + check['label'],
                        'student_answer': '\n'.join(m + ': ' + context[m]['raw'] for m in traces if m in context) or 'Preuve absente.',
                        'correct_answer': check['feedback'], 'status': '✅' if valid else '⚠️' if absent else '❌',
                        'diagnostic': diagnostic, 'evaluation_status': state,
                        'points': points if valid else 0.0, 'max_points': points})
    optional_review = evaluator in {f'td{number}-s1' for number in range(1, 8)}
    review_note = ('Les explications ne sont pas évaluées automatiquement. Comparez-les aux critères du TD ; '
                   'sollicitez l’enseignant si une difficulté persiste.' if optional_review else
                   'Les justifications sont à relire humainement.')
    limit_note = LIMIT_NOTE.replace('Les explications et interprétations restent à relire humainement.', review_note) if optional_review else LIMIT_NOTE
    details.append({'check': 'Portée du score', 'student_answer': limit_note, 'correct_answer': ('Un point par question. ' if all(weight == 1.0 for weight in weights) else 'Barème par question indiqué dans le sujet. ') + review_note, 'status': 'ℹ️', 'points': 0.0, 'max_points': 0.0})
    info.update(score_brut=score, score_nature='technique_provisoire', score_max=maximum,
                relecture_humaine='facultative' if optional_review else 'requise', contract_version=2, review_evidence=review_evidence(notebook, len(checks)))
    return score, details, maximum, info, None
