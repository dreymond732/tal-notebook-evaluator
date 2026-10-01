# Sondes de reproduction de la revue S3

Référence : `c649cfe51f0dce66efcaef7aad652c0b92d606ad`.
Ces scripts sont du code d'audit enseignant, non des solutions étudiantes. Ils
construisent des traces JSON inertes et appellent les validateurs ; ils n'exécutent
pas le code des cellules. Les tests HTTP utilisent une persistance temporaire.

Enregistrer chaque bloc sous le nom indiqué, adapter sa constante `ROOT` au chemin
du clone à auditer, puis lancer `python NOM_DU_SCRIPT.py` dans un environnement
contenant les dépendances serveur. Les valeurs attendues sont celles de la
référence auditée ; des assertions peuvent donc cesser de reproduire un défaut
après sa correction. Ne pas les exécuter contre le serveur de production.
Les scripts ci-dessous couvrent attribution/dépôt, défauts de TD1–TD3 et références
quantitatives des sept contrôles ; les 169 tests du dépôt complètent ces sondes.

## transverse.py

```python
"""Read-only product audit: synthetic uploads, isolated temporary persistence."""
import copy
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path('/workspace/scratch/299f4372d5c4/tal-s3-complete-audit')
sys.path.insert(0, str(ROOT / 'app'))
from app import create_app
import outils
import routes
from notebook_contract import load_catalog

entries = [e for e in load_catalog() if e['semester'] == 'S3' and not e['id'].startswith('td-r')]
app = create_app()
app.config.update(TESTING=True)
results = {'scope': len(entries), 'identity': [], 'homonyms': [], 'metadata_fallback': {}}
results['identity_parser'] = {}
for case, source in {'reordered': 'prenom="Alice"\nnom="Dupont"\nclasse="G1"',
                     'comment': '# nom="Commentaire"\nnom="Dupont"\nprenom="Alice"\nclasse="G1"'}.items():
    results['identity_parser'][case] = outils.extract_identification_info([
        {'cell_type': 'code', 'metadata': {'tal': {'question': 'identity', 'role': 'identification'}}, 'source': source}])

def post(client, nb):
    return client.post('/submit', data={'file': (io.BytesIO(json.dumps(nb).encode()), 'copie.ipynb')}, content_type='multipart/form-data')

def identity(nb, number, blank=False):
    cell = next(c for c in nb['cells'] if c.get('metadata', {}).get('tal', {}).get('role') == 'identification')
    cell['source'] = ('nom=""\nprenom=""\nclasse="G1"\n' if blank else 'nom="Modele"\nprenom="Test"\nclasse="G1"\n') + f'numero_etudiant="{number}"'

with app.test_client() as client:
    for entry in entries:
        source = json.loads((ROOT / entry['notebook']).read_text())
        blank = copy.deepcopy(source)
        identity(blank, '', blank=True)
        with tempfile.TemporaryDirectory() as directory, patch.object(outils, 'BASE_DIR', directory):
            response = post(client, blank)
            files = list(Path(directory).rglob('*'))
            results['identity'].append({'id': entry['id'], 'status': response.status_code,
                'notebooks': len([p for p in files if p.suffix == '.ipynb']),
                'reports': len([p for p in files if p.suffix == '.html'])})
        with tempfile.TemporaryDirectory() as directory, patch.object(outils, 'BASE_DIR', directory):
            for number in ('100001', '100002'):
                nb = copy.deepcopy(source)
                identity(nb, number)
                post(client, nb)
            files = list(Path(directory).rglob('*'))
            csv_file = next(p for p in files if p.suffix == '.csv')
            rows = list(csv.reader(csv_file.open(), delimiter=';'))
            results['homonyms'].append({'id': entry['id'],
                'notebooks_after_two': len([p for p in files if p.suffix == '.ipynb']),
                'reports_after_two': len([p for p in files if p.suffix == '.html']),
                'csv_rows': len(rows) - 1, 'student_number_column': 'Numéro étudiant' in rows[0]})
    # A provided cell cannot score with explicit metadata, but dropping every cell
    # contract turns on legacy collection even though notebook metadata is v1.
    payload = {'metadata': {'tal': {'id': 'td4-s3', 'version': 1, 'evaluator': 'td4-s3'}}, 'cells': [
        {'cell_type': 'code', 'metadata': {'tal': {'question': 'example', 'role': 'example'}},
         'source': 'print("S3_TD4_Q1:", value)', 'outputs': [{'output_type': 'stream', 'name': 'stdout',
            'text': 'S3_TD4_Q1: {"chat":2,"livre":2,"N":4}\n'}]},
        {'cell_type': 'code', 'metadata': {'tal': {'question': 'Q1', 'role': 'answer'}}, 'source': '', 'outputs': []}]}
    for label in ('tagged', 'no_cell_metadata'):
        nb = copy.deepcopy(payload)
        if label == 'no_cell_metadata':
            for cell in nb['cells']:
                cell['metadata'] = {}
        with patch('routes.process_submission') as persistence:
            response = post(client, nb)
            results['metadata_fallback'][label] = {'status': response.status_code, 'persisted': persistence.called,
                'score': persistence.call_args.args[4] if persistence.called else None}

print(json.dumps(results, ensure_ascii=False, indent=2))
```

