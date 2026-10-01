"""S1 rename, complete cell metadata and evaluator/distribution compatibility.

Saved traces are synthetic regression evidence, never executed submissions and
never a claim that the historical formative checkers assess semantic correctness.
"""
import copy
import importlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
sys.path.insert(0, str(ROOT / 'tests'))
from app import create_app
import outils
from notebook_contract import load_catalog, resolve_notebook, validate_cell_metadata
from prepare_student_notebooks import submission_cell
from routes import EVALUATORS
from test_notebook_migration_integrity import S1_RENAMED_SUBJECTS
from test_td2_s1 import SOURCES as TD2_SOURCES, OUTPUTS as TD2_OUTPUTS

# Independent, nonzero Q1 probes for all seven real evaluators. Subsequent
# questions are intentionally unanswered, exercising success and failure together.
Q1_PROBES = {
    1: ('cout_total = 3 * 4\nprint("Résultat Q1 :", cout_total)', 'Résultat Q1 : 12\n'),
    2: (TD2_SOURCES[0], TD2_OUTPUTS[0]),
    3: ('mots = ["texte"]\nmots.append("corpus")\nmots.pop()\nprint("Résultat Q1 :", mots)', "Résultat Q1 : ['texte']\n"),
    4: ('for mot in ["texte"]:\n    print("Résultat Q1 :", mot.upper())', 'Résultat Q1 : TEXTE\n'),
    5: ('def longueur_texte(texte):\n    return len(texte)\nprint("Résultat Q1 :", longueur_texte("tal"))', 'Résultat Q1 : 3\n'),
    6: ('with open("corpus.txt", encoding="utf-8") as fichier:\n    texte = fichier.read()\nprint("Résultat Q1 :", texte)', 'Résultat Q1 : texte\n'),
    7: ('import re\nprint("Résultat Q1 :", bool(re.search("tal", "TAL", re.IGNORECASE)))', 'Résultat Q1 : True\n'),
}
QUESTION_COUNTS = (6, 7, 6, 7, 6, 6, 7)


def subjects():
    entries = {e['id']: e for e in load_catalog()}
    for number, path in enumerate(S1_RENAMED_SUBJECTS.values(), 1):
        yield number, entries[f'td{number}-s1'], json.loads((ROOT / path).read_text())


def observed_copy(number, notebook):
    nb = copy.deepcopy(notebook)
    indexed = validate_cell_metadata(nb)
    indexed['identity', 'identification']['source'] = [
        '# Complétez les informations entre les guillemets.\n',
        'nom = "Modele"\nprenom = "Test"\nclasse = "S1"\n']
    source, output = Q1_PROBES[number]
    answer = indexed['Q1', 'answer']
    answer['source'] = source.splitlines(keepends=True)
    answer['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': output}]
    return nb


class S1ReviewTests(unittest.TestCase):
    def test_seven_names_root_contracts_and_all_45_question_cells(self):
        self.assertEqual(len(S1_RENAMED_SUBJECTS), 7)
        self.assertEqual({p.name for p in (ROOT / 'Notebooks TD/S1').glob('*.ipynb')},
                         {Path(p).name for p in S1_RENAMED_SUBJECTS.values()})
        total_answers, total_cells = 0, 0
        for number, entry, nb in subjects():
            with self.subTest(evaluator=entry['id']):
                self.assertEqual(nb['metadata']['tal'], {
                    'id': f'td{number}-s1', 'evaluator': f'td{number}-s1', 'version': 1})
                self.assertEqual((entry['semester'], entry['mode'], entry['active']), ('S1', 'td', True))
                self.assertEqual(resolve_notebook(nb), entry)
                indexed = validate_cell_metadata(nb)
                self.assertEqual(len(indexed), len(nb['cells']))
                self.assertEqual(len({c['id'] for c in nb['cells']}), len(nb['cells']))
                answers = {q for q, role in indexed if role == 'answer'}
                self.assertEqual(answers, {f'Q{i}' for i in range(1, QUESTION_COUNTS[number - 1] + 1)})
                self.assertIn(('identity', 'identification'), indexed)
                self.assertEqual(nb['cells'][-1], submission_cell())
                self.assertEqual(nb['metadata']['tal_tutor']['session']['notebook'], entry['notebook'])
                total_answers += len(answers)
                total_cells += len(nb['cells'])
        self.assertEqual((total_answers, total_cells), (45, 130))

    def test_all_seven_real_evaluators_keep_nonzero_scores_and_feedback(self):
        for number, entry, subject in subjects():
            with self.subTest(evaluator=entry['id']):
                nb = observed_copy(number, subject)
                legacy = copy.deepcopy(nb)
                legacy['cells'].pop()  # The added infrastructure is not an answer.
                legacy['metadata'].pop('tal')
                for cell in legacy['cells']:
                    cell['metadata'].pop('tal')
                evaluate = importlib.import_module(EVALUATORS[entry['evaluator']][1]).check_notebook
                current = evaluate(json.dumps(nb), 'nom-libre.ipynb')
                previous = evaluate(json.dumps(legacy), 'ancien_nom_python_texte.ipynb')
                self.assertEqual(current, previous)
                self.assertEqual((current[0], current[2], current[4]), (1, QUESTION_COUNTS[number - 1], None))
                # The identity and answer in a restitution cell must never count.
                no_answer = copy.deepcopy(nb)
                answer = validate_cell_metadata(no_answer)['Q1', 'answer']
                trace = copy.deepcopy(answer['outputs'])
                answer['outputs'] = []
                no_answer['cells'][-1]['source'] = [
                    '# Complétez les informations entre les guillemets.\n',
                    'nom = "Intrus"\nprenom = "Intrus"\nclasse = "Intrus"\n',
                    'raise RuntimeError("Le serveur ne doit pas exécuter cette cellule")\n',
                    Q1_PROBES[number][0]]
                no_answer['cells'][-1]['outputs'] = trace
                rejected_trace = evaluate(json.dumps(no_answer), 'copie.ipynb')
                self.assertEqual(rejected_trace[0], 0)
                self.assertEqual(rejected_trace[3]['nom'], 'Modele')
                self.assertIsNone(rejected_trace[4])

    def test_single_entry_routes_all_seven_independently_of_uploaded_filename(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(outils, 'BASE_DIR', directory):
            app = create_app()
            app.config.update(TESTING=True)
            client = app.test_client()
            for number, entry, subject in subjects():
                with self.subTest(evaluator=entry['id']):
                    nb = observed_copy(number, subject)
                    response = client.post('/submit', data={
                        'file': (io.BytesIO(json.dumps(nb).encode()), 'mon_travail.ipynb')},
                        content_type='multipart/form-data')
                    self.assertEqual(response.status_code, 200)
                    self.assertTrue((Path(directory) / entry['evaluator'] / 'S1').is_dir())
                    self.assertIn('MODELE', response.get_data(as_text=True).upper())
            self.assertEqual({p.name for p in Path(directory).iterdir()},
                             {f'td{n}-s1' for n in range(1, 8)})


if __name__ == '__main__':
    unittest.main()
