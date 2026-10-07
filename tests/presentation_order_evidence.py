"""Frozen parent and narrow reversible title move for historical comparisons.

This helper does not call the production migrator. Historical fixtures remain
unchanged. The dedicated presentation test checks the new tree against parent.
"""
import copy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'tests/fixtures/presentation_order_source_baseline.json'
RENAMED = {
    'Notebooks TD/S3/TD1_S3_fondations_spacy.ipynb': 'Notebooks TD/S3/TD1.a_S3_fondations_spacy.ipynb',
    'Notebooks TD/S3/R1_S3_doc_spacy.ipynb': 'Notebooks TD/S3/TD1.b_S3_doc_spacy.ipynb',
    'Notebooks TD/S3/TD1B_S3_entites_similarite_regles.ipynb': 'Notebooks TD/S3/TD1.c_S3_entites_similarite_regles.ipynb',
}


def current_path(path):
    return RENAMED.get(path, path)


def parent_raw(path):
    return json.loads(SNAPSHOT.read_text())['subjects'][path]


def before_title_move(notebook, path):
    """Undo only the exact H1 relocation, with all current prose preserved."""
    previous = json.loads(parent_raw(path))
    original_intro = next(c for c in previous['cells'][1:] if c['cell_type'] == 'markdown'
                          and re.match(r'\A[ \t\r\n]*# ', ''.join(c['source'])))
    original_source = ''.join(original_intro['source'])
    match = re.match(r'\A([ \t\r\n]*)(#[ \t]+[^\n]+)(?:\n|$)', original_source)
    result = copy.deepcopy(notebook)
    source = ''.join(result['cells'][0]['source'])
    prefix = match[2] + '\n\n'
    if not source.startswith(prefix):
        raise AssertionError(f'Unexpected first heading: {path}')
    result['cells'][0]['source'] = source[len(prefix):].splitlines(keepends=True)
    intro_index = previous['cells'].index(original_intro)
    intro = result['cells'][intro_index]
    if intro.get('id') != original_intro.get('id') or intro['metadata'] != original_intro['metadata']:
        raise AssertionError(f'Introduction identity changed: {path}')
    text = ''.join(intro['source'])
    leading = match[1]
    if not text.startswith(leading):
        raise AssertionError(f'Introduction whitespace changed: {path}')
    restored = leading + match[2] + '\n' + text[len(leading):]
    intro['source'] = restored.splitlines(keepends=True) if isinstance(intro['source'], list) else restored
    return result
