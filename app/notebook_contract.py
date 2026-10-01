"""Trusted notebook catalogue and inert, explicit cell identification.

Metadata is routing information, never permission to import a module or run code.
Old notebooks remain supported only on an explicitly selected legacy route.
"""
import ast
import json
import re
from pathlib import Path


class ContractError(ValueError):
    """An uploaded notebook cannot be resolved unambiguously."""


WRONG_VERSION = 'mauvaise version du notebook'
STRICT_REVISIONS = frozenset({'td-r0-s3', 'td-r1-s3', 'td-r2-s3'})
S3_QUESTION_COUNTS = {**{f'td{n}-s3': (6 if n == 1 else 7) for n in range(8)},
                      **{f'controle-td{n}-s3': 7 for n in range(1, 8)},
                      **{name: 4 for name in STRICT_REVISIONS}}
STRICT_S3 = frozenset(S3_QUESTION_COUNTS)
S1_QUESTION_COUNTS = {f'td{n}-s1': count for n, count in enumerate((6, 7, 6, 7, 6, 6, 7), 1)}
STRICT_S1 = frozenset(S1_QUESTION_COUNTS)
STRICT_V2 = STRICT_S3 | STRICT_S1
QUESTION_COUNTS = {**S3_QUESTION_COUNTS, **S1_QUESTION_COUNTS}


CELL_ROLES = frozenset({'answer', 'prompt', 'example', 'provided',
                        'identification', 'submission', 'infrastructure', 'practice'})


def load_catalog():
    data = json.loads(Path(__file__).with_name('notebook_catalog.json').read_text(encoding='utf-8'))
    if data.get('schema_version') != 1 or not isinstance(data.get('notebooks'), list):
        raise ValueError('Catalogue TAL invalide.')
    entries = data['notebooks']
    ids, paths, evaluators = set(), set(), set()
    for entry in entries:
        if (not isinstance(entry, dict) or not isinstance(entry.get('id'), str)
                or not entry['id'] or entry['id'] in ids
                or type(entry.get('version')) is not int or entry['version'] < 1
                or entry.get('mode') not in {'td', 'controle'}
                or entry.get('semester') not in {'S1', 'S2', 'S3'}
                or type(entry.get('active')) is not bool
                or not isinstance(entry.get('notebook'), str)
                or not entry['notebook'] or entry['notebook'] in paths):
            raise ValueError('Entrée du catalogue TAL invalide ou dupliquée.')
        evaluator = entry.get('evaluator')
        if entry['active']:
            if not isinstance(evaluator, str) or not evaluator or evaluator in evaluators:
                raise ValueError('Évaluateur du catalogue TAL invalide ou dupliqué.')
            evaluators.add(evaluator)
        elif evaluator is not None:
            raise ValueError('Un sujet inactif ne doit pas déclarer de correcteur actif.')
        ids.add(entry['id'])
        paths.add(entry['notebook'])
    return entries


def validate_catalog(evaluators, modes, semesters):
    active = {entry['evaluator']: entry for entry in load_catalog() if entry['active']}
    if set(active) != set(evaluators) or set(modes) != set(evaluators):
        raise ValueError('Le catalogue doit couvrir exactement tous les correcteurs actifs.')
    for name, entry in active.items():
        if entry['mode'] != modes.get(name) or entry['semester'] != semesters.get(name):
            raise ValueError('Mode ou semestre incohérent dans le catalogue TAL.')


def _metadata(value):
    metadata = value.get('metadata', {})
    if not isinstance(metadata, dict):
        raise ContractError('Métadonnées du notebook invalides.')
    return metadata


def validate_cell_metadata(notebook):
    """Return the unique (question, role) index; never use code as identifiers."""
    if not isinstance(notebook, dict) or not isinstance(notebook.get('cells', []), list):
        raise ContractError('Structure du notebook invalide.')
    indexed = {}
    for cell in notebook.get('cells', []):
        if not isinstance(cell, dict):
            raise ContractError('Cellule de notebook invalide.')
        metadata = _metadata(cell)
        if 'tal' not in metadata:
            continue
        contract = metadata['tal']
        if (not isinstance(contract, dict)
                or not isinstance(contract.get('question'), str)
                or not contract['question'].strip()
                or not isinstance(contract.get('role'), str)
                or contract['role'] not in CELL_ROLES):
            raise ContractError('Identification de cellule TAL invalide.')
        key = (contract['question'], contract['role'])
        if key in indexed:
            raise ContractError('Plusieurs cellules portent la même identification TAL.')
        indexed[key] = cell
    return indexed


def resolve_cells(notebook, question, role='answer', legacy=None):
    """Resolve explicit cells or, only without cell metadata, the legacy adapter."""
    indexed = validate_cell_metadata(notebook)
    # A deployment-only submission cell does not migrate legacy exercise cells.
    explicit = any(r not in {'submission', 'infrastructure'} for _, r in indexed)
    if explicit:
        cell = indexed.get((question, role))
        return [cell] if cell is not None else []
    return list(legacy(notebook, question, role)) if legacy is not None else []


def evaluation_cells(notebook):
    validate_cell_metadata(notebook)
    return [cell for cell in notebook.get('cells', [])
            if _metadata(cell).get('tal', {}).get('role') not in {'submission', 'infrastructure'}]