## td0_3.py

```python
"""Read-only evaluator probes: constructed JSON only; no submitted source executed."""
import sys,json,copy,re,importlib
from pathlib import Path
ROOT=Path('/workspace/scratch/299f4372d5c4/tal-s3-complete-audit')
sys.path.insert(0,str(ROOT/'app'))
from s3_audit_data import TEXT0,TEXT1,TEXT2
import app_correction_TD3_S3 as td3
import s3_audit_linguistic as ling

def trace(td,q,v):
 return {'cell_type':'code','metadata':{'tal':{'question':f'Q{q}','role':'answer'}},'source':f'print("S3_TD{td}_Q{q}:", json.dumps(resultat_q{q}))','outputs':[{'output_type':'stream','name':'stdout','text':f'S3_TD{td}_Q{q}: '+json.dumps(v)+'\n'}]}
def run(td,values,transform=None):
 cells=[trace(td,q,v) for q,v in values.items()]
 if transform: transform(cells)
 nb={'metadata':{'tal':{'id':f'td{td}-s3','evaluator':f'td{td}-s3','version':1}},'cells':cells}
 r=importlib.import_module(f'app_correction_TD{td}_S3').check_notebook(json.dumps(nb),'audit.ipynb')
 return {'score':r[0],'max':r[2],'questions':[d['check'].split(' — ')[0] for d in r[1] if d['points']],'error':r[4]}

def row(form,source,pos='NOUN',lemma=None):
 p=source.index(form);return {'forme':form,'lemme':lemma or form.lower(),'pos':pos,'tag':None,'debut':p,'fin':p+len(form)}

results={}
# False but structurally plausible TD1: one 'token' equal to whole source, arbitrary counts.
t1={1:{'annotations':[row(TEXT1,TEXT1)]},2:{'phrases':[{'texte':TEXT1,'tokens':len(TEXT1)}]},3:{'noms':[TEXT1.lower()],'verbes':[],'mots_pleins':[TEXT1.lower()]},4:{'verbe':'Les','verbe_debut':0,'dependant':'Les','dependant_debut':0,'relation':'obj','interpretation':''},5:{'split':len(TEXT0.split()),'tokens':len(TEXT0),'non_ponctuation':1,'interpretation':''},6:{'texte':TEXT1,'phrases':4,'annotations':[row(w,TEXT1) for w in ['Elles','comparent','ensuite','résultats','interprétation']],'noms':['inventé'],'verbes':['inventer'],'question':''}}
results['TD1_false_but_plausible']=run(1,t1)
oversized=copy.deepcopy(t1[1]);oversized['annotations'][0]['fin']=999
results['TD1_Q1_out_of_range_fin']=run(1,{1:oversized})
# Q3 order/repeats: explicit annotations list known to evaluator; reversing still accepted.
anns=[{'forme':m.group(),'lemme':m.group().lower(),'pos':'NOUN','tag':'NOUN','debut':m.start(),'fin':m.end()} for m in re.finditer(r'\w+',TEXT1)]
results['TD1_Q3_reversed_mots_pleins']=run(1,{1:{'annotations':anns},3:{'noms':[r['lemme'] for r in anns],'verbes':[],'mots_pleins':[r['lemme'] for r in reversed(anns)]}})
# Completely invented frequencies propagate all the way to full TD2.
words=TEXT2.split()[:10]
t2={1:{'caracteres':len(TEXT2),'phrases':1,'tokens':len(TEXT2),'annotations':[{'forme':w,'lemme':'zzz','pos':'NOUN'} for w in words]},2:{'noms':{'licorne':2,'dragon':1},'verbes':{'voler':1}},3:{'exclusions':['licorne'],'avant':{'licorne':2,'dragon':1},'apres':{'dragon':1},'justification':''},4:{'pos':{'NOUN':1},'top3':[['NOUN',1]],'limite':''},5:{'lemmes':['invente'],'controle':[{'forme':'L','lemme':'zzz','pos':'NOUN','jugement':''}]*5,'limite_modele':''},6:{'frequences':{'dragon':1},'hypothese':'','verification':''},7:{'general_noms':{'licorne':2,'dragon':1},'specialise_noms':{'licorne':2,'dragon':1},'general_verbes':{'voler':1},'specialise_verbes':{'voler':1},'combine':{'licorne':2,'dragon':1,'voler':1},'comparaison':''}}
results['TD2_false_but_plausible']=run(2,t2)
# Wrong input structurally invalid for Q2 still powers dependent question.
invalidq2={'noms':{'notice':True,'livre':1},'verbes':{'lire':1}}
results['TD2_invalid_parent_propagation']=run(2,{2:invalidq2,3:{'exclusions':['notice'],'avant':{'notice':1,'livre':1},'apres':{'livre':1},'justification':''},6:{'frequences':{'livre':1},'hypothese':'','verification':''},7:{'general_noms':{'notice':1,'livre':1},'specialise_noms':{'notice':1,'livre':1},'general_verbes':{'lire':1},'specialise_verbes':{'lire':1},'combine':{'notice':1,'livre':1,'lire':1},'comparaison':''}})
# The three pieces prove only one distinct pivot occurrence.
source,_=td3.resources();m=next(re.finditer(r'\bintelligence\b',source,re.I))
proofs=[{'debut':m.start()-i,'fin':m.end()+i,'passage':source[m.start()-i:m.end()+i]} for i in range(3)]
results['TD3_Q7_same_occurrence_three_windows']=run(3,{7:{'affirmation':'G1','preuves':proofs,'convention_proposee':'','limite':''}})
# Position fin outside corpus accepted due Python slicing clamp.
proofs=[{'debut':m.start(),'fin':len(source)+i,'passage':source[m.start():]} for i in range(1,4)]
results['TD3_Q7_out_of_range_fin_helper']=td3.evidence({'affirmation':'G1','preuves':proofs,'convention_proposee':'','limite':''})
# small source known index; fin beyond end includes final '.', provenance-only scope yet positions wrong.
s='Les lecteurs lisent. Une lectrice lit.';exact=[{'forme':'lit','debut':s.index('lit'),'fin':s.index('lit')+3}]
results['TD3_Q3_out_of_range_fin']=run(3,{3:{'fragment':exact,'forme':exact,'lemme':[{'forme':s,'debut':0,'fin':999}],'explication':''}})
results['TD0_empty_required_explanation']=run(0,{7:{'split':['L’analyse,','c’est','utile','!'],'limites':''}})
# Safeguards should correctly reject these cases, without executing submitted source.
from app_correction_TD0_S3 import EXPECTED
results['TD0_correct']=run(0,dict(enumerate(EXPECTED,1)))
results['TD0_false_value']=run(0,{1:{'caracteres':0}})
results['TD0_recorded_error']=run(0,{1:EXPECTED[0]},lambda cells:cells[0]['outputs'].append({'output_type':'error','ename':'Error','evalue':'fixture','traceback':[]}))
results['TD0_source_comments_only']=run(0,{1:EXPECTED[0]},lambda cells:cells[0].update(source='# '+cells[0]['source']))
results['TD0_source_wrong_role']=run(0,{1:EXPECTED[0]},lambda cells:cells[0]['metadata']['tal'].update(role='example'))
results['TD0_print_inside_if']=run(0,{1:EXPECTED[0]},lambda cells:cells[0].update(source='if True:\n    '+cells[0]['source']))
results['TD0_source_crashes_before_print_but_no_error_trace']=run(0,{1:EXPECTED[0]},lambda cells:cells[0].update(source='raise ValueError("inert")\n'+cells[0]['source']))
print(json.dumps(results,ensure_ascii=False,indent=2))
```

