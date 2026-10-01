"""Non-executing R0/R1/R2 contract tests; saved traces are explicit fixtures."""
import copy
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
from notebook_contract import load_catalog, resolve_notebook, ContractError
from revision_s3 import check_revision, R1_TOKENS, R2_TOKENS, TEXT_R0, _freq


def answer(q, source, value):
    return {'cell_type': 'code', 'metadata': {'tal': {'question': f'Q{q}', 'role': 'answer'}},
            'source': source, 'outputs': [{'output_type': 'stream', 'name': 'stdout',
            'text': f'Résultat Q{q} : {value!r}\n'}]}


def fixture(r):
    identity = {'cell_type': 'code', 'metadata': {'tal': {'question': 'identity', 'role': 'identification'}},
                'source': 'nom="Modele"\nprenom="Test"\nclasse="S3"\nnumero_etudiant="900001"', 'outputs': []}
    if r == 0:
        cells = [answer(1, '''def compter_mots(texte):
    return len(texte.split())
x={'principal':compter_mots(texte),'vide':compter_mots(''),'essai':compter_mots('Un essai')}
print('Résultat Q1 :',x)''', {'principal': 15, 'vide': 0, 'essai': 2}),
        answer(2, '''mots_normalises=texte.lower().split()
print('Résultat Q2 :',mots_normalises)''', TEXT_R0.lower().split()),
        answer(3, '''def frequences(texte):
    comptes={}
    for mot in texte.lower().split():
        comptes[mot]=comptes.get(mot,0)+1
    return comptes
x={'principal':dict(frequences(texte)),'essai':dict(frequences('Mot mot autre'))}
print('Résultat Q3 :',x)''', {'principal': _freq(TEXT_R0.lower().split()), 'essai': {'mot':2,'autre':1}}),
        answer(4, '''limite='La ponctuation conserve des formes distinctes.'
x={'comptes':frequences('Python Python.'),'limite':limite}
print('Résultat Q4 :',x)''', {'comptes': {'python':1,'python.':1}, 'limite':'La ponctuation conserve des formes distinctes.'})]
    elif r == 1:
        cells = [answer(1, "doc=nlp(texte)\nprint('Résultat Q1 :',len(doc))", 8),
        answer(2, "annotations=[]\nfor token in doc:\n    annotations.append((token.text,token.lemma_,token.pos_))\nprint('Résultat Q2 :',annotations)", R1_TOKENS),
        answer(3, "noms=[token.lemma_ for token in doc if token.pos_=='NOUN']\nprint('Résultat Q3 :',noms)", ['traducteur','document']),
        answer(4, "verbes=[]\nfor token in doc:\n    if token.pos_=='VERB':\n        verbes.append(token.lemma_)\nprint('Résultat Q4 :',verbes)", [])]
    else:
        fn = '''def frequences_lemmas(texte,stopwords=None):
    doc=nlp(texte)
    lemmes=[token.lemma_ for token in doc if token.pos_=='NOUN']
    return Counter(lemmes)
'''
        filtered = '''def frequences_lemmas(texte,stopwords=None):
    if stopwords is None:
        stopwords=[]
    doc=nlp(texte)
    lemmes=[token.lemma_ for token in doc if token.pos_=='NOUN' and not token.is_stop and token.lemma_ not in stopwords]
    return Counter(lemmes)
'''
        expected = {'texte':2,'terme':1,'répétition':1}
        cells = [answer(1, fn+"print('Résultat Q1 :',dict(frequences_lemmas(texte)))", expected),
        answer(2, "annotations=[(token.text,token.lemma_,token.pos_) for token in nlp(texte)]\nprint('Résultat Q2 :',annotations)", R2_TOKENS),
        answer(3, filtered+"tests={'sans_exclusions':dict(frequences_lemmas(texte)),'avec_exclusions':dict(frequences_lemmas(texte,['texte']))}\nprint('Résultat Q3 :',tests)",
               {'sans_exclusions':expected,'avec_exclusions':{'terme':1,'répétition':1}}),
        answer(4, "classements={'avant':frequences_lemmas(texte).most_common(),'apres':frequences_lemmas(texte,['texte']).most_common()}\nprint('Résultat Q4 :',classements)",
               {'avant':[('texte',2),('terme',1),('répétition',1)],'apres':[('terme',1),('répétition',1)]})]
    evaluator = f'td-r{r}-s3'
    return {'metadata': {'tal': {'id': evaluator, 'evaluator': evaluator, 'version':2}}, 'cells': [identity]+cells}


