"""Trusted notebook catalogue and inert, explicit cell identification.

Metadata is routing information, never permission to import a module or run code.
Old notebooks remain supported only on an explicitly selected legacy route.
"""
import json
from pathlib import Path


class ContractError(ValueError):
    """An uploaded notebook cannot be resolved unambiguously."""


CELL_ROLES = frozenset({'answer', 'prompt', 'example', 'provided',
                        'identification', 'submission', 'infrastructure'})


def load_catalog():
    data = json.loads(Path(__file__).with_name('notebook_catalog.json').read_text(encoding='utf-8'))
    if data.get('schema_version') != 1 or not isinstance(data.get('notebooks'), list):
        raise ValueError('Catalogue TAL invalide.')
    entries = data['notebooks']
    ids, paths, evaluators = set(), set(), set()
    for entry in entries:
        if (not isinstance(entry, dict) or not isinstance(entry.get('id'), str)
                or not entry['id'] or entry['id'] in ids
                or entry.get('version') != 1 or type(entry['version']) is not int
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
    if (require_metadata or 'tal' in metadata) and not isinstance(notebook.get('cells'), list):
        raise ContractError('Le notebook doit contenir une liste de cellules.')
    validate_cell_metadata(notebook)
    if 'tal' not in metadata:
        if require_metadata:
            raise ContractError("Ce notebook ne contient pas d’identifiant TAL. Utilisez le dépôt de son semestre pour une ancienne version.")
        return None
    contract = metadata['tal']
    if (not isinstance(contract, dict) or not isinstance(contract.get('id'), str)
            or type(contract.get('version')) is not int
            or not isinstance(contract.get('evaluator'), (str, type(None)))):
        raise ContractError('Identification TAL invalide ou incomplète.')
    entry = next((entry for entry in load_catalog() if entry['id'] == contract['id']), None)
    if entry is None:
        raise ContractError('Ce notebook ne correspond à aucun sujet enregistré.')
    if not entry['active']:
        raise ContractError('Le dépôt de ce sujet n’est pas activé. Contactez l’enseignant.')
    if contract['version'] != entry['version']:
        raise ContractError('Cette version du notebook n’est pas prise en charge.')
    if contract.get('evaluator') != entry['evaluator']:
        raise ContractError('L’identifiant et le correcteur du notebook sont incohérents.')
    if expected_evaluator is not None and expected_evaluator != entry['evaluator']:
        raise ContractError('Ce notebook ne correspond pas au dépôt sélectionné. Utilisez le dépôt automatique.')
    return dict(entry)
