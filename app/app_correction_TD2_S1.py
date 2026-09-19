"""TD2 S1: traces enregistrées et syntaxe reliée aux affichages, jamais exécutées.

Le score est formatif: ni la fraîcheur des sorties ni la compréhension de la
réponse libre ne peuvent être certifiées par cette analyse statique.
"""
import ast
import json
import re

import outils

EVAL_ID = "td2-s1"
MAX_SCORE_TOTAL = 7.0
CHECKS = [
    {"label": label, "source": [], "output": f"Résultat Q{i} :", "points": 1.0}
    for i, label in enumerate([
        "Nettoyage de bord", "Transformation de chaîne", "Indexation et tranche",
        "Découpage", "Recomposition", "Nettoyage de plusieurs chaînes",
        "Trace du découpage et interprétation à relire",
    ], 1)
]
TOKENS = ["La", "traduction", "automatique", "aide", "parfois"]
EXEMPLES = ["  Bonjour  ", "TAL", "  Corpus Français"]
EXPECTED = {
    "Q1": ("Le TAL transforme des textes.",), "Q1b": (35, 29),
    "Q2": ("le tal transforme des corpus.",), "Q2b": (True, False),
    "Q3": ("t", "n", "toke"), "Q3b": ("oken", 12),
    "Q4": (TOKENS, "automatique"), "Q4b": (5, "parfois"),
    "Q5": ("La | traduction | automatique | aide | parfois",),
    "Q5b": (TOKENS, True),
    "Q6": (["bonjour", "tal", "corpus français"],), "Q6b": (EXEMPLES,),
    "Q7b": (["L’analyse,", "c’est", "utile", "!"],),
}
MARKER = re.compile(r"^Résultat (Q[1-7]b?)\s*:\s?(.*)$")
LIMIT_NOTE = ("Analyse statique des traces enregistrées : réexécutez les cellules "
              "dans l’ordre avant l’envoi. Une sortie modifiée ou périmée ne peut "
              "pas être authentifiée par le correcteur.")


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return "".join(value)
    return ""


def _nodes(expr, bindings):
    """Dépendances syntaxiques capturées au moment d'une affectation."""
    result = list(ast.walk(expr))
    for node in list(result):
        if isinstance(node, ast.List):
            node._td2_elements = tuple(_nodes(element, bindings) for element in node.elts)
        if isinstance(node, ast.Name):
            result.extend(bindings.get(node.id, ()))
    # Déduplication pour éviter l'explosion lors des réutilisations successives.
    return tuple({id(node): node for node in result}.values())


def _read_traces(cells):
    bindings, displays, outputs, warnings = {}, {}, {}, []
    for cell_index, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = _text(cell.get("source", ""))
        try:
            tree = ast.parse(source)
        except (SyntaxError, ValueError, RecursionError):
            tree = None
        errors = any(isinstance(out, dict) and out.get("output_type") == "error"
                     for out in cell.get("outputs", []))
        if tree is not None:
            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While, ast.ListComp, ast.SetComp,
                                     ast.DictComp, ast.GeneratorExp, ast.Import, ast.ImportFrom,
                                     ast.If, ast.FunctionDef, ast.AsyncFunctionDef)):
                    warnings.append("Une notion hors programme apparaît (boucle, compréhension, import, condition ou fonction) : reprenez avec les notions du TD2.")
            for statement in tree.body:
                if isinstance(statement, ast.Assign):
                    dependencies = _nodes(statement.value, bindings)
                    for target in statement.targets:
                        if isinstance(target, ast.Name):
                            bindings[target.id] = dependencies
                        elif isinstance(target, (ast.Tuple, ast.List)) and isinstance(statement.value, (ast.Tuple, ast.List)):
                            if len(target.elts) == len(statement.value.elts):
                                for name, value in zip(target.elts, statement.value.elts):
                                    if isinstance(name, ast.Name):
                                        bindings[name.id] = _nodes(value, bindings)
                if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
                    continue
                call = statement.value
                if not isinstance(call.func, ast.Name) or call.func.id != "print" or not call.args:
                    continue
                first = call.args[0]
                if not isinstance(first, ast.Constant) or not isinstance(first.value, str):
                    continue
                match = MARKER.fullmatch(first.value)
                if not match or match.group(2):
                    continue
                marker = match.group(1)
                dependencies = tuple(node for arg in call.args[1:] for node in _nodes(arg, bindings))
                displays.setdefault(marker, []).append((cell_index, dependencies, len(call.args) - 1, errors))
        # Un print peut être réparti entre plusieurs blocs stream par Jupyter.
        stdout = "".join(_text(out.get("text", "")) for out in cell.get("outputs", [])
                         if out.get("output_type") == "stream" and out.get("name", "stdout") == "stdout")
        for line in stdout.splitlines():
            match = MARKER.fullmatch(line)
            if match:
                outputs.setdefault(match.group(1), []).append((cell_index, match.group(2)))
    return displays, outputs, sorted(set(warnings))


