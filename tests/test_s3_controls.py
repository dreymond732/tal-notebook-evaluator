"""Contrôles cumulatifs : traces privées, score provisoire, aucun code exécuté."""
import copy
import csv
import importlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from app import create_app
import outils
import routes
from s3_audit import same
from s3_controls import check_control


def trace(control, q, value):
    return {'cell_type': 'code', 'source': f'print("S3_C{control}_Q{q}:", json.dumps(resultat_q{q}, ensure_ascii=False))',
            'outputs': [{'output_type': 'stream', 'name': 'stdout', 'text': f'S3_C{control}_Q{q}: ' + json.dumps(value, ensure_ascii=False) + '\n'}]}


def notebook(cells):
    return json.dumps({'nbformat': 4, 'nbformat_minor': 5, 'cells': cells})


class ControlTraceTests(unittest.TestCase):
    checks = [{'label': 'Mesure', 'validate': lambda v, context: same(v, {'n': 3}), 'feedback': 'Critère privé'}] * 7

    def evaluate(self, cells):
        return check_control(notebook(cells), 'copie.ipynb', 1, self.checks)

    def test_score_weight_metadata_and_no_human_quality_points(self):
        result = self.evaluate([trace(1, q, {'n': 3}) for q in range(1, 8)])
        self.assertEqual((result[0], result[2], result[4]), (20, 20, None))
        self.assertEqual([d['max_points'] for d in result[1]], [2, 3, 3, 3, 3, 3, 3])
        self.assertEqual(result[3]['score_nature'], 'technique_provisoire')
        self.assertEqual(result[3]['relecture_humaine'], 'requise')
        self.assertEqual(self.evaluate([trace(1, 1, {'n': 3})])[0], 2)
        self.assertEqual(self.evaluate([trace(1, 2, {'n': 3})])[0], 3)

    def test_no_execution_and_forgery_limit(self):
        item = trace(1, 1, {'n': 3})
        item['source'] = "raise RuntimeError('NE JAMAIS EXECUTER')\n" + item['source']
        self.assertEqual(self.evaluate([item])[0], 2)
        from s3_controls import HUMAN_REVIEW
        self.assertIn('authenticité', HUMAN_REVIEW)

    def test_invalid_duplicate_nonfinite_wrong_source_and_bool_are_rejected(self):
        item = trace(1, 1, {'n': 3})
        td_item = copy.deepcopy(item)
        td_item['source'] = td_item['source'].replace('S3_C1', 'S3_TD1')
        source_only = dict(item, outputs=[])
        output_only = dict(item, source='resultat_q1 = {}')
        markdown = dict(item, cell_type='markdown')
        error = copy.deepcopy(item)
        error['outputs'].append({'output_type': 'error', 'ename': 'ValueError'})
        for cells in ([item, item], [source_only, output_only], [markdown], [error], [td_item], [trace(2, 1, {'n': 3})], [trace(1, 1, {'n': True})]):
            self.assertEqual(self.evaluate(cells)[0], 0)
        for payload in ('{"n":NaN}', '{"n":3,"n":3}', 'null', '"ok"'):
            broken = copy.deepcopy(item)
            broken['outputs'][0]['text'] = 'S3_C1_Q1: ' + payload
            self.assertEqual(self.evaluate([broken])[0], 0)

    def test_malformed_notebook_returns_controlled_error(self):
        for raw in ('{', '[]', '{"cells":[null]}', '{"cells":[{"source":[42]}]}'):
            result = check_control(raw, 'copie.ipynb', 1, self.checks)
            self.assertEqual((result[0], result[2]), (0, 20))
            self.assertTrue(result[4])


class ControlRouteTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        p = patch.object(outils, 'BASE_DIR', self.directory.name)
        p.start()
        self.addCleanup(p.stop)
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_seven_real_subjects_modules_get_post_selector_proxy_and_private_persistence(self):
        selector = self.client.get('/', headers={'X-Forwarded-Prefix': '/universite/tal'}).get_data(as_text=True)
        for n in range(1, 8):
            with self.subTest(control=n):
                identifier = f'controle-td{n}-s3'
                self.assertEqual(routes.EVALUATOR_MODES[identifier], 'controle')
                module = importlib.import_module(routes.EVALUATORS[identifier][1])
                self.assertEqual(module.MAX_SCORE_TOTAL, 20)
                self.assertIn('/universite/tal/eval/' + identifier, selector)
                response = self.client.get('/eval/' + identifier, headers={'X-Forwarded-Prefix': '/universite/tal'})
                self.assertEqual(response.status_code, 200)
                self.assertIn('action="/universite/tal/eval/' + identifier, response.get_data(as_text=True))
                paths = list((ROOT / 'Notebooks contrôles finaux/S3').glob(f'Controle_TD{n}_S3*.ipynb'))
                self.assertEqual(len(paths), 1)
                nb = json.loads(paths[0].read_text())
                identity = next(c for c in nb['cells'] if c['cell_type'] == 'code' and 'Complétez les informations entre les guillemets.' in ''.join(c['source']))
                source = ''.join(identity['source'])
                for k, v in [('nom', 'Exemple'), ('prenom', 'Alice'), ('classe', 'S3')]:
                    source = re.sub(rf'(?m)^{k}\s*=.*$', f'{k} = "{v}"', source)
                identity['source'] = source
                nb['cells'].append(trace(n, 1, {'private': '<script>SECRET_COPIE</script>'}))
                payload = json.dumps(nb).encode()
                response = self.client.post('/eval/' + identifier, data={'file': (io.BytesIO(payload), 'copie.ipynb')}, content_type='multipart/form-data')
                public = response.get_data(as_text=True)
                self.assertIn('Copie reçue et enregistrée', public)
                for secret in ('SECRET_COPIE', 'Score technique', 'Critère technique', '✅', '❌'):
                    self.assertNotIn(secret, public)
                base = Path(self.directory.name) / identifier / 'S3'
                report_path = next(base.rglob('*.html'))
                report = report_path.read_text()
                self.assertIn('Score technique provisoire', report)
                self.assertIn('Relecture humaine', report)
                self.assertNotIn('<script>SECRET_COPIE</script>', report)
                self.assertEqual(next(base.rglob('*.ipynb')).read_bytes(), payload)
                rows = list(csv.reader(io.StringIO(next(base.rglob('*.csv')).read_text()), delimiter=';'))
                self.assertIn('Nature du score', rows[0])
                self.assertIn('technique_provisoire', rows[1])
                self.assertIn('requise', rows[1])
                self.assertEqual(self.client.get('/soumissions/' + str(report_path.relative_to(Path(self.directory.name)))).status_code, 404)

    def test_private_report_escapes_student_trace(self):
        details = [{'check': 'Mesure', 'student_answer': '<script>SECRET</script>', 'correct_answer': 'GOLD_PRIVE', 'status': '❌', 'points': 0, 'max_points': 2}]
        result = (0, details, 20, {'nom': 'X', 'prenom': 'Y', 'classe': 'S3', 'score_nature': 'technique_provisoire', 'score_max': 20, 'relecture_humaine': 'requise'}, None)
        from types import SimpleNamespace
        with patch.object(routes, 'import_module', return_value=SimpleNamespace(check_notebook=lambda *args: result)):
            response = self.client.post('/eval/controle-td1-s3', data={'file': (io.BytesIO(b'{}'), 'copie.ipynb')}, content_type='multipart/form-data')
        public = response.get_data(as_text=True)
        self.assertNotIn('GOLD_PRIVE', public)
        report = next(Path(self.directory.name).rglob('*.html')).read_text()
        self.assertIn('&lt;script&gt;SECRET&lt;/script&gt;', report)
        self.assertNotIn('<script>', report)
        self.assertIn('GOLD_PRIVE', report)


