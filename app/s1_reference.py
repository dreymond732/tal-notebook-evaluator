"""Trusted S1 references and inert syntax checks; never run submitted programs.

Saved values are compared with independently specified course cases. Syntax
checks describe evidence, not a proof of a program's behaviour or authorship.
"""
import ast
import csv
import io


def _literal(raw):
    from s1_revision import literal
    return literal(raw)


def _same(a, b):
    # bool is not a numeric measurement, despite Python's True == 1.
    if type(a) is not type(b):
        return False
    if isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], v) for k, v in b.items())
    if isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return a == b


def _value(expected, transform=None):
    def check(raw, proof, context):
        try:
            value = _literal(raw)
            return _same(transform(value) if transform else value, expected)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
            return False
    return check


def _proofs(proofs):
    return list(proofs.values())


def _nodes(proofs):
    return [node for proof in _proofs(proofs) for node in proof.nodes]


def _calls(proofs, name):
    return any(p.calls(name) for p in _proofs(proofs))


def _has(proofs, kind):
    return any(isinstance(n, kind) for n in _nodes(proofs))


def _syntax(*calls, kinds=(), alternative=None):
    return lambda proofs, context: (all(_calls(proofs, c) for c in calls)
        and all(_has(proofs, k) for k in kinds)
        and (alternative is None or alternative(proofs)))


def _function(name, *calls, kinds=()):
    return _syntax(name, *calls, kinds=(ast.FunctionDef, ast.Return, *kinds))


def _question(label, traces, syntax, feedback=None):
    return {'label': label, 'points': 1.0, 'traces': traces, 'syntax': syntax,
            'feedback': feedback or 'Vérifiez les données, le traitement demandé et les affichages enregistrés.'}


def _phrase_binding(proof):
    bindings = []
    for node in proof.nodes:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, (ast.AnnAssign, ast.AugAssign)) else []
        if any(isinstance(target, ast.Name) and target.id == 'phrase' for target in targets):
            bindings.append(node)
    return max(bindings, key=lambda node: node.lineno) if bindings else None


def _phrase(raw, proof, context):
    if proof.argc != 2:
        return False
    try:
        phrase = _literal(context['Q6b']['raw'])
        companion = context['Q6b']['proof']
        if type(phrase) is not str or not _phrase_text(context['Q6b']['raw'], companion, context):
            return False
        binding = _phrase_binding(proof)
        # Both displays must concern the same binding. A literal gives an extra
        # independent check; a concatenation/f-string stays inert and is checked
        # through its saved repr, without interpreting the submitted expression.
        companion_binding = _phrase_binding(companion)
        if binding is None or companion_binding is None:
            return False
        known = []
        for current in (binding, companion_binding):
            is_literal = isinstance(current, (ast.Assign, ast.AnnAssign)) and isinstance(current.value, ast.Constant)
            known.append(is_literal)
            if is_literal and (type(current.value.value) is not str or current.value.value != phrase):
                return False
        if binding is not companion_binding and not all(known):
            return False
        uses_length = any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                          and node.func.id == 'len' and len(node.args) == 1
                          and isinstance(node.args[0], ast.Name) and node.args[0].id == 'phrase'
                          for node in proof.nodes)
        uses_membership = any(isinstance(node, ast.Compare) and len(node.ops) == 1
                              and isinstance(node.ops[0], ast.In) and isinstance(node.left, ast.Constant)
                              and node.left.value == 'TAL' and isinstance(node.comparators[0], ast.Name)
                              and node.comparators[0].id == 'phrase' for node in proof.nodes)
        from s1_revision import matches
        return uses_length and uses_membership and matches(raw, (len(phrase), 'TAL' in phrase))
    except (KeyError, ValueError, SyntaxError, TypeError):
        return False


def _phrase_text(raw, proof, context):
    if proof.argc != 1:
        return False
    try:
        linked_repr = any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                          and node.func.id == 'repr' and len(node.args) == 1
                          and isinstance(node.args[0], ast.Name) and node.args[0].id == 'phrase'
                          for node in proof.nodes)
        return linked_repr and type(_literal(raw)) is str
    except (ValueError, SyntaxError, TypeError):
        return False


LEXICON = {'book': 'livre', 'language': 'langage', 'data': 'données', 'corpus': 'corpus'}


def _lexicon(raw, proof, context):
    if proof.argc != 1:
        return False
    try:
        value = _literal(raw)
        return any(_same(value, dict(LEXICON, language=translation)) for translation in ('langage', 'langue'))
    except (ValueError, SyntaxError, TypeError):
        return False


