"""Question-specific formative examples; never imported by control evaluators.

Examples compute values from the subject's data in the student's environment.
No reference model output or invented linguistic judgment is substituted for it.
"""
from textwrap import dedent


EXAMPLES = {}


def _add(evaluator, rows):
    for number, (code, explanation) in enumerate(rows, 1):
        EXAMPLES[(evaluator, number)] = (dedent(code).strip(), explanation)


def solution_for(evaluator, number):
    code, explanation = EXAMPLES[(evaluator, number)]
    if evaluator.startswith('td-r'):
        return code, explanation
    marker = 'S3_TD1B' if evaluator == 'td1b-s3' else 'S3_TD' + evaluator[2]
    return ('import json\n' + code + '\n'
            + f'print("{marker}_Q{number}:", json.dumps(resultat_q{number}, ensure_ascii=False))'), explanation


_add('td0-s3', [
    ('''with open("corpus_td0.txt", encoding="utf-8") as fichier:
    texte = fichier.read()
assert texte == texte_source
with open(RESSOURCES / "faguet_source.txt", encoding="utf-8", newline="") as fichier:
    original_faguet = fichier.read()
print("Longueur du texte Faguet original :", len(original_faguet))
resultat_q1 = {"caracteres": len(texte)}''', 'Lisez le fichier en UTF-8 avant de compter ses caractères, y compris espaces et retours à la ligne.'),
    ('''mots_bruts = texte.split()
resultat_q2 = {"mots": mots_bruts}''', 'split() découpe sur les espaces et conserve la ponctuation attachée aux mots. Cette liste est un découpage brut.'),
    ('''compteur = 0
for mot in mots_bruts:
    compteur += 1
assert compteur == len(mots_bruts)
resultat_q3 = {"occurrences": len(mots_bruts)}''', 'Comptez les éléments de la liste ; un mot répété contribue à chaque occurrence.'),
    ('''formes_distinctes = set(mots_bruts)
assert len(formes_distinctes) <= len(mots_bruts)
resultat_q4 = {"formes": len(formes_distinctes)}''', 'Un ensemble ne conserve chaque chaîne qu’une fois. La casse et la ponctuation distinguent encore les formes.'),
    ('''def frequences_brutes(liste_mots):
    comptes = {}
    for mot in liste_mots:
        comptes[mot] = comptes.get(mot, 0) + 1
    return comptes
comptes = frequences_brutes(mots_bruts)
assert sum(comptes.values()) == len(mots_bruts)
assert len(comptes) == len(formes_distinctes)
assert frequences_brutes([]) == {}
resultat_q5 = {"frequences": comptes}''', 'La fonction incrémente le dictionnaire pour chaque forme exacte ; la somme des effectifs retrouve le nombre d’occurrences.'),
    ('''def frequences_minuscules(texte):
    return frequences_brutes(texte.lower().split())
comptes_minuscules = frequences_minuscules(texte)
assert sum(comptes_minuscules.values()) == len(mots_bruts)
resultat_q6 = {"frequences": comptes_minuscules}''', 'Passez en minuscules avant le découpage. Cette transformation ne retire pas la ponctuation et ne lemmatise pas.'),
    ('''microcas = "L’analyse, c’est utile !"
resultat_q7 = {"split": microcas.split(),
               "limites": "La virgule reste attachée à L’analyse, tandis que ! forme un élément séparé car il est précédé d’un espace."}''', 'Observez les éléments exacts de la liste. Votre synthèse doit expliquer les limites de split(), pas seulement annoncer que le résultat est correct. Sa qualité se vérifie avec les critères du sujet, sans point automatique.'),
])