## c1_4.py

```python
"""Read-only S3 C1-C4 audit; constructs inert fictional trace fixtures, never executes uploaded code."""
import sys, json, re, importlib, copy, tempfile, io
from pathlib import Path
from collections import Counter
from unittest.mock import patch
ROOT=Path('/workspace/scratch/299f4372d5c4/tal-s3-complete-audit')
sys.path.insert(0,str(ROOT/'app'))
import outils
from app import create_app
from s3_controls_data import C1,C2,C3
from s3_controls_linguistic import annotations, freq, concordances, spans, citations, normalize
from s3_controls_quantitative import EXPECTED

def rows(source):
    result=[]
    for m in re.finditer(r'\w+|[^\w\s]',source):
        form=m[0]; punctuation=not form.isalnum()
        pos='VERB' if form=='observe' else 'PUNCT' if punctuation else 'NOUN'
        result.append(dict(forme=form,lemme=form.lower(),pos=pos,tag=pos,debut=m.start(),fin=m.end(),ponctuation=punctuation,espace=False,mot_vide=False))
    assert annotations(result,source)
    return result

def c1_values():
    s=C1['texte_musee']; r=rows(s); w=s.lower().split()
    return [dict(caracteres=len(s),split=s.split(),frequences=dict(Counter(w)),formes=len(set(w))),
            {'annotations':r},
            dict(phrases=[dict(texte=s,debut=0,fin=len(s),tokens=len(r))],total_tokens=len(r)),
            dict(noms=[x['lemme'] for x in r if x['pos']=='NOUN'],verbes=['observe'],contenu=[x['lemme'] for x in r if x['pos'] in {'NOUN','VERB','ADJ'}]),
            dict(verbe='observe',verbe_debut=s.index('observe'),dependant='visiteuse',dependant_debut=s.index('visiteuse'),relation='TEST_RELATION_NON_CERTIFIEE'),
            dict(annotations=rows(C1['texte_transport']),split=len(C1['texte_transport'].split()),tokens=len(rows(C1['texte_transport'])),lexicaux=sum(not x['ponctuation'] for x in rows(C1['texte_transport']))),
            dict(bilans=[dict(id=id,caracteres=len(src),split=len(src.split()),tokens=len(rows(src)),phrases=1 if src else 0,annotations=rows(src)) for id,src in [('musee',s),('transport',C1['texte_transport']),('meteo',C1['texte_meteo']),('vide','')]])]

def c2_values():
    r=rows(C2['texte_atelier']); other=rows(C2['texte_alimentation']); counts=dict(Counter(x['pos'] for x in r if not x['ponctuation']))
    return [dict(annotations=r,caracteres=len(C2['texte_atelier'])),dict(noms=freq(r,{'NOUN'}),verbes=freq(r,{'VERB'})),dict(exclusions=['atelier'],avant=freq(r,{'NOUN'}),apres=freq(r,{'NOUN'},['atelier'])),dict(pos=counts,top3=[[k,v] for k,v in sorted(counts.items(),key=lambda x:-x[1])[:3]]),dict(noms={'marin':1,'caisse':2},verbes={'charger':1,'rester':1},combine={'marin':1,'caisse':2,'charger':1,'rester':1},exclus={'marin':1,'charger':1,'rester':1},vide={}),dict(frequences=freq(r,{'NOUN'},['atelier'])),dict(annotations=other,noms=freq(other,{'NOUN'}),verbes=freq(other,{'VERB'}),combine=freq(other,{'NOUN','VERB'}),vide={})]

def c3_values():
    s=C3['texte_patrimoine']; n=normalize(s)
    return [dict(caracteres=len(s),split=len(s.split()),formes=len(set(s.lower().split())),citations=[r['id'] for r in C3['citations']]),dict(concordances=concordances(s,'plan',12),absent=[]),dict(fragment=spans(s,'plan'),forme=spans(s,'plan',True),expression=spans(s,'comptes rendus',True),lemme=[dict(forme=s[:2],debut=0,fin=2)]),dict(citations=citations(s,C3['citations'])),dict(normalisees=[dict(id=r['id'],retrouvee=normalize(r['citation']) in n,debut_normalise=n.find(normalize(r['citation']))) for r in C3['citations']],candidats=[dict(id=i,passage=s[:2],debut=0,fin=2) for i in ['P2','P3']]),dict(tests=[dict(id=t['id'],resultats=concordances(t['source'],t['motif'],t['largeur']),erreur=not bool(t['motif'])) for t in C3['tests_concordance']]),dict(fragment=concordances(C3['texte_radio'],'port',10),forme=spans(C3['texte_radio'],'port',True),citations=citations(C3['texte_radio'],C3['citations_radio']))]

def nb(n,values):
    doc=json.loads((ROOT/f'Notebooks contrôles finaux/S3/Controle_TD{n}_S3.ipynb').read_text())
    for c in doc['cells']:
        m=c.get('metadata',{}).get('tal',{})
        if m.get('role')=='answer':
            q=int(m['question'][1:]); value=values[q-1]
            c['source']=f'print("S3_C{n}_Q{q}:", json.dumps(resultat_q{q}, ensure_ascii=False))'
            c['outputs']=[dict(output_type='stream',name='stdout',text=f'S3_C{n}_Q{q}: '+json.dumps(value,ensure_ascii=False)+'\n')]
    return doc

def evaluate(n,doc):
    return importlib.import_module(f'app_correction_Controle_TD{n}_S3').check_notebook(json.dumps(doc),'fixture.ipynb')

result={}; values={1:c1_values(),2:c2_values(),3:c3_values(),4:EXPECTED[4]}
for n,v in values.items():
    out=evaluate(n,nb(n,v)); assert out[0]==20 and out[2]==20 and out[4] is None
result['synthetic_consistent_traces_score']={n:evaluate(n,nb(n,v))[0] for n,v in values.items()}
result['note']='C1-C3 annotations deliberately synthetic: proves consistency-only scope, NOT linguistic truth.'

# Independent full C4 oracle from preexisting Designer fixture.
fixture=json.loads((ROOT/'tests/fixtures/s3_controls_quantitative_expected.json').read_text())['4']
assert evaluate(4,nb(4,[fixture[f'Q{q}'] for q in range(1,8)]))[0]==20

def leaves(x,path=()):
    if isinstance(x,dict):
        for k,v in x.items(): yield from leaves(v,path+(k,))
    elif isinstance(x,list):
        for k,v in enumerate(x): yield from leaves(v,path+(k,))
    else: yield path,x

def setpath(x,path,value):
    for key in path[:-1]: x=x[key]
    x[path[-1]]=value
mutations=0
for q,v in enumerate(values[4],1):
    for path,val in leaves(v):
        if type(val) is not int: continue
        for replacement in (val+1, bool(val)):
            bad=copy.deepcopy(values[4]); setpath(bad[q-1],path,replacement)
            out=evaluate(4,nb(4,bad)); assert out[0]==20-(2 if q==1 else 3),(q,path,replacement,out[0]); mutations+=1
result['C4_wrong_integer_bool_leaf_mutations_rejected']=mutations

# Removal of an upstream trace produces blanket wrong statuses downstream.
for n,q in [(1,2),(2,1)]:
    doc=nb(n,values[n]); c=next(c for c in doc['cells'] if c.get('metadata',{}).get('tal',{}).get('question')==f'Q{q}'); c['outputs']=[]
    out=evaluate(n,doc)
    result[f'C{n}_missing_Q{q}']={'score':out[0],'zero_questions':[d['check'] for d in out[1] if d['points']==0],'dependent_feedback':out[1][3]['correct_answer']}

app=create_app(); app.config['TESTING']=True
with tempfile.TemporaryDirectory() as temp, patch.object(outils,'BASE_DIR',temp):
    client=app.test_client()
    for n in range(1,5):
        doc=nb(n,values[n]); payload=json.dumps(doc).encode()
        response=client.post('/submit',data={'file':(io.BytesIO(payload),'fixture.ipynb')},content_type='multipart/form-data',follow_redirects=True)
        public=response.get_data(as_text=True)
        result[f'C{n}_blank_identity_route']={'received':'Copie reçue et enregistrée' in public,'score_leaked':'Score technique provisoire' in public,'saved_notebooks':len(list((Path(temp)/f'controle-td{n}-s3').rglob('*.ipynb')))}
        assert 'Copie reçue et enregistrée' in public and 'Score technique provisoire' not in public

# Identity extraction ignores student number even if supplied.
doc=nb(1,values[1]); identity=next(c for c in doc['cells'] if c.get('metadata',{}).get('tal',{}).get('role')=='identification')
identity['source']='nom="Fictif"\nprenom="Camille"\nclasse="S3"\nnumero_etudiant="123456789"'
result['student_number_returned']=evaluate(1,doc)[3].get('numero_etudiant')

# Reference data edits are not checked at submission; historic outputs remain accepted.
doc=nb(4,values[4]); provided=next(c for c in doc['cells'] if 'mobilite = ' in ''.join(c['source'])); provided['source']='mobilite = []'
result['C4_changed_provided_data_score']=evaluate(4,doc)[0]

# Missing all cell metadata reactivates legacy collection even under current notebook metadata.
doc=nb(4,values[4])
for c in doc['cells']: c['metadata'].pop('tal',None)
result['C4_all_cell_ids_removed_score']=evaluate(4,doc)[0]

# Example-role trace cannot count when current explicit IDs remain.
doc=nb(4,values[4]); answer=next(c for c in doc['cells'] if c.get('metadata',{}).get('tal',{}).get('question')=='Q1'); answer['metadata']['tal']['role']='example'
result['C4_Q1_example_role_score']=evaluate(4,doc)[0]; assert result['C4_Q1_example_role_score']==18

identity['source']='prenom="Alice"\nnom="Dupont"\nclasse="S3"'
result['reordered_identity']=evaluate(1,doc)[3] if False else outils.extract_identification_info([identity])
identity['source']='# nom="Commentaire"\nnom="Dupont"\nprenom="Alice"\nclasse="S3"'
result['comment_shadow_identity']=outils.extract_identification_info([identity])
print(json.dumps(result,ensure_ascii=False,indent=2))
```