def grade(r, notebook):
    return check_revision(json.dumps(notebook), f'td-r{r}-s3')


class RevisionChecks(unittest.TestCase):
    def test_reference_traces_all_questions(self):
        for r in range(3):
            result = grade(r,fixture(r))
            self.assertIsNone(result[4])
            self.assertEqual(result[0],4,result[1])

    def test_versions_identity_and_question_contract(self):
        for r in range(3):
            for version in [None,1,True,'2',3]:
                nb=fixture(r)
                if version is None: nb['metadata'].pop('tal')
                else: nb['metadata']['tal']['version']=version
                self.assertEqual(grade(r,nb)[4],'mauvaise version du notebook')
            nb=fixture(r); nb['cells'][1]['metadata']={}
            self.assertEqual(grade(r,nb)[4],'mauvaise version du notebook')
            nb=fixture(r); nb['cells'][0]['source']='nom="Modele"'
            self.assertIn('numéro étudiant',grade(r,nb)[4])
            nb=fixture(r); nb['cells'].append(copy.deepcopy(nb['cells'][1]))
            self.assertTrue(grade(r,nb)[4])

    def test_wrong_values_and_markers_do_not_score(self):
        for r in range(3):
            nb=fixture(r)
            for q, cell in enumerate(nb['cells'][1:],1):
                cell['outputs'][0]['text']=f'Résultat Q{q} : False\n'
            self.assertEqual(grade(r,nb)[0],0)

    def test_examples_and_wrong_cells_do_not_supply_answers(self):
        for r in range(3):
            nb=fixture(r)
            for cell in list(nb['cells'][1:]):
                decoy=copy.deepcopy(cell)
                decoy['metadata']['tal']['role']='example'
                nb['cells'].append(decoy)
                cell['source']='';cell['outputs']=[]
            self.assertEqual(grade(r,nb)[0],0)

    def test_spacing_parameter_names_cell_order_and_ties(self):
        for r in range(3):
            nb=fixture(r)
            for cell in nb['cells'][1:]:
                cell['source']=cell['source'].replace('doc=nlp','doc = nlp')
            if r==0:
                nb['cells'][1]['source']=nb['cells'][1]['source'].replace('def compter_mots(texte):\n    return len(texte.split())','def compter_mots(message):\n    return len(message.split())')
            if r==2:
                nb['cells'][3]['source']=nb['cells'][3]['source'].replace('not token.is_stop','token.is_stop == False')
                nb['cells'][4]['outputs'][0]['text']="Résultat Q4 : {'avant':[('texte',2),('répétition',1),('terme',1)],'apres':[('répétition',1),('terme',1)]}\n"
            nb['cells'].reverse()
            self.assertEqual(grade(r,nb)[0],4,grade(r,nb)[1])

    def test_local_lemma_alias_in_filtered_loop(self):
        nb=fixture(2)
        source=nb['cells'][3]['source']
        source=source.replace("    lemmes=[token.lemma_ for token in doc if token.pos_=='NOUN' and not token.is_stop and token.lemma_ not in stopwords]", "    lemmes=[]\n    for token in doc:\n        lemme=token.lemma_\n        if token.pos_=='NOUN' and not token.is_stop and lemme not in stopwords:\n            lemmes.append(lemme)")
        nb['cells'][3]['source']=source
        self.assertEqual(grade(2,nb)[0],4,grade(2,nb)[1])

    def test_invalid_outputs_and_sources_remain_local(self):
        for value in [None,{},1,['bad',1]]:
            nb=fixture(0);nb['cells'][4]['source']=value
            self.assertIsNone(grade(0,nb)[4]);self.assertEqual(grade(0,nb)[0],3)
        for output in [[{'output_type':'error','ename':'ValueError'}],None,[42],
                       [{'output_type':'stream','text':None}]]:
            nb=fixture(1);nb['cells'][1]['outputs']=output
            self.assertEqual(grade(1,nb)[0],3)

    def test_static_prerequisite_does_not_require_earlier_output(self):
        for r,q in [(0,3),(1,1),(2,1),(2,3)]:
            nb=fixture(r);nb['cells'][q]['outputs']=[]
            self.assertEqual(grade(r,nb)[0],3,grade(r,nb)[1])

    def test_hardcoded_return_and_disconnected_or_overwritten_calculation(self):
        nb=fixture(0)
        nb['cells'][1]['source']=nb['cells'][1]['source'].replace('return len(texte.split())','len(texte.split())\n    return 15')
        self.assertEqual(grade(0,nb)[1][0]['points'],0)
        for code in ["mots_normalises=texte.lower().split()\nmots_normalises=[]\nprint('Résultat Q2 :',mots_normalises)",
                     "mots_normalises=[]\nprint('Résultat Q2 :',mots_normalises)\nmots_normalises=texte.lower().split()",
                     "texte.lower().split()\nprint('Résultat Q2 :',[])"]:
            nb=fixture(0);nb['cells'][2]['source']=code
            self.assertEqual(grade(0,nb)[1][1]['points'],0)

    def test_ineffective_exclusions_or_wrong_pos_lemma_counts(self):
        nb=fixture(2)
        nb['cells'][3]['source']=nb['cells'][3]['source'].replace('token.lemma_ not in stopwords','token.text not in stopwords')
        self.assertEqual(grade(2,nb)[1][2]['points'],0)
        nb=fixture(2);nb['cells'][3]['outputs'][0]['text']="Résultat Q3 : {'sans_exclusions':{'texte':2,'terme':1,'répétition':1},'avec_exclusions':{'texte':2,'terme':1,'répétition':1}}"
        self.assertEqual(grade(2,nb)[1][2]['points'],0)
        nb=fixture(1);nb['cells'][4]['outputs'][0]['text']="Résultat Q4 : ['analyser']"
        self.assertEqual(grade(1,nb)[1][3]['points'],0)

    def test_no_execution_and_duplicate_results(self):
        nb=fixture(1)
        nb['cells'][1]['source']="raise RuntimeError('DO_NOT_EXECUTE')\n"+nb['cells'][1]['source']
        self.assertIsNone(grade(1,nb)[4])
        nb['cells'][1]['outputs'][0]['text']+='Résultat Q1 : 8\n'
        self.assertEqual(grade(1,nb)[1][0]['points'],0)
        nb=fixture(0);nb['cells'][1]['outputs'][0]['text']="Résultat Q1 : {'principal':15,'vide':0,'essai':2,'essai':2}"
        self.assertEqual(grade(0,nb)[1][0]['points'],0)