_add('td1-s3', [
    ('''annotations = []
for token in doc:
    if not token.is_punct:
        annotations.append({"forme": token.text, "lemme": token.lemma_,
                            "pos": token.pos_, "tag": token.tag_,
                            "debut": token.idx, "fin": token.idx + len(token.text)})
resultat_q1 = {"annotations": annotations}''', 'Parcourez doc dans l’ordre. Les bornes doivent restituer exactement chaque forme dans texte ; les étiquettes sont les prédictions du modèle chargé.'),
    ('''phrases = []
for phrase in doc.sents:
    phrases.append({"texte": phrase.text, "tokens": len(phrase)})
resultat_q2 = {"phrases": phrases}''', 'Chaque phrase conserve son texte et son nombre de tokens, ponctuation comprise. Comparez avec votre segmentation manuelle.'),
    ('''noms, verbes, mots_pleins = [], [], []
for token in doc:
    if token.pos_ == "NOUN":
        noms.append(token.lemma_)
    if token.pos_ == "VERB":
        verbes.append(token.lemma_)
    if token.pos_ in {"NOUN", "VERB", "ADJ"} and not token.is_stop:
        mots_pleins.append(token.lemma_)
resultat_q3 = {"noms": noms, "verbes": verbes, "mots_pleins": mots_pleins}''', 'Filtrez les tokens puis prélevez leurs lemmes. Conservez l’ordre et les répétitions ; la liste des mots pleins applique aussi le filtre des mots vides.'),
    ('''from spacy import displacy
phrase = list(doc.sents)[0]
displacy.render(phrase, style="dep", jupyter=True)
verbes_phrase = [token for token in phrase if token.pos_ == "VERB"]
verbe = verbes_phrase[0]
dependant = list(verbe.children)[0]
resultat_q4 = {"verbe": verbe.text, "verbe_debut": verbe.idx,
               "dependant": dependant.text, "dependant_debut": dependant.idx,
               "relation": dependant.dep_,
               "interpretation": "La relation affichée décrit un lien syntaxique proposé entre ces deux tokens ; elle ne permet pas de décider à qui attribuer un propos cité."}''', 'Exemple de repérage d’un verbe et de l’un de ses dépendants dans la première phrase. Précisez votre interprétation en nommant les deux tokens et en discutant la relation observée ; la syntaxe seule ne résout pas la question du locuteur.'),
    ('''doc_td0 = nlp(texte_td0)
resultat_q5 = {"split": len(texte_td0.split()), "tokens": len(doc_td0),
               "non_ponctuation": sum(1 for t in doc_td0 if not t.is_punct and not t.is_space),
               "interpretation": "split() suit les espaces ; spaCy sépare aussi certains éléments de ponctuation et contractions. Les unités comptées diffèrent."}''', 'Appliquez les trois règles au même texte. Gardez les tokens d’espacement hors du troisième compte ; dans votre commentaire, expliquez deux écarts précis avec les unités réellement obtenues.'),
    ('''extrait = "Les étudiantes analysent des corpus français. Elles comparent ensuite les résultats et rédigent une interprétation."
doc_extrait = nlp(extrait)
annotations = []
for token in list(doc_extrait)[:5]:
    annotations.append({"forme": token.text, "lemme": token.lemma_, "pos": token.pos_,
                        "debut": token.idx, "fin": token.idx + len(token.text)})
resultat_q6 = {"texte": extrait, "phrases": len(list(doc_extrait.sents)),
               "annotations": annotations,
               "noms": [t.lemma_ for t in doc_extrait if t.pos_ == "NOUN"],
               "verbes": [t.lemma_ for t in doc_extrait if t.pos_ == "VERB"],
               "question": "Quels noms désignent les objets analysés et quels verbes décrivent les activités ?"}''', 'Exemple sur deux phrases du sujet. Pour votre transfert, choisissez votre propre extrait de deux à quatre phrases, contrôlez ses cinq premières annotations et formulez une question qui lui convient.'),
])

_add('td2-s3', [
    ('''with open("corpus_td2.txt", encoding="utf-8") as fichier:
    texte = fichier.read()
doc_corpus = nlp(texte)
doc = doc_corpus
annotations = [{"forme": t.text, "lemme": t.lemma_, "pos": t.pos_}
               for t in doc if not t.is_punct and not t.is_space]
resultat_q1 = {"caracteres": len(texte), "phrases": len(list(doc.sents)),
               "tokens": len(doc), "annotations": annotations[:10]}''', 'Lisez le fichier puis annotez son contenu. Conservez les dix premières annotations hors ponctuation et espaces ; le compte total inclut tous les tokens.'),
    ('''from collections import Counter
def frequences_noms(texte, exclusions=None):
    if exclusions is None:
        exclusions = set()
    doc = nlp(texte)
    return Counter(t.lemma_.lower() for t in doc
                   if t.pos_ == "NOUN" and not t.is_punct and not t.is_stop
                   and t.lemma_.lower() not in exclusions)
def frequences_verbes(texte, exclusions=None):
    if exclusions is None:
        exclusions = set()
    doc = nlp(texte)
    return Counter(t.lemma_.lower() for t in doc
                   if t.pos_ == "VERB" and not t.is_punct and not t.is_stop
                   and t.lemma_.lower() not in exclusions)
resultat_q2 = {"noms": dict(frequences_noms(texte)), "verbes": dict(frequences_verbes(texte))}''', 'Comptez les lemmes après sélection de la catégorie. Ne comptez pas seulement les formes différentes : les répétitions augmentent l’effectif.'),
    ('''exclusions = ["notice"]
avant = dict(frequences_noms(texte))
apres = dict(frequences_noms(texte, exclusions))
resultat_q3 = {"exclusions": exclusions, "avant": avant, "apres": apres,
               "justification": "Cet essai retire le lemme notice pour observer son effet sur la distribution ; ce choix doit être discuté selon la question étudiée."}''', 'Exemple d’exclusion explicite sur le corpus fourni. Le dictionnaire après conserve exactement les autres effectifs ; justifiez votre propre choix.'),
    ('''from collections import Counter
comptes_pos = Counter(t.pos_ for t in doc if not t.is_punct and not t.is_space)
resultat_q4 = {"pos": dict(comptes_pos), "top3": comptes_pos.most_common(3),
               "limite": "Les catégories sont proposées par un modèle et doivent être vérifiées sur les occurrences."}''', 'Triez les catégories selon leurs effectifs. Les ex æquo peuvent avoir plusieurs ordres ; inspectez les tokens qui justifient les comptes.'),
    ('''tokens = [t for t in doc if not t.is_punct and not t.is_space]
controle = []
for token in tokens[:5]:
    controle.append({"forme": token.text, "lemme": token.lemma_, "pos": token.pos_,
                     "jugement": "À compléter après examen du token dans sa phrase."})
lemmes_contenu = [t.lemma_ for t in doc_corpus
                  if t.pos_ in {"NOUN", "VERB", "ADJ"} and not t.is_punct and not t.is_stop]
resultat_q5 = {"lemmes": lemmes_contenu, "controle": controle,
               "limite_modele": "Une sortie de modèle est une proposition à examiner, pas une annotation humaine de référence."}''', 'Ce code prépare cinq occurrences pour votre contrôle manuel. Remplacez chaque invitation par un jugement argumenté ; le programme ne peut pas rédiger cette vérification à votre place.'),
    ('''import matplotlib.pyplot as plt
from wordcloud import WordCloud
frequences = resultat_q3["apres"]
plt.bar(list(frequences), list(frequences.values()))
plt.ylabel("Occurrences de lemmes nominaux")
plt.xticks(rotation=45)
plt.show()
nuage = WordCloud(background_color="white", random_state=42).generate_from_frequencies(frequences)
plt.figure()
plt.imshow(nuage)
plt.axis("off")
plt.show()
resultat_q6 = {"frequences": frequences,
               "hypothese": "À formuler à partir du graphique obtenu.",
               "verification": "À compléter en revenant aux phrases qui contiennent les lemmes retenus."}''', 'Les deux figures utilisent les mêmes fréquences filtrées. Rédigez ensuite une hypothèse et sa vérification dans le texte ; le score ne certifie ni les images ni l’interprétation.'),
    ('''from collections import Counter
def frequences_pos(texte, categories, exclusions=None):
    if exclusions is None:
        exclusions = set()
    doc = nlp(texte)
    return Counter(t.lemma_.lower() for t in doc
                   if t.pos_ in categories and not t.is_punct and not t.is_stop
                   and t.lemma_.lower() not in exclusions)
resultat_q7 = {"general_noms": dict(frequences_pos(texte, {"NOUN"})),
               "specialise_noms": dict(frequences_noms(texte)),
               "general_verbes": dict(frequences_pos(texte, {"VERB"})),
               "specialise_verbes": dict(frequences_verbes(texte)),
               "combine": dict(frequences_pos(texte, {"NOUN", "VERB"})),
               "comparaison": "Le filtre paramétrable reproduit les comptes des fonctions spécialisées ; les essais sur d’autres données restent à comparer."}''', 'Paramétrez les catégories et comparez avec les deux fonctions indépendantes de Q2. Testez aussi le texte vide et le transfert sur les 5 000 premiers caractères de Faguet. La combinaison additionne les effectifs lorsqu’un même lemme apparaît dans les deux catégories.'),
])