def _translation(raw, proof, context):
    if proof.argc != 1:
        return False
    if raw.strip() not in ('langage', 'langue'):
        return False
    try:
        lexicon = _literal(context['Q3b']['raw'])
        return raw.strip() == lexicon['language']
    except (KeyError, ValueError, SyntaxError, TypeError):
        return False



def _entries(raw, proof, context):
    if proof.argc != 1:
        return False
    try:
        value = _literal(raw)
        if type(value) is not list or len(value) != 4 or any(type(v) is not str for v in value):
            return False
        # Dictionary insertion order is immaterial; all four pairs are required.
        translations = ('langage', 'langue')
        prior = context.get('Q3b')
        if prior and _lexicon(prior['raw'], prior['proof'], context):
            translations = (_literal(prior['raw'])['language'],)
        return any(sorted(value) == sorted(f'{key} -> {val}' for key, val in dict(LEXICON, language=t).items())
                   for t in translations)
    except (ValueError, SyntaxError, TypeError):
        return False


def _prose(raw):
    return bool(raw.strip()) and raw.strip() not in {'...', 'À compléter', 'A compléter', 'TODO'}


def _tuple_type_reason(raw, proof, context):
    if proof.argc != 2:
        return False
    prefix = "<class 'tuple'> "
    return raw.startswith(prefix) and _prose(raw[len(prefix):])


def _mutation(proofs, context):
    return proofs['Q1a'].calls('append') and proofs['Q1'].calls('pop')


def _count_syntax(proofs):
    return _calls(proofs, 'get') or _has(proofs, ast.If)


def _increment(proofs):
    return _has(proofs, ast.AugAssign) or _has(proofs, ast.Add)


def _set_operations(proofs):
    return ((_has(proofs, ast.BitAnd) or _calls(proofs, 'intersection'))
            and (_has(proofs, ast.Sub) or _calls(proofs, 'difference')))


AFFILIATIONS_TEXT = ('durand alice;Laboratoire TAL\nDURAND ALICE;Laboratoire TAL\n'
                     'Durand Alice;Centre de traduction\nMartin bob;Centre de traduction\n'
                     'MARTIN BOB;Centre de traduction\n')
RECORDS = [['durand alice', 'Laboratoire TAL'], ['DURAND ALICE', 'Laboratoire TAL'],
           ['Durand Alice', 'Centre de traduction'], ['Martin bob', 'Centre de traduction'],
           ['MARTIN BOB', 'Centre de traduction']]
AFFILIATIONS = {'Durand Alice': {'Laboratoire TAL', 'Centre de traduction'},
                'Martin Bob': {'Centre de traduction'}}


def _records(raw, proof, context):
    if proof.argc != 1:
        return False
    try:
        records = _literal(raw)
        return type(records) is list and len(records) == 5 and all(
            type(row) in (tuple, list) and _same(list(row), ref) for row, ref in zip(records, RECORDS))
    except (ValueError, SyntaxError, TypeError):
        return False


def _first_record(raw, proof, context):
    if proof.argc != 1:
        return False
    try:
        row = _literal(raw)
        return type(row) in (tuple, list) and _same(list(row), RECORDS[0])
    except (ValueError, SyntaxError, TypeError):
        return False


def _split_once(proofs, context):
    for n in _nodes(proofs):
        if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Attribute) or n.func.attr != 'split':
            continue
        args = dict((k.arg, k.value) for k in n.keywords)
        sep = n.args[0] if n.args else args.get('sep')
        limit = n.args[1] if len(n.args) > 1 else args.get('maxsplit')
        if (isinstance(sep, ast.Constant) and sep.value == ';' and isinstance(limit, ast.Constant)
                and type(limit.value) is int and limit.value == 1):
            return True
    return False


def _open_options(proofs, write=False):
    for n in _nodes(proofs):
        if not isinstance(n, ast.Call):
            continue
        name = n.func.id if isinstance(n.func, ast.Name) else getattr(n.func, 'attr', '')
        if name != 'open':
            continue
        kwargs = {k.arg: k.value for k in n.keywords}
        enc = kwargs.get('encoding')
        if not isinstance(enc, ast.Constant) or enc.value not in ('utf-8', 'utf8', 'UTF-8'):
            continue
        if write:
            mode = n.args[1] if len(n.args) > 1 else kwargs.get('mode')
            newline = kwargs.get('newline')
            if not (isinstance(mode, ast.Constant) and mode.value in ('w', 'wt')
                    and isinstance(newline, ast.Constant) and newline.value == ''):
                continue
        return True
    return False


