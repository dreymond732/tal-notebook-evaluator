"""Independent saved answers, never executed; the grader only parses these strings."""
import copy
import importlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from s1_revision import collect, matches
from s2_reference import CHECKS

# Each tuple is (student-source specimen, recorded stdout). Sources are inert:
# no eval(), exec(), notebook runner or filesystem access occurs in these tests.
ANSWERS = {
2: [
('mot="Python"\nr=mot[::-1]', 'nohtyP'),
('animaux=["chat","chien","souris"]\nr="-".join(animaux)', 'chat-chien-souris'),
('import math\nr=f"{math.pi:.2f}"', '3.14'),
('sources=[1,2,3,4]\nr=[x*x for x in sources]', '[1,4,9,16]'),
('donnees=[1,2,2,3,4,1,1]\nr=len(set(donnees))', '4'),
('langues=["Français","Anglais"]\ncodes=["FR","EN"]\nr=dict(zip(langues,codes))', "{'Français':'FR','Anglais':'EN'}"),
('scores={"joueur1":10,"joueur2":25,"joueur3":15}\nr=sum(scores.values())', '50'),
('personnes={"Alice":25,"Bob":17,"Charlie":30}\nr=sorted([nom for nom,age in personnes.items() if age>=18])', "['Alice','Charlie']"),
('texte="baba"\nr={}\nfor lettre in texte:\n r[lettre]=r.get(lettre,0)+1', "{'b':2,'a':2}"),
('matrice=[[1,2],[3,4],[5,6]]\nr=[]\nfor row in matrice:\n for n in row:\n  r.append(n)', '[1,2,3,4,5,6]'),
('r=[0,1]\nwhile r[-1]+r[-2]<10:\n r.append(r[-1]+r[-2])', '[0,1,1,2,3,5,8]'),
('def est_anagramme(a,b):\n return sorted(a)==sorted(b)\nr=est_anagramme("gare","rage")', 'True'),
('nombres=[5,8,12,15,20,3]\nr=[x for x in nombres if x%2==0 and x>10]', '[12,20]'),
],
3: [
('nb_heures="12"\ntarif=25\nr=int(nb_heures)*tarif', '300'),
('r={"deb":13,"fin":19}', "{'deb':13,'fin':19}"),
('note=14\nr=10<=note<16', 'True'),
('texte="  Python, TAL!  "\nr=texte.strip().lower().replace(",", "").replace("!", "")', 'python tal'),
('r=2', '2'),
('outils=["tal","nlp","python"]\noutils.insert(1,"spacy")\noutils.pop()\nr=outils', "['tal','spacy','nlp']"),
('mots=["corpus","tal","annotation","nlp","python"]\nr=0\nfor i,mot in enumerate(mots):\n if len(mot)>4:\n  r+=1', '3'),
('r=[n*n for n in range(10) if n%2==0]', '[0,4,16,36,64]'),
('tokens=["tal","est","cool","tal","python"]\nr={}\nfor t in tokens:\n r[t]=r.get(t,0)+1', "{'tal':2,'est':1,'cool':1,'python':1}"),
('compteur=3\nr=[]\nwhile compteur>0:\n r.append(compteur)\n compteur-=1', '[3,2,1]'),
('def normaliser_token(tok):\n return tok.strip().lower().rstrip(".,!?")\nr=normaliser_token("  TAL! ")', 'tal'),
('def addition(a,b=10):\n return a+b\nr=addition(7)', '17'),
('mots=["tal","annotation","python","nlp"]\npaires=[(m,len(m)) for m in mots]\nr=sorted(paires,key=lambda pair:pair[1],reverse=True)', "[('annotation',10),('python',6),('tal',3),('nlp',3)]"),
('A={1,2,3}\nB={3,4}\nr={"intersection":A&B,"union":A|B}', "{'intersection':{3},'union':{1,2,3,4}}"),
('x=0\ntry:\n r=10/x\nexcept ZeroDivisionError:\n r=None', 'None'),
('n=5\nr=1\nfor k in range(1,n+1):\n r*=k', '120'),
('valeurs=[3,10,7]\nm=max(valeurs)\nr={"max":m,"index":valeurs.index(m)}', "{'max':10,'index':1}"),
('tokens=["tal","est","cool"]\nr=[]\nfor i in range(len(tokens)-1):\n r.append((tokens[i],tokens[i+1]))', "[('tal','est'),('est','cool')]"),
('cles=["a","b","c"]\nvaleurs=[1,2,3]\nr=dict(zip(cles,valeurs))', "{'a':1,'b':2,'c':3}"),
('r=[n for n in range(10) if n%3!=0]', '[1,2,4,5,7,8]'),
('r=1', '1'),
('import math\nvaleurs=[2,4,4,4,5,5,7,9]\nm=sum(valeurs)/len(valeurs)\nv=sum((x-m)**2 for x in valeurs)/len(valeurs)\nr={"moyenne":m,"ecart_type":math.sqrt(v)}', "{'moyenne':5.0,'ecart_type':2.0}"),
('r=4', '4'),
('def contient_liste(valeurs,cible):\n for v in valeurs:\n  if v==cible:\n   return True\n return False\nr=contient_liste([1,4,9],4)', 'True'),
('def somme_n(n):\n if n==1:\n  return 1\n return n+somme_n(n-1)\nr=somme_n(5)', '15'),
('mots=["tal","python","spacy"]\nr={m:len(m) for m in mots}', "{'tal':3,'python':6,'spacy':5}"),
('valeurs=[4,1,9,2,7]\nr=sorted(valeurs,reverse=True)[:2]', '[9,7]'),
('phrase="le tal et la python"\nstopwords={"le","la","les"}\nr=[t for t in phrase.split() if t not in stopwords]', "['tal','et','python']"),
('verbes=["analyser","extraire"]\nnoms=["corpus","termes","tokens"]\nr=[]\nfor v in verbes:\n for n in noms:\n  r.append((v,n))', "[('analyser','corpus'),('analyser','termes'),('analyser','tokens'),('extraire','corpus'),('extraire','termes'),('extraire','tokens')]"),
('a,b=48,18\nwhile b!=0:\n a,b=b,a%b\nr=a', '6'),
],
4: [
('animaux=["chat","chien","chat","oiseau","chien"]\nr=set(animaux)', "{'chat','chien','oiseau'}"),
('r={"chat","chien"}\nr.add("souris")', "{'chat','chien','souris'}"),
('vocabulaire={"corpus","token","lemme"}\nr="token" in vocabulaire', 'True'),
('a={"python","code","data"}\nb={"java","code","data"}\nr=a.intersection(b)', "{'data','code'}"),
('a={"python","algo"}\nb={"data","code"}\nr=a.union(b)', "{'data','code','python','algo'}"),
('fruits={"pomme","orange","citron","poire"}\nagrumes={"orange","citron"}\nr=fruits.difference(agrumes)', "{'pomme','poire'}"),
('a={"linux","macos"}\nb={"windows","macos"}\nr=a.symmetric_difference(b)', "{'linux','windows'}"),
('dictionnaire={"le","chat","dort","mange"}\nphrase={"le","chat"}\nr=phrase<=dictionnaire', 'True'),
('utilisateurs=["user1","user2","user3","user4"]\nbase=set(utilisateurs)\nr="user3" in base', 'True'),
('tags=["tag1","tag2","tag1","tag3","tag2"]\nr=set(tags)', "{'tag1','tag2','tag3'}"),
('phrase1=["le","chat","est","noir"]\nphrase2=["le","chien","est","blanc"]\nr=set(phrase1)&set(phrase2)', "{'le','est'}"),
('classe={"Jean","Marie","Paul","Sophie"}\nrendus={"Marie","Sophie"}\nr=classe-rendus', "{'Paul','Jean'}"),
('a={"pomme","banane","cerise"}\nb={"pomme","banane","fraise"}\nr=len(a&b)/len(a|b)', '0.5'),
('alphabet=set("abcdefghijklmnopqrstuvwxyz")\nphrase="Portez ce vieux whisky au juge blond".lower()\nr=set(phrase)>=alphabet', 'True'),
],
5: [
('r=[x*x for x in range(21) if x%2==0]', '[0,4,16,36,64,100,144,196,256,324,400]'),
('mots=["chat","arbre","python","ecole","igloo","banane","orange"]\nr=[m for m in mots if m[0] in "aeiouy"]', "['arbre','ecole','igloo','orange']"),
('phrase="le traitement automatique du langage est passionnant"\nr={m:len(m) for m in phrase.split()}', "{'le':2,'traitement':10,'automatique':11,'du':2,'langage':7,'est':3,'passionnant':11}"),
('phrase="le traitement automatique du langage est passionnant"\nr=" ".join(phrase.split()[::-1])', 'passionnant est langage du automatique traitement le'),
('cles=["nom","prenom","age"]\nvaleurs=["Dupont","Jean",25]\nr=dict(zip(cles,valeurs))', "{'nom':'Dupont','prenom':'Jean','age':25}"),
('mot="radar"\nr=mot==mot[::-1]', 'True'),
('a="chien"\nb="niche"\nr=sorted(a)==sorted(b)', 'True'),
('a="AGCTTAG"\nb="AGCTATG"\nr=sum(x!=y for x,y in zip(a,b))', '2'),
('organisation="Traitement Automatique des Langues"\nr="".join(m[0] for m in organisation.split()).upper()', 'TADL'),
('message="abc"\ndecalage=1\nr="".join(chr(ord(c)+decalage) for c in message)', 'bcd'),
('matrice=[[1,2],[3,4],[5,6]]\nr=[x for row in matrice for x in row]', '[1,2,3,4,5,6]'),
('d1={"a":10,"b":20,"c":30}\nd2={"b":5,"c":10,"d":40}\nr=dict(d1)\nfor k,v in d2.items():\n r[k]=r.get(k,0)+v', "{'a':10,'b':25,'c':40,'d':40}"),
('cours={"Alice":"Maths","Bob":"Maths","Charlie":"Physique"}\nr={}\nfor nom,matiere in cours.items():\n if matiere not in r:\n  r[matiere]=[]\n r[matiere].append(nom)', "{'Maths':['Alice','Bob'],'Physique':['Charlie']}"),
('scores=[("Alice",12),("Bob",15),("Charlie",10)]\nr=sorted(scores,key=lambda x:x[1],reverse=True)', "[('Bob',15),('Alice',12),('Charlie',10)]"),
('data=[1,2,3,2,4,2,5,1]\nr=max(data,key=data.count)', '2'),
('texte="Bonjour, comment ça va?"\nr=texte.lower().replace(","," ").replace("?"," ").split()', "['bonjour','comment','ça','va']"),
('tokens=["le","chat","est","noir","et","le","chien","dort"]\nstopwords={"le","est","et"}\nr=[t for t in tokens if t not in stopwords]', "['chat','noir','chien','dort']"),
('mots=["je","suis","content"]\nr=list(zip(mots,mots[1:]))', "[('je','suis'),('suis','content')]"),
('mots=["un","deux","trois","quatre"]\nr=list(zip(mots,mots[1:],mots[2:]))', "[('un','deux','trois'),('deux','trois','quatre')]"),
('a={"chat","chien","souris"}\nb={"chat","oiseau","souris"}\nr=len(a&b)/len(a|b)', '0.5'),
('doc=["a","b","a","c","a","b"]\nr=doc.count("a")/len(doc)', '0.5'),
('a=[1,2,3]\nb=[4,5,6]\nr=sum(x*y for x,y in zip(a,b))', '32'),
('mots=["programmation","programme","progrès"]\nr=mots[0]\nfor m in mots[1:]:\n while not m.startswith(r):\n  r=r[:-1]', 'progr'),
('vocab=["chat","chien"]\ncontexte=["le","chat","mange","le","chien"]\nr={mot:contexte.count(mot) for mot in vocab}', "{'chat':1,'chien':1}"),
('texte="  Python est Super!!  "\nr=texte.strip().lower().replace("!","").split()', "['python','est','super']"),
],
'dm': [
('mot="bonjour"\nr=mot[:3]', 'bon'),
('r=[1,2,3]\nr.append(4)', '[1,2,3,4]'),
('l=[1,2,3]\nr=l[-1]', '3'),
('d={"nom":"A","age":20}\nr=d["age"]', '20'),
('d={"nom":"A","age":20}\nd["ville"]="Paris"\nr=d', "{'nom':'A','age':20,'ville':'Paris'}"),
('r=sum([1,2,3])', '6'),
('mot="test"\nr=mot.upper()', 'TEST'),
('phrase="mon chat"\nr=phrase.replace("chat","chien")', 'mon chien'),
('r=len([1,2,3,4,5])', '5'),
('r=set([1,1,2,2])', '{1,2}'),
('r=10>5', 'True'),
('r="a-b-c".split("-")', "['a','b','c']"),
('r=[1]+[2]', '[1,2]'),
('r=abs(-5)', '5'),
('r=max([1,9,3])', '9'),
('r=int("42")', '42'),
('r=round(3.14159,2)', '3.14'),
('r=2 in [1,2,3]', 'True'),
('d={"a":1}\nr=list(d.keys())', "['a']"),
('d={"a":1}\nr=list(d.values())', '[1]'),
('r=[x*x for x in range(1,6)]', '[1,4,9,16,25]'),
('r={x:x*x for x in [1,2,3]}', '{1:1,2:4,3:9}'),
('l=[1,2,3,4]\nr=[x for x in l if x%2==0]', '[2,4]'),
('matrice=[[1,2],[3,4]]\nr=[]\nfor row in matrice:\n for x in row:\n  r.append(x)', '[1,2,3,4]'),
('mot="abac"\nr={}\nfor c in mot:\n r[c]=r.get(c,0)+1', "{'a':2,'b':1,'c':1}"),
('k=["a","b"]\nv=[1,2]\nr=dict(zip(k,v))', "{'a':1,'b':2}"),
('d={"a":1,"b":2}\nr={v:k for k,v in d.items()}', "{1:'a',2:'b'}"),
('mat=[[1,2],[3,4]]\nr=[list(col) for col in zip(*mat)]', '[[1,3],[2,4]]'),
('l1=[1,2,3]\nl2=[2,3,4]\nr=set(l1)&set(l2)', '{2,3}'),
('n=5\nr=1\nfor x in range(1,n+1):\n r*=x', '120'),
],
}