class RevisionRoutes(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        patcher=patch.object(outils,'BASE_DIR',self.temp.name);patcher.start();self.addCleanup(patcher.stop)
        self.client=create_app().test_client()

    def post(self, nb, path):
        return self.client.post(path,data={'file':(io.BytesIO(json.dumps(nb).encode()),'copy.ipynb')})

    def test_old_s3_never_corrects_or_persists_and_other_semesters_keep_legacy(self):
        for evaluator in ['td-r0-s3','td-r1-s3','td-r2-s3','td1-s3','controle-td1-s3']:
            for metadata in [{},{'tal':{'id':evaluator,'evaluator':evaluator,'version':0}}]:
                nb={'cells':[],'metadata':metadata}
                with patch('routes.process_submission') as persist:
                    for path in ['/submit',f'/eval/{evaluator}']:
                        response=self.post(nb,path)
                        self.assertIn('mauvaise version du notebook',response.get_data(as_text=True))
                    persist.assert_not_called()
        self.assertEqual(list(Path(self.temp.name).rglob('*')),[])
        for evaluator in ['Controletilt-s1','td2-S2']:
            self.assertIsNone(resolve_notebook({'cells':[]},evaluator,require_metadata=False))

    def test_new_reference_persists_and_renders_technical_score_safely(self):
        nb=fixture(0)
        nb['cells'][4]['source']+="\n# <script>alert('xss')</script>"
        body=self.post(nb,'/submit').get_data(as_text=True)
        self.assertIn('Score technique provisoire',body)
        self.assertIn('&lt;script&gt;',body)
        self.assertNotIn("<script>alert('xss')",body)
        copies=list(Path(self.temp.name).rglob('*.ipynb'))
        self.assertEqual(len(copies),1)
        self.assertIn('td-r0-s3-v2',str(copies[0]))
        self.assertIn('_900001_',copies[0].name)
        csv_path=next(Path(self.temp.name).rglob('*.csv'))
        import csv
        with csv_path.open() as handle:
            rows=list(csv.reader(handle,delimiter=';'))
        self.assertEqual(len(rows[0]),len(rows[1]))
        self.assertEqual(rows[1][-1],'900001')
        self.assertEqual(rows[1][7],'4.0')


if __name__=='__main__': unittest.main()
