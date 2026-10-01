"""Independent examples of saved S1 answers: no student source is executed."""
import copy
import json
import importlib
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from s1_reference import CHECKS
from s1_revision import collect, matches

# Hand-authored traces, separate from the grader's reference constants. Each
# source is parsed only; even open()/CSV code is never run by these tests.
ANSWERS = {
1: [
('prix_par_mot=.12\nnb_mots=125\ncout_total=prix_par_mot*nb_mots', [('Q1','cout_total','15.0')]),
('note=14.5', [('Q2','type(note)',"<class 'float'>")]),
('meme_nombre=nb_mots==125\ncommande_importante=nb_mots>=100 and prix_par_mot>0', [('Q3','meme_nombre,commande_importante','True True')]),
('langue_source="français"\nlangue_cible="anglais"\nphrase_presentation=f\'Traduction du {langue_source} vers l’{langue_cible}.\'', [('Q4','phrase_presentation','Traduction du français vers l’anglais.')]),
('volume_saisi="80"\nvolume_corrige=int(volume_saisi)+20', [('Q5','volume_corrige,type(volume_corrige)',"100 <class 'int'>")]),
('phrase="Le TAL aide."', [('Q6','len(phrase),"TAL" in phrase','12 True'), ('Q6b','repr(phrase)',"'Le TAL aide.'")]),
],
3: [
('outils=["corpus","lexique","concordancier"]\noutils.append("tokeniseur")\nprint("Résultat Q1a :",outils)\noutils.pop()', [('Q1','outils',"['corpus', 'lexique', 'concordancier']")]),
('langues_romanes=("français","italien","espagnol")\nchoix_tuple="La collection doit rester stable."', [('Q2','type(langues_romanes),choix_tuple',"<class 'tuple'> La collection doit rester stable."), ('Q2b','langues_romanes',"('français', 'italien', 'espagnol')")]),
('lexique={"book":"livre","language":"langue","data":"données"}\nlexique["corpus"]="corpus"', [('Q3','lexique["language"]','langue'), ('Q3b','lexique',"{'book':'livre','language':'langue','data':'données','corpus':'corpus'}")]),
('entrees_lexique=[]\nfor anglais,francais in lexique.items():\n entrees_lexique.append(f"{anglais} -> {francais}")', [('Q4','entrees_lexique',"['book -> livre','language -> langue','data -> données','corpus -> corpus']")]),
('formes=["texte","corpus","texte","donnée","corpus","analyse"]\nvocabulaire=set(formes)', [('Q5','len(formes),len(vocabulaire)','6 4'), ('Q5b','vocabulaire',"{'analyse','texte','donnée','corpus'}")]),
('corpus_a=["texte","analyse","langue","corpus"]\ncorpus_b=["langue","corpus","modèle"]\na=set(corpus_a)\nb=set(corpus_b)\ncommuns=a.intersection(b)\nseulement_a=a.difference(b)', [('Q6','communs,seulement_a',"{'corpus','langue'} {'analyse','texte'}")]),
],
4: [
('mots=["TAL","corpus","analyse","IA"]\nmajuscules=[]\nfor mot in mots:\n majuscules.append(mot.upper())', [('Q1','majuscules',"['TAL','CORPUS','ANALYSE','IA']")]),
('mots_longs=[]\nfor mot in mots:\n if len(mot)>5:\n  mots_longs.append(mot)', [('Q2','mots_longs',"['corpus','analyse']")]),
('mots_avec_a=[]\nfor mot in mots:\n if "a" in mot.lower():\n  mots_avec_a.append(mot)', [('Q3','mots_avec_a',"['TAL','analyse','IA']")]),
('positions_paires=list(range(0,11,2))', [('Q4','positions_paires','[0,2,4,6,8,10]')]),
('multiple=7\nmultiples=[]\nwhile multiple<=70:\n multiples.append(multiple)\n multiple=multiple+7', [('Q5','multiples','[7,14,21,28,35,42,49,56,63,70]')]),
('mots_a_compter="le TAL traite le langage et le texte".lower().split()\nfrequences={}\nfor mot in mots_a_compter:\n if mot in frequences:\n  frequences[mot]=frequences[mot]+1\n else:\n  frequences[mot]=1', [('Q6','frequences',"{'le':3,'tal':1,'traite':1,'langage':1,'et':1,'texte':1}")]),
('longueurs_mots_longs=[len(mot) for mot in mots if len(mot)>5]', [('Q7','longueurs_mots_longs','[6,7]')]),
],
5: [
('def longueur_texte(texte):\n return len(texte)', [('Q1','longueur_texte("TAL"),longueur_texte("corpus")','3 6')]),
('def normaliser(texte):\n return texte.strip().lower()', [('Q2','normaliser("  Bonjour TAL  ")','bonjour tal')]),
('def nombre_mots(texte):\n return len(normaliser(texte).split())', [('Q3','nombre_mots("  Le TAL traite les textes  ")','5')]),
('lexique={"language":"langage","data":"données","book":"livre"}\ndef traduire_mot(mot,lexique):\n mot=normaliser(mot)\n return lexique.get(mot,mot)', [('Q4','traduire_mot("language",lexique),traduire_mot("Unknown",lexique)','langage unknown')]),
('def traduire_phrase(phrase,lexique):\n return " ".join([traduire_mot(mot,lexique) for mot in phrase.split()])', [('Q5','traduire_phrase("Language data",lexique)','langage données')]),
('def resume_texte(texte):\n texte_normalise=normaliser(texte)\n return {"texte_normalise":texte_normalise,"nb_caracteres":len(texte_normalise),"nb_mots":nombre_mots(texte)}', [('Q6','resume_texte("  Le TAL avance  ")',"{'texte_normalise':'le tal avance','nb_caracteres':13,'nb_mots':3}")]),
],
6: [
('with open("affiliations_s1.txt",encoding="utf-8") as fichier:\n texte_affiliations=fichier.read()', [('Q1','len(texte_affiliations)','156')]),
('lignes=texte_affiliations.splitlines()', [('Q2','len(lignes)','5')]),
('enregistrements=[]\nfor ligne in lignes:\n enregistrements.append(ligne.split(\';\',maxsplit=1))', [('Q3','enregistrements[0]',"['durand alice','Laboratoire TAL']"), ('Q3b','enregistrements',"[['durand alice','Laboratoire TAL'],['DURAND ALICE','Laboratoire TAL'],['Durand Alice','Centre de traduction'],['Martin bob','Centre de traduction'],['MARTIN BOB','Centre de traduction']]")]),
('def normaliser_personne(identite):\n return " ".join(identite.split()).title()', [('Q4','normaliser_personne("DURAND ALICE")','Durand Alice'), ('Q4b','normaliser_personne("durand alice"),normaliser_personne("Durand Alice"),normaliser_personne("  Durand   Alice  ")','Durand Alice Durand Alice Durand Alice')]),
('affiliations_par_personne={}\nfor personne,affiliation in enregistrements:\n personne=normaliser_personne(personne)\n if personne not in affiliations_par_personne:\n  affiliations_par_personne[personne]=set()\n affiliations_par_personne[personne].add(affiliation)', [('Q5','affiliations_par_personne["Durand Alice"]',"{'Centre de traduction','Laboratoire TAL'}"), ('Q5b','affiliations_par_personne',"{'Durand Alice':{'Laboratoire TAL','Centre de traduction'},'Martin Bob':{'Centre de traduction'}}")]),
('import csv\nfrom pathlib import Path\nwith open("affiliations_uniques.csv","w",encoding="utf-8",newline="") as fichier:\n writer=csv.writer(fichier)\n writer.writerow(["personne","nb_affiliations","affiliations"])\n for personne,affiliations in affiliations_par_personne.items():\n  writer.writerow([personne,len(affiliations)," | ".join(affiliations)])', [('Q6','repr(Path("affiliations_uniques.csv").read_text(encoding="utf-8"))', repr('personne,nb_affiliations,affiliations\r\nMartin Bob,1,Centre de traduction\r\nDurand Alice,2,Centre de traduction | Laboratoire TAL\r\n'))]),
],
7: [
('import re\ntexte="Le tal traite parfois 12 documents en 2026."\ntal_present=bool(re.search("TAL",texte,re.I))', [('Q1','tal_present','True')]),
('texte_nombres="Version 2 : 14 corpus, 3 langues et 250 phrases."\nnombres=re.findall(r"[0-9]+",texte_nombres)', [('Q2','nombres',"['2','14','3','250']")]),
('texte_mots="L’analyse, c’est déjà 2 étapes !"\nmots_regex=re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+",texte_mots)\ncommentaire_mots="Les apostrophes ne délimitent pas les fragments de split."', [('Q3','mots_regex,commentaire_mots',"['L','analyse','c','est','déjà','étapes'] Les apostrophes ne délimitent pas les fragments de split.")]),
('journal="Le 03/09/2026, Alice a relu 12 segments."\njournal_sans_date=re.sub(r"[0-9]{2}/[0-9]{2}/[0-9]{4}","[DATE]",journal)', [('Q4','journal_sans_date','Le [DATE], Alice a relu 12 segments.')]),
('def nettoyer_texte(texte):\n texte=texte.lower()\n texte=re.sub(r"\\d{2}/\\d{2}/\\d{4}","[DATE]",texte)\n texte=re.sub(r"\\d+","",texte)\n return " ".join(texte.split())', [('Q5','nettoyer_texte("  Le 03/09/2026 comporte 12 exemples. ")','le [DATE] comporte exemples.')]),
('def analyser_texte(texte):\n texte_nettoye=nettoyer_texte(texte)\n mots=re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+",texte_nettoye)\n frequences={}\n for mot in mots:\n  frequences[mot]=frequences.get(mot,0)+1\n return {"texte_nettoye":texte_nettoye,"mots":mots,"frequences":frequences}', [('Q6','analyser_texte("Le TAL, le TAL : 2 exemples.")',"{'texte_nettoye':'le tal, le tal : exemples.','mots':['le','tal','le','tal','exemples'],'frequences':{'le':2,'tal':2,'exemples':1}}")]),
('limite_regex="Un mot peut avoir deux sens ; son contexte aide à les distinguer."', [('Q7','limite_regex','Un mot peut avoir deux sens ; son contexte aide à les distinguer.')]),
],
}