CORPUS = "Le chat, mange la souris.\nLe chien; aboie fort!!\nL'oiseau vole... dans le ciel.\nLa souris (petite) court vite.\nCHAT et chien sont des amis?\n123 souris mangent 456 graines."
TOKENS = "['chat','mange','souris','chien','aboie','fort','oiseau','vole','ciel','souris','petite','court','vite','chat','chien','amis','souris','mangent','graines']"
COUNTS = "{'chat':2,'mange':1,'souris':3,'chien':2,'aboie':1,'fort':1,'oiseau':1,'vole':1,'ciel':1,'petite':1,'court':1,'vite':1,'amis':1,'mangent':1,'graines':1}"
CSV_LINES = ['Mot;Frequence','chat;2','mange;1','souris;3','chien;2','aboie;1','fort;1','oiseau;1','vole;1','ciel;1','petite;1','court;1','vite;1','amis;1','mangent;1','graines;1']
ANSWERS[6] = [
('with open("corpus_sale.txt",encoding="utf-8") as f:\n contenu=f.read()\nr=repr(contenu)', repr(CORPUS)),
('with open("corpus_sale.txt",encoding="utf-8") as f:\n r=f.readlines()', repr(CORPUS.splitlines(keepends=True))),
('def nettoyer_ligne(txt):\n txt=txt.lower()\n for p in ".,;!?":\n  txt=txt.replace(p," ")\n return txt\nr=nettoyer_ligne("Le chien; aboie fort!!")', 'le chien  aboie fort  '),
('texte="le chien  aboie fort"\nr=texte.split()', "['le','chien','aboie','fort']"),
('tokens=["123","souris","mangent","456","graines"]\nr=[t for t in tokens if not t.isdigit()]', "['souris','mangent','graines']"),
('tokens=["le","chat","et","la","souris"]\nstopwords={"le","la","les","et","des","dans","un","une"}\nr=[t for t in tokens if t not in stopwords]', "['chat','souris']"),
('stopwords={"le","la","les","et","des","dans","un","une","l","sont","du","est"}\ntous=[]\nwith open("corpus_sale.txt",encoding="utf-8") as f:\n for ligne in f:\n  ligne=ligne.lower()\n  for p in ".,;!?\'()":\n   ligne=ligne.replace(p," ")\n  for mot in ligne.split():\n   if not mot.isdigit() and mot not in stopwords:\n    tous.append(mot)\nr=tous', TOKENS),
('frequences={}\nfor mot in tous:\n frequences[mot]=frequences.get(mot,0)+1\nr=frequences', COUNTS),
('with open("lexique.csv","w",encoding="utf-8") as f:\n f.write("Mot;Frequence\\n")\n for mot,n in frequences.items():\n  f.write(f"{mot};{n}\\n")\ntry:\n with open("lexique.csv",encoding="utf-8") as f:\n  contenu_csv=f.read().strip().split("\\n")\n r=contenu_csv[:3]\nexcept OSError:\n r="Erreur fichier"', "['Mot;Frequence','chat;2','mange;1']"),
('with open("lexique_trie.csv","w",encoding="utf-8") as f:\n f.write("Mot;Frequence\\n")\n for mot,n in sorted(frequences.items(),key=lambda x:x[1],reverse=True):\n  f.write(f"{mot};{n}\\n")\nr=[]\ntry:\n with open("lexique_trie.csv",encoding="utf-8") as f:\n  lines=f.readlines()[1:]\n  for line in lines:\n   m,c=line.strip().split(";")\n   r.append((m,int(c)))\nexcept OSError:\n pass', "[('souris',3),('chat',2),('chien',2),('mange',1),('aboie',1),('fort',1),('oiseau',1),('vole',1),('ciel',1),('petite',1),('court',1),('vite',1),('amis',1),('mangent',1),('graines',1)]"),
]