def _same_value(value, expected):
    if type(value) is not type(expected):
        return False
    if isinstance(expected, list):
        return len(value) == len(expected) and all(_same_value(a, b) for a, b in zip(value, expected))
    return value == expected


def _matches(text, expected):
    """Compare uniquement les littéraux imprimés; aucune expression évaluée."""
    if len(text) > 4096:
        return False
    if isinstance(expected[0], list):
        match = re.fullmatch(r"(\[.*\])(?:\s+(.*))?", text)
        if not match:
            return False
        try:
            value = ast.literal_eval(match.group(1))
        except (ValueError, SyntaxError, RecursionError):
            return False
        return (_same_value(value, expected[0]) and
                (match.group(2) or "") == " ".join(str(v) for v in expected[1:]))
    return text == " ".join(str(v) for v in expected)


def _method(nodes, name):
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == name for n in nodes)


def _builtin(nodes, name):
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == name for n in nodes)


def _index(nodes, value):
    for node in nodes:
        if isinstance(node, ast.Subscript):
            try:
                if type(ast.literal_eval(node.slice)) is int and ast.literal_eval(node.slice) == value:
                    return True
            except (ValueError, TypeError):
                pass
    return False


def _last_index(nodes, length):
    if _index(nodes, -1) or _index(nodes, length - 1):
        return True
    return any(isinstance(n, ast.Subscript) and isinstance(n.slice, ast.BinOp)
               and isinstance(n.slice.op, ast.Sub)
               and isinstance(n.slice.right, ast.Constant) and n.slice.right.value == 1
               and isinstance(n.slice.left, ast.Call)
               and isinstance(n.slice.left.func, ast.Name) and n.slice.left.func.id == "len"
               and len(n.slice.left.args) == 1
               and ast.dump(n.slice.left.args[0]) == ast.dump(n.value)
               for n in nodes)


def _slice(nodes, lower, upper):
    return any(isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice)
               and (n.slice.lower is None and lower == 0 or
                    isinstance(n.slice.lower, ast.Constant) and n.slice.lower.value == lower)
               and isinstance(n.slice.upper, ast.Constant) and n.slice.upper.value == upper
               and (n.slice.step is None or isinstance(n.slice.step, ast.Constant) and n.slice.step.value == 1)
               for n in nodes)


def _syntax(marker, nodes, argc):
    m = lambda name: _method(nodes, name)
    length = lambda: _builtin(nodes, "len")
    rules = {
        "Q1": lambda: m("strip"), "Q1b": length,
        "Q2": lambda: m("lower") and m("replace"),
        "Q2b": lambda: any(isinstance(n, ast.In) for n in nodes),
        "Q3": lambda: _index(nodes, 0) and _last_index(nodes, 12) and _slice(nodes, 0, 4),
        "Q3b": lambda: _slice(nodes, 1, 5) and length(),
        "Q4": lambda: m("split") and _index(nodes, 2),
        "Q4b": lambda: length() and _last_index(nodes, 5),
        "Q5": lambda: m("join"), "Q5b": lambda: m("split") and any(isinstance(n, ast.Eq) for n in nodes),
        "Q6": lambda: any(isinstance(n, ast.List) and len(getattr(n, "_td2_elements", ())) == 3
                          and all(_method(element, "strip") and _method(element, "lower")
                                  and _index(element, i)
                                  for i, element in enumerate(n._td2_elements)) for n in nodes),
        "Q6b": lambda: any(isinstance(n, ast.List) for n in nodes),
        "Q7": lambda: argc == 1,
        "Q7b": lambda: m("split"),
    }
    return argc == len(EXPECTED.get(marker, (None,))) and rules[marker]()


