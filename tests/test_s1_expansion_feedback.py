"""Execute trusted report examples locally, then grade only their saved traces.

No submitted source is executed: answer text comes exclusively from the static
application catalogue. All course file operations are isolated in temporary dirs.
"""
import contextlib
import copy
import importlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from notebook_contract import load_catalog, validate_cell_metadata
from routes import EVALUATORS
from s1_expansion_feedback import SOLUTIONS

IDS = {f'td{td}-{part}-s1' for td in (3, 4, 5, 6)
       for part in ('one', 'bis', 'ter')}


@contextlib.contextmanager
def temporary_working_directory():
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as directory:
        try:
            os.chdir(directory)
            yield Path(directory)
        finally:
            os.chdir(previous)


def execute_trusted_examples(identifier):
    """Prepare a synthetic copy from course cells and application-owned text."""
    entry = next(item for item in load_catalog() if item['id'] == identifier)
    source_path = ROOT / entry['notebook']
    notebook = json.loads(source_path.read_text(encoding='utf-8'))
    cells = validate_cell_metadata(notebook)
    cells['identity', 'identification']['source'] = (
        'nom="Exemple"\nprenom="Camille"\nclasse="S1"\n'
        'numero_etudiant="SYNTHETIQUE-EXEMPLES"')
    for number, solution in enumerate(SOLUTIONS[identifier], 1):
        cells[f'Q{number}', 'answer']['source'] = solution['solution_code']
    namespace = {'__name__': '__trusted_report_examples__'}
    count = 0
    for cell in notebook['cells']:
        role = cell.get('metadata', {}).get('tal', {}).get('role')
        if cell['cell_type'] != 'code' or role not in {'provided', 'example', 'answer'}:
            continue
        source = ''.join(cell['source'])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            # Trusted course preparation/examples and the static catalogue only.
            exec(compile(source, f'<trusted-example:{identifier}>', 'exec'), namespace)
        cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout',
                            'text': stdout.getvalue()}]
        cell['execution_count'] = count + 1
        count += 1
    return notebook, namespace