_add('td-r0-s3', [
    ('''def compter_mots(texte):
    return len(texte.split())
tests_comptage = {"principal": compter_mots(texte), "vide": compter_mots(""),
                  "essai": compter_mots("Un essai")}
print("Résultat Q1 :", tests_comptage)''', 'La fonction reçoit le texte en paramètre et renvoie le nombre d’éléments issus de split(). Testez aussi le cas vide.'),
    ('''mots_normalises = texte.lower().split()
print("Résultat Q2 :", mots_normalises)''', 'La minuscule précède le découpage ; la ponctuation reste attachée aux chaînes.'),
    ('''def frequences(texte):
    comptes = {}
    for mot in texte.lower().split():
        comptes[mot] = comptes.get(mot, 0) + 1
    return comptes
tests_frequences = {"principal": frequences(texte), "essai": frequences("Mot mot autre")}
print("Résultat Q3 :", dict(tests_frequences))''', 'get(mot, 0) initialise le premier compte ; chaque répétition ajoute une unité. Comparez le test au calcul manuel.'),
    ('''bilan_limite = {"comptes": frequences("Python Python."),
                "limite": "Le point final distingue python. de python ; la minuscule ne retire pas la ponctuation."}
print("Résultat Q4 :", bilan_limite)''', 'Réutilisez la fonction de Q3. La différence entre les deux clés fournit un exemple concret de la limite observée.'),
])

_add('td-r1-s3', [
    ('''doc = nlp(texte)
print("Résultat Q1 :", len(doc))''', 'nlp transforme la chaîne en Doc ; len(doc) compte ses tokens, ponctuation comprise.'),
    ('''annotations = []
for token in doc:
    annotations.append((token.text, token.lemma_, token.pos_))
print("Résultat Q2 :", annotations)''', 'Chaque tuple associe forme, lemme et catégorie d’un même token. Inspectez les prédictions avant de formuler votre observation.'),
    ('''noms = []
for token in doc:
    if token.pos_ == "NOUN":
        noms.append(token.lemma_)
print("Résultat Q3 :", noms)''', 'Sélectionnez les tokens de catégorie NOUN puis ajoutez leur lemme ; ne filtrez pas une liste de chaînes privées de leurs attributs.'),
    ('''verbes = []
for token in doc:
    if token.pos_ == "VERB":
        verbes.append(token.lemma_)
print("Résultat Q4 :", verbes)''', 'Conservez les catégories effectivement prédites. Si la liste est vide, revenez aux annotations de Q2 et discutez les erreurs possibles du modèle.'),
])

_add('td-r2-s3', [
    ('''from collections import Counter
def frequences_lemmas(texte, stopwords=None):
    doc = nlp(texte)
    lemmes = [token.lemma_ for token in doc if token.pos_ == "NOUN"]
    return Counter(lemmes)
print("Résultat Q1 :", dict(frequences_lemmas(texte)))''', 'La fonction calcule les effectifs des lemmes nominaux. À ce stade, stopwords est prévu dans la signature mais le filtrage sera ajouté en Q3.'),
    ('''doc = nlp(texte)
annotations = []
for token in doc:
    annotations.append((token.text, token.lemma_, token.pos_))
print("Résultat Q2 :", annotations)''', 'Ce tableau expose les prédictions qui ont déterminé les fréquences. Une étiquette inattendue appelle une vérification dans le contexte.'),
    ('''def frequences_lemmas(texte, stopwords=None):
    if stopwords is None:
        stopwords = set()
    doc = nlp(texte)
    lemmes = [token.lemma_ for token in doc
              if token.pos_ == "NOUN" and not token.is_stop
              and token.lemma_ not in stopwords]
    return Counter(lemmes)
tests_filtrage = {"sans_exclusions": dict(frequences_lemmas(texte)),
                  "avec_exclusions": dict(frequences_lemmas(texte, {"texte"}))}
print("Résultat Q3 :", tests_filtrage)''', 'Distinguez mots vides du modèle et exclusions supplémentaires. Comparez avant/après avec le même texte ; les lemmes conservés gardent leurs effectifs.'),
    ('''classements = {"avant": frequences_lemmas(texte).most_common(),
               "apres": frequences_lemmas(texte, {"texte"}).most_common()}
print("Résultat Q4 :", classements)''', 'Réutilisez la fonction révisée. Comparez les rangs et les effectifs ; le tri seul ne démontre pas la pertinence linguistique du classement.'),
])

