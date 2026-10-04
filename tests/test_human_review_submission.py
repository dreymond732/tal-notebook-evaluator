"""TD1B's former manual-only contract is retired, without silent v2 fallback."""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from app import create_app
import outils
import prepare_student_notebooks as prep
import routes
from notebook_contract import ContractError, load_catalog, resolve_notebook
import app_correction_TD1B_S3 as grader


def values():
    return [
        {'texte': grader.TEXT1, 'entites': copy.deepcopy(grader.ENTITIES1)},
        {'texte': grader.TEXT2, 'entites': copy.deepcopy(grader.ENTITIES2),
         'selection': grader.selection(grader.ENTITIES2),
         'essai': {'texte': 'Lina parle à Paris.', 'entites': [['Lina', 'PER'], ['Paris', 'LOC']], 'selection': [['Lina', 'PER']]}},
        {'vecteurs': {'chien': True, 'chat': True, 'voiture': True}, 'scores': dict(grader.SCORES),
         'variation': {'original': grader.PHRASES[0], 'modifie': 'Le chat ne dort pas sur le tapis.', 'score': 0.9}},
        {'texte': grader.TEXT4, 'avant': copy.deepcopy(grader.ENTITIES4), 'apres': copy.deepcopy(grader.ENTITIES4),
         'pipeline': ['tok2vec', 'morphologizer', 'parser', 'attribute_ruler', 'lemmatizer', 'entity_ruler', 'ner'],
         'regles': [{'label': 'ORG', 'pattern': 'Université de Toulon'}, {'label': 'ORG', 'pattern': 'Atelier Orion'},
                    {'label': 'LOC', 'pattern': 'Plage bleue'}, {'label': 'DATE', 'pattern': '12 juin 2025'}],
         'essais': [{'texte': t, 'sans_regles': [], 'avec_regles': rows} for t, rows in [
             ('Université de Toulon', [['Université de Toulon', 'ORG']]),
             ('Atelier Orion', [['Atelier Orion', 'ORG']]), ('Plage bleue', [['Plage bleue', 'LOC']]),
             ('12 juin 2025', [['12 juin 2025', 'DATE']]), ('atelier orion change de sens', [])]]}]


def notebook(records=None):
    cells = [{'cell_type': 'code', 'metadata': {'tal': {'question': 'identity', 'role': 'identification'}},
              'source': 'nom="Exemple"\nprenom="Test"\nclasse="S3"\nnumero_etudiant="E1"', 'outputs': []}]
    for q, value in enumerate(values() if records is None else records, 1):
        cells.append({'cell_type': 'code', 'id': f'answer-q{q}',
          'metadata': {'tal': {'question': f'Q{q}', 'role': 'answer'}},
          'source': f'raise RuntimeError("NEVER_EXECUTE")\nprint("S3_TD1B_Q{q}:", resultat)',
          'outputs': [{'output_type': 'stream', 'name': 'stdout', 'text': f'S3_TD1B_Q{q}: '+json.dumps(value)+'\n'}]})
    return {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {'tal': {
        'id': 'td1b-s3', 'evaluator': 'td1b-s3', 'version': 3}}, 'cells': cells}


