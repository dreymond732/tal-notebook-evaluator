"""TD4 preservation and evaluator safety; independent of generated model answers."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
from notebook_contract import load_catalog, validate_cell_metadata
from routes import EVALUATORS

IDS=('td4-one-s1','td4-bis-s1','td4-ter-s1')


def fixture(identifier):
    entry=next(e for e in load_catalog() if e['id']==identifier)
    nb=json.loads((ROOT/entry['notebook']).read_text())
    validate_cell_metadata(nb)['identity','identification']['source']=(
        'nom="Exemple"\nprenom="Camille"\nclasse="S1"\nnumero_etudiant="TD4-SYNTHETIQUE"')
    return nb


def grade(identifier, notebook):
    module=importlib.import_module(EVALUATORS[identifier][1])
    return module.check_notebook(json.dumps(notebook),'nom-libre.ipynb')


class TD4ExpansionTests(unittest.TestCase):
    def test_historical_td4_and_previous_nine_subjects_are_byte_identical(self):
        proof=json.loads((ROOT/'tests/fixtures/td4_swinnen_source_baseline.json').read_text())
        self.assertEqual(proof['source_commit'],'126cf63cbae085cf095a4488d547296a7ce7df02')
        self.assertEqual(len(proof['sha256']),12)
        for path,expected in proof['sha256'].items():
            with self.subTest(path=path):
                self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),expected)

    def test_previous_nine_rubrics_remain_identical(self):
        proof=json.loads((ROOT/'tests/fixtures/td4_swinnen_source_baseline.json').read_text())
        current=json.loads((ROOT/'app/s1_expansion_rubrics.json').read_text())
        self.assertEqual(len(proof['previous_rubrics_sha256']),9)
        for identifier,expected in proof['previous_rubrics_sha256'].items():
            with self.subTest(identifier=identifier):
                actual=hashlib.sha256(json.dumps(current[identifier],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
                self.assertEqual(actual,expected)

    def test_wrong_route_and_missing_answer_are_rejected(self):
        from notebook_contract import resolve_notebook, ContractError
        for identifier in IDS:
            nb=fixture(identifier)
            with self.subTest(identifier=identifier):
                with self.assertRaises(ContractError):resolve_notebook(nb,'td4-s1')
                missing=copy.deepcopy(nb)
                missing['cells'].remove(validate_cell_metadata(missing)['Q6','answer'])
                self.assertEqual(grade(identifier,missing)[4],'mauvaise version du notebook')

    def test_infinite_loop_text_is_never_executed(self):
        modules={identifier:importlib.import_module(EVALUATORS[identifier][1]) for identifier in IDS}
        for identifier in IDS:
            nb=fixture(identifier)
            for c in nb['cells']:
                if c.get('metadata',{}).get('tal',{}).get('role')=='answer':
                    c['source']='while True:\n    raise RuntimeError("NEVER_EXECUTE")'
            with self.subTest(identifier=identifier), patch('builtins.exec',side_effect=AssertionError('No notebook execution')):
                result=modules[identifier].check_notebook(json.dumps(nb),'test.ipynb')
                self.assertEqual((result[0],result[2],result[4]),(0,6,None))

    def test_maximum_requires_search_without_builtin_shortcut(self):
        nb=fixture('td4-ter-s1')
        cell=validate_cell_metadata(nb)['Q2','answer']
        valid=('nombres=[32,5,12,8,3,75,2,15]\nnegatifs=[-8,-3,-12]\n'
               'maximum_nombres=nombres[0]\nfor nombre in nombres:\n'
               '    if nombre>maximum_nombres:\n        maximum_nombres=nombre\n'
               'maximum_negatifs=negatifs[0]\nfor nombre in negatifs:\n'
               '    if nombre>maximum_negatifs:\n        maximum_negatifs=nombre\n'
               'print("Résultat Q2 :",maximum_nombres,maximum_negatifs)')
        cell['source']=valid
        cell['outputs']=[{'output_type':'stream','name':'stdout','text':'Résultat Q2 : 75 -3\n'}]
        self.assertEqual(grade('td4-ter-s1',nb)[0],1)
        for expression in ('max(nombres)','sorted(nombres)[-1]'):
            cell['source']=('nombres=[32,5,12,8,3,75,2,15]\nnegatifs=[-8,-3,-12]\n'
                            f'for n in nombres:\n    maximum_nombres={expression}\n'
                            'maximum_negatifs=negatifs[0]\nfor n in negatifs:\n'
                            '    if n>maximum_negatifs:\n        maximum_negatifs=n\n'
                            'print("Résultat Q2 :",maximum_nombres,maximum_negatifs)')
            self.assertEqual(grade('td4-ter-s1',nb)[0],0)

    def test_frequency_comparison_requires_both_taught_constructions(self):
        nb=fixture('td4-ter-s1');cell=validate_cell_metadata(nb)['Q4','answer']
        first=('mots_a_compter="le TAL traite le langage et le texte".lower().split()\n'
               'frequences={}\nfor mot in mots_a_compter:\n'
               '    frequences[mot]=frequences.get(mot,0)+1\n')
        alternative=('frequences_autrement={}\nfor mot in mots_a_compter:\n'
                     '    if mot in frequences_autrement:\n'
                     '        frequences_autrement[mot]+=1\n'
                     '    else:\n        frequences_autrement[mot]=1\n')
        final=('total_effectifs=0\nfor mot,effectif in frequences.items():\n'
               '    total_effectifs+=effectif\n'
               'print("Résultat Q4 :",frequences,frequences_autrement,total_effectifs,len(mots_a_compter))')
        frequencies={'le':3,'tal':1,'traite':1,'langage':1,'et':1,'texte':1}
        cell['outputs']=[{'output_type':'stream','name':'stdout','text':f'Résultat Q4 : {frequencies!r} {frequencies!r} 8 8\n'}]
        cell['source']=first+alternative+final
        self.assertEqual(grade('td4-ter-s1',nb)[0],1)
        cell['source']=first+('frequences_autrement={}\nfor mot in mots_a_compter:\n'
                              '    frequences_autrement[mot]=frequences_autrement.get(mot,0)+1\n')+final
        self.assertEqual(grade('td4-ter-s1',nb)[0],0)