_add('td3-s3', [
    ('''champs = ["unite", "fenetre", "normalisation", "agregation"]
absents = [champ for champ in champs if any(a.get(champ) is None for a in affirmations)]
resultat_q1 = {"sha256": hashlib.sha256((RESSOURCES / "faguet_source.txt").read_bytes()).hexdigest(),
               "affirmations": [a["id"] for a in affirmations],
               "prompts": len(set(a["prompt"] for a in affirmations + citations)),
               "parametres_absents": absents,
               "limite": "Les réponses appartiennent à la même conversation et dépendent des échanges précédents ; leurs fourchettes ne sont pas des mesures de référence."}''', 'Reliez chaque information aux fichiers fournis. Les paramètres absents restent absents : ne les reconstruisez pas à partir des nombres annoncés.'),
    ('''def concordances_exactes(source, motif, largeur=20):
    if motif == "":
        raise ValueError("Le motif ne doit pas être vide.")
    resultats, position = [], 0
    while True:
        debut = source.find(motif, position)
        if debut == -1:
            break
        fin = debut + len(motif)
        resultats.append({"debut": debut, "fin": fin, "pivot": source[debut:fin],
                          "gauche": source[max(0, debut-largeur):debut],
                          "droite": source[fin:fin+largeur]})
        position = fin
    return resultats
resultat_q2 = {"concordances": concordances_exactes(source_test, "droit"),
               "absent": concordances_exactes(source_test, "justice")}''', 'La recherche avance à la fin du résultat précédent, sans chevauchement. Testez séparément les bords, le fragment dans un mot, le texte vide et le motif vide, puis explorez Faguet.'),
    ('''source = "Les lecteurs lisent. Une lectrice lit."
doc_recherche = nlp(source)
def ligne(token):
    return {"forme": token.text, "debut": token.idx, "fin": token.idx + len(token.text)}
resultat_q3 = {
    "fragment": [{"forme": r["pivot"], "debut": r["debut"], "fin": r["fin"]}
                 for r in concordances_exactes(source, "lit")],
    "forme": [ligne(t) for t in doc_recherche if t.text == "lit"],
    "lemme": [ligne(t) for t in doc_recherche if t.lemma_ == "lire"],
    "explication": "Un fragment cherche une sous-chaîne, une forme désigne un token entier et le lemme dépend de l’analyse du modèle. Une famille lexicale ne se confond pas avec un lemme."}''', 'Comparez les listes réellement obtenues ; ne remplacez pas une prédiction du modèle pour obtenir l’écart espéré. Le transfert et le PhraseMatcher restent à appliquer à Faguet.'),
    ('''lignes = []
for citation in citations:
    debut = texte_faguet.find(citation["citation"])
    lignes.append({"id": citation["id"], "citation": citation["citation"],
                   "debut": debut, "exacte": debut >= 0})
resultat_q4 = {"citations": lignes,
               "limite": "Une citation absente comme chaîne exacte peut exprimer une idée proche : cette proximité et la fidélité au sens demandent une lecture du passage."}''', 'Cherchez dans le texte original, retours à la ligne compris. Une recherche normalisée ne doit pas modifier le verdict d’identité exacte.'),
    ('''position = texte_faguet.find("légalement")
debut = max(0, position - 45)
passage = texte_faguet[debut:position + 100]
resultat_q5 = {"id": "C1", "passage_source": passage, "debut": debut,
               "difference": "Comparez ici, mot à mot, la citation originale et ce passage, y compris naturally/naturellement et les retours à la ligne.",
               "verdict": "À rédiger après cette comparaison : distinguez transformation typographique et substitution lexicale."}''', 'Cet exemple localise un candidat autour du fragment distinctif. Ajustez son étendue et rédigez votre qualification ; conservez la citation Gemini intacte.'),
    ('''tests = [
    {"source": "La preuve vient du texte.", "citation": "preuve vient", "exacte_attendue": True},
    {"source": "La preuve vient du texte.", "citation": "preuve arrive", "exacte_attendue": False}]
for test in tests:
    test["exacte_observee"] = test["citation"] in test["source"]
resultat_q6 = {"tests": tests,
               "regle_humaine": "Après la recherche, vérifier le sens, la négation et la personne dont le propos est rapporté ; les mots communs ne suffisent pas."}''', 'Les attentes sont fixées avant la recherche. Créez vos propres deux cas et comparez aussi les deux passages contenant professions demandés dans le sujet.'),
    ('''doc_preuves = nlp(texte_faguet)
pivots = [t for t in doc_preuves if t.text.lower() == "intelligence"]
preuves = []
for token in pivots[:3]:
    debut = max(0, token.idx - 80)
    fin = min(len(texte_faguet), token.idx + len(token.text) + 80)
    preuves.append({"debut": debut, "fin": fin, "passage": texte_faguet[debut:fin]})
resultat_q7 = {"affirmation": "G1", "preuves": preuves,
               "convention_proposee": "Proposition à tester : formes minuscules et présence au plus une fois par phrase ; groupe d’associés à expliciter.",
               "limite": "Ces passages documentent des emplois du pivot, pas encore un compte d’association comparable au nombre de Gemini."}''', 'Le filtre porte sur le token entier. Les trois preuves doivent couvrir trois occurrences différentes ; vérifiez si les fenêtres retenues permettent réellement d’interpréter les passages.'),
])

