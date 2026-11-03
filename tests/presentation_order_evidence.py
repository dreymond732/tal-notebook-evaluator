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


def s1_current_path(path):
    """Translate only current S1 source paths; frozen fixture keys stay intact."""
    import re
    if not path.startswith("Notebooks TD/S1/"):
        return path
    path = re.sub(r"TD([1-7])_S1_([^/]+\.ipynb)",
                  lambda m: f"S1_TD{m[1]}_{m[2]}", path)
    def variant(match):
        n, label, detail = match.groups()
        v = label if n == "3" else {"one": "A", "bis": "B", "ter": "C"}[label]
        return f"S1_TD{n}_{v}_{detail}"
    path = re.sub(r"TD([3-6])-(one|bis|ter)_S1_([^/]+\.ipynb)", variant, path)
    return path


def s1_legacy_path(path):
    """Inverse map for comparison against immutable historical fixtures."""
    import re
    if not path.startswith("Notebooks TD/S1/"):
        return path
    def variant(match):
        n, label, detail = match.groups()
        v = label if n == "3" else {"A": "one", "B": "bis", "C": "ter"}[label]
        return f"TD{n}-{v}_S1_{detail}"
    path = re.sub(r"S1_TD([3-6])_(one|bis|ter|A|B|C)_([^/]+\.ipynb)", variant, path)
    path = re.sub(r"S1_TD([1-7])_([^/]+\.ipynb)",
                  lambda m: f"TD{m[1]}_S1_{m[2]}", path)
    return path


def current_path(path):
    return s1_current_path(RENAMED.get(path, path))


def parent_raw(path):
    original = s1_legacy_path(path)
    return json.loads(SNAPSHOT.read_text())['subjects'][original]


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
    if s1_legacy_path(path) != path:
        # Les nouveaux titres S1 diffèrent des titres historiques congelés.
        expected = re.match(r'\A(#[^\n]+\n\n)', source)
        if expected and expected[1].startswith('# S1 — TD'):
            prefix = expected[1]
    if not source.startswith(prefix):
        raise AssertionError(f'Unexpected first heading: {path}')
    result['cells'][0]['source'] = source[len(prefix):].splitlines(keepends=True)
    if s1_legacy_path(path) != path:
        result['metadata']['tal_tutor']['session']['notebook'] = s1_legacy_path(path)
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