def notebook(course):
    cells=[]
    for number,(source,raw) in enumerate(ANSWERS[course],1):
        source += f'\nprint("Résultat Q{number} :",r)'
        stdout=f'Résultat Q{number} : {raw}\n'
        if (course,number)==(6,9):
            source+='\nprint("Résultat Q9b :",contenu_csv)'
            stdout+=f'Résultat Q9b : {CSV_LINES!r}\n'
        if (course,number)==(6,10):
            source+='\nwith open("lexique_trie.csv",encoding="utf-8") as f:\n entete=f.readline().rstrip("\\r\\n")\nprint("Résultat Q10b :",entete)'
            stdout+='Résultat Q10b : Mot;Frequence\n'
        cells.append({'cell_type':'code','source':source,'metadata':{'tal':{'question':f'Q{number}','role':'answer'}},
            'outputs':[{'output_type':'stream','name':'stdout','text':stdout}]})
    return {'cells':cells}


def results(course, nb):
    sources,outputs=collect(nb)
    context={m:{'raw':outputs[m][0][1],'proof':p[0][1],'value_ok':False}
        for m,p in sources.items() if len(p)==1 and len(outputs.get(m,[]))==1 and p[0][0]==outputs[m][0][0] and not p[0][2]}
    result=[]
    for check in CHECKS[course]:
        valid=True
        for marker,expected in check['traces'].items():
            if marker not in context:
                valid=False; continue
            item=context[marker]
            try:
                ok=expected(item['raw'],item['proof'],context) if callable(expected) else item['proof'].argc==len(expected) and matches(item['raw'],expected)
            except (ValueError,TypeError,SyntaxError,KeyError,IndexError):ok=False
            item['value_ok']=ok;valid &=ok
        if valid and check.get('syntax'):
            valid &= check['syntax']({m:context[m]['proof'] for m in check['traces']},context)
        result.append(bool(valid))
    return result


