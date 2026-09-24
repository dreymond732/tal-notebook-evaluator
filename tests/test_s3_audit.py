"""Contrat des traces S3, sécurité sans exécution et routes réelles."""
import importlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from app import create_app
import outils
import routes
from s3_audit import check_audit, same


def cell(source, output='', name='stdout'):
    return {'cell_type': 'code', 'source': source, 'outputs': [
        {'output_type': 'stream', 'name': name, 'text': output}] if output else []}


def trace(td, question, value):
    return cell(f"print('S3_TD{td}_Q{question}:', json.dumps(resultat_Q{question}, ensure_ascii=False))",
                f'S3_TD{td}_Q{question}: ' + json.dumps(value, ensure_ascii=False) + '\n')


def notebook(cells):
    return json.dumps({'nbformat': 4, 'nbformat_minor': 5, 'cells': cells})


class TraceTests(unittest.TestCase):
    checks = [{'label': 'Comptage', 'validate': lambda value: same(value, {'n': 3}),
               'feedback': 'Le comptage attendu vaut 3.'}]

    def check(self, cells, td=0):
        return check_audit(notebook(cells), 'copie.ipynb', td, self.checks)

    def test_exact_recorded_value_and_type_required(self):
        for value, expected in [({'n': 3}, 1), ({'n': 2}, 0), ({'n': True}, 0), ('ok', 0), ({'n': 3.0}, 0)]:
            self.assertEqual(self.check([trace(0, 1, value)])[0], expected)

    def test_sources_are_never_executed(self):
        item = trace(0, 1, {'n': 3})
        item['source'] = "raise RuntimeError('le serveur ne doit jamais exécuter ceci')\n" + item['source']
        self.assertEqual(self.check([item])[0], 1)

    def test_missing_duplicate_cross_cell_wrong_td_and_markdown_are_rejected(self):
        item = trace(0, 1, {'n': 3})
        markdown = dict(item, cell_type='markdown')
        for cells in [[], [item, item], [cell(item['source']), cell('x=1', item['outputs'][0]['text'])],
                      [trace(1, 1, {'n': 3})], [markdown],
                      [cell('# ' + item['source'], item['outputs'][0]['text'])]]:
            self.assertEqual(self.check(cells)[0], 0)

    def test_errors_stderr_and_invalid_source_are_rejected(self):
        error = trace(0, 1, {'n': 3})
        error['outputs'].append({'output_type': 'error', 'ename': 'ValueError'})
        stderr = trace(0, 1, {'n': 3})
        stderr['outputs'][0]['name'] = 'stderr'
        invalid = trace(0, 1, {'n': 3})
        invalid['source'] += '\nif :'
        for item in (error, stderr, invalid):
            self.assertEqual(self.check([item])[0], 0)

    def test_fragmented_stdout_is_joined_and_nonfinite_and_duplicate_keys_rejected(self):
        item = trace(0, 1, {'n': 3})
        item['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': part}
                           for part in ['S3_TD0_', 'Q1: {"n":', '3}\n']]
        self.assertEqual(self.check([item])[0], 1)
        for raw in ['{"n":NaN}', '{"n":3,"n":3}', '{not JSON}', 'ok']:
            item = cell("print('S3_TD0_Q1:', result)", 'S3_TD0_Q1: ' + raw)
            self.assertEqual(self.check([item])[0], 0)

    def test_malformed_notebook_is_controlled(self):
        for payload in ['{', '[]', '{"cells":[null]}', '{"cells":[{"source":[42]}]}',
                        '{"cells":[{"outputs":[null]}]}']:
            score, _, maximum, _, error = check_audit(payload, 'x.ipynb', 0, self.checks)
            self.assertEqual((score, maximum), (0, 1))
            self.assertTrue(error)

    def test_plausible_forgery_cannot_be_authenticated_and_limit_is_explicit(self):
        # Une trace fabriquée plausible reste acceptée : la limite est volontairement démontrée.
        result = self.check([cell("print('S3_TD0_Q1:', invented)", 'S3_TD0_Q1: {"n":3}')])
        self.assertEqual(result[0], 1)
        self.assertIn('authenticité', result[1][-1]['student_answer'])