## c5_7.py

```python
"""Independent audit of teacher numeric specifications; never execute notebook code."""
import ast, copy, importlib, json, math, re, sys
from pathlib import Path
ROOT = Path('/workspace/scratch/299f4372d5c4/tal-s3-complete-audit')
sys.path.insert(0, str(ROOT/'app'))
from s3_controls_quantitative import EXPECTED

def source_data(n):
    nb = json.loads((ROOT/f'Notebooks contrôles finaux/S3/Controle_TD{n}_S3.ipynb').read_text())
    data = {}
    # Teacher's literal dataset cell only, evaluated with literal_eval (no executable AST).
    for node in ast.parse(''.join(nb['cells'][5]['source'])).body:
        if isinstance(node, ast.Assign):
            data[node.targets[0].id] = ast.literal_eval(node.value)
    return nb, data

def close(actual, expected):
    if isinstance(expected,dict): return actual.keys()==expected.keys() and all(close(actual[k],v) for k,v in expected.items())
    if isinstance(expected,list): return len(actual)==len(expected) and all(close(a,b) for a,b in zip(actual,expected))
    if type(expected) is float: return type(actual) in (int,float) and math.isclose(actual,expected,abs_tol=1e-6,rel_tol=0)
    return type(actual)==type(expected) and actual==expected

def incidence(rows, left, right):
    # Alternative oracle: boolean vectors via delimited expression regular expressions.
    def pattern(expressions): return re.compile('|'.join('(?<=\\|)'+re.escape('|'.join(e))+'(?=\\|)' for e in expressions))
    a, b = pattern(left),pattern(right)
    both=[]; mp=ma=0
    for i,row in enumerate(rows):
        phrase='|'+'|'.join(row)+'|'; p=bool(a.search(phrase)); q=bool(b.search(phrase)); mp+=p; ma+=q
        if p and q: both.append(i)
    return dict(N=len(rows),marge_pivot=mp,marge_associe=ma,cooc=len(both),indices=both)

nb5,d5=source_data(5); nb6,d6=source_data(6); nb7,d7=source_data(7)
# Independent hand-counted C5 reference, proportions carried as exact fractions.
c5=[
 dict(N=10,marge_pivot=4,marge_associe=7,cooc=3,indices=[0,1,2]),
 dict(audio_sachant_visite=3/4,visite_sachant_audio=3/7,table=[[3,1],[4,2]]),
 dict(audio=dict(cooc=3,marge_associe=7,conditionnelle=3/4,base=7/10,ecart=3/4-7/10),atelier=dict(cooc=2,marge_associe=2,conditionnelle=2/4,base=2/10,ecart=2/4-2/10)),
 dict(court=dict(effectif=3,taille=10,pour_mille=300.),long=dict(effectif=5,taille=25,pour_mille=200.),global_placeholder=None),
 dict(sans_pivot=None,sans_associe=0.,rare=1.,rare_effectif=1,rare_denominateur=1),
 dict(k1=dict(indices_pivots=[0],couverts=1,total=3,proportion=1/3),k2=dict(indices_pivots=[0,4,8],couverts=3,total=3,proportion=1.),k4=dict(indices_pivots=[0,4,8],couverts=3,total=3,proportion=1.),paires_k4=5),
 dict(plage_vent=dict(N=8,marge_pivot=4,marge_associe=5,cooc=2,indices=[0,3]),vent_sachant_plage=.5,plage_sachant_vent=.4,base_vent=.625,alerte_sachant_plage=.5,base_alerte=.375,table=[[2,2],[3,1]])]
del c5[3]['global_placeholder'];c5[3]['global']=dict(effectif=8,taille=35,pour_mille=8000/35)
assert incidence(d5['mediation'],[['visite']],[['audio']])==c5[0]
assert incidence(d5['bulletins_littoral'],[['plage']],[['vent']])==c5[6]['plage_vent']

# C6: independent tokens/offsets come from original text regex, not backend token_offsets.
text=d6['texte_exposition']; matches=list(re.finditer(r'\w+|[^\w\s]',text)); tokens=[m[0] for m in matches]
assert tokens==d6['flux_exposition']; size=len(tokens); terms=d6['termes_exposition']
pos={t:[i for i,m in enumerate(matches) if m[0].lower()==t] for t in terms}
parts=[tokens[i:i+12] for i in range(0,size,12)]
counts={t:[sum(word.lower()==t for word in part) for part in parts] for t in terms}
alphas=[sum(word.isalpha() for word in part) for part in parts]
pairs={t:[sum(1 for p in pos['affiche'] for q in pos[t] if 0<abs(p-q)<=k) for k in [1,3,6]] for t in ['public','atelier']}
con=[]
for i in [pos['affiche'][0],pos['affiche'][-1]]:
 a=max(0,i-2);b=min(size,i+3);l=matches[a].start();r=matches[b-1].end()
 con.append(dict(indice=i,debut_token=a,fin_token=b,debut_caractere=l,fin_caractere=r,passage=text[l:r]))
fiches=d6['fiches_exposition']; sets=list(map(set,fiches)); matrix=[[sum(a in row and b in row for row in sets) if a!=b else 0 for b in terms] for a in terms]
c6=[dict(N=size,termes={t:dict(positions=p,relatives=[i/size for i in p]) for t,p in pos.items()}),
 dict(bornes=[[0,12],[12,24],[24,36],[36,48]],tailles_flux=[12]*4,tailles_alpha=alphas,effectifs=counts),
 {t:[1000*c/a for c,a in zip(values,alphas)] for t,values in counts.items()},
 dict(k=[1,3,6],**pairs,couverture_public_k6=sum(any(abs(p-q)<=6 for q in pos['public']) for p in pos['affiche'])/len(pos['affiche'])),
 dict(concordances=con),dict(termes=terms,matrice=matrix,preuves_affiche_public=[i for i,row in enumerate(sets) if {'affiche','public'}<=row]),
 dict(bornes=[[0,9],[9,19],[19,29]],tailles_alpha=[8,8,8],effectifs=dict(atelier=[2,0,1],prototype=[1,1,1]),taux=dict(atelier=[250.,0.,125.],prototype=[125.]*3))]
c6[6]['global']={t:dict(effectif=3,taille_alpha=24,pour_mille=125.,moyenne_taux_segmentaires=125.) for t in ['atelier','prototype']}
# Independently verify hand-counted second corpus bounds and counts.
for j,(a,b) in enumerate(c6[6]['bornes']):
 part=d6['flux_ateliers'][a:b];assert sum(s.isalpha() for s in part)==8
 for term in ['atelier','prototype']:assert sum(s.lower()==term for s in part)==c6[6]['effectifs'][term][j]

# C7 independent incidence engine + explicit documentary judgments and offsets.
ann=d7['affirmations_mediatheque']; rows=d7['phrases_mediatheque']
measures={a['id']:incidence(rows,a['pivots'],a['associes']) for a in ann}
quotes=[]
for i,q in enumerate(d7['citations_mediatheque']):
 found=d7['texte_mediatheque'].find(q['texte']); end=found+len(q['texte']) if found>=0 else None
 quotes.append(dict(id=q['id'],exacte=(i==0),debut=found if found>=0 else None,fin=end,normalisee=(i!=1)))
gardens=[dict(id=a['id'],mesure_union=incidence(d7['phrases_jardin'],a['pivots'],a['associes']),verdict=v) for a,v in zip(d7['affirmations_jardin'],['compatible selon le protocole','contredit selon le protocole','insuffisamment défini'])]
c7=[dict(annonces=[dict(id=f'M{i}',manquants=['agregation'] if i==3 else [],mesurable=i!=3) for i in range(1,5)]),
 dict(mesures=measures),dict(citations=quotes),
 dict(verdicts=dict(M1='compatible selon le protocole',M2='contredit selon le protocole',M3='insuffisamment défini',M4='contredit selon le protocole')),
 dict(union_M3=4,somme_M3=5,expressions_acces_libre=[1,6],mots_acces_libre=[1,3,6],faux_rapprochements=[3],silence_singulier=1,silence_groupe=2),
 dict(union_jardin=incidence(d7['phrases_jardin'],[['eau']],[['sol'],['compost']]),conditionnelle=.5,somme_paires=3,expression_compost=1,vide=dict(N=0,marge_pivot=0,marge_associe=0,cooc=0,indices=[]),conditionnelle_vide=None,conditionnelle_pivot_absent=None),
 dict(audit_jardin=gardens,citation_exacte=True,debut_citation=108,fin_citation=121)]
assert d7['texte_jardin'][108:121]==d7['citation_jardin']
assert d7['texte_mediatheque'][174:205]==d7['citations_mediatheque'][0]['texte']
results={}
for n,base,expected in [(5,nb5,c5),(6,nb6,c6),(7,nb7,c7)]:
 for q,ref in enumerate(expected,1):assert close(EXPECTED[n][q-1],ref),(n,q,EXPECTED[n][q-1],ref)
 mod=importlib.import_module(f'app_correction_Controle_TD{n}_S3')
 def notebook(values):
  nb=copy.deepcopy(base)
  for cell in nb['cells']:
   tag=cell.get('metadata',{}).get('tal',{})
   if tag.get('role')=='answer':
    q=int(tag['question'][1:]);cell['outputs']=[dict(output_type='stream',name='stdout',text=f'S3_C{n}_Q{q}: '+json.dumps(values[q-1],ensure_ascii=False)+'\n')]
  return nb
 def evaluate(nb):return mod.check_notebook(json.dumps(nb),'audit-inerte.ipynb')
 full=notebook(expected);assert evaluate(full)[0]==20
 # Scalar structural corruption for each question must lose exactly its weight.
 mutations=[]
 for q in range(1,8):
  wrong=copy.deepcopy(expected);wrong[q-1]['AUDIT_UNEXPECTED_FIELD']=42
  score=evaluate(notebook(wrong))[0];assert score==20-(2 if q==1 else 3);mutations.append(score)
 # Mutate one existing leaf per question (not only an unexpected key).
 def altered(value):
  value=copy.deepcopy(value)
  if isinstance(value,dict):
   k=next(iter(value));value[k]=altered(value[k]);return value
  if isinstance(value,list):
   if value:value[0]=altered(value[0])
   else:value.append(99)
   return value
  if type(value) is bool:return not value
  if isinstance(value,(int,float)):return value+1
  if isinstance(value,str):return value+'_WRONG'
  return 0
 for q in range(1,8):
  wrong=copy.deepcopy(expected);wrong[q-1]=altered(wrong[q-1])
  assert evaluate(notebook(wrong))[0]==20-(2 if q==1 else 3)
 # Wrong numerical value for selected quantitative and documentary cases.
 wrong=copy.deepcopy(expected)
 if n==5:wrong[1]['table'][1][1]=0
 if n==6:wrong[2]['affiche'][0]=1000*2/12
 if n==7:wrong[3]['verdicts']['M3']='compatible selon le protocole'
 assert evaluate(notebook(wrong))[0]==17
 # Existing explicit metadata: incorrect role excludes saved expected answer.
 bad=copy.deepcopy(full);next(c for c in bad['cells'] if c.get('metadata',{}).get('tal',{}).get('question')=='Q1')['metadata']['tal']['role']='example'
 assert evaluate(bad)[0]==18
 # A recorded execution error in the answer cell prevents its numerical points.
 bad=copy.deepcopy(full);next(c for c in bad['cells'] if c.get('metadata',{}).get('tal',{}).get('question')=='Q2')['outputs'].append(dict(output_type='error',ename='RuntimeError',evalue='audit',traceback=[]))
 assert evaluate(bad)[0]==17
 results[n]=dict(questions_independently_verified=7,full_score=evaluate(full)[0],per_question_corruption_scores=mutations,wrong_role_score=18,error_cell_score=17)
print(json.dumps(results,indent=2,ensure_ascii=False))
print('PASS: 21 references independently checked; 21 structural mutations; 21 changed answer leaves; 3 wrong values; 3 role exclusions; 3 error exclusions. No notebook executed.')
```

