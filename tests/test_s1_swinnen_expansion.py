"""Independent saved traces: nine isolated contracts, safe routing and alternatives."""
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
from app import create_app
import outils
from notebook_contract import ContractError, load_catalog, resolve_notebook, validate_cell_metadata
from routes import EVALUATORS
from s1_expansion import CHECKS

IDS = {f'td{n}-{part}-s1' for n in (3, 5, 6) for part in ('one', 'bis', 'ter')}


def fixture(identifier):
    entry = next(e for e in load_catalog() if e['id'] == identifier)
    nb = json.loads((ROOT / entry['notebook']).read_text())
    validate_cell_metadata(nb)['identity', 'identification']['source'] = (
        'nom="Exemple"\nprenom="Camille"\nclasse="S1"\nnumero_etudiant="SYNTHETIQUE-EXPANSION"')
    return nb


def answer(nb, question, source, stdout):
    cell = validate_cell_metadata(nb)[question, 'answer']
    cell['source'] = source
    cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': stdout}]


def grade(identifier, nb):
    return importlib.import_module(EVALUATORS[identifier][1]).check_notebook(json.dumps(nb), 'nom-libre.ipynb')


class ExpansionTests(unittest.TestCase):
    def test_nine_complete_contracts_blank_answers_and_no_code_execution(self):
        self.assertEqual(set(CHECKS), IDS)
        with patch('builtins.exec', side_effect=AssertionError('No student execution')):
            for identifier in sorted(IDS):
                with self.subTest(identifier=identifier):
                    nb = fixture(identifier)
                    self.assertEqual(resolve_notebook(nb)['evaluator'], identifier)
                    for cell in nb['cells']:
                        if cell['cell_type'] == 'code' and cell['metadata']['tal']['role'] == 'answer':
                            cell['source'] = 'raise RuntimeError("NEVER_EXECUTE")'
                    # Import before the exec trap would be needed for a new module;
                    # modules are preloaded by setUpModule below.
                    score, details, maximum, info, error = grade(identifier, nb)
                    self.assertEqual((score, maximum, error), (0, 6, None))
                    self.assertEqual(info['relecture_humaine'], 'facultative')
                    self.assertEqual(len([d for d in details if d['max_points']]), 6)
                    malformed = copy.deepcopy(nb)
                    malformed['metadata']['tal']['version'] = 1
                    self.assertEqual(grade(identifier, malformed)[4], 'mauvaise version du notebook')
                    missing = copy.deepcopy(nb)
                    missing['cells'].remove(validate_cell_metadata(missing)['Q6', 'answer'])
                    self.assertEqual(grade(identifier, missing)[4], 'mauvaise version du notebook')

    def test_lexicon_variants_are_consistent_and_order_independent(self):
        for choice in ('langue', 'langage'):
            nb = fixture('td3-ter-s1')
            lex = {'language': choice, 'book': 'livre', 'data': 'données'}
            source = f'lexique = {lex!r}\nlexique["corpus"]="corpus"\nprint("Résultat Q1a :", lexique["language"])\nprint("Résultat Q1b :", lexique)\nentrees=[]\nfor cle,valeur in lexique.items():\n    entrees.append(cle + " -> " + valeur)\nprint("Résultat Q1 :", entrees)'
            lex['corpus'] = 'corpus'
            entries = [k+' -> '+v for k,v in lex.items()]
            stdout = f'Résultat Q1a : {choice}\nRésultat Q1b : {lex!r}\nRésultat Q1 : {entries!r}\n'
            answer(nb, 'Q1', source, stdout)
            self.assertEqual(grade('td3-ter-s1', nb)[0], 1)
            answer(nb, 'Q1', source, stdout.replace('Résultat Q1a : '+choice, 'Résultat Q1a : incohérent'))
            self.assertEqual(grade('td3-ter-s1', nb)[0], 0)

    def test_record_pairs_accept_both_sequence_types_but_keep_fields_strict(self):
        for constructor in ('list', 'tuple'):
            nb = fixture('td6-bis-s1')
            source = f'with open("affiliations_s1.txt", encoding="utf-8") as fichier:\n    texte=fichier.read()\nenregistrements=[]\nfor ligne in texte.splitlines():\n    enregistrements.append({constructor}(ligne.split(";",1)))\nprint("Résultat Q1 :", enregistrements[0])\nprint("Résultat Q1b :", enregistrements)'
            rows = [('durand alice','Laboratoire TAL'),('DURAND ALICE','Laboratoire TAL'),('Durand Alice','Centre de traduction'),('Martin bob','Centre de traduction'),('MARTIN BOB','Centre de traduction')]
            if constructor == 'list': rows = [list(row) for row in rows]
            answer(nb, 'Q1', source, f'Résultat Q1 : {rows[0]!r}\nRésultat Q1b : {rows!r}\n')
            self.assertEqual(grade('td6-bis-s1', nb)[0], 1)
            rows[0] = [123, 'Laboratoire TAL']
            answer(nb, 'Q1', source, f'Résultat Q1 : {rows[0]!r}\nRésultat Q1b : {rows!r}\n')
            self.assertEqual(grade('td6-bis-s1', nb)[0], 0)

    def test_csv_reader_links_saved_writes_without_execution(self):
        from s1_revision import collect
        for imports, writer, reader in [('import csv', 'csv.writer', 'csv.reader'),
                                         ('import csv as c', 'c.writer', 'c.reader'),
                                         ('from csv import reader as lire, writer as ecrire', 'ecrire', 'lire')]:
            nb = fixture('td6-ter-s1')
            source = (imports + '\nwith open("documents.csv", "w", encoding="utf-8", newline="") as sortie:\n'
                      + f'    ecrivain={writer}(sortie)\n'
                      + '    ecrivain.writerow(["document","pages"])\n'
                      + '    ecrivain.writerow(["rapport",12])\n'
                      + '    ecrivain.writerow(["note",3])\n'
                      + 'with open("documents.csv", encoding="utf-8", newline="") as entree:\n'
                      + f'    documents_relus=list({reader}(entree))\n'
                      + 'print("Résultat Q1 :", documents_relus)')
            output = "Résultat Q1 : [['document', 'pages'], ['rapport', '12'], ['note', '3']]\n"
            answer(nb, 'Q1', source, output)
            self.assertEqual(grade('td6-ter-s1', nb)[0], 1)
            proof = collect(nb)[0]['Q1'][0][1]
            self.assertTrue(proof.calls('writer'))
            self.assertTrue(proof.calls('writerow'))
            answer(nb, 'Q1', 'documents_relus=[["document","pages"],["rapport","12"],["note","3"]]\nprint("Résultat Q1 :", documents_relus)', output)
            self.assertEqual(grade('td6-ter-s1', nb)[0], 0)

    def test_csv_import_in_taught_example_is_context_not_answer_credit(self):
        nb = fixture('td6-ter-s1')
        source = ('with open("documents.csv", "w", newline="") as f:\n'
                  '    w=csv.writer(f)\n    w.writerow(["document","pages"])\n'
                  '    w.writerow(["rapport",12])\n    w.writerow(["note",3])\n'
                  'with open("documents.csv", newline="") as f:\n'
                  '    rows=list(csv.reader(f))\nprint("Résultat Q1 :", rows)')
        output="Résultat Q1 : [['document', 'pages'], ['rapport', '12'], ['note', '3']]\n"
        answer(nb, 'Q1', source, output)
        self.assertEqual(grade('td6-ter-s1', nb)[0], 1)
        # Writes in the example must never supply the student's construction.
        extra=copy.deepcopy(validate_cell_metadata(nb)['Q1','answer'])
        extra['metadata']['tal']={'question':'fake-example','role':'example'}
        nb['cells'].insert(2,extra)
        answer(nb,'Q1','import csv\nwith open("documents.csv") as f:\n    rows=list(csv.reader(f))\nprint("Résultat Q1 :", rows)', output)
        self.assertEqual(grade('td6-ter-s1', nb)[0], 0)

    def test_unordered_csv_keeps_header_counts_and_distinct_affiliations(self):
        from s1_revision import Proof
        validator = CHECKS['td6-ter-s1'][4]['traces']['Q5']
        proof = Proof((), (None,), '', {})
        rows = [['personne','nb_affiliations','affiliations'], ['Martin Bob','1','Centre de traduction'], ['Durand Alice','2','Laboratoire TAL | Centre de traduction']]
        self.assertTrue(validator(repr(rows), proof, {}))
        for bad in (
            [rows[1], rows[0], rows[2]],
            [rows[0], rows[1], ['Durand Alice','1','Laboratoire TAL | Centre de traduction']],
            [rows[0], rows[1], ['Durand Alice','2','Laboratoire TAL | Laboratoire TAL']],
            [rows[0], rows[1], rows[2], rows[2]],
        ):
            self.assertFalse(validator(repr(bad), proof, {}))

    def test_all_nine_routes_auto_submission_and_separate_persistence(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(outils, 'BASE_DIR', directory):
            app = create_app(); app.config['TESTING'] = True
            client = app.test_client()
            for identifier in sorted(IDS):
                self.assertEqual(client.get('/eval/'+identifier).status_code, 200)
                response = client.post('/submit', data={'file': (io.BytesIO(json.dumps(fixture(identifier)).encode()), 'travail.ipynb')}, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 200)
                self.assertTrue((Path(directory)/(identifier+'-v2')/'S1').is_dir())
            self.assertEqual({p.name for p in Path(directory).iterdir()}, {identifier+'-v2' for identifier in IDS})


def setUpModule():
    for identifier in IDS:
        importlib.import_module(EVALUATORS[identifier][1])