class S3RouteTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        p = patch.object(outils, 'BASE_DIR', self.directory.name)
        p.start()
        self.addCleanup(p.stop)
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_all_eight_modules_routes_selector_and_proxy(self):
        selector = self.client.get('/semestre/S3', headers={'X-Forwarded-Prefix': '/universite/tal'}).get_data(as_text=True)
        for number in range(8):
            identifier = f'td{number}-s3'
            self.assertEqual(routes.EVALUATOR_MODES[identifier], 'td')
            module = importlib.import_module(routes.EVALUATORS[identifier][1])
            result = module.check_notebook(notebook([]), 'vide.ipynb')
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0], 0)
            self.assertEqual(result[2], module.MAX_SCORE_TOTAL)
            response = self.client.get('/eval/' + identifier, headers={'X-Forwarded-Prefix': '/universite/tal'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('/universite/tal/eval/' + identifier, selector)

    def test_real_post_identity_persistence_html_escaping_and_proxy(self):
        # Importer la vraie cellule d'identification du sujet évite une fixture artificielle.
        path = ROOT / 'Notebooks TD/S3/TD4_S3_cooccurrences.ipynb'
        nb = json.loads(path.read_text())
        identity = next(c for c in nb['cells'] if c['cell_type'] == 'code' and 'Complétez les informations entre les guillemets.' in ''.join(c['source']))
        identity = json.loads(json.dumps(identity))
        source = ''.join(identity['source'])
        import re
        for name, value in [('nom', 'Exemple'), ('prenom', 'Alice'), ('classe', 'S3')]:
            source = re.sub(rf'(?m)^{name}\s*=.*$', f'{name} = "{value}"', source)
        identity['source'] = source
        hostile = trace(4, 1, {'html': '<script>alert(1)</script>'})
        content = notebook([identity, hostile]).encode()
        response = self.client.post('/eval/td4-s3', data={'file': (io.BytesIO(content), 'copie.ipynb')},
                                    content_type='multipart/form-data', headers={'X-Forwarded-Prefix': '/universite/tal'})
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ALICE'.lower().capitalize(), html)
        self.assertIn('EXEMPLE', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('/universite/tal/eval/td4-s3', html)
        root = Path(self.directory.name)
        self.assertEqual(len(list(root.rglob('*.ipynb'))), 1)
        self.assertEqual(len(list(root.rglob('*.html'))), 1)
        self.assertEqual(len(list(root.rglob('*.csv'))), 1)
        self.assertEqual(next(root.rglob('*.ipynb')).read_bytes(), content)
        self.assertIn('EXEMPLE', next(root.rglob('*.csv')).read_text())

class AuditCalculationTests(unittest.TestCase):
    def check(self, td, values):
        module = importlib.import_module(f'app_correction_TD{td}_S3')
        return module.check_notebook(notebook([trace(td, q, value) for q, value in enumerate(values, 1)]), 'copie.ipynb')

    def test_phrase_margins_union_and_pair_sum_are_not_confused(self):
        values = [{'chat': 2, 'livre': 2, 'N': 4}, {'chat_livre': 1, 'chat_plume': 1, 'livre_plume': 0},
                  {'somme_paires': 3, 'union': 2}, {'k1': 1, 'k3': 2}, {'sans_frontiere': 1, 'dans_phrase': 0},
                  {'formes_chat': 1, 'lemmes_chat': 2}, {'N': 4, 'cooc': 1, 'marge_pivot': 2, 'marge_associe': 2}]
        self.assertEqual(self.check(4, values)[0], 7)
        values[2]['union'] = 3
        self.assertEqual(self.check(4, values)[0], 6)

    def test_conditional_proportions_denominator_zero_and_rounding(self):
        values = [{'conditionnelle': 0.666667, 'base': 0.5},
                  {'A': 0.75, 'B': 0.5, 'base_A': 0.75, 'base_B': 0.166667},
                  {'court': 40.0, 'long': 20.0}, {'associe_sachant_pivot': 0.666667, 'pivot_sachant_associe': 0.5},
                  {'sans_pivot': None, 'sans_associe': 0.0}, {'k1': 0.5, 'k3': 1.0},
                  {'effectif': 2, 'denominateur': 3, 'proportion': 0.666667}]
        self.assertEqual(self.check(5, values)[0], 7)
        values[4]['sans_pivot'] = 0
        self.assertEqual(self.check(5, values)[0], 6)

    def test_no_unconditional_llm_truth_verdict(self):
        values = [{'mesurable': False, 'manquants': ['unite', 'fenetre', 'normalisation', 'agregation']},
                  {'N': 4, 'cooc': 1, 'marge_pivot': 2, 'marge_associe': 2},
                  {'exacte': True, 'debut': 3, 'fin': 15, 'alteree': False},
                  {'dans_intervalle': 'compatible selon le protocole', 'hors_intervalle': 'contredit selon le protocole'},
                  {'somme_paires': 3, 'union': 2}, {'N': 5, 'cooc': 2, 'marge_pivot': 3, 'marge_associe': 3},
                  {'indefini': 'insuffisamment défini', 'defini': 'compatible selon le protocole'}]
        self.assertEqual(self.check(7, values)[0], 7)
        values[6]['indefini'] = 'faux'
        self.assertEqual(self.check(7, values)[0], 6)

class LinguisticCoherenceTests(unittest.TestCase):
    def test_offsets_cover_text_and_reject_missing_and_invented_words(self):
        from s3_audit_linguistic import q1_td1
        source = 'Les livres.'
        rows = [{'forme': 'Les', 'lemme': 'le', 'pos': 'DET', 'tag': 'DET', 'debut': 0, 'fin': 3},
                {'forme': 'livres', 'lemme': 'livre', 'pos': 'NOUN', 'tag': 'NOUN', 'debut': 4, 'fin': 10}]
        self.assertTrue(q1_td1({'annotations': rows}, source))
        self.assertFalse(q1_td1({'annotations': rows[:1]}, source))
        rows[1]['debut'] = 5
        self.assertFalse(q1_td1({'annotations': rows}, source))

    def test_exclusion_counts_and_generalized_counts_are_cross_checked(self):
        from s3_audit_linguistic import exclusions, generalization
        context = {2: {'noms': {'livre': 2, 'notice': 1}, 'verbes': {'lire': 2}}}
        value = {'exclusions': ['livre'], 'avant': {'livre': 2, 'notice': 1}, 'apres': {'notice': 1}, 'justification': ''}
        self.assertTrue(exclusions(value, context))
        value['apres']['notice'] = 2
        self.assertFalse(exclusions(value, context))
        value = {'general_noms': {'livre': 2, 'notice': 1}, 'specialise_noms': {'livre': 2, 'notice': 1},
                 'general_verbes': {'lire': 2}, 'specialise_verbes': {'lire': 2},
                 'combine': {'livre': 2, 'notice': 1, 'lire': 2}, 'comparaison': ''}
        self.assertTrue(generalization(value, context))
        value['combine']['lire'] = 1
        self.assertFalse(generalization(value, context))

    def test_manual_linguistic_review_allows_free_order(self):
        from s3_audit_linguistic import linguistic_review
        rows = [{'forme': form, 'lemme': form.lower(), 'pos': 'NOUN', 'jugement': ''}
                for form in ['livre', 'un', 'lit', 'lecteur', 'Le']]
        self.assertTrue(linguistic_review({'lemmes': ['lecteur', 'lire', 'livre'], 'controle': rows, 'limite_modele': ''}, 'Le lecteur lit un livre.'))

    def test_top_pos_rejects_boolean_count_and_accepts_tied_categories(self):
        from s3_audit_linguistic import pos_counts
        value = {'pos': {'DET': 1, 'NOUN': 1, 'VERB': 1}, 'top3': [['VERB', 1], ['DET', 1], ['NOUN', 1]], 'limite': ''}
        self.assertTrue(pos_counts(value, 'Le lecteur lit.'))
        value['top3'][0][1] = True
        self.assertFalse(pos_counts(value, 'Le lecteur lit.'))


class CorpusEvidenceTests(unittest.TestCase):
    def test_td0_counts_fixed_source_and_limit_microcase(self):
        from app_correction_TD0_S3 import check_notebook
        values = [(1, {'caracteres': 277}), (3, {'occurrences': 47}), (4, {'formes': 41}),
                  (7, {'split': ['L’analyse,', 'c’est', 'utile', '!'], 'limites': ''})]
        result = check_notebook(notebook([trace(0, q, value) for q, value in values]), 'td0.ipynb')
        self.assertEqual(result[0], 4)
        self.assertIn('qualité', result[1][6]['correct_answer'])

    def test_fixed_corpus_hash_and_crlf_offsets(self):
        import app_correction_TD3_S3 as td3
        source, citations = td3.resources()
        self.assertIn('\r\n', source)
        self.assertEqual(len(source), 456257)
        rows = [{'id': item['id'], 'citation': item['citation'], 'debut': source.find(item['citation']),
                 'exacte': item['citation'] in source} for item in citations]
        value = {'citations': rows, 'limite': ''}
        self.assertTrue(td3.exact_citations(value))
        self.assertTrue(td3.exact_citations({'citations': list(reversed(rows)), 'limite': ''}))
        rows[0]['exacte'] = True
        self.assertFalse(td3.exact_citations(value))
        pivot = source.index('naturellement')
        start = source.rfind('légalement', 0, pivot)
        # Choisir le passage de C1 où les deux termes apparaissent dans la même phrase.
        for found in __import__('re').finditer('légalement', source):
            end = source.find('naturellement', found.start())
            if 0 < end - found.start() < 100:
                start, pivot = found.start(), end
                break
        passage = source[start:pivot + len('naturellement')]
        proof = {'id': 'C1', 'passage_source': passage, 'debut': start, 'difference': '', 'verdict': ''}
        self.assertTrue(td3.altered_citation(proof))
        proof['debut'] = len(source[:start].replace('\r\n', '\n'))
        self.assertFalse(td3.altered_citation(proof))

    def test_absent_or_changed_corpus_is_controlled_not_silently_accepted(self):
        import app_correction_TD3_S3 as td3
        with tempfile.TemporaryDirectory() as directory:
            empty = Path(directory)
            td3.resources.cache_clear()
            with patch.object(td3, 'LOCAL_RESOURCES', empty):
                result = td3.check_notebook(notebook([]), 'x.ipynb')
                self.assertEqual(result[0], 0)
                self.assertIn('Ressource S3', result[4])
                (empty / 'faguet_source.txt').write_text('corpus modifié')
                self.assertIn('Empreinte', td3.check_notebook(notebook([]), 'x.ipynb')[4])
            td3.resources.cache_clear()

    def test_evidence_rejects_duplicate_or_wrong_pivot_passages(self):
        import app_correction_TD3_S3 as td3
        source, _ = td3.resources()
        import re
        positions = list(re.finditer(r'\baptitudes?\b', source, re.IGNORECASE))[:3]
        value = {'affirmation': 'G2', 'preuves': [{'debut': m.start(), 'fin': m.end(), 'passage': m.group()} for m in positions],
                 'convention_proposee': '', 'limite': ''}
        self.assertTrue(td3.evidence(value))
        value['affirmation'] = 'G1'
        self.assertFalse(td3.evidence(value))
        value['affirmation'] = 'G2'
        value['preuves'] = [value['preuves'][0]] * 3
        self.assertFalse(td3.evidence(value))

class SourceContractTests(unittest.TestCase):
    def test_real_td3_loader_preserves_original_line_endings_for_offsets(self):
        import ast
        path = ROOT / 'Notebooks TD/S3/TD3_S3_concordances_citations.ipynb'
        nb = json.loads(path.read_text())
        values = []
        for item in nb['cells']:
            if item['cell_type'] != 'code':
                continue
            try:
                tree = ast.parse(''.join(item['source']))
            except SyntaxError:
                continue
            for node in tree.body:
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'texte_faguet' for t in node.targets):
                    values.append(node.value)
        self.assertEqual(len(values), 1)
        expr = values[0]
        self.assertIsInstance(expr, ast.Call)
        self.assertEqual(expr.func.attr, 'decode')
        self.assertEqual(expr.args[0].value.lower().replace('-', ''), 'utf8')
        self.assertEqual(expr.func.value.func.attr, 'read_bytes')