class S2SavedAnswersTests(unittest.TestCase):
    def test_all_122_independent_saved_answers(self):
        self.assertEqual(sum(len(v) for v in ANSWERS.values()),122)
        for course in ANSWERS:
            with self.subTest(course=course):
                actual=results(course,notebook(course))
                self.assertEqual([i+1 for i,v in enumerate(actual) if not v],[])

    def test_all_six_real_wrappers_preserve_weights_and_strict_gate(self):
        mappings=[(2,'TD2_S2','td2-S2',20),(3,'TD3_S2','td3-S2',30),
            (4,'TD4_S2','td4-S2',40),(5,'TD5_S2','td5-S2',25),
            (6,'TD6_S2','td6-S2',20),('dm','devoirMaisonS2','ControleDevoirMaisonS2',40)]
        for course,module,evaluator,maximum in mappings:
            nb=notebook(course)
            nb['metadata']={'tal':{'id':evaluator,'evaluator':evaluator,'version':2}}
            nb['cells'].insert(0,{'cell_type':'code','metadata':{'tal':{'question':'identity','role':'identification'}},
                'source':'nom="Synthétique"\nprenom="Essai"\nclasse="S2"\nnumero_etudiant="FICTIF-S2-001"','outputs':[]})
            wrapper=importlib.import_module('app_correction_'+module).check_notebook
            with self.subTest(course=course):
                score,details,total,info,error=wrapper(json.dumps(nb),'copie.ipynb')
                self.assertIsNone(error)
                self.assertEqual((score,total),(maximum,maximum))
                self.assertEqual(info['score_nature'],'technique_provisoire')
                self.assertEqual(info['numero_etudiant'],'FICTIF-S2-001')
                nb['metadata']['tal']['version']=1
                self.assertEqual(wrapper(json.dumps(nb),'old.ipynb')[4],'mauvaise version du notebook')

    def test_revised_subjects_accept_independent_answers(self):
        root=Path(__file__).resolve().parents[1]
        entries=json.loads((root/'app/notebook_catalog.json').read_text())['notebooks']
        mappings={2:'TD2_S2',3:'TD3_S2',4:'TD4_S2',5:'TD5_S2',6:'TD6_S2','dm':'devoirMaisonS2'}
        for course,module in mappings.items():
            wrapper=importlib.import_module('app_correction_'+module)
            entry=next(item for item in entries if item['evaluator']==wrapper.EVAL_ID)
            nb=json.loads((root/entry['notebook']).read_text())
            replacements={cell['metadata']['tal']['question']:cell for cell in notebook(course)['cells']}
            for cell in nb['cells']:
                tag=cell.get('metadata',{}).get('tal',{})
                if tag.get('role')=='identification':
                    cell['source']='nom="Synthétique"\nprenom="Essai"\nclasse="S2"\nnumero_etudiant="FICTIF-S2-002"'
                if tag.get('role')=='answer':
                    replacement=replacements[tag['question']]
                    cell['source']=replacement['source'];cell['outputs']=replacement['outputs']
            score,details,total,info,error=wrapper.check_notebook(json.dumps(nb),'copie.ipynb')
            with self.subTest(course=course):
                self.assertIsNone(error)
                self.assertEqual(score,total)

    def test_negative_indices_and_explicit_constructs(self):
        nb=notebook(3)
        nb['cells'][1]['outputs'][0]['text']="Résultat Q2 : {'deb':-18,'fin':-12}\n"
        self.assertTrue(results(3,nb)[1])
        alternatives={
            7:'mots=["corpus","tal","annotation","nlp","python"]\nr=sum(len(m)>4 for m in mots)',
            12:'def addition(a,b):\n return a+b\nr=addition(7,10)',
            15:'x=0\nr=10/x if x else None',
            19:'r={"a":1,"b":2,"c":3}',
            25:'def somme_n(n):\n return 15\nr=somme_n(5)',
            26:'mots=["tal","python","spacy"]\nr=dict(zip(mots,[3,6,5]))',
        }
        for q,source in alternatives.items():
            nb=notebook(3);nb['cells'][q-1]['source']=source+f'\nprint("Résultat Q{q} :",r)'
            with self.subTest(q=q):self.assertFalse(results(3,nb)[q-1])

    def test_interval_rejects_original_or_and_accepts_equivalent_bounds(self):
        variants=[
            ('r=note>=10 and note<16', True),
            ('r=10<=note<16', True),
            ('r=16>note>=10', True),
            ('r=not (note<10 or note>=16)', True),
            ('if note<10 or note>=16:\n r=False\nelse:\n r=True', True),
            ('if note>=10 or note<16:\n r=True\nelse:\n r=False', False),
            ('r=10<note<=16', False),
            ('r=note>=10', False),
        ]
        for expression,expected in variants:
            nb=notebook(3)
            nb['cells'][2]['source']='note=14\n'+expression+'\nprint("Résultat Q3 :",r)'
            with self.subTest(expression=expression):
                self.assertEqual(results(3,nb)[2],expected)

    def test_previous_csv_write_cannot_validate_next_destination(self):
        nb=notebook(6)
        cell=nb['cells'][9]
        # Keep all correct saved traces but remove the actual writing block.
        cell['source']=cell['source'][cell['source'].index('r=[]'):]
        self.assertFalse(results(6,nb)[9])
        # A named path and keyword mode are equivalent to positional literals.
        nb=notebook(6)
        nb['cells'][9]['source']='destination="./lexique_trie.csv"\n'+nb['cells'][9]['source'].replace(
            'open("lexique_trie.csv","w",encoding="utf-8")',
            'open(destination,mode="w",encoding="utf-8")')
        self.assertTrue(results(6,nb)[9])

    def test_exception_handler_is_not_proof_of_file_work(self):
        nb=notebook(6)
        nb['cells'][8]['source']='r=[]\ncontenu_csv=[]\ntry:\n pass\nexcept Exception:\n with open("lexique.csv","w") as f:\n  f.write("inventé")\n with open("lexique.csv") as f:\n  contenu_csv=f.read().splitlines()\n r=contenu_csv[:3]\nprint("Résultat Q9 :",r)\nprint("Résultat Q9b :",contenu_csv)'
        self.assertFalse(results(6,nb)[8])

    def test_every_wrong_saved_result_fails(self):
        for course in ANSWERS:
            for index in range(len(ANSWERS[course])):
                nb=notebook(course)
                nb['cells'][index]['outputs'][0]['text']=f'Résultat Q{index+1} : __incorrect__\n'
                with self.subTest(course=course,q=index+1):
                    self.assertFalse(results(course,nb)[index])

    def test_missing_none_is_not_answer_none(self):
        nb=notebook(3);nb['cells'][14]['outputs']=[]
        self.assertFalse(results(3,nb)[14])
        self.assertTrue(results(3,notebook(3))[14])

    def test_types_are_not_coerced(self):
        for course,q,bad in [(2,12,'1'),(2,5,'True'),(4,1,"['chat','chien','oiseau']"),
                (3,14,"{'intersection':{True},'union':{True,2,3,4}}"),(5,21,'True')]:
            nb=notebook(course);nb['cells'][q-1]['outputs'][0]['text']=f'Résultat Q{q} : {bad}\n'
            with self.subTest(course=course,q=q):self.assertFalse(results(course,nb)[q-1])

    def test_cross_question_and_practice_never_supply_proof(self):
        for course in ANSWERS:
            for role in ('practice','provided','example','submission'):
                nb=notebook(course);nb['cells'][0]['metadata']['tal']['role']=role
                with self.subTest(course=course,role=role):self.assertFalse(results(course,nb)[0])
            nb=notebook(course);nb['cells'][0]['metadata']['tal']['question']='Q99'
            self.assertFalse(results(course,nb)[0])

    def test_repeated_or_error_outputs_never_supply_proof(self):
        for course in ANSWERS:
            nb=notebook(course);nb['cells'][0]['outputs'][0]['text']*=2
            self.assertFalse(results(course,nb)[0])
            nb=notebook(course);nb['cells'][0]['outputs'].append({'output_type':'error','ename':'ValueError'})
            self.assertFalse(results(course,nb)[0])

    def test_literals_and_comments_are_not_algorithm(self):
        for course,q in [(2,4),(3,10),(4,9),(5,1),('dm',24),(6,9)]:
            nb=notebook(course);cell=nb['cells'][q-1]
            cell['source']='# '+cell['source'].replace('\n','\n# ')+f'\nr=[]\nprint("Résultat Q{q} :",r)'
            with self.subTest(course=course,q=q):self.assertFalse(results(course,nb)[q-1])

    def test_permitted_order_variants(self):
        examples=[(3,13,"[('annotation',10),('python',6),('nlp',3),('tal',3)]"),
                  (5,13,"{'Physique':['Charlie'],'Maths':['Bob','Alice']}"),
                  ('dm',29,'(3,2)'),('dm',29,'[3,2]'),(4,1,"{'oiseau','chien','chat'}")]
        for course,q,raw in examples:
            nb=notebook(course);nb['cells'][q-1]['outputs'][0]['text']=f'Résultat Q{q} : {raw}\n'
            with self.subTest(course=course,q=q):self.assertTrue(results(course,nb)[q-1])

    def test_bad_lengths_duplicates_and_case(self):
        for course,q,raw in [(3,13,"[('annotation',10),('python',6),('tal',3),('tal',3)]"),
            ('dm',29,'[2,3,3]'),(5,13,"{'Maths':['Alice','Alice'],'Physique':['Charlie']}"),
            (5,9,'TAL'),(2,1,'nohtyp')]:
            nb=notebook(course);nb['cells'][q-1]['outputs'][0]['text']=f'Résultat Q{q} : {raw}\n'
            with self.subTest(course=course,q=q):self.assertFalse(results(course,nb)[q-1])

    def test_csv_is_complete_order_independent_and_has_header(self):
        nb=notebook(6);cell=nb['cells'][8]
        shuffled=[CSV_LINES[0],*reversed(CSV_LINES[1:])]
        cell['outputs'][0]['text']=f'Résultat Q9 : {shuffled[:3]!r}\nRésultat Q9b : {shuffled!r}\n'
        self.assertTrue(results(6,nb)[8])
        for truncated in (CSV_LINES[:3],CSV_LINES[:-1],[*CSV_LINES[:-1],CSV_LINES[1]]):
            cell['outputs'][0]['text']=f'Résultat Q9 : {truncated[:3]!r}\nRésultat Q9b : {truncated!r}\n'
            self.assertFalse(results(6,nb)[8])
        nb=notebook(6);nb['cells'][9]['outputs'][0]['text']=nb['cells'][9]['outputs'][0]['text'].replace('Mot;Frequence','Wrong;Header')
        self.assertFalse(results(6,nb)[9])

    def test_csv_frequency_ties_are_free_but_descending_required(self):
        nb=notebook(6);cell=nb['cells'][9]
        cell['outputs'][0]['text']=cell['outputs'][0]['text'].replace("('chat',2),('chien',2)","('chien',2),('chat',2)")
        self.assertTrue(results(6,nb)[9])
        cell['outputs'][0]['text']=cell['outputs'][0]['text'].replace("('souris',3),('chien',2)","('chien',2),('souris',3)")
        self.assertFalse(results(6,nb)[9])

    def test_trailing_spaces_and_last_line_are_preserved(self):
        nb=notebook(6);nb['cells'][2]['outputs'][0]['text']='Résultat Q3 : le chien  aboie fort\n'
        self.assertFalse(results(6,nb)[2])
        self.assertTrue(results(6,notebook(6))[1])


if __name__=='__main__':unittest.main()
