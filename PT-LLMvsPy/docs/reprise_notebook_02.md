# Notebook 02 — correspondance des activités et des références

Cette fiche accompagne la lecture du [cahier 02](../notebooks/02_mesures_lexicales.ipynb). Elle compare la [version distribuée après le cahier 01](https://github.com/dreymond732/tal-notebook-evaluator/blob/fcb176f6e9454ff49a276d82d63eef80b6f6fabe/PT-LLMvsPy/notebooks/02_mesures_lexicales.ipynb) aux cinq étapes du descriptif de séance.

## Ce qui change dans le travail en classe

| Dans le 02 précédent | Dans le 02 révisé | Ce que l’étudiant peut montrer |
|---|---|---|
| §1, reprise du 01. Les annonces de Gemini arrivaient après le STTR. | §0, reprendre le corpus et identifier les sources. | Ouvrir le TXT ou le ZIP du 01 avec son numéro. Distinguer une valeur publiée par Studio d’un calcul proposé dans la conversation Gemini. |
| §2, prédiction sur phrase personnelle. Le tableau des filtres sur le livre arrivait au §3. | §1, aller du comptage manuel aux trois filtres sur Faguet. | Retrouver un token d’espacement, un signe de ponctuation et une unité rejetée par le filtre alphabétique. Lire le nombre de tokens et de phrases de chaque ligne avant d’interpréter leur rapport. Confronter une mesure à une annonce. |
| §3, formes, lemmes, classements de fréquences, TTR par blocs et annonces dans la même section. | §2, comparer les représentations du mot. Conserver les fréquences par rang et pour une même entrée, puis l’étude du TTR par blocs. | Prévoir un regroupement sur sa phrase. Sur le livre, lire les écarts de types, d’hapax et de TTR à unité de comptage constante. Retrouver le nombre de blocs complets du STTR et le nombre de tokens du reliquat. |
| §4, cinq champs, détail d’une entrée et annotation de *vote*. | §3, relier l’écart d’un champ à une entrée de sa liste, puis à une occurrence localisée. | Lire l’effectif en formes et en lemmes. Vérifier la catégorie et le sens en contexte. Expliquer le risque que ferait courir une lecture automatique de *droit*, *état* ou *lettre*. |
| §5, marques de voix, locutions, noms et inspection d’une abréviation. | §4, examiner une graphie réellement comptée, un contexte de parole et la frontière détectée après une abréviation. | Distinguer les graphies réunies sous la clé `m`, le nombre de mentions d’une personne et l’attribution d’un propos. Un point final d’abréviation peut être intérieur à la phrase. |
| §6, règle de présence en phrase, préparation du 03 et consignes de sauvegarde réunies. | Deux moments distincts en fin de séance. | Expliquer pourquoi une phrase où le pivot se répète compte une seule fois. Préparer la question Studio *femme(s)/homme(s)* et le protocole M4 *femme/droit*. Récupérer son JSON et le rouvrir au 03 avec le corpus du 01. |

Le 02 et son test de structure étaient déjà dépourvus de l’appel à `auditer_reapplication`. La reprise inscrit cette propriété dans le test. Le chargement passe par `preparer_atelier` pour accepter les deux formats du 01. Le cahier ne redemande aucune empreinte à l’étudiant. Les métadonnées des exports antérieurs restent utilisables.

## Ce que contient le JSON du 02

Le nom reste `resultats_02_<numero>.json`. Les 22 rubriques de premier niveau du JSON précédent sont conservées. Elles comprennent les mesures, classements de fréquences, champs, preuves, réponses personnelles et les deux questions dans `travail_03`. La preuve de champ conserve la forme et ses positions et fournit désormais la phrase où cette occurrence a été lue. Le 03 et le 04 continuent de lire les rubriques qu’ils utilisaient déjà.

| Ajout | Ce qu’on peut vérifier en rouvrant le JSON |
|---|---|
| `decompte_tokens` | Mettre en regard le total brut de la bibliothèque, `len(doc)`, le nombre de tokens d’espacement et le volume hors espaces. |
| `logiciel_formes`, `meme_decoupage`, `formes_comparables` | Identifier le pipeline utilisé pour les formes, savoir si les tokens et les débuts de phrase coïncident et retrouver la mesure de référence qui sert à calculer l’écart avec les lemmes. |
| `abreviations`, `abreviation_choisie`, `preuves_abreviation` | Retrouver les décomptes par graphie, le choix personnel et les extraits avec leurs bornes. La réponse de l’étudiant se trouve dans `observations.abreviation`. |
| `essais_personnels.voix` | Relire la variante écrite pour repérer les mentions tout en conservant la phrase initiale utilisée pour le STTR dans `essais_personnels.lexique`. |

Après une correction, l’étudiant vérifie son numéro et la présence de sa réponse dans le dernier fichier téléchargé. Il conserve ce JSON dans son dossier personnel et le réimporte au 03 avec le TXT ou le ZIP du 01. La copie des trois JSON sur le dossier partagé intervient à la revue du 04.

## Repères chiffrés pour le débriefing

Exécution sur le TXT produit par le plan commun du 01, avec spaCy 3.8.18 et `fr_core_news_sm` 3.8.0. Les cahiers étudiants affichent leurs propres résultats à l’exécution.

| Convention | Tokens N | Phrases S | N/S | Types V | Hapax | TTR |
|---|---:|---:|---:|---:|---:|---:|
| Formes minuscules, hors espaces | 94 654 | 3 433 | 27,572 | 8 899 | 4 792 | 0,09402 |
| Formes minuscules, hors espaces et ponctuation | 81 077 | 3 433 | 23,617 | 8 879 | 4 791 | 0,10951 |
| Formes minuscules, tokens alphabétiques | 74 090 | 3 416 | 21,689 | 8 380 | 4 421 | 0,11311 |
| Lemmes, mêmes tokens alphabétiques | 74 090 | 3 416 | 21,689 | 5 926 | 2 787 | 0,07998 |

`tokens_bruts_spacy` vaut ici 95 575, soit les 94 654 tokens hors espaces et 921 tokens pour lesquels `is_space` vaut vrai. En retirant la ponctuation, on retire 13 577 tokens et le nombre de phrases retenues reste le même. Le passage au filtre alphabétique écarte encore 6 987 tokens et 17 segments qui ne contiennent aucun token alphabétique. Le `sentencizer` détermine les frontières en amont de ces filtres.

| Champ lexical | Formes | Lemmes | Écart |
|---|---:|---:|---:|
| Genre et anthropologie | 1 032 | 1 819 | +787 |
| Droit et institutions | 339 | 411 | +72 |
| Mœurs et famille | 625 | 766 | +141 |
| Travail et éducation | 235 | 404 | +169 |
| Féminisme et idéologies | 308 | 380 | +72 |

Les cinq gains dépendent des listes de cibles et des lemmes attribués. Le lemme *lettre* réunit ici « gens de lettres » et « cette lettre » dans un passage sur un envoi. La lecture des deux passages permet de discuter leur rattachement au champ du travail et de l’éducation. Dans « je vote aux élections », le modèle classe *vote* comme verbe et lui donne le lemme *vote*. Une recherche du seul lemme *voter* perd cette occurrence. Pour l’énonciation, les 75 unités comptées sous `m` sont des `m'` dans cette exécution. La graphie `M.` conserve son point et a un décompte distinct.

## Bibliothèque et références

| Ressource | Place dans la version révisée |
|---|---|
| [Fonctions de mesure](../src/tal_toolkit/metriques_globales.py) | Même API. `ProtocoleGlobal` fixe le filtre et la représentation. `calculer_metriques_globales` produit les mesures et leurs traces. `comparer_annonces` les rapproche des valeurs déclarées. |
| [Analyse lexicale du 02](../src/tal_toolkit/analyse_pt02.py) | Même API. `analyser_lexique_pt02` fournit les compteurs, le STTR, les listes de champs, les locutions et les mentions. `CHAMPS_LEXICAUX` et `PERSONNES` rendent consultables les choix de vocabulaire. |
| [Entrées et sorties du PT](../src/tal_toolkit/atelier.py) | Même circuit. `preparer_atelier` ouvre la sortie du 01 et fournit la fonction de sauvegarde. `charger_modele_francais` charge le modèle avec la segmentation en phrases utilisée dans l’atelier. |
| Manning, Raghavan et Schütze (2008), chapitre 2, et Bird, Klein et Loper (2009), chapitre 3 | Les deux lectures du 02 précédent restent associées à la tokenisation et à la normalisation. [Manning et al.](https://www.cambridge.org/highereducation/books/introduction-to-information-retrieval/669D108D20F556C5C30957D63B5AB65C/the-term-vocabulary-and-postings-lists/ED26D3C6F7EBDC3E0FB53B160874AB72) · [Bird et al.](https://www.nltk.org/book/ch03.html) |
| Evert (2009), « Corpora and collocations » | Lecture conservée pour la transition au 03. Le chapitre publié est distingué du manuscrit étendu de 2007 déjà proposé. [Chapitre publié](https://doi.org/10.1515/9783110213881.2.1212) · [Manuscrit](https://stephanie-evert.de/PUB/Evert2007HSK_extended_manuscript.pdf) |
| Documentation spaCy | Deux accès directs ajoutés pour interpréter `is_space`, `is_punct`, `is_alpha`, `lemma_` et identifier le modèle français. [Attributs du token](https://spacy.io/api/token) · [Modèles français](https://spacy.io/models/fr) |
| Matériaux du projet | Le rapport Studio, son [tableau d’annonces](../data/annonces_globales_gemini.json), la [conversation Gemini](https://share.gemini.google/43HURKzcfoet) et la [matrice du PT](matrice_pretraitements_gemini.md) restent les sources des affirmations à vérifier et des protocoles proposés. |
