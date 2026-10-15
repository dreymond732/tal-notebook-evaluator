"""Separate revision edition: no student execution or change to assessment mode."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from notebook_contract import resolve_notebook
from tutor_metadata import (CELL_START, CELL_END, CONTEXT_BUDGET, migrate_notebook,
                            render_context, validate_session)

SOURCE = ROOT / 'Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb'
EDITION = ROOT / 'Notebooks contrôles finaux/S1/devoir_S1_tuteur.ipynb'
SOURCE_SHA256 = '6fd62ebefdb8e8cd1a7673edf1dbfca2b26a02745dd2ab98a6183f9ea46122f1'


class DevoirS1TutorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sessions = json.loads((ROOT / 'docs/pedagogy/tutor_sessions.json').read_text())['sessions']
        cls.session = next(s for s in sessions if s['id'] == 'devoir_S1_tuteur')
        cls.control = next(s for s in sessions if s['id'] == 'DM_INTERMEDIAIRE_S1')
        cls.source = json.loads(SOURCE.read_text())
        cls.edition = json.loads(EDITION.read_text())

    def test_original_control_and_all_assignment_cells_are_preserved(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), SOURCE_SHA256)
        self.assertEqual(len(self.edition['cells']), 45)
        self.assertEqual(self.edition['cells'][2:], self.source['cells'][2:])
        for before, after in zip(self.source['cells'][:2], self.edition['cells'][:2]):
            self.assertEqual({k: v for k, v in before.items() if k != 'source'},
                             {k: v for k, v in after.items() if k != 'source'})
        before, after = copy.deepcopy(self.source), copy.deepcopy(self.edition)
        for nb in (before, after):
            nb.pop('cells')
            nb['metadata'].pop('tal_tutor')
            nb['metadata']['colab'].pop('aiContexts')
        self.assertEqual(after, before)

    def test_revision_profile_has_exactly_eighteen_complete_question_cards(self):
        self.assertEqual(self.session['tutor_profile'], 'devoir_S1_tuteur')
        self.assertEqual(self.session['activity'], 'td')
        self.assertEqual(self.session['semester'], 1)
        context = render_context(self.session)
        self.assertLessEqual(len(context), CONTEXT_BUDGET)
        lines = {match[1]: match[2] for match in re.finditer(r'^(Q\d+) — (.*)$', context, re.M)}
        self.assertEqual(set(lines), {f'Q{q}' for q in range(1, 19)})
        for exercise in self.session['exercises']:
            for concept in exercise['available_concepts']:
                self.assertIn(concept, lines[exercise['id']])
        cards = {e['id']: e for e in self.session['exercises']}
        self.assertIn('/', cards['Q1']['introduced_here'])
        self.assertIn('priorités', cards['Q2']['introduced_here'])
        self.assertIn('ordre insertion', cards['Q9']['introduced_here'])
        self.assertIn('indice sûr', cards['Q14']['introduced_here'])
        self.assertTrue({'composition', 'for', 'get()', 'accumulation'} <=
                        set(cards['Q18']['available_concepts']))

    def test_revision_instructions_are_synchronized_and_idempotent(self):
        context = render_context(self.session)
        self.assertIn('RÉVISION GUIDÉE PAR QUESTION', context)
        self.assertIn('TOUTES les notions', context)
        self.assertIn('Une seule question par tour', context)
        self.assertIn('S1 : AUCUN code', context)
        self.assertNotIn('CONTRÔLE — AUCUNE ASSISTANCE', context)
        stored = next(iter(self.edition['metadata']['colab']['aiContexts'].values()))['context']
        self.assertEqual(stored, context)
        first = ''.join(self.edition['cells'][0]['source'])
        self.assertEqual(first.split('\n\n', 1)[1], f'<!-- {CELL_START}\n{context}{CELL_END} -->\n')
        self.assertEqual(migrate_notebook(self.edition, self.session), self.edition)
        self.assertIn('révision', ''.join(self.edition['cells'][1]['source']).lower())
        self.assertNotIn("L'assistance du tuteur, d'un LLM ou d'un service de génération de code est interdite",
                         ''.join(self.edition['cells'][1]['source']))

    def test_control_still_refuses_help_and_grading_mode_stays_private(self):
        context = render_context(self.control)
        self.assertIn('CONTRÔLE — AUCUNE ASSISTANCE', context)
        self.assertNotIn('RÉVISION GUIDÉE PAR QUESTION', context)
        self.assertEqual(migrate_notebook(self.source, self.control), self.source)
        entry = resolve_notebook(self.edition)
        self.assertEqual((entry['id'], entry['evaluator'], entry['mode']),
                         ('dm-intermediaire-s1', 'dm-intermediaire-s1', 'controle'))

    def test_profile_cannot_be_attached_to_a_control_or_another_edition(self):
        bad = copy.deepcopy(self.session)
        del bad['tutor_profile']
        with self.assertRaises(ValueError):
            render_context(bad)
        bad = copy.deepcopy(self.control)
        bad['tutor_profile'] = 'devoir_S1_tuteur'
        with self.assertRaises(ValueError):
            render_context(bad)
        mutations = {'semester': 2, 'activity': 'controle', 'id': 'DM_INTERMEDIAIRE_S1',
                     'notebook': self.control['notebook'], 'tutor_profile': 'unknown'}
        for field, value in mutations.items():
            with self.subTest(field=field):
                bad = copy.deepcopy(self.session)
                bad[field] = value
                with self.assertRaises(ValueError):
                    validate_session(bad)

    def test_partial_empty_or_library_enabled_revision_cards_are_rejected(self):
        bad = copy.deepcopy(self.session)
        bad['exercises'].pop()
        with self.assertRaises(ValueError):
            render_context(bad)
        bad = copy.deepcopy(self.session)
        bad['exercises'][0]['available_concepts'] = []
        bad['exercises'][0]['introduced_here'] = []
        with self.assertRaises(ValueError):
            render_context(bad)
        for field in ('allowed_libraries', 'provided_libraries'):
            bad = copy.deepcopy(self.session)
            bad[field] = ['math']
            with self.subTest(field=field), self.assertRaises(ValueError):
                render_context(bad)


if __name__ == '__main__':
    unittest.main()