_MICRO = '[["chat", "livre", "chat"], ["livre"], ["chat", "plume"], ["plume"]]'
_MARGE = '''def marge(contextes, terme):
    return sum(1 for contexte in contextes if terme in contexte)'''
_COOC = '''def cooc_phrases(contextes, pivot, associe):
    return sum(1 for contexte in contextes if pivot in contexte and associe in contexte)'''
_UNION = '''def cooc_union(contextes, pivot, associes):
    return sum(1 for contexte in contextes
               if pivot in contexte and any(a in contexte for a in associes))'''
_FENETRE = '''def cooc_fenetre(tokens, pivot, associe, k):
    if k < 1:
        raise ValueError("k doit être au moins égal à 1.")
    pivots = [i for i, mot in enumerate(tokens) if mot == pivot]
    associes = [i for i, mot in enumerate(tokens) if mot == associe]
    return sum(1 for i in pivots for j in associes if 0 < abs(i-j) <= k)'''
_MESURER = _MARGE + '\n' + _COOC + '''
def mesurer_phrase(contextes, pivot, associe):
    return {"N": len(contextes), "cooc": cooc_phrases(contextes, pivot, associe),
            "marge_pivot": marge(contextes, pivot), "marge_associe": marge(contextes, associe)}'''

_add('td4-s3', [
    (_MARGE + '\ncontextes = ' + _MICRO + '''
resultat_q1 = {"chat": marge(contextes, "chat"), "livre": marge(contextes, "livre"), "N": len(contextes)}''', 'Chaque contexte contribue une fois au plus à la marge, même si chat est répété. Appliquez ensuite la fonction aux phrases de Faguet en déclarant le filtre des tokens.'),
    (_COOC + '\ncontextes = ' + _MICRO + '''
resultat_q2 = {"chat_livre": cooc_phrases(contextes, "chat", "livre"),
               "chat_plume": cooc_phrases(contextes, "chat", "plume"),
               "livre_plume": cooc_phrases(contextes, "livre", "plume")}''', 'Une paire compte une fois par phrase. Vérifiez symétrie, marges et pivot absent ; retrouvez ensuite les phrases communes des deux paires de Faguet.'),
    (_COOC + '\n' + _UNION + '''
contextes = [["chat", "livre", "plume"], ["chat", "livre"], ["plume"]]
associes = ["livre", "plume"]
resultat_q3 = {"somme_paires": sum(cooc_phrases(contextes, "chat", a) for a in associes),
               "union": cooc_union(contextes, "chat", associes)}''', 'Une phrase avec les deux associés contribue deux fois à la somme et une fois à l’union. Gardez ces conventions distinctes en examinant la ligne Intelligence.'),
    (_FENETRE + '''
tokens = ["chat", "lit", "un", "livre", "chat", "lit"]
resultat_q4 = {"k1": cooc_fenetre(tokens, "chat", "livre", 1),
               "k3": cooc_fenetre(tokens, "chat", "livre", 3)}''', 'Comptez les paires de positions, pas seulement les pivots couverts. Pour Faguet, conservez ponctuation et mots vides dans le flux de distance.'),
    (_FENETRE + '''
phrases_test = [["chat"], ["livre"]]
flux = [mot for phrase in phrases_test for mot in phrase]
resultat_q5 = {"sans_frontiere": cooc_fenetre(flux, "chat", "livre", 1),
               "dans_phrase": sum(cooc_fenetre(p, "chat", "livre", 1) for p in phrases_test)}''', 'La concaténation autorise une paire qui traverse la frontière. Comparez ensuite vos trois unités dans Faguet en conservant leurs définitions et leurs preuves.'),
    ('''annotations = [{"forme": "chat", "lemme": "chat"}, {"forme": "chats", "lemme": "chat"},
               {"forme": "chaton", "lemme": "chaton"}]
def compter(annotations, cle, valeur):
    return sum(1 for annotation in annotations if annotation[cle] == valeur)
resultat_q6 = {"formes_chat": compter(annotations, "forme", "chat"),
               "lemmes_chat": compter(annotations, "lemme", "chat")}''', 'Cette table manuelle isole le changement de représentation. Sur Faguet, vérifiez cinq annotations et gardez les autres choix constants lors de la comparaison.'),
    (_MESURER + '\ncontextes = ' + _MICRO + '''
resultat_q7 = mesurer_phrase(contextes, "chat", "livre")
assert 0 <= resultat_q7["cooc"] <= resultat_q7["marge_pivot"] <= resultat_q7["N"]
assert 0 <= resultat_q7["cooc"] <= resultat_q7["marge_associe"] <= resultat_q7["N"]''', 'Assemblez les fonctions pour produire les quatre effectifs du microcas. L’export demandé doit aussi contenir les protocoles et passages de vos deux paires réelles.'),
])

_PROPORTION = '''def proportion(effectif, denominateur):
    return None if denominateur == 0 else effectif / denominateur'''