class CompanionContractTests(unittest.TestCase):
    def test_catalog_routes_and_version(self):
        entry = resolve_notebook(notebook())
        self.assertEqual((entry['version'], entry['evaluator']), (3, 'td1b-s3'))
        self.assertFalse(any(e.get('assessment') == 'human_review' for e in load_catalog()))
        self.assertEqual(len(routes.EVALUATORS), 34)
        routes.validate_evaluator_semesters()
        for version in (None, 1, 2, True, '3', 4):
            nb = notebook(); nb['metadata']['tal']['version'] = version
            with self.subTest(version=version), self.assertRaisesRegex(ContractError, '^mauvaise version du notebook$'):
                resolve_notebook(nb)
        nb = notebook(); nb['metadata']['tal'].update(version=2, evaluator=None)
        self.assertEqual(grader.check_notebook(json.dumps(nb), 'old.ipynb')[4], 'mauvaise version du notebook')

    def test_blank_and_missing_duplicate_cross_question_evidence(self):
        result = grader.check_notebook(json.dumps(notebook()), 'copy.ipynb')
        self.assertEqual((result[0], result[2], result[4]), (4, 4, None))
        self.assertEqual(result[3]['contract_version'], 3)
        self.assertEqual(result[3]['relecture_humaine'], 'facultative')
        for change in ('empty', 'comment', 'duplicate', 'wrong_prefix', 'error', 'html', 'bad_json'):
            nb = notebook(); cell = nb['cells'][1]
            if change == 'empty': cell['outputs'] = []
            elif change == 'comment': cell['source'] = '# '+cell['source'].replace('\n', '\n# ')
            elif change == 'duplicate': cell['outputs'] *= 2
            elif change == 'wrong_prefix': cell['outputs'][0]['text'] = cell['outputs'][0]['text'].replace('TD1B', 'TD1')
            elif change == 'error': cell['outputs'].append({'output_type': 'error', 'ename': 'ValueError'})
            elif change == 'html': cell['outputs'] = [{'output_type': 'display_data', 'data': {'text/html': 'S3_TD1B_Q1: '+json.dumps(values()[0])}}]
            else: cell['outputs'][0]['text'] = 'S3_TD1B_Q1: {"entites": NaN}'
            with self.subTest(change=change): self.assertEqual(grader.check_notebook(json.dumps(nb), 'copy.ipynb')[0], 3)
        for change in ('missing', 'duplicate', 'markdown'):
            nb = notebook()
            if change == 'missing': nb['cells'].pop()
            elif change == 'duplicate': nb['cells'].append(copy.deepcopy(nb['cells'][-1]))
            else: nb['cells'][-1]['cell_type'] = 'markdown'
            self.assertEqual(grader.check_notebook(json.dumps(nb), 'x')[4], 'mauvaise version du notebook')

    def test_wrong_results_and_technical_limits(self):
        mutations = [lambda v: v[0]['entites'].append(['2024', 'DATE']),
                     lambda v: v[1]['selection'].append(['Paris', 'LOC']),
                     lambda v: v[1]['essai']['selection'].clear(),
                     lambda v: v[2]['scores'].update(chien_chat=True),
                     lambda v: v[2]['scores'].update(chien_chat=0.1),
                     lambda v: v[2]['variation'].update(score=1.01),
                     lambda v: v[3]['pipeline'].reverse(),
                     lambda v: v[3]['essais'].pop(),
                     lambda v: v[3]['essais'][3].update(avec_regles=[]),
                     lambda v: v[3]['essais'][3].update(sans_regles=[['12 juin 2025', 'DATE']]),
                     lambda v: v[3]['essais'][0].update(avec_regles=[['Inventé', 'ORG']])]
        for change in mutations:
            record = values(); change(record)
            self.assertEqual(grader.check_notebook(json.dumps(notebook(record)), 'x')[0], 3)
        record = values(); record[2]['scores'] = {k: round(v, 5) for k,v in record[2]['scores'].items()}
        # Free model predictions are not claimed to be recalculated server-side.
        record[1]['essai'].update(entites=[], selection=[])
        record[3]['regles'].append({'label': 'PER', 'pattern': 'Personne supplémentaire'})
        self.assertEqual(grader.check_notebook(json.dumps(notebook(record)), 'x')[0], 4)

    def test_upload_metadata_cannot_reactivate_manual_review(self):
        nb = notebook(); nb['metadata']['tal']['assessment'] = 'human_review'
        self.assertEqual(resolve_notebook(nb)['assessment'], 'automatic')
        nb['metadata']['tal']['evaluator'] = None
        with self.assertRaises(ContractError): resolve_notebook(nb)
        data = {'schema_version': 1, 'notebooks': load_catalog()}
        next(e for e in data['notebooks'] if e['id'] == 'td1b-s3').update(assessment='human_review', evaluator=None)
        with patch('notebook_contract.Path.read_text', return_value=json.dumps(data)), self.assertRaises(ValueError): load_catalog()

    def test_companion_distribution_retains_metadata_tutor_and_only_injects_url(self):
        entry = next(e for e in load_catalog() if e['id'] == 'td1b-s3')
        source = ROOT / entry['notebook']; original = json.loads(source.read_text())
        self.assertEqual(resolve_notebook(original)['version'], 3)
        with tempfile.TemporaryDirectory() as temporary, patch.object(prep, 'load_catalog', return_value=[entry]):
            output = Path(temporary) / 'dist'
            self.assertEqual(prep.render(output, 'https://example.test/course'), 1)
            self.assertEqual(prep.verify_rendered(output, 'https://example.test/course'), 1)
            rendered = json.loads((output / entry['notebook']).read_text())
        self.assertEqual(rendered['cells'][:-1], original['cells'][:-1])
        self.assertEqual(rendered['metadata'], original['metadata'])
        self.assertNotIn(prep.URL_PLACEHOLDER, json.dumps(rendered))


class CompanionRoutesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        base = patch.object(outils, 'BASE_DIR', str(self.root)); base.start(); self.addCleanup(base.stop)
        self.app = create_app(); self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def post(self, nb, route='/submit'):
        return self.client.post(route, data={'file': (io.BytesIO(json.dumps(nb).encode()), '../../copy.ipynb')})

    def test_real_routes_save_versioned_escaped_report_and_grade_without_execution(self):
        nb = notebook(); nb['cells'][1]['outputs'].append({'output_type': 'display_data', 'data': {'text/html': '<script>UNTRUSTED_HTML</script>'}})
        nb['cells'].append({'cell_type': 'markdown', 'id': 'note', 'metadata': {'tal_review': {'question': 'Q1'}}, 'source': 'Analyse <script>'})
        nb['cells'].append({'cell_type': 'markdown', 'id': 'bilan', 'metadata': {'tal': {'question': 'practice-bilan', 'role': 'practice'}, 'tal_review': {'question': 'bilan'}}, 'source': 'Bilan personnel <preuve>'})
        for route in ('/submit', '/eval/td1b-s3'):
            body = self.post(nb, route).get_data(as_text=True)
            self.assertIn('4.00 / 4.0', body)
            self.assertNotIn('UNTRUSTED_HTML', body)
            self.assertNotIn('Analyse <script>', body)
            self.assertIn('Analyse &lt;script&gt;', body)
            self.assertIn('Bilan personnel &lt;preuve&gt;', body)
        paths = list(self.root.rglob('*.ipynb'))
        self.assertEqual(len(paths), 1)
        self.assertIn('td1b-s3-v3', str(paths[0]))
        self.assertEqual(json.loads(paths[0].read_text()), nb)
        self.assertEqual(len(list(self.root.rglob('*.html'))), 1)
        self.assertEqual(len(list(self.root.rglob('*.csv'))), 1)
        self.assertEqual(self.client.get('/health').json['evaluators'], 34)

    def test_first_storage_failure_is_visible_without_a_score(self):
        real_open = open
        for route in ('/submit', '/eval/td1b-s3'):
            for stage in ('csv', '.ipynb', '.html'):
                # A new client/session for every failure proves no previous
                # response is needed to reveal the current request's error.
                self.client = self.app.test_client()
                def fail_write(path, *args, **kwargs):
                    if str(path).endswith(stage):
                        raise OSError('écriture impossible')
                    return real_open(path, *args, **kwargs)
                failing = (patch.object(outils, 'log_grade_to_csv', side_effect=OSError('écriture impossible'))
                           if stage == 'csv' else patch.object(routes, 'open', side_effect=fail_write, create=True))
                with self.subTest(route=route, stage=stage), failing:
                    body = self.post(notebook(), route).get_data(as_text=True)
                self.assertIn('Erreur lors de la sauvegarde', body)
                self.assertNotIn('4.00 / 4.0', body)
                self.assertNotIn('Travail reçu', body)
                # The flash is consumed by this response, not delayed to the next.
                following = self.client.get('/eval/td1b-s3').get_data(as_text=True)
                self.assertNotIn('Erreur lors de la sauvegarde', following)

    def test_v2_and_invalid_identity_do_not_save(self):
        for route in ('/submit', '/eval/td1b-s3'):
            nb = notebook(); nb['metadata']['tal'].update(version=2, evaluator=None)
            self.assertIn('mauvaise version du notebook', self.post(nb, route).get_data(as_text=True))
            nb = notebook(); nb['cells'][0]['source'] = 'nom=run_code()'
            self.post(nb, route)
        self.assertEqual(list(self.root.rglob('*')), [])