class LinguisticContractTests(unittest.TestCase):
    def test_original_split_case_and_lower_frequencies_are_distinct(self):
        from collections import Counter
        from s3_controls_data import C1
        from s3_controls_linguistic import c1q1
        source = C1['texte_musee']
        value = {'caracteres': len(source), 'split': source.split(), 'frequences': dict(Counter(source.lower().split())), 'formes': len(set(source.lower().split()))}
        self.assertTrue(c1q1(value, {}))
        value['split'] = source.lower().split()
        self.assertFalse(c1q1(value, {}))

    def test_annotation_offsets_full_coverage_flags_and_alternative_pos(self):
        from s3_controls_linguistic import annotations
        source = 'La porte.'
        rows = [dict(forme=form, lemme=lemma, pos=pos, tag=pos, debut=start, fin=end, ponctuation=punct, espace=False, mot_vide=False)
                for form, lemma, pos, start, end, punct in [('La', 'le', 'DET', 0, 2, False), ('porte', 'porte', 'NOUN', 3, 8, False), ('.', '.', 'PUNCT', 8, 9, True)]]
        self.assertTrue(annotations(rows, source))
        changed = copy.deepcopy(rows)
        changed[1]['lemme'], changed[1]['pos'] = 'porter', 'VERB'
        self.assertTrue(annotations(changed, source))  # qualité linguistique explicitement humaine
        self.assertFalse(annotations(rows[:-1], source))
        changed[1]['debut'] = 4
        self.assertFalse(annotations(changed, source))
        changed = copy.deepcopy(rows)
        changed[0]['mot_vide'] = 1
        self.assertFalse(annotations(changed, source))
        self.assertTrue(annotations([], ''))

    def test_dependency_requires_two_tokens_in_second_sentence(self):
        from s3_controls_data import C1
        from s3_controls_linguistic import c1q5
        source = C1['texte_musee']
        rows = []
        for match in re.finditer(r"\w+|[^\w\s]", source):
            form = match[0]
            pos = 'VERB' if form == 'observe' else ('PUNCT' if not form.isalnum() else 'NOUN')
            rows.append(dict(forme=form, lemme=form.lower(), pos=pos, tag=pos, debut=match.start(), fin=match.end(), ponctuation=pos == 'PUNCT', espace=False, mot_vide=False))
        value = dict(verbe='observe', verbe_debut=source.index('observe'), dependant='visiteuse', dependant_debut=source.index('visiteuse'), relation='nsubj')
        self.assertTrue(c1q5(value, {2: {'annotations': rows}}))
        value['dependant'], value['dependant_debut'] = value['verbe'], value['verbe_debut']
        self.assertFalse(c1q5(value, {2: {'annotations': rows}}))

    def test_manual_gold_frequencies_exclusion_empty_and_bool(self):
        from s3_controls_linguistic import c2q5
        value = {'noms': {'marin': 1, 'caisse': 2}, 'verbes': {'charger': 1, 'rester': 1}, 'combine': {'marin': 1, 'caisse': 2, 'charger': 1, 'rester': 1}, 'exclus': {'marin': 1, 'charger': 1, 'rester': 1}, 'vide': {}}
        self.assertTrue(c2q5(value, {}))
        value['exclus']['caisse'] = 2
        self.assertFalse(c2q5(value, {}))
        del value['exclus']['caisse']
        value['noms']['marin'] = True
        self.assertFalse(c2q5(value, {}))

    def test_concordance_oracle_handles_substrings_repeats_and_empty_pattern(self):
        from s3_controls_linguistic import c3q6
        value = {'tests': [
            {'id': 'T1', 'erreur': False, 'resultats': [{'debut': 0, 'fin': 4, 'pivot': 'plan', 'gauche': '', 'droite': ' pl'}, {'debut': 5, 'fin': 9, 'pivot': 'plan', 'gauche': 'an ', 'droite': ''}]},
            {'id': 'T2', 'erreur': False, 'resultats': [{'debut': 0, 'fin': 4, 'pivot': 'plan', 'gauche': '', 'droite': 'tati'}, {'debut': 11, 'fin': 15, 'pivot': 'plan', 'gauche': 'ion ', 'droite': ''}]},
            {'id': 'T3', 'erreur': False, 'resultats': []}, {'id': 'T4', 'erreur': True, 'resultats': []}]}
        self.assertTrue(c3q6(value, {}))
        value['tests'].reverse()
        self.assertTrue(c3q6(value, {}))
        value['tests'][-1]['resultats'].pop()
        self.assertFalse(c3q6(value, {}))

    def test_citations_are_exact_not_normalized_and_free_id_order(self):
        from s3_controls_data import C3
        from s3_controls_linguistic import c3q4
        value = {'citations': [dict(q, debut=C3['texte_patrimoine'].find(q['citation']), exacte=q['id'] == 'P1') for q in C3['citations']]}
        self.assertTrue(c3q4(value, {}))
        value['citations'].reverse()
        self.assertTrue(c3q4(value, {}))
        value['citations'][2]['exacte'] = True  # P2 ne devient pas exacte par normalisation implicite
        self.assertFalse(c3q4(value, {}))

    def test_subject_corpora_match_backend_without_executing_code(self):
        import ast
        from s3_controls_data import C1, C2, C3
        for n, contract in enumerate([C1, C2, C3], 1):
            nb = json.loads((ROOT / f'Notebooks contrôles finaux/S3/Controle_TD{n}_S3.ipynb').read_text())
            found = {}
            for cell in nb['cells']:
                if cell['cell_type'] != 'code':
                    continue
                try:
                    tree = ast.parse(''.join(cell['source']))
                except SyntaxError:
                    continue
                for statement in tree.body:
                    if isinstance(statement, ast.Assign):
                        for target in statement.targets:
                            if isinstance(target, ast.Name) and target.id in contract:
                                try:
                                    found[target.id] = ast.literal_eval(statement.value)
                                except (ValueError, TypeError):
                                    pass
            for name, expected in contract.items():
                if name == 'expression':  # consigne textuelle
                    continue
                self.assertEqual(found.get(name), expected, (n, name))


class QuantitativeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads((ROOT / 'tests/fixtures/s3_controls_quantitative_expected.json').read_text())

    def evaluate(self, control, values):
        module = importlib.import_module(f'app_correction_Controle_TD{control}_S3')
        return module.check_notebook(notebook([trace(control, q, v) for q, v in enumerate(values, 1)]), 'copie.ipynb')

    def test_independent_designer_oracles_match_recomputed_backend_all_28_checks(self):
        # Les valeurs arrondies proviennent du contrat Designer ; le backend les recalcule.
        from s3_controls_quantitative import EXPECTED
        for n in range(4, 8):
            values = [self.expected[str(n)][f'Q{q}'] for q in range(1, 8)]
            self.assertEqual(self.evaluate(n, values)[0], 20, n)
            self.assertEqual(self.evaluate(n, EXPECTED[n])[0], 20, ('non arrondi', n))

    def test_union_sum_positional_pairs_and_expressions_are_distinct(self):
        values = [copy.deepcopy(self.expected['4'][f'Q{q}']) for q in range(1, 8)]
        values[2]['union'] = values[2]['somme_paires']
        values[3]['k3']['paires'] = [[0, 3]]
        values[5]['expressions'].append([1, 0])  # accès ... libre n'est pas contigu
        self.assertEqual(self.evaluate(4, values)[0], 11)

    def test_denominator_zero_bool_and_contingency_errors_are_rejected(self):
        values = [copy.deepcopy(self.expected['5'][f'Q{q}']) for q in range(1, 8)]
        values[0]['cooc'] = True
        values[1]['table'][1][1] = 0
        values[4]['sans_pivot'] = 0
        self.assertEqual(self.evaluate(5, values)[0], 12)

    def test_visual_tables_require_positions_denominators_and_exact_passages(self):
        values = [copy.deepcopy(self.expected['6'][f'Q{q}']) for q in range(1, 8)]
        values[1]['tailles_alpha'][0] = values[1]['tailles_flux'][0]
        values[4]['concordances'][1]['passage'] = 'discute une affiche . Un'
        self.assertEqual(self.evaluate(6, values)[0], 14)

    def test_unknown_protocol_never_gets_binary_verdict_and_transfer_is_checked(self):
        values = [copy.deepcopy(self.expected['7'][f'Q{q}']) for q in range(1, 8)]
        values[3]['verdicts']['M3'] = 'compatible selon le protocole'
        values[6]['audit_jardin'][0]['mesure_union']['cooc'] = 3
        self.assertEqual(self.evaluate(7, values)[0], 14)

    def test_numeric_tolerance_finite_types_and_key_order(self):
        from s3_controls_quantitative import equivalent
        self.assertTrue(equivalent(0.333333, 1/3))
        self.assertFalse(equivalent(0.333, 1/3))
        self.assertFalse(equivalent(True, 1))
        self.assertFalse(equivalent(True, 1.0))
        self.assertFalse(equivalent(float('nan'), 1.0))
        self.assertTrue(equivalent({'b': 2, 'a': 1}, {'a': 1, 'b': 2}))

    def test_all_quantitative_notebook_data_match_fixed_corpora(self):
        import ast
        import s3_controls_data
        for n in range(4, 8):
            expected = getattr(s3_controls_data, 'C' + str(n))
            nb = json.loads((ROOT / f'Notebooks contrôles finaux/S3/Controle_TD{n}_S3.ipynb').read_text())
            found = {}
            for item in nb['cells']:
                if item['cell_type'] != 'code':
                    continue
                try:
                    tree = ast.parse(''.join(item['source']))
                except SyntaxError:
                    continue
                for node in tree.body:
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id in expected:
                                found[target.id] = ast.literal_eval(node.value)
            self.assertEqual(found, expected, n)