def notebook(td):
    cells = []
    for q, (src, traces) in enumerate(ANSWERS[td], 1):
        source = src + '\n' + '\n'.join(f'print("Résultat {m} :",{args})' for m, args, raw in traces)
        stdout = '\n'.join(f'Résultat {m} : {raw}' for m, args, raw in traces) + '\n'
        if td == 3 and q == 1:
            stdout = "Résultat Q1a : ['corpus','lexique','concordancier','tokeniseur']\n" + stdout
        cells.append({'cell_type':'code','metadata':{'tal':{'question':f'Q{q}','role':'answer'}},'source':source,
                      'outputs':[{'output_type':'stream','name':'stdout','text':stdout}]})
    return {'cells': cells}


def results(td, nb):
    sources, outputs = collect(nb)
    context = {marker:{'raw':outputs[marker][0][1], 'proof':proofs[0][1], 'value_ok':False}
               for marker, proofs in sources.items() if len(proofs)==1 and len(outputs.get(marker,[]))==1
               and proofs[0][0]==outputs[marker][0][0] and not proofs[0][2]}
    result = []
    for check in CHECKS[td]:
        valid = True
        for marker, expected in check['traces'].items():
            if marker not in context:
                valid=False; continue
            item=context[marker]
            ok = bool(item['raw'].strip()) if expected is None else expected(item['raw'],item['proof'],context) if callable(expected) else (item['proof'].argc==len(expected) and matches(item['raw'],expected))
            item['value_ok']=ok
            valid &= ok
        if valid:
            valid &= check['syntax']({m:context[m]['proof'] for m in check['traces']},context)
        result.append(bool(valid))
    return result