def resolve_notebook(notebook, expected_evaluator=None, require_metadata=True):
    """Resolve only a trusted registry entry; never derive imports from uploads."""
    if not isinstance(notebook, dict):
        raise ContractError('Le fichier ne contient pas un notebook valide.')
    metadata = _metadata(notebook)
    strict_v2 = any(entry['evaluator'] == expected_evaluator and entry['evaluator'] in STRICT_V2
                    for entry in load_catalog() if entry['active']) if expected_evaluator else False
    require_metadata = require_metadata or strict_v2
    if (require_metadata or 'tal' in metadata) and not isinstance(notebook.get('cells'), list):
        raise ContractError('Le notebook doit contenir une liste de cellules.')
    if 'tal' not in metadata:
        if require_metadata:
            raise ContractError(WRONG_VERSION)
        validate_cell_metadata(notebook)
        return None
    contract = metadata['tal']
    if (not isinstance(contract, dict) or not isinstance(contract.get('id'), str)
            or type(contract.get('version')) is not int
            or not isinstance(contract.get('evaluator'), (str, type(None)))):
        raise ContractError(WRONG_VERSION)
    entry = next((entry for entry in load_catalog() if entry['id'] == contract['id']), None)
    if entry is None:
        raise ContractError('Ce notebook ne correspond à aucun sujet enregistré.')
    if not entry['active']:
        raise ContractError('Le dépôt de ce sujet n’est pas activé. Contactez l’enseignant.')
    if contract['version'] != entry['version']:
        raise ContractError(WRONG_VERSION)
    if contract.get('evaluator') != entry['evaluator']:
        raise ContractError('L’identifiant et le correcteur du notebook sont incohérents.')
    if expected_evaluator is not None and expected_evaluator != entry['evaluator']:
        raise ContractError('Ce notebook ne correspond pas au dépôt sélectionné. Utilisez le dépôt automatique.')
    if entry['evaluator'] in STRICT_V2:
        _strict_cell_contract(notebook, entry['evaluator'])
    else:
        validate_cell_metadata(notebook)
    return dict(entry)


def _strict_cell_contract(notebook, evaluator):
    """A complete cell contract is required even when all responses are blank."""
    try:
        index = validate_cell_metadata(notebook)
        questions = {(f'Q{q}', 'answer') for q in range(1, QUESTION_COUNTS[evaluator] + 1)}
        answers = {key for key in index if key[1] == 'answer'}
        identities = {key for key in index if key[1] == 'identification'}
        if answers != questions or identities != {('identity', 'identification')}:
            raise ContractError(WRONG_VERSION)
        if any(index[key].get('cell_type') != 'code'
               for key in questions | identities):
            raise ContractError(WRONG_VERSION)
        return index
    except (ContractError, KeyError) as exc:
        raise ContractError(WRONG_VERSION) from exc


def literal_identity(source, fields=('nom', 'prenom', 'classe'), strict=False):
    """Read exact, top-level literal assignments without evaluating any code."""
    if isinstance(source, list) and all(isinstance(part, str) for part in source):
        source = ''.join(source)
    if not isinstance(source, str) or len(source) > 100000:
        raise ValueError('Cellule d’identification invalide.')
    tree = ast.parse(source)
    info = {}
    for node in tree.body:
        targets = node.targets if isinstance(node, ast.Assign) else (
            [node.target] if isinstance(node, ast.AnnAssign) else [])
        for target in targets:
            if isinstance(target, ast.Name) and target.id in fields:
                if strict and target.id in info:
                    raise ValueError('Une seule affectation est attendue pour chaque champ d’identification.')
                # A non-literal reassignment cannot leave an earlier valid identity.
                info[target.id] = node.value.value if isinstance(node.value, ast.Constant) else None
    return info


def strict_contract_identity(notebook, evaluator=None):
    """Gate supported S1/S3 v2 and return the four required identity fields before correction."""
    entry = resolve_notebook(notebook, expected_evaluator=evaluator, require_metadata=True)
    if entry['evaluator'] not in STRICT_V2 or entry['version'] != 2:
        raise ContractError(WRONG_VERSION)
    index = _strict_cell_contract(notebook, entry['evaluator'])
    fields = ('nom', 'prenom', 'classe', 'numero_etudiant')
    try:
        info = literal_identity(index[('identity', 'identification')].get('source', ''),
                                fields, strict=True)
        if any(not isinstance(info.get(key), str) or not info[key].strip()
               or info[key].strip() in {'...', 'NON_RENSEIGNE', 'NON_RENSEIGNEE'}
               for key in fields):
            raise ValueError('Complétez nom, prénom, classe et numéro étudiant dans la cellule d’identification.')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', info['numero_etudiant'].strip()):
            raise ValueError('Numéro étudiant invalide : utilisez lettres, chiffres, tiret ou soulignement.')
    except (ValueError, TypeError, SyntaxError, RecursionError) as exc:
        raise ContractError(str(exc)) from exc
    return {key: info[key].strip() for key in fields}


def s3_contract_identity(notebook, evaluator=None):
    """Compatibility entry point for the existing S3 engines."""
    return strict_contract_identity(notebook, evaluator)