def check_notebook(content_str, filename):
    try:
        notebook = json.loads(content_str)
    except (json.JSONDecodeError, TypeError) as exc:
        return 0.0, [], MAX_SCORE_TOTAL, {}, f"Erreur JSON: {exc}"
    if not isinstance(notebook, dict) or not isinstance(notebook.get("cells"), list):
        return 0.0, [], MAX_SCORE_TOTAL, {}, "Erreur notebook : liste de cellules absente."
    cells = notebook["cells"]
    for cell in cells:
        if not isinstance(cell, dict) or not isinstance(cell.get("source", ""), (str, list)):
            return 0.0, [], MAX_SCORE_TOTAL, {}, "Erreur notebook : cellule mal formée."
        if isinstance(cell.get("source"), list) and not all(isinstance(v, str) for v in cell["source"]):
            return 0.0, [], MAX_SCORE_TOTAL, {}, "Erreur notebook : source mal formée."
        if cell.get("cell_type") == "code":
            if not isinstance(cell.get("outputs", []), list) or not all(isinstance(v, dict) for v in cell.get("outputs", [])):
                return 0.0, [], MAX_SCORE_TOTAL, {}, "Erreur notebook : sorties mal formées."
    displays, outputs, warnings = _read_traces(cells)

    def inspect(marker):
        sources, records = displays.get(marker, []), outputs.get(marker, [])
        if len(sources) != 1 or len(records) != 1:
            return False, f"{marker} : un affichage de code et une sortie uniques sont attendus."
        cell, nodes, argc, errors = sources[0]
        if errors or cell != records[0][0]:
            return False, f"{marker} : sortie absente de la cellule correspondante ou erreur d’exécution enregistrée."
        if not _syntax(marker, nodes, argc):
            return False, f"{marker} : reprendre la manipulation demandée et l’affichage des variables calculées."
        value = records[0][1]
        if marker == "Q7":
            valid = bool(value.strip()) and value.strip() not in {"...", "À compléter", "A compléter"}
        else:
            valid = _matches(value, EXPECTED[marker])
        return valid, (f"{marker} : trace conforme." if valid else
                       f"{marker} : résultat enregistré différent de l’attendu; vérifiez valeur, type et ordre.")

    details, score = [], 0.0
    for number, check in enumerate(CHECKS, 1):
        main_ok, main_feedback = inspect(f"Q{number}")
        extra_ok, extra_feedback = inspect(f"Q{number}b")
        if number == 7:
            points = float(extra_ok and main_ok)
            feedback = ("Le point porte sur la trace du découpage et la présence d’une interprétation. "
                        "Le sens de votre commentaire reste à relire avec l’enseignant : il n’est pas évalué automatiquement.")
        else:
            points = 0.5 * (main_ok + extra_ok)
            feedback = "Chaque trace conforme vaut 0,5 point. "
        score += points
        details.append({
            "check": check["label"], "student_answer": main_feedback + " " + extra_feedback,
            "correct_answer": feedback + " " + LIMIT_NOTE + (" " + " ".join(warnings) if warnings else ""),
            "status": "✅" if points == 1.0 else "❌", "points": points, "max_points": 1.0,
        })
    info = outils.extract_identification_info(cells)
    info["score_brut"] = score
    return score, details, MAX_SCORE_TOTAL, info, None
