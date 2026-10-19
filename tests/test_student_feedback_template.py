"""Student reports display inert notebook excerpts separately from feedback."""
import sys
import unittest
from pathlib import Path

from bs4 import BeautifulSoup
from flask import render_template

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from app import create_app


class StudentFeedbackTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

    def render(self, details, **extra):
        params = dict(display_name='TD1', score=0, max_score=1,
                      student_info={'nom': 'Test', 'prenom': 'Test', 'classe': 'S1'},
                      details=details, evaluator_name='td1-s1', is_td=True)
        params.update(extra)
        with self.app.test_request_context('/eval/td1-s1'):
            return render_template('corrector_template.html', **params)

    def detail(self, **extra):
        result = dict(check='Q1', student_code='print("Résultat Q1 :", 42)',
                      student_output='Résultat Q1 : 42\n', answer_cells=[3, 5],
                      student_answer='Ancien résumé', correct_answer='Ancien corrigé',
                      diagnostic='La sortie ne correspond pas à la valeur demandée.',
                      action='Recalculez la valeur, puis exécutez la cellule.',
                      solution_code='print("Résultat Q1 :", 43)',
                      solution_explanation='La valeur attendue est 43.',
                      status='❌', points=0.0, max_points=1.0)
        result.update(extra)
        return result

    def test_evidence_and_feedback_are_distinct_and_reference_cells(self):
        html = self.render([self.detail()])
        soup = BeautifulSoup(html, 'html.parser')
        row = soup.select('#feedback-table tbody tr')[0]
        cells = row.find_all('td', recursive=False)
        self.assertIn('print("Résultat Q1 :", 42)', cells[1].get_text())
        self.assertIn('Résultat Q1 : 42', cells[1].get_text())
        self.assertIn('3, 5', cells[1].get_text())
        self.assertNotIn('La sortie ne correspond', cells[1].get_text())
        self.assertIn('La sortie ne correspond', cells[3].get_text())
        self.assertIn('Recalculez la valeur', cells[3].get_text())
        self.assertIn('print("Résultat Q1 :", 43)', cells[2].get_text())
        self.assertIn('La valeur attendue est 43.', cells[2].get_text())
        self.assertIn('À reprendre', cells[3].get_text())
        self.assertNotIn('Ancien résumé', html)
        self.assertNotIn('Note Finale', html)
        self.assertIn('Score formatif provisoire', html)
        self.assertIn('n’exécute pas votre programme', html)
        self.assertIn('sortie périmée', html)
        self.assertIn('restent à autoévaluer avec les critères du TD', html)

    def test_all_notebook_and_solution_text_is_escaped(self):
        payload = '<script>alert("copie")</script><img src=x onerror=alert(1)>'
        html = self.render([self.detail(student_code=payload, student_output=payload,
                    solution_code=payload, solution_explanation=payload,
                    diagnostic=payload, action=payload)])
        soup = BeautifulSoup(html, 'html.parser')
        self.assertIsNone(soup.select_one('img'))
        self.assertEqual(len(soup.find_all('script')), 1)  # Local solution toggle only.
        for cell in soup.select('#feedback-table tbody td')[1:4]:
            self.assertIn(payload, cell.get_text())
        self.assertIn('&lt;script&gt;', html)

    def test_scope_is_an_information_block_without_fake_grade_or_warning(self):
        scope = dict(check='Portée du score', student_answer='Vérification limitée au fichier.',
                     correct_answer='Sans point.', status='ℹ️', points=0, max_points=0)
        html = self.render([self.detail(), scope])
        soup = BeautifulSoup(html, 'html.parser')
        self.assertEqual(len(soup.select('#feedback-table tbody tr')), 1)
        self.assertIn('Vérification limitée au fichier.', soup.select_one('.score-scope').get_text())
        self.assertNotIn('0.00 / 0.00', html)
        self.assertNotIn('⚠️', soup.select_one('.score-scope').get_text())

    def test_missing_evidence_is_explicit_and_legacy_s2_remains_readable(self):
        empty = BeautifulSoup(self.render([self.detail(student_code='', student_output='',
                                                      answer_cells=[])]), 'html.parser')
        self.assertIn('Aucun code de réponse retrouvé', empty.get_text())
        self.assertIn('Aucune sortie textuelle enregistrée', empty.get_text())
        old = dict(check='Q1', student_answer='Réponse historique <script>ancien</script>',
                   correct_answer='Attendu historique', status='✅', points=1, max_points=1)
        html = self.render([old], evaluator_name='td1-s2')
        self.assertIn('Réponse historique &lt;script&gt;ancien&lt;/script&gt;', html)
        self.assertIn('Attendu historique', html)
        success = BeautifulSoup(html, 'html.parser').select_one('.status-ok')
        self.assertEqual(success.get_text(), '✓')

    def test_ungraded_observations_are_not_presented_as_missing_evidence(self):
        html = self.render([self.detail(status='ℹ️', points=0, max_points=0)])
        row = BeautifulSoup(html, 'html.parser').select_one('#feedback-table tbody tr')
        self.assertIn('À autoévaluer', row.select_one('.status').get_text())
        self.assertEqual(row.select_one('.points').get_text(), 'Non noté')
        self.assertNotIn('À vérifier', row.get_text())
        self.assertNotIn('0.00 / 0.00', row.get_text())

    def test_missing_or_blocked_evidence_takes_precedence_over_legacy_error_symbol(self):
        for state, expected in [('non_verifiable', 'Non vérifiable'),
                                ('preuve_absente', 'Résultat manquant ou inexploitable')]:
            with self.subTest(state=state):
                html = self.render([self.detail(status='❌', evaluation_status=state)])
                row = BeautifulSoup(html, 'html.parser').select_one('#feedback-table tbody tr')
                self.assertEqual(row.select_one('.status-label').get_text().strip(), expected)
                self.assertNotIn('À reprendre', row.select_one('.status').get_text())
                self.assertEqual(row.select_one('.points').get_text().strip(), '0.00 / 1.00')

    def test_saved_report_toggle_has_no_external_dependency(self):
        html = self.render([self.detail()])
        soup = BeautifulSoup(html, 'html.parser')
        self.assertIsNotNone(soup.select_one('#toggle-solutions[aria-controls="feedback-table"]'))
        self.assertTrue(soup.select_one('#toggle-solutions').has_attr('checked'))
        self.assertIn('show-solutions', soup.body['class'])
        self.assertEqual(soup.select_one('th.solution-col').get_text(), 'Résultat attendu')
        self.assertEqual(soup.select('script[src]'), [])
        self.assertIn("classList.toggle('show-solutions', this.checked)", html)
        self.assertIsNotNone(soup.select_one('noscript'))
        self.assertIn('max-width: 1000px', html)

    def test_success_shows_only_accessible_green_check_without_redundant_feedback(self):
        html = self.render([self.detail(status='✅', points=1,
                                      evaluation_status='conforme')])
        soup = BeautifulSoup(html, 'html.parser')
        status = soup.select_one('td.status')
        self.assertEqual(status.get_text().strip(), '✓')
        self.assertEqual(status.select_one('.status-ok')['aria-label'], 'Critères vérifiés satisfaits')
        self.assertNotIn('La sortie ne correspond', html)
        self.assertNotIn('Recalculez la valeur', html)
        self.assertIn('print("Résultat Q1 :", 42)', soup.select_one('td[data-label="Votre réponse retrouvée"]').get_text())
        self.assertIn('print("Résultat Q1 :", 43)', soup.select_one('td.solution-col').get_text())

    def test_graded_success_with_missing_written_field_still_requests_completion(self):
        html = self.render([self.detail(status='✅', points=1,
                         evaluation_status='conforme', missing_fields=['interpretation'])])
        status = BeautifulSoup(html, 'html.parser').select_one('td.status')
        self.assertIsNone(status.select_one('.status-ok'))
        self.assertIn('À compléter', status.get_text())
        self.assertIn('interpretation', status.get_text())

    def test_student_supplement_preserves_ungraded_text_without_internal_cell_id(self):
        evidence = [dict(question='Q1', omitted=0, cells=[dict(cell_number=7,
                     cell_id='internal-answer-q1', kind='markdown',
                     source='Mon interprétation <script>essai</script>', source_truncated=True,
                     outputs='', outputs_truncated=False, figures=[])])]
        info = dict(nom='Test', prenom='Test', classe='S3', review_evidence=evidence)
        html = self.render([self.detail()], student_info=info)
        soup = BeautifulSoup(html, 'html.parser')
        self.assertIn('Autres productions enregistrées', soup.get_text())
        self.assertIn('Mon interprétation <script>essai</script>', soup.get_text())
        self.assertIn('Extrait tronqué', soup.get_text())
        self.assertNotIn('internal-answer-q1', html)
        self.assertNotIn('qualité ni sa provenance', html)
        with self.app.test_request_context('/'):
            control = render_template('s3_review_evidence.html', student_info=info,
                                      evaluator_name='controle-td1-s3', is_td=False)
        self.assertIn('internal-answer-q1', control)
        self.assertIn('qualité ni sa provenance', control)


if __name__ == '__main__':
    unittest.main()