def _csv_value(raw, proof, context):
    if proof.argc != 1:
        return False
    try:
        text = _literal(raw)
        if type(text) is not str:
            return False
        rows = list(csv.reader(io.StringIO(text)))
        if len(rows) != 3 or rows[0] != ['personne', 'nb_affiliations', 'affiliations']:
            return False
        names = set()
        for row in rows[1:]:
            if len(row) != 3 or row[0] in names or row[0] not in AFFILIATIONS:
                return False
            names.add(row[0])
            values = row[2].split(' | ')
            if len(values) != len(set(values)) or set(values) != AFFILIATIONS[row[0]] or row[1] != str(len(values)):
                return False
        return names == set(AFFILIATIONS)
    except (ValueError, SyntaxError, TypeError, csv.Error):
        return False


def _csv_syntax(proofs, context):
    return (_has(proofs, ast.With) and _open_options(proofs, write=True)
            and (_calls(proofs, 'writer') or _calls(proofs, 'DictWriter'))
            and (_calls(proofs, 'writerow') or _calls(proofs, 'writerows'))
            and (_calls(proofs, 'read_text') or _calls(proofs, 'read')))


def _regex_words(raw, proof, context):
    if proof.argc != 2:
        return False
    # The first print argument is a literal list; the rest is a free comment.
    # Parse the bracket-closed list inertly, accepting either repr quote style.
    end = raw.find(']')
    if end < 0:
        return False
    return _value(['L', 'analyse', 'c', 'est', 'déjà', 'étapes'])(raw[:end+1], proof, context) and _prose(raw[end+1:])


def _ignorecase(proofs):
    return _calls(proofs, 'lower') or _calls(proofs, 'casefold') or any((isinstance(n, ast.Attribute) and n.attr in ('IGNORECASE', 'I'))
               or (isinstance(n, ast.Constant) and isinstance(n.value, str) and '(?i)' in n.value)
               for n in _nodes(proofs))


def _price(raw, proof, context):
    if proof.argc != 1:
        return False
    try:
        value = _literal(raw)
        return type(value) in (int, float) and abs(value - 15.0) < 1e-9
    except (ValueError, SyntaxError, TypeError, OverflowError):
        return False


def _presentation(raw, proof, context):
    if proof.argc != 1:
        return False
    return raw in ('Traduction du français vers l’anglais.', "Traduction du français vers l'anglais.")


def _added_corpus(proofs):
    for node in _nodes(proofs):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant)
                    and target.slice.value == 'corpus'):
                return True
    return False