_PROPORTIONS = _PROPORTION + '''
def proportions(N, marge_pivot, marge_associe, cooc):
    return {"conditionnelle": proportion(cooc, marge_pivot), "base": proportion(marge_associe, N)}'''
_COUVERTURE = '''def couverture_pivots(tokens, pivot, associe, k):
    if k < 1:
        raise ValueError("k doit être au moins égal à 1.")
    pivots = [i for i, mot in enumerate(tokens) if mot == pivot]
    associes = [i for i, mot in enumerate(tokens) if mot == associe]
    couverts = sum(1 for i in pivots if any(0 < abs(i-j) <= k for j in associes))
    return None if not pivots else couverts / len(pivots)'''
_add('td5-s3', [
    (_PROPORTIONS + '''
mesures = proportions(8, 3, 4, 2)
resultat_q1 = {cle: None if valeur is None else round(valeur, 6) for cle, valeur in mesures.items()}''', 'La proportion conditionnelle divise par les phrases avec pivot ; la base divise par toutes les phrases. Complétez avec votre schéma des huit cases et votre paire de Faguet.'),
    (_PROPORTIONS + '''
A = proportions(12, 4, 9, 3)
B = proportions(12, 4, 2, 2)
resultat_q2 = {"A": round(A["conditionnelle"], 6), "B": round(B["conditionnelle"], 6),
               "base_A": round(A["base"], 6), "base_B": round(B["base"], 6)}''', 'Comparez chaque proportion à sa propre base : l’associé le plus fréquent près du pivot n’est pas nécessairement le plus concentré relativement à sa présence globale.'),
    ('''def pour_mille(effectif, taille):
    return None if taille == 0 else 1000 * effectif / taille
resultat_q3 = {"court": pour_mille(4, 100), "long": pour_mille(8, 400)}''', 'Le taux utilise la taille du segment, pas celle de l’autre extrait. Appliquez la même unité aux deux moitiés contiguës de Faguet et conservez les indices.'),
    (_PROPORTION + '''
resultat_q4 = {"associe_sachant_pivot": round(proportion(2, 3), 6),
               "pivot_sachant_associe": round(proportion(2, 4), 6)}''', 'L’inversion conserve la cooccurrence et change le dénominateur. Vérifiez les quatre cases du tableau 2 × 2 et explicitez les deux populations dans votre commentaire.'),
    (_PROPORTION + '''
resultat_q5 = {"sans_pivot": proportion(0, 0), "sans_associe": proportion(0, 5)}''', 'Zéro sur cinq est défini et vaut zéro ; zéro sur zéro n’est pas défini. Conservez les effectifs pour discuter aussi les petits nombres.'),
    (_COUVERTURE + '''
tokens = ["chat", "lit", "un", "livre", "chat", "lit"]
resultat_q6 = {"k1": couverture_pivots(tokens, "chat", "livre", 1),
               "k3": couverture_pivots(tokens, "chat", "livre", 3)}''', 'Chaque position du pivot contribue au plus une fois. Comparez fenêtres 5, 10 et 25 dans Faguet avec le même flux non filtré et les effectifs couverts/total.'),
    (_PROPORTION + '''
cooc, marge_pivot = 2, 3
resultat_q7 = {"effectif": cooc, "denominateur": marge_pivot,
               "proportion": round(proportion(cooc, marge_pivot), 6)}''', 'Le résultat du microcas garde numérateur et dénominateur. Votre export et votre paragraphe doivent également distinguer observation, interprétation possible et limites du protocole.'),
])

_add('td6-s3', [
    ('''def positions(tokens, forme):
    return [i for i, token in enumerate(tokens) if token == forme]
flux = ["a", "cible", "b", "cible"]
indices = positions(flux, "cible")
resultat_q1 = {"positions": indices, "relatives": [i / len(flux) for i in indices]}''', 'Divisez les indices par la taille du flux complet. Pour votre dispersion de Faguet, conservez les indices spaCy d’origine et reliez les zones à des passages.'),
    ('''def segmenter(tokens, nb_segments):
    N = len(tokens)
    return [tokens[int(j*N/nb_segments):int((j+1)*N/nb_segments)]
            for j in range(nb_segments)]
flux = ["chat", "chat", "a", "b", "c", "d", "chat", "e"]
segments = segmenter(flux, 4)
resultat_q2 = {"effectifs": [s.count("chat") for s in segments], "tailles": [len(s) for s in segments]}''', 'Les bornes couvrent tout le flux sans chevauchement. Testez aussi onze tokens ; les dix segments de Faguet conservent leurs bornes et dénominateurs alphabétiques.'),
    ('''segments_test = [["chat", "lit"], ["plume", "chat", "lit", "ici"]]
resultat_q3 = {mot: [1000 * segment.count(mot) / len(segment) for segment in segments_test]
               for mot in ["chat", "plume"]}''', 'Les deux segments ont des tailles différentes. Pour la carte de Faguet, calculez les taux avec les tailles alphabétiques et gardez une échelle commune aux lignes.'),
    (_FENETRE + '''
tokens = ["chat", "a", "livre", "chat"]
fenetres = [1, 2, 3]
resultat_q4 = {"k": fenetres, "cooc": [cooc_fenetre(tokens, "chat", "livre", k) for k in fenetres]}''', 'Reprenez exactement le compte de paires du TD4. Présentez séparément la couverture du TD5 ; ces mesures n’ont pas la même unité.'),
    ('''tokens = ["avant", "chat", "puis", "plume", "après"]
indice, marge = 3, 1
debut, fin = max(0, indice-marge), min(len(tokens), indice+marge+1)
resultat_q5 = {"debut": debut, "fin": fin, "contexte": " ".join(tokens[debut:fin])}''', 'La fin exclue inclut le token situé une place après le pivot. Le join appartient au microcas ; les passages de Faguet doivent être extraits de la source originale par leurs bornes caractères.'),
    ('''resultat_q6 = {"etiquettes": ["segment 1", "segment 2"], "valeurs": resultat_q3["chat"]}
plt.bar(resultat_q6["etiquettes"], resultat_q6["valeurs"])
plt.ylabel("Occurrences de chat pour mille tokens")
plt.show()''', 'Réutilisez les taux calculés en Q3. La tâche complète comprend aussi la matrice de cooccurrences de Faguet, sa diagonale conventionnelle et la relecture de la figure.'),
    ('''segments_test = [["chat", "lit"], ["plume", "chat", "lit", "ici"]]
effectif = sum(s.count("chat") for s in segments_test)
taille = sum(len(s) for s in segments_test)
resultat_q7 = {"effectif": effectif, "taille": taille, "pour_mille": round(1000*effectif/taille, 6)}''', 'Additionnez les effectifs et les tailles avant de diviser. L’export final doit aussi relier les visualisations aux trois passages et à vos deux lectures argumentées.'),
])

