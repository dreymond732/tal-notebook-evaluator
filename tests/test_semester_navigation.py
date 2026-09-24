"""Parcours étudiant complet, liens historiques et préfixe du proxy."""
import importlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from app import create_app
import outils
import routes


class SemesterNavigationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        base = patch.object(outils, 'BASE_DIR', directory.name)
        base.start()
        self.addCleanup(base.stop)
        self.client = create_app().test_client()

    def page(self, path, prefix=''):
        response = self.client.get(path, headers={'X-Forwarded-Prefix': prefix})
        self.assertEqual(response.status_code, 200)
        return BeautifulSoup(response.data, 'html.parser')

    def test_home_then_semester_lists_reach_every_evaluator_once(self):
        for prefix in ('', '/universite/tal'):
            with self.subTest(prefix=prefix):
                home = self.page('/', prefix)
                self.assertEqual([a['href'] for a in home.select('a.card')],
                                 [prefix + '/semestre/' + s for s in ('S1', 'S2', 'S3')])
                self.assertFalse(home.select('a[href*="/eval/"]'))
                reached = []
                for semester, count in [('S1', 8), ('S2', 6), ('S3', 18)]:
                    page = self.page('/semestre/' + semester, prefix)
                    self.assertIn(semester, page.h1.text)
                    self.assertEqual(page.select_one('nav a')['href'], prefix + '/')
                    cards = page.select('a.card')
                    self.assertEqual(len(cards), count)
                    for card in cards:
                        name = card['href'].split('/eval/')[1]
                        self.assertTrue(card['href'].startswith(prefix + '/eval/'))
                        self.assertEqual(routes.EVALUATOR_SEMESTERS[name], semester)
                        # Vérification indépendante à partir du module existant.
                        self.assertTrue(routes.EVALUATORS[name][1].endswith(semester))
                        reached.append(name)
                self.assertCountEqual(reached, routes.EVALUATORS)

    def test_all_historical_get_routes_import_and_return_to_their_semester(self):
        prefix = '/universite/tal'
        for name, (_, module_name) in routes.EVALUATORS.items():
            with self.subTest(name=name):
                module = importlib.import_module(module_name)
                self.assertTrue(callable(module.check_notebook))
                page = self.page('/eval/' + name, prefix)
                links = [a['href'] for a in page.select('a')]
                self.assertIn(prefix + '/semestre/' + routes.EVALUATOR_SEMESTERS[name], links)
                self.assertIn(prefix + '/', links)
                self.assertIsNotNone(page.find('form', method='post'))

    def test_control_badges_follow_explicit_modes_even_for_td_urls(self):
        page = self.page('/semestre/S2')
        for name in ('td2-S2', 'td4-S2'):
            card = page.find('a', href='/eval/' + name)
            self.assertIn('controle', card['class'])
            self.assertEqual(card.select_one('.badge').text.strip(), 'Contrôle — dépôt')

    def test_post_results_receipts_and_errors_keep_semester_navigation(self):
        checker = SimpleNamespace(check_notebook=lambda *args: (0, [], 20, {}, None))
        with patch.object(routes, 'import_module', return_value=checker), \
                patch.object(routes, 'process_submission'):
            for name in ('td1-s1', 'ControleDevoirMaisonS2', 'controle-td1-s3'):
                for upload in (False, True):
                    with self.subTest(name=name, upload=upload):
                        data = {'file': (io.BytesIO(b'{}'), 'test.ipynb')} if upload else {}
                        response = self.client.post('/eval/' + name, data=data,
                                                    headers={'X-Forwarded-Prefix': '/universite/tal'})
                        self.assertEqual(response.status_code, 200)
                        self.assertIn('/universite/tal/semestre/' + routes.EVALUATOR_SEMESTERS[name],
                                      response.get_data(as_text=True))

    def test_unknown_semester_and_evaluator(self):
        self.assertEqual(self.client.get('/semestre/S4').status_code, 404)
        response = self.client.get('/eval/inconnu', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('non trouvé', response.get_data(as_text=True))

    def test_incomplete_or_invalid_classification_prevents_startup(self):
        for classification in ({}, dict(routes.EVALUATOR_SEMESTERS, **{'td1-s1': 'S4'}),
                               dict(routes.EVALUATOR_SEMESTERS, inconnu='S1')):
            with patch.dict(routes.EVALUATOR_SEMESTERS, classification, clear=True):
                with self.assertRaises(ValueError):
                    create_app()


if __name__ == '__main__':
    unittest.main()
