"""Concordances et citations : contrôle de passages contre le corpus figé."""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import re

from s3_audit import check_audit, integer, keys, same
from s3_audit_data import TEXT3
from s3_audit_linguistic import strings

EVAL_ID = 'td3-s3'
MAX_SCORE_TOTAL = 7.0
SOURCE_SHA256 = 'c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa'
LOCAL_RESOURCES = Path(__file__).resolve().parent / 's3_resources'
REPO_RESOURCES = Path(__file__).resolve().parents[1] / 'Notebooks TD/S3/ressources'


@lru_cache(maxsize=1)
def resources():
    directory = LOCAL_RESOURCES if LOCAL_RESOURCES.exists() else REPO_RESOURCES
    raw = (directory / 'faguet_source.txt').read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('Empreinte du corpus de référence incorrecte.')
    # decode préserve les CRLF du fichier original ; read_text() les convertirait.
    source = raw.decode('utf-8')
    citations = json.loads((directory / 'citations_gemini.json').read_text(encoding='utf-8'))
    return source, citations


def concordances(source, motif, width=20):
    results, start = [], 0
    while (start := source.find(motif, start)) != -1:
        end = start + len(motif)
        results.append({'debut': start, 'fin': end, 'pivot': motif,
                        'gauche': source[max(0, start - width):start], 'droite': source[end:end + width]})
        start = end
    return results


def provenance(value):
    return (keys(value, ['sha256', 'affirmations', 'prompts', 'parametres_absents', 'limite'])
            and value['sha256'] == SOURCE_SHA256 and strings(value['affirmations']) and sorted(value['affirmations']) == ['G1', 'G2', 'G3', 'G4', 'G5', 'G6']
            and same(value['prompts'], 3) and strings(value['parametres_absents']) and len(value['parametres_absents']) >= 2
            and isinstance(value['limite'], str))


def research_modes(value):
    source = 'Les lecteurs lisent. Une lectrice lit.'
    if not keys(value, ['fragment', 'forme', 'lemme', 'explication']):
        return False
    exact = [{'forme': 'lit', 'debut': source.index('lit'), 'fin': source.index('lit') + 3}]
    if not same(value['fragment'], exact) or not same(value['forme'], exact):
        return False
    rows = value['lemme']
    return (isinstance(rows, list) and len(rows) >= 1 and all(
        keys(row, ['forme', 'debut', 'fin']) and integer(row['debut']) and integer(row['fin'])
        and row['fin'] > row['debut'] and source[row['debut']:row['fin']] == row['forme'] for row in rows)
        and isinstance(value['explication'], str))


def exact_citations(value):
    source, citations = resources()
    if not keys(value, ['citations', 'limite']):
        return False
    expected = []
    for citation in citations:
        position = source.find(citation['citation'])
        expected.append({'id': citation['id'], 'citation': citation['citation'], 'debut': position, 'exacte': position >= 0})
    rows = value['citations']
    return (isinstance(rows, list) and len(rows) == len(expected)
            and all(keys(row, ['id', 'citation', 'debut', 'exacte']) for row in rows)
            and len({row['id'] for row in rows}) == len(expected)
            and same({row['id']: row for row in rows}, {row['id']: row for row in expected})
            and isinstance(value['limite'], str))


def altered_citation(value):
    source, _ = resources()
    if not keys(value, ['id', 'passage_source', 'debut', 'difference', 'verdict']) or value['id'] != 'C1':
        return False
    passage = value['passage_source']
    return (isinstance(passage, str) and 'légalement' in passage and 'naturellement' in passage
            and integer(value['debut']) and source[value['debut']:value['debut'] + len(passage)] == passage
            and isinstance(value['difference'], str) and isinstance(value['verdict'], str))


def student_tests(value):
    if not keys(value, ['tests', 'regle_humaine']) or not isinstance(value['tests'], list) or len(value['tests']) != 2:
        return False
    rows = value['tests']
    for row in rows:
        if not keys(row, ['source', 'citation', 'exacte_attendue', 'exacte_observee']):
            return False
        if not all(isinstance(row[k], str) and row[k] for k in ['source', 'citation']):
            return False
        actual = row['citation'] in row['source']
        if not same(row['exacte_attendue'], actual) or not same(row['exacte_observee'], actual):
            return False
    return {row['exacte_observee'] for row in rows} == {True, False} and isinstance(value['regle_humaine'], str)


def evidence(value):
    source, _ = resources()
    if not keys(value, ['affirmation', 'preuves', 'convention_proposee', 'limite']) or value['affirmation'] not in ['G1', 'G2']:
        return False
    rows = value['preuves']
    if not isinstance(rows, list) or len(rows) < 3:
        return False
    positions = set()
    for row in rows:
        if not keys(row, ['debut', 'fin', 'passage']) or not integer(row['debut']) or not integer(row['fin']):
            return False
        passage = row['passage']
        if (row['fin'] <= row['debut'] or not isinstance(passage, str) or source[row['debut']:row['fin']] != passage
                or not re.search(r'\b' + ('intelligence' if value['affirmation'] == 'G1' else 'aptitudes?') + r'\b', passage, re.IGNORECASE)):
            return False
        positions.add((row['debut'], row['fin']))
    return len(positions) >= 3 and isinstance(value['convention_proposee'], str) and isinstance(value['limite'], str)


CHECKS = [
    {'label': 'Provenance', 'validate': provenance, 'feedback': 'Empreinte du fichier original, G1–G6, trois prompts et paramètres manquants. La pertinence des paramètres est à relire humainement.'},
    {'label': 'Concordances exactes', 'validate': lambda v: same(v, {'concordances': concordances(TEXT3, 'droit'), 'absent': []}),
     'feedback': 'Trois occurrences exactes de droit, indices et contextes largeur 20 ; justice absent.'},
    {'label': 'Modes de recherche', 'validate': research_modes,
     'feedback': 'Fragment et forme exacts ; lemmes contrôlés uniquement pour leur provenance, sans certifier le modèle.'},
    {'label': 'Citations exactes', 'validate': exact_citations,
     'feedback': 'Comparaison exacte des trois citations, respectant casse, ponctuation et CRLF du texte original.'},
    {'label': 'Passage source de C1', 'validate': altered_citation,
     'feedback': 'Passage exact et position d’origine contenant légalement et naturellement. Qualification de l’altération à relire humainement.'},
    {'label': 'Deux cas de test contrastés', 'validate': student_tests,
     'feedback': 'Un exact et un altéré ; valeurs attendues et observées conformes à une recherche exacte. La règle humaine n’est pas notée automatiquement.'},
    {'label': 'Trois preuves distinctes', 'validate': evidence,
     'feedback': 'Au moins trois positions distinctes et passages exacts contenant le pivot intelligence (G1) ou aptitude(s) (G2). Convention et interprétation à relire humainement.'},
]


def check_notebook(content_str, filename):
    try:
        resources()
    except (OSError, ValueError, UnicodeError) as exc:
        return 0.0, [], MAX_SCORE_TOTAL, {}, 'Ressource S3 indisponible ou invalide : ' + str(exc)
    return check_audit(content_str, filename, 3, CHECKS)