_CHAMPS = '''def champs_manquants(affirmation):
    return [champ for champ in ["unite", "fenetre", "normalisation", "agregation"]
            if affirmation.get(champ) is None]'''
_MOTEUR = '''def contient_expression(tokens, expression):
    return bool(expression) and any(tokens[i:i+len(expression)] == expression
                                    for i in range(len(tokens)-len(expression)+1))
def mesurer(contextes, pivots, associes, agregation="union"):
    preuves, marge_pivot, marge_associe, cooc = [], 0, 0, 0
    for i, contexte in enumerate(contextes):
        presents_p = [contient_expression(contexte, p) for p in pivots]
        presents_a = [contient_expression(contexte, a) for a in associes]
        marge_pivot += int(any(presents_p))
        marge_associe += int(any(presents_a))
        if any(presents_p) and any(presents_a):
            preuves.append(i)
        if agregation == "union":
            cooc += int(any(presents_p) and any(presents_a))
        elif agregation == "somme_paires":
            cooc += sum(int(p and a) for p in presents_p for a in presents_a)
        else:
            raise ValueError("Agrégation inconnue")
    return {"N": len(contextes), "cooc": cooc, "marge_pivot": marge_pivot,
            "marge_associe": marge_associe, "preuves": preuves}'''
_COMPARER = '''def comparer_intervalle(valeur, borne_basse, borne_haute):
    if borne_basse > borne_haute:
        raise ValueError("Bornes inversées")
    return ("compatible selon le protocole" if borne_basse <= valeur <= borne_haute
            else "contredit selon le protocole")'''
_add('td7-s3', [
    (_CHAMPS + '''
annonce = {"pivot": "chat", "associes": ["livre"], "intervalle": [2, 4],
           "unite": None, "fenetre": None, "normalisation": None, "agregation": None}
manquants = champs_manquants(annonce)
resultat_q1 = {"mesurable": not manquants, "manquants": manquants}''', 'Une absence de protocole empêche la comparaison directe ; elle ne prouve pas un nombre faux. Gardez séparées les six annonces originales et vos propositions.'),
    (_MOTEUR + '\ncontextes = ' + _MICRO + '''
mesure = mesurer(contextes, [["chat"]], [["livre"]], "union")
resultat_q2 = {cle: mesure[cle] for cle in ["N", "cooc", "marge_pivot", "marge_associe"]}''', 'Le moteur reconnaît des expressions contiguës et garde les indices de preuve. Dans Faguet, ignorez seulement les tokens d’espacement pour ces expressions et conservez les positions d’origine.'),
    ('''def verifier_exactement(source, citation):
    debut = source.find(citation)
    fin = debut + len(citation) if debut >= 0 else -1
    return {"exacte": debut >= 0, "debut": debut, "fin": fin,
            "passage": source[debut:fin] if debut >= 0 else ""}
source = "La preuve vient du texte."
exacte = verifier_exactement(source, "preuve vient")
resultat_q3 = {cle: exacte[cle] for cle in ["exacte", "debut", "fin"]}
resultat_q3["alteree"] = verifier_exactement(source, "preuve arrive")["exacte"]''', 'Une variante proche reste absente comme chaîne exacte. Pour les trois citations réelles, distinguez identité, candidat proche et absence de localisation, en conservant chaque différence.'),
    (_COMPARER + '''
resultat_q4 = {"dans_intervalle": comparer_intervalle(3, 2, 4),
               "hors_intervalle": comparer_intervalle(5, 2, 4)}
assert comparer_intervalle(2, 2, 4) == comparer_intervalle(4, 2, 4)''', 'Les bornes sont inclusives. Avant toute application aux annonces réelles, vérifiez que corpus, unité, normalisation et agrégation permettent cette comparaison.'),
    (_MOTEUR + '''
contextes = [["chat", "livre", "plume"], ["chat", "livre"], ["plume"]]
resultat_q5 = {mode: mesurer(contextes, [["chat"]], [["livre"], ["plume"]], mode)["cooc"]
               for mode in ["somme_paires", "union"]}''', 'Les deux mesures appliquent les mêmes termes à deux agrégations. Définissez aussi les alternatives et expressions des six annonces réelles, sans choisir une convention pour retrouver Gemini.'),
    (_MOTEUR + '''
contextes = [["livre", "plume"], ["livre"], ["plume"], ["livre", "plume", "plume"], ["autre"]]
mesure = mesurer(contextes, [["livre"]], [["plume"]], "union")
resultat_q6 = {cle: mesure[cle] for cle in ["N", "cooc", "marge_pivot", "marge_associe"]}''', 'La définition est rappelée ici pour rendre l’exemple lisible : dans votre notebook, réutilisez le même moteur figé en Q2 sans le modifier. Il traite un nouveau corpus. Ajoutez les attentes manuelles du voisin et les cas limites ; les tests de comptage ne valident pas les annotations linguistiques.'),
    (_CHAMPS + '\n' + _MOTEUR + '\n' + _COMPARER + '''
def auditer(affirmation, contextes, protocole_original):
    if champs_manquants(protocole_original):
        return "insuffisamment défini"
    compte = mesurer(contextes, affirmation["pivots"], affirmation["associes"],
                     protocole_original["agregation"])["cooc"]
    return comparer_intervalle(compte, *affirmation["intervalle"])
contextes = ''' + _MICRO + '''
annonce = {"pivots": [["chat"]], "associes": [["livre"]], "intervalle": [0, 2]}
incomplet = {cle: None for cle in ["unite", "fenetre", "normalisation", "agregation"]}
complet = {"unite": "présence par phrase", "fenetre": "phrase entière",
           "normalisation": "formes minuscules", "agregation": "union"}
resultat_q7 = {"indefini": auditer(annonce, contextes, incomplet),
               "defini": auditer(annonce, contextes, complet)}''', 'La garde précède le calcul et la comparaison. Cet exemple traite les deux protocoles du microcas ; votre livrable complet relie aussi six annonces, citations, mesures, figures, tests, passages et synthèse argumentée.'),
])