CHECKS = {
1: [
    _question('Calcul numérique', {'Q1': _price}, _syntax(kinds=(ast.Mult,))),
    _question('Observation de type', {'Q2': ("<class 'float'>",)}, _syntax('type')),
    _question('Comparaison et conjonction', {'Q3': (True, True)}, _syntax(kinds=(ast.Eq, ast.And))),
    _question('f-string', {'Q4': _presentation}, _syntax(kinds=(ast.JoinedStr, ast.FormattedValue))),
    _question('Conversion en entier', {'Q5': (100, "<class 'int'>")}, _syntax('int', 'type', kinds=(ast.Add,))),
    _question('Chaîne et appartenance', {'Q6': _phrase, 'Q6b': _phrase_text}, _syntax('len', kinds=(ast.In,))),
],
3: [
    _question('Modification de liste', {'Q1a': (['corpus', 'lexique', 'concordancier', 'tokeniseur'],), 'Q1': (['corpus', 'lexique', 'concordancier'],)}, _mutation),
    _question('Tuple et justification', {'Q2': _tuple_type_reason, 'Q2b': (('français', 'italien', 'espagnol'),)}, _syntax('type', alternative=lambda p: _has(p, ast.Tuple) or _calls(p, 'tuple'))),
    _question('Dictionnaire', {'Q3': _translation, 'Q3b': _lexicon}, _syntax(kinds=(ast.Dict, ast.Subscript), alternative=_added_corpus)),
    _question('Parcours clé-valeur', {'Q4': _entries}, _syntax('items', kinds=(ast.For,))),
    _question('Ensemble', {'Q5': (6, 4), 'Q5b': ({'texte', 'corpus', 'donnée', 'analyse'},)}, _syntax('set', 'len')),
    _question('Comparaison d’ensembles', {'Q6': ({'langue', 'corpus'}, {'texte', 'analyse'})}, _syntax(alternative=_set_operations)),
],
4: [
    _question('Boucle de parcours', {'Q1': (['TAL', 'CORPUS', 'ANALYSE', 'IA'],)}, _syntax('upper', kinds=(ast.For,))),
    _question('Filtrage par longueur', {'Q2': (['corpus', 'analyse'],)}, _syntax('len', kinds=(ast.For, ast.If))),
    _question('Filtrage par appartenance', {'Q3': (['TAL', 'analyse', 'IA'],)}, _syntax(kinds=(ast.For, ast.In), alternative=lambda p: _calls(p, 'lower') or _calls(p, 'upper'))),
    _question('Positions avec range', {'Q4': ([0, 2, 4, 6, 8, 10],)}, _syntax('range')),
    _question('Boucle while bornée', {'Q5': ([7, 14, 21, 28, 35, 42, 49, 56, 63, 70],)}, _syntax(kinds=(ast.While,), alternative=_increment)),
    _question('Fréquences', {'Q6': ({'le': 3, 'tal': 1, 'traite': 1, 'langage': 1, 'et': 1, 'texte': 1},)}, _syntax(kinds=(ast.For,), alternative=_count_syntax)),
    _question('Compréhension', {'Q7': ([6, 7],)}, _syntax('len', kinds=(ast.ListComp,), alternative=lambda p: any(isinstance(n, ast.comprehension) and n.ifs for n in _nodes(p)))),
],
5: [
    _question('Fonction et retour', {'Q1': (3, 6)}, _function('longueur_texte', 'len')),
    _question('Normalisation réutilisable', {'Q2': ('bonjour tal',)}, _function('normaliser', 'strip', 'lower')),
    _question('Composition', {'Q3': (5,)}, _function('nombre_mots', 'normaliser', 'split', 'len')),
    _question('Traduction sécurisée', {'Q4': ('langage', 'unknown')}, _syntax('traduire_mot', kinds=(ast.FunctionDef, ast.Return), alternative=lambda p: _calls(p, 'get') or _has(p, ast.If) or _has(p, ast.IfExp))),
    _question('Traduction de phrase', {'Q5': ('langage données',)}, _function('traduire_phrase', 'traduire_mot', 'split', 'join')),
    _question('Dictionnaire de synthèse', {'Q6': ({'texte_normalise': 'le tal avance', 'nb_caracteres': 13, 'nb_mots': 3},)}, _function('resume_texte', 'normaliser', 'nombre_mots', 'len')),
],
6: [
    _question('Lecture UTF-8 contextualisée', {'Q1': (156,)}, _syntax('read', kinds=(ast.With,), alternative=lambda p: _open_options(p))),
    _question('Découpage en lignes', {'Q2': (5,)}, _syntax('splitlines', 'len')),
    _question('Séparation structurée', {'Q3': _first_record, 'Q3b': _records}, _split_once),
    _question('Fonction de normalisation', {'Q4': ('Durand Alice',), 'Q4b': ('Durand Alice', 'Durand Alice', 'Durand Alice')}, _function('normaliser_personne', 'title')),
    _question('Dédoublonnage', {'Q5': ({'Laboratoire TAL', 'Centre de traduction'},), 'Q5b': (AFFILIATIONS,)}, _syntax(alternative=lambda p: _calls(p, 'set') or _has(p, ast.Set))),
    _question('Écriture CSV', {'Q6': _csv_value}, _csv_syntax),
],
7: [
    _question('Recherche insensible à la casse', {'Q1': (True,)}, _syntax('search', alternative=_ignorecase)),
    _question('Extraction de nombres', {'Q2': (['2', '14', '3', '250'],)}, _syntax('findall')),
    _question('Extraction de mots et commentaire', {'Q3': _regex_words}, _syntax('findall')),
    _question('Remplacement de date', {'Q4': ('Le [DATE], Alice a relu 12 segments.',)}, _syntax('sub')),
    _question('Nettoyage paramétré', {'Q5': ('le [DATE] comporte exemples.',)}, _function('nettoyer_texte', 'sub', 'lower')),
    _question('Pipeline', {'Q6': ({'texte_nettoye': 'le tal, le tal : exemples.', 'mots': ['le', 'tal', 'le', 'tal', 'exemples'], 'frequences': {'le': 2, 'tal': 2, 'exemples': 1}},)}, _function('analyser_texte', 'nettoyer_texte', 'findall')),
    _question('Limite interprétée — présence à relire', {'Q7': None}, lambda p, c: True,
              'La présence de la réponse est relevée ; sa pertinence linguistique nécessite une relecture humaine.'),
],
}


# Diagnostics only: fixed quantitative references are still checked independently.
DEPENDENCIES = {
    3: {4: ['Q3']},
    4: {2: ['Q1'], 3: ['Q1'], 7: ['Q1']},
    5: {3: ['Q2'], 4: ['Q2'], 5: ['Q4'], 6: ['Q2', 'Q3']},
    6: {2: ['Q1'], 3: ['Q2'], 5: ['Q3', 'Q4'], 6: ['Q5']},
    7: {6: ['Q5']},
}
for _td, _questions in DEPENDENCIES.items():
    for _question_number, _dependencies in _questions.items():
        CHECKS[_td][_question_number - 1]['dependencies'] = _dependencies
