"""Trusted S1 expansion rubrics, using the existing inert trace evaluator.

Only application-owned reference literals and predicates are loaded here.
Student files, source statements and function bodies are never executed.
"""
import ast
import json
from pathlib import Path

from s1_revision import literal, same


def _syntax(calls, nodes):
    classes = tuple(getattr(ast, name) for name in nodes)

    def validate(proofs, context):
        return (all(any(proof.calls(call) for proof in proofs.values()) for call in calls)
                and all(any(proof.has_node(cls) for proof in proofs.values()) for cls in classes))
    return validate


def _unordered_rows(expected):
    """Compare typed rows without imposing their order; retain duplicates."""
    def validate(raw, proof, context):
        if proof.argc != 1:
            return False
        rows = literal(raw)
        if not isinstance(rows, list) or len(rows) != len(expected):
            return False
        remaining = list(expected)
        for row in rows:
            index = next((i for i, item in enumerate(remaining) if same(row, item)), None)
            if index is None:
                return False
            remaining.pop(index)
        return not remaining
    return validate


def _affiliation_csv(expected):
    """CSV rows: header, counts, people and affiliations; row orders are free."""
    def table(rows):
        if type(rows) is not list or not rows or rows[0] != ['personne', 'nb_affiliations', 'affiliations']:
            raise ValueError('En-tête CSV incorrect.')
        result = {}
        for row in rows[1:]:
            if type(row) is not list or len(row) != 3 or any(type(x) is not str for x in row) or row[0] in result:
                raise ValueError('Ligne CSV incorrecte ou répétée.')
            affiliations = row[2].split(' | ')
            if len(affiliations) != len(set(affiliations)) or str(len(affiliations)) != row[1]:
                raise ValueError('Compte des affiliations incorrect.')
            result[row[0]] = set(affiliations)
        return result
    wanted = table(expected[0])
    def validate(raw, proof, context):
        if proof.argc != 1:
            return False
        try:
            return same(table(literal(raw)), wanted)
        except (ValueError, SyntaxError, TypeError):
            return False
    return validate


def _flexible_pairs(expected):
    """Only inner record pairs accept list/tuple; outer list and strings stay strict."""
    wanted = expected[0]
    def pair(value, reference):
        return (type(value) in (tuple, list) and len(value) == len(reference)
                and all(same(a, b) for a, b in zip(value, reference)))
    def validate(raw, proof, context):
        if proof.argc != 1:
            return False
        value = literal(raw)
        if type(wanted) is tuple:
            return pair(value, wanted)
        return (type(value) is list and len(value) == len(wanted)
                and all(pair(a, b) for a, b in zip(value, wanted)))
    return validate


def _lexicon_trace(marker):
    """Accept both translations and any entry order, consistently across traces."""
    def validate(raw, proof, context):
        choice = context.get('Q1a', {}).get('raw')
        if choice not in {'langue', 'langage'} or proof.argc != 1:
            return False
        lexicon = {'book': 'livre', 'language': choice, 'data': 'données', 'corpus': 'corpus'}
        if marker == 'Q1a':
            return raw == choice
        if marker == 'Q1b':
            return same(literal(raw), lexicon)
        entries = literal(raw)
        wanted = [key + ' -> ' + value for key, value in lexicon.items()]
        return type(entries) is list and len(entries) == len(wanted) and sorted(entries) == sorted(wanted)
    return validate


def _checks():
    data = json.loads(Path(__file__).with_name('s1_expansion_rubrics.json').read_text(encoding='utf-8'))
    result = {}
    for identifier, questions in data.items():
        result[identifier] = []
        for question in questions:
            traces = {marker: literal(value) for marker, value in question['traces'].items()}
            if question.get('flexible_pairs'):
                traces = {marker: _flexible_pairs(value) for marker, value in traces.items()}
            if question.get('lexicon_variants'):
                traces = {marker: _lexicon_trace(marker) for marker in traces}
            if question.get('unordered_rows') and not question.get('csv_affiliations'):
                traces = {marker: _unordered_rows(value[0]) for marker, value in traces.items()}
            if question.get('csv_affiliations'):
                traces = {marker: _affiliation_csv(value) for marker, value in traces.items()}
            check = {'label': question['label'], 'traces': traces,
                     'feedback': question['feedback'], 'points': 1.0}
            if question.get('required_calls') or question.get('required_nodes'):
                check['syntax'] = _syntax(question.get('required_calls', []), question.get('required_nodes', []))
            result[identifier].append(check)
    return result


CHECKS = _checks()
