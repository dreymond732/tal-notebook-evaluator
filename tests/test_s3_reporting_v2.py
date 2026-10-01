"""Diagnostics de dépendances et collecte de preuves sans HTML actif ni exécution."""
import importlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from s3_audit import grade_traces
from s3_review import review_evidence


def traces(values):
    displays = {q: [(q, False)] for q in values}
    records = {q: [(q, json.dumps(v))] for q, v in values.items()}
    return displays, records


class ReportingV2Tests(unittest.TestCase):
    def test_missing_invalid_and_incorrect_are_distinguished(self):
        checks = [dict(label='quantité', validate=lambda v: v == 3, feedback='exact')]
        for values, state in [({}, 'preuve_absente'), ({1: 4}, 'incorrect'), ({1: 3}, 'conforme')]:
            result = grade_traces(*traces(values), checks, [1])
            self.assertEqual(result[1][0]['evaluation_status'], state)
        displays, records = traces({1: 3})
        records[1][0] = (1, '{')
        self.assertEqual(grade_traces(displays, records, checks, [1])[1][0]['evaluation_status'], 'preuve_absente')

    def test_c1_missing_annotations_blocks_three_checks_without_claiming_three_errors(self):
        checks = importlib.import_module('app_correction_Controle_TD1_S3').CHECKS
        score, details, deferred = grade_traces(*traces({3: {}, 4: {}, 5: {}}), checks, [2, 3, 3, 3, 3, 3, 3], contextual=True)
        self.assertEqual(score, 0)
        self.assertEqual(deferred, 9)
        self.assertEqual(details[1]['evaluation_status'], 'preuve_absente')
        for d in details[2:5]:
            self.assertEqual(d['evaluation_status'], 'non_verifiable')
            self.assertEqual(d['dependencies'], ['Q2'])
            self.assertIn('aucune erreur de calcul indépendante', d['diagnostic'])

    def test_c2_usable_annotations_do_not_depend_on_upstream_length_correctness(self):
        from s3_controls_data import C2
        import re
        source = C2['texte_atelier']
        rows = [dict(forme=m[0], lemme=m[0].lower(), pos='NOUN', tag='NOUN', debut=m.start(), fin=m.end(), ponctuation=False, espace=False, mot_vide=False) for m in re.finditer(r'\w+|[^\w\s]', source)]
        checks = importlib.import_module('app_correction_Controle_TD2_S3').CHECKS
        from s3_controls_linguistic import freq
        values = {1: {'annotations': rows, 'caracteres': -1}, 2: {'noms': freq(rows, {'NOUN'}), 'verbes': {}}}
        score, details, deferred = grade_traces(*traces(values), checks, [2, 3, 3, 3, 3, 3, 3], contextual=True)
        self.assertEqual(details[0]['evaluation_status'], 'incorrect')
        self.assertEqual(details[1]['evaluation_status'], 'conforme')
        self.assertEqual(score, 3)
        self.assertEqual(deferred, 0)

    def test_missing_written_presence_is_separate_from_technical_point(self):
        checks = [dict(label='quantité', validate=lambda v: v.get('n') == 3,
                       feedback='exact', required_text_fields=['limites'])]
        result = grade_traces(*traces({1: {'n': 3, 'limites': ''}}), checks, [1])
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1][0]['missing_fields'], ['limites'])
        self.assertIn('Production rédigée absente', result[1][0]['diagnostic'])
        result = grade_traces(*traces({1: {'n': 3, 'limites': 'x'}}), checks, [1])
        self.assertEqual(result[1][0]['missing_fields'], [])  # présence, pas qualité

    def test_c2_missing_annotation_schema_marks_twelve_points_for_recheck(self):
        checks = importlib.import_module('app_correction_Controle_TD2_S3').CHECKS
        result = grade_traces(*traces({1: {'annotations': True}, 2: {}, 3: {}, 4: {}, 6: {}}),
                              checks, [2, 3, 3, 3, 3, 3, 3], contextual=True)
        self.assertEqual(result[2], 12)
        self.assertEqual(result[1][0]['evaluation_status'], 'incorrect')
        for q in (2, 3, 4, 6):
            self.assertEqual(result[1][q - 1]['evaluation_status'], 'non_verifiable')

    def test_safe_question_association_is_order_independent_and_mime_only(self):
        malicious = '<script>alert("x")</script>'
        cells = [
            {'cell_type': 'markdown', 'id': 'analyse', 'metadata': {'tal_review': {'question': 'Q2'}}, 'source': malicious},
            {'cell_type': 'code', 'metadata': {'tal': {'question': 'Q2', 'role': 'answer'}}, 'source': '# commentaire', 'outputs': [{'output_type': 'display_data', 'data': {'text/html': malicious, 'image/svg+xml': malicious}}]},
            {'cell_type': 'markdown', 'metadata': {'tal_review': {'question': ['invalide']}}, 'source': 'libre'},
        ]
        evidence = review_evidence({'cells': cells}, 7)
        self.assertEqual(evidence[0]['question'], 'Q2')
        self.assertEqual(len(evidence[0]['cells']), 2)
        self.assertEqual(evidence[0]['cells'][1]['figures'], ['image/svg+xml', 'text/html'])
        self.assertEqual(evidence[0]['cells'][1]['outputs'], '')
        self.assertEqual(evidence[1]['cells'][0]['source'], 'libre')
        from app import create_app
        from flask import render_template
        with create_app().test_request_context('/'):
            html = render_template('s3_controle_report_template.html', display_name='Contrôle', student_info={'review_evidence': evidence}, details=[], score=0, max_score=20)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)
        self.assertIn('id="cell-1"', html)
        self.assertIn('image/svg+xml', html)
        self.assertEqual(html.count('Aucun affichage visuel enregistré dans cette cellule ; à vérifier si demandé.'), 2)

    def test_source_and_unassigned_evidence_limits_are_explicit(self):
        cells = [{'cell_type': 'markdown', 'source': 'x' * 20000}] * 14
        evidence = review_evidence({'cells': cells}, 7)
        self.assertEqual(evidence[0]['omitted'], 2)
        self.assertTrue(evidence[0]['cells'][0]['source_truncated'])
        self.assertEqual(len(evidence[0]['cells'][0]['source']), 16000)
        evidence = review_evidence({'cells': [{'cell_type': 'code', 'source': '', 'outputs': [
            {'output_type': 'stream', 'text': 'x' * 5000}]}]}, 7)
        self.assertTrue(evidence[0]['cells'][0]['outputs_truncated'])
        self.assertEqual(len(evidence[0]['cells'][0]['outputs']), 4000)


if __name__ == '__main__':
    unittest.main()
