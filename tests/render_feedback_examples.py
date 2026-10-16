"""Generate two anonymous illustrative reports; submitted code is never run.

Usage: python tests/render_feedback_examples.py --output-dir /tmp/tal-feedback
The S1 saved traces come from independent regression fixtures. The S3 example
intentionally contains a saved error and no usable quantitative trace.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from flask import render_template
from app import create_app
from notebook_contract import load_catalog
from routes import EVALUATORS
from test_s1_report_feedback import subject
from test_s1_v2_results import notebook as saved_s1_answers


def render_examples(destination):
    destination.mkdir(parents=True, exist_ok=True)
    s1 = subject(1)
    saved = saved_s1_answers(1)['cells']
    for cell in s1['cells']:
        tag = cell.get('metadata', {}).get('tal', {})
        if tag.get('role') == 'answer':
            cell.update(copy.deepcopy(saved[int(tag['question'][1:]) - 1]))
    entry = next(e for e in load_catalog() if e['evaluator'] == 'td1-s3')
    s3 = json.loads((ROOT / entry['notebook']).read_text())
    for cell in s3['cells']:
        tag = cell.get('metadata', {}).get('tal', {})
        if tag.get('role') == 'identification':
            cell['source'] = 'nom="Exemple"\nprenom="Alex"\nclasse="Demonstration"\nnumero_etudiant="DEMO001"'
        if tag.get('question') == 'Q1' and tag.get('role') == 'answer':
            cell['source'] = 'annotations = []\nfor token in doc:\n    annotations.append(token.text)\nprint(annotations)'
            cell['outputs'] = [{'output_type': 'error', 'ename': 'NameError',
                                'evalue': "name 'doc' is not defined", 'traceback': []}]
    app = create_app()
    for evaluator, notebook in [('td1-s1', s1), ('td1-s3', s3)]:
        from importlib import import_module
        score, details, maximum, info, error = import_module(EVALUATORS[evaluator][1]).check_notebook(json.dumps(notebook), 'exemple.ipynb')
        if error:
            raise RuntimeError(error)
        if evaluator == 'td1-s1' and score != maximum:
            raise RuntimeError('The illustrative successful copy must get all points.')
        with app.test_request_context('/eval/' + evaluator, environ_base={'SCRIPT_NAME': '/universite/tal'}):
            html = render_template('corrector_template.html', display_name=EVALUATORS[evaluator][0],
                evaluator_name=evaluator, allowed_extension='.ipynb', score=score, details=details,
                max_score=maximum, student_info=info, is_td=True)
        path = destination / ('rapport_' + evaluator.replace('-', '_') + '.html')
        html = html.replace('<body>', '<body><p role="note" style="text-align:center">Exemple synthétique de restitution — aucune copie étudiante réelle.</p>', 1)
        path.write_text(html)
        print(f'{path}: {score}/{maximum}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    render_examples(parser.parse_args().output_dir)