class S1ReferenceTests(unittest.TestCase):
    def test_all_38_independent_cases(self):
        for td, checks in CHECKS.items():
            with self.subTest(td=td):
                self.assertEqual(results(td,notebook(td)), [True]*len(checks))

    def test_six_wrappers_end_to_end_with_subject_contracts(self):
        root=Path(__file__).resolve().parents[1]
        total=0
        for td in ANSWERS:
            subject=next((root/'Notebooks TD'/'S1').glob(f'TD{td}_*.ipynb'))
            nb=json.loads(subject.read_text())
            replacements={cell['metadata']['tal']['question']:cell for cell in notebook(td)['cells']}
            for cell in nb['cells']:
                tag=cell.get('metadata',{}).get('tal',{})
                if tag.get('role')=='identification':
                    cell['source']='nom="Essai"\nprenom="Alex"\nclasse="S1"\nnumero_etudiant="SYNTHETIQUE-001"'
                if tag.get('role')=='answer':
                    replacement=replacements[tag['question']]
                    cell['source']=replacement['source'];cell['outputs']=replacement['outputs']
            result=importlib.import_module(f'app_correction_TD{td}_S1').check_notebook(json.dumps(nb),'synthetic.ipynb')
            with self.subTest(td=td):
                self.assertIsNone(result[4])
                self.assertEqual(result[0],len(CHECKS[td]))
                self.assertEqual(result[3]['score_nature'],'technique_provisoire')
            total+=result[0]
        self.assertEqual(total,38)

    def test_wrong_saved_results_never_pass(self):
        for td, checks in CHECKS.items():
            for q in range(1,len(checks)+1):
                nb=notebook(td)
                # Q7 is expressly a presence check, not a semantic classifier.
                bad='' if (td,q)==(7,7) else 'False'
                out=nb['cells'][q-1]['outputs'][0]
                out['text']=re.sub(rf'^Résultat Q{q} : .*$', f'Résultat Q{q} : {bad}', out['text'], flags=re.M)
                with self.subTest(td=td,q=q):
                    self.assertFalse(results(td,nb)[q-1])

    def test_constants_and_dead_comments_are_not_constructs(self):
        for td,q in ((1,1),(1,4),(4,1),(5,1),(7,2)):
            nb=notebook(td)
            raw=ANSWERS[td][q-1][1][0][2]
            nb['cells'][q-1]['source']='# '+nb['cells'][q-1]['source'].replace('\n','\n# ')+'\nprint("Résultat Q%d :", %r)'%(q,raw)
            with self.subTest(td=td,q=q):
                self.assertFalse(results(td,nb)[q-1])

    def test_strict_counts_and_order(self):
        for td,q,old,new in ((4,6,"'tal':1","'tal':True"),(4,1,"'TAL','CORPUS'","'CORPUS','TAL'"),(5,6,"'nb_mots':3","'nb_mots':True"),(6,6,'Martin Bob,1','Martin Bob,2')):
            nb=notebook(td); out=nb['cells'][q-1]['outputs'][0]
            self.assertIn(old,out['text']); out['text']=out['text'].replace(old,new)
            with self.subTest(td=td,q=q): self.assertFalse(results(td,nb)[q-1])

    def test_marker_in_other_question_or_practice_is_not_proof(self):
        for role in ('practice','example'):
            nb=notebook(4); cell=nb['cells'][0];cell['metadata']['tal']['role']=role
            self.assertFalse(results(4,nb)[0])
        nb=notebook(4);nb['cells'][0]['metadata']['tal']['question']='extra'
        self.assertFalse(results(4,nb)[0])

    def test_unordered_sets_and_lexicon_entries(self):
        nb=notebook(3)
        nb['cells'][3]['outputs'][0]['text']="Résultat Q4 : ['corpus -> corpus','data -> données','language -> langue','book -> livre']\n"
        self.assertTrue(results(3,nb)[3])

    def test_explicitly_allowed_variants(self):
        variants = (
            (1,1,'cout_total=prix_par_mot*nb_mots','cout_total=nb_mots * prix_par_mot', '15.0','15'),
            (1,4,'l’',"l\\'",'l’',"l'"),
            (4,5,'multiple=multiple+7','multiple+=7',None,None),
            (4,6,'if mot in frequences:\n  frequences[mot]=frequences[mot]+1\n else:\n  frequences[mot]=1','frequences[mot]=frequences.get(mot,0)+1',None,None),
            (6,3,"split(';',maxsplit=1)",'split(";", 1)',None,None),
            (7,1,'re.search("TAL",texte,re.I)','re.search("tal",texte.lower())',None,None),
            (7,1,'re.search("TAL",texte,re.I)','re.search("(?i)TAL",texte)',None,None),
        )
        for td,q,old,new,oldout,newout in variants:
            nb=notebook(td);cell=nb['cells'][q-1]
            self.assertIn(old,cell['source'])
            cell['source']=cell['source'].replace(old,new)
            if oldout is not None: cell['outputs'][0]['text']=cell['outputs'][0]['text'].replace(oldout,newout)
            with self.subTest(td=td,q=q,new=new): self.assertTrue(results(td,nb)[q-1])

    def test_lexicon_inconsistency_and_missing_mutation(self):
        nb=notebook(3)
        nb['cells'][3]['outputs'][0]['text']=nb['cells'][3]['outputs'][0]['text'].replace('language -> langue','language -> langage')
        self.assertFalse(results(3,nb)[3])
        nb=notebook(3)
        nb['cells'][0]['source']=nb['cells'][0]['source'].replace('outils.append("tokeniseur")','outils=["corpus","lexique","concordancier","tokeniseur"]')
        self.assertFalse(results(3,nb)[0])
        nb=notebook(3)
        nb['cells'][2]['source']=nb['cells'][2]['source'].replace('"data":"données"}', '"data":"données","corpus":"corpus"}').replace('lexique["corpus"]="corpus"','')
        self.assertFalse(results(3,nb)[2])

    def test_free_phrase_without_tal_and_empty_text_are_valid(self):
        for phrase in ('Un texte sans sigle.', ''):
            nb=notebook(1)
            nb['cells'][5]['source']=f'phrase={phrase!r}\nprint("Résultat Q6 :",len(phrase),"TAL" in phrase)\nprint("Résultat Q6b :",repr(phrase))'
            nb['cells'][5]['outputs'][0]['text']=f'Résultat Q6 : {len(phrase)} False\nRésultat Q6b : {phrase!r}\n'
            self.assertTrue(results(1,nb)[5])

    def test_personal_phrase_composition_is_not_interpreted(self):
        for expression in ('"Le TAL " + "aide."', 'f"Le {sigle} aide."'):
            nb=notebook(1)
            nb['cells'][5]['source']=nb['cells'][5]['source'].replace('phrase="Le TAL aide."', f'sigle="TAL"\nphrase={expression}')
            self.assertTrue(results(1,nb)[5])
            # A mismatching saved sentence no longer agrees with the length.
            nb['cells'][5]['outputs'][0]['text']=nb['cells'][5]['outputs'][0]['text'].replace("'Le TAL aide.'", "'Le TAL aide beaucoup.'")
            self.assertFalse(results(1,nb)[5])
        nb=notebook(1)
        nb['cells'][5]['source']=nb['cells'][5]['source'].replace('repr(phrase)', 'repr("Le TAL aide.")')
        self.assertFalse(results(1,nb)[5])
        nb=notebook(1)
        nb['cells'][5]['source']=nb['cells'][5]['source'].replace('print("Résultat Q6b', 'phrase="Le TAL lit.."\nprint("Résultat Q6b')
        self.assertFalse(results(1,nb)[5])
        nb=notebook(1)
        nb['cells'][5]['outputs'][0]['text']=nb['cells'][5]['outputs'][0]['text'].replace("'Le TAL aide.'", "'Le TAL lit..'")
        # Same length and membership: the known literal remains an independent check.
        self.assertFalse(results(1,nb)[5])

    def test_uppercase_filter_is_an_allowed_equivalent(self):
        nb=notebook(4)
        nb['cells'][2]['source']=nb['cells'][2]['source'].replace('"a" in mot.lower()', '"A" in mot.upper()')
        self.assertTrue(results(4,nb)[2])
        nb['cells'][2]['outputs'][0]['text']="Résultat Q3 : ['TAL','IA']\n"
        self.assertFalse(results(4,nb)[2])

    def test_commentary_is_presence_not_quality(self):
        nb=notebook(7)
        nb['cells'][6]['outputs'][0]['text']='Résultat Q7 : x\n'
        self.assertTrue(results(7,nb)[6])
        nb['cells'][2]['outputs'][0]['text']="Résultat Q3 : ['L','analyse','c','est','déjà','étapes']\n"
        self.assertFalse(results(7,nb)[2])
        nb['cells'][2]['outputs'][0]['text'] = "Résultat Q3 : ['L','analyse','c','est','déjà','étapes'] ...\n"
        self.assertFalse(results(7,nb)[2])
        nb=notebook(3)
        nb['cells'][1]['outputs'][0]['text']=nb['cells'][1]['outputs'][0]['text'].replace('La collection doit rester stable.','...')
        self.assertFalse(results(3,nb)[1])


if __name__=='__main__':
    unittest.main()