class ExpansionFeedbackTests(unittest.TestCase):
    def test_72_examples_obey_all_twelve_saved_trace_contracts(self):
        self.assertEqual(set(SOLUTIONS), IDS)
        paths = [ROOT / entry['notebook'] for entry in load_catalog()
                 if entry['id'] in IDS]
        original_subjects = {path: path.read_bytes() for path in paths}
        self.assertEqual(len(paths), 12)
        count = 0
        for identifier in sorted(IDS):
            with self.subTest(identifier=identifier), temporary_working_directory():
                solutions = SOLUTIONS[identifier]
                self.assertEqual(len(solutions), 6)
                for item in solutions:
                    self.assertEqual(set(item), {'solution_code', 'solution_explanation'})
                    self.assertTrue(item['solution_code'].strip())
                    self.assertTrue(item['solution_explanation'].strip())
                    count += 1
                notebook, _ = execute_trusted_examples(identifier)
                grader = importlib.import_module(EVALUATORS[identifier][1])
                with patch('builtins.exec', side_effect=AssertionError('The server must not execute examples or submissions')):
                    score, details, maximum, _, error = grader.check_notebook(
                        json.dumps(notebook), 'copie-synthetique.ipynb')
                self.assertIsNone(error)
                self.assertEqual((score, maximum), (6, 6))
                graded = [detail for detail in details if detail['max_points']]
                self.assertEqual(len(graded), 6)
                self.assertTrue(all(detail['points'] == 1 for detail in graded), graded)
                for detail, solution in zip(graded, solutions):
                    self.assertEqual(detail['solution_code'], solution['solution_code'])
                    self.assertEqual(detail['solution_explanation'], solution['solution_explanation'])
                    self.assertTrue(detail['student_code'])
                    self.assertTrue(detail['student_output'])
        self.assertEqual(count, 72)
        self.assertEqual({path: path.read_bytes() for path in paths}, original_subjects)

    def test_function_examples_respect_subject_edge_cases(self):
        with temporary_working_directory():
            _, functions = execute_trusted_examples('td5-one-s1')
            self.assertEqual(functions['longueur_texte'](''), 0)
            self.assertEqual(functions['ligne_caracteres'](0, 'é'), '')
            self.assertEqual(functions['volume_boite'](1.5, 2, 3), 9.0)
            maximum = functions['maximum3']
            for arguments, expected in [((4, 4, 1), 4), ((1, 4, 4), 4),
                                        ((4, 1, 4), 4), ((-8, -3, -12), -3)]:
                self.assertEqual(maximum(*arguments), expected)
            self.assertEqual(functions['normaliser']('  DEUX   MOTS  '), 'deux   mots')
            self.assertEqual(functions['annoncer_atelier']('  '), 'Au programme : ')

            _, functions = execute_trusted_examples('td5-bis-s1')
            self.assertEqual(functions['texte'], 'Archives')
            self.assertEqual(functions['traduire_mot'](' BOOK ', {'book': 'livret'}), 'livret')
            self.assertEqual(functions['traduire_mot'](' Mystery ', {}), 'mystery')
            self.assertEqual(functions['traduire_ou_signaler']('Mystery', {}, 'absent'), 'absent')

            _, functions = execute_trusted_examples('td5-ter-s1')
            self.assertEqual(functions['compte_caractere']('e', 'ÉEée'), 1)
            self.assertEqual(functions['nombre_mots'](' \n\t '), 0)
            self.assertEqual(functions['traduire_phrase'](' BOOK  Unknown ', {'book': 'livret'}), 'livret unknown')
            self.assertEqual(functions['resume_texte']('  DEUX   MOTS  '),
                             {'texte_normalise': 'deux   mots', 'nb_caracteres': 11, 'nb_mots': 2})
            source = [' TAL ', '', ' TAL ']
            original = copy.deepcopy(source)
            summaries = functions['resumer_corpus'](source)
            self.assertEqual(source, original)
            self.assertEqual(summaries[0], summaries[2])
            self.assertEqual(functions['resumer_corpus']([]), [])

    def test_collection_and_file_examples_keep_data_and_types(self):
        with temporary_working_directory() as directory:
            _, data = execute_trusted_examples('td3-one-s1')
            self.assertEqual(data['reference'], ['texte', 'corpus', 'langue'])
            self.assertIsNot(data['reference'], data['revision'])
            self.assertEqual(data['mots'], ['texte', 'langue', 'texte', 'corpus', 'analyse'])
            _, data = execute_trusted_examples('td3-bis-s1')
            self.assertIs(type(data['code_unique']), tuple)
            self.assertEqual(data['code_unique'], ('fr',))
            self.assertEqual(data['reference'], ('français', 'italien', 'espagnol'))
            _, data = execute_trusted_examples('td6-one-s1')
            self.assertEqual(data['lignes_utiles'], ['Archive', 'Musée', '  Salle A  '])
            self.assertEqual((directory / 'lignes_utiles.txt').read_text(encoding='utf-8'),
                             'Archive\nMusée\n  Salle A  \n')
            self.assertEqual(data['texte_triple_relu'], data['texte_source'].replace(' ', '   '))
            _, data = execute_trusted_examples('td6-bis-s1')
            self.assertIn('06000', data['fiches_relues'])
            self.assertEqual(data['normaliser_personne'](''), '')
            self.assertEqual(data['groupes_atelier'],
                             {'Lamy Zoé': {'Studio;annexe', 'Musée'}, 'Petit Chloé': {'Musée'}})
            _, data = execute_trusted_examples('td6-ter-s1')
            self.assertEqual(data['lieux_relus'][1], ['Musée, aile nord', 'Toulon'])
            self.assertTrue(all(type(row[1]) is str for row in data['documents_relus']))
            self.assertTrue(all(len(row) == 3 for row in data['nouveaux_relus']))
            self.assertIn('Centre, langues', data['nouveaux_relus'][1][2])
            self.assertIn('"Centre, langues | Musée"',
                          (directory / 'affiliations_nouvelles.csv').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