_ENTITES = '''def entites(texte, pipeline):
    return [[entite.text, entite.label_] for entite in pipeline(texte).ents]'''
_add('td1b-s3', [
    (_ENTITES + '''
resultat_q1 = {"texte": texte_q1, "entites": entites(texte_q1, nlp_entites)}''', 'Conservez les entités réellement proposées par le modèle md fixé. Discutez ensuite les éléments que vous aviez anticipés ; une absence peut venir du modèle.'),
    (_ENTITES + '''
def selectionner(lignes):
    return [ligne for ligne in lignes if ligne[1] in {"PER", "ORG"}]
entites_q2 = entites(texte_q2, nlp_entites)
texte_personnel = "Emmanuel Macron visite Google à Toulon."
entites_personnelles = entites(texte_personnel, nlp_entites)
resultat_q2 = {"texte": texte_q2, "entites": entites_q2, "selection": selectionner(entites_q2),
               "essai": {"texte": texte_personnel, "entites": entites_personnelles,
                         "selection": selectionner(entites_personnelles)}}''', 'Le filtrage s’applique aux prédictions sans changer leurs labels. Remplacez le texte d’essai par le vôtre, puis interprétez les erreurs éventuelles à partir des mentions observées.'),
    ('''nlp_sim = spacy.load("fr_core_news_md")
mots = {mot: nlp_sim(mot) for mot in ["chien", "chat", "voiture"]}
phrase1, phrase2 = "Le chat est sur le tapis.", "Le chien est sur le canapé."
variation = "Le chat est sous le tapis."
resultat_q3 = {
    "vecteurs": {mot: doc.has_vector for mot, doc in mots.items()},
    "scores": {"chien_chat": float(mots["chien"].similarity(mots["chat"])),
               "chien_voiture": float(mots["chien"].similarity(mots["voiture"])),
               "phrases": float(nlp_sim(phrase1).similarity(nlp_sim(phrase2)))},
    "variation": {"original": phrase1, "modifie": variation,
                  "score": float(nlp_sim(phrase1).similarity(nlp_sim(variation)))}}''', 'Calculez les scores avec le modèle md. Comparez les valeurs observées et votre modification ; une forte similarité ne garantit ni équivalence des phrases ni fidélité au sens.'),
    (_ENTITES + '''
nlp_sans_regles = spacy.load("fr_core_news_md")
nlp_regles = spacy.load("fr_core_news_md")
avant = entites(texte_q4, nlp_sans_regles)
regles = [{"label": "ORG", "pattern": "Université de Toulon"},
          {"label": "ORG", "pattern": "Bibliothèque des Salins"},
          {"label": "LOC", "pattern": "Port des Salins"},
          {"label": "DATE", "pattern": "16 octobre 2026"}]
ruler = nlp_regles.add_pipe("entity_ruler", before="ner")
ruler.add_patterns(regles)
textes = [texte_q4, "La Bibliothèque des Salins accueille des lecteurs.",
          "Nous visitons le Port des Salins.", "La séance a lieu le 16 octobre 2026.",
          "La Bibliothèque des Salins participe le 16 octobre 2026.",
          "Nous étudions à l’université de Toulon.",
          "Dans cette fiction, Bibliothèque des Salins est le titre d’un roman."]
essais = [{"texte": texte, "sans_regles": entites(texte, nlp_sans_regles),
           "avec_regles": entites(texte, nlp_regles)} for texte in textes]
resultat_q4 = {"texte": texte_q4, "avant": avant, "apres": entites(texte_q4, nlp_regles),
               "pipeline": nlp_regles.pipe_names, "regles": regles, "essais": essais}''', 'Rechargez les modèles pour éviter de multiplier les règles à chaque exécution. Cet exemple couvre les quatre règles et propose une variante de casse et un usage fictif ambigu. Examinez leurs effets réels ; une expression identique peut changer de rôle selon le contexte.'),
])
