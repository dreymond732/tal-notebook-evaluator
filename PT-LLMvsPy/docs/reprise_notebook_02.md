# Comparer les fréquences des formes et des lemmes — activités et références

Cette fiche accompagne la lecture du cahier [Comparer les fréquences des formes et des lemmes](../notebooks/02_comparer_les_frequences_des_formes_et_des_lemmes.ipynb). Elle compare la [version distribuée après la préparation du corpus](https://github.com/dreymond732/tal-notebook-evaluator/blob/fcb176f6e9454ff49a276d82d63eef80b6f6fabe/PT-LLMvsPy/notebooks/02_mesures_lexicales.ipynb) aux cinq étapes du descriptif de séance.

## Ce qui change dans le travail en classe

| Dans la version précédente | Dans le cahier révisé | Ce que l’étudiant peut montrer |
|---|---|---|
| §1, reprise du corpus nettoyé. Les annonces de Gemini arrivaient après le STTR. | §0, reprendre le corpus et identifier les sources. | Ouvrir le TXT ou l’archive du corpus nettoyé avec son numéro. Distinguer une valeur du rapport chiffré transmis le 10 novembre 2026 d’un calcul proposé dans la conversation Gemini. |
| §2, prédiction sur phrase personnelle. Le tableau des filtres sur le livre arrivait au §3. | §1, aller du comptage manuel aux trois filtres sur Faguet et écrire la condition d’un filtre personnel dans `filtrer`. | Retrouver un token d’espacement, un signe de ponctuation et une unité rejetée par le filtre alphabétique. Lire le nombre de tokens et de phrases de chaque ligne avant d’interpréter leur rapport. Confronter une mesure à une annonce. |
| §3, formes, lemmes, classements de fréquences, TTR par blocs et annonces dans la même section. | §2, comparer les représentations du mot. Conserver les fréquences par rang et pour une même entrée, puis l’étude du TTR par blocs. | Prévoir un regroupement sur sa phrase. Sur le livre, comparer le nombre de formes distinctes et de lemmes distincts, les hapax et le TTR à filtre constant. Modifier la représentation dans `compter_ma_version` et tester son choix sur la phrase puis le livre. Retrouver le nombre de blocs complets du STTR et le nombre de tokens du reliquat. |
| §4, cinq champs, détail d’une entrée et annotation de *vote*. | §3, relier l’écart d’un champ à une entrée de sa liste, puis à une occurrence localisée. | Lire l’effectif en formes et en lemmes. Vérifier la catégorie et le sens en contexte. Expliquer le risque que ferait courir une lecture automatique de *droit*, *état* ou *lettre*. |
| §5, marques de voix, locutions, noms et inspection d’une abréviation. | §4, examiner une graphie réellement comptée, un contexte de parole et la frontière détectée après une abréviation. | Distinguer les graphies réunies sous la clé `m`, le nombre de mentions d’une personne et l’attribution d’un propos. Un point final d’abréviation peut être intérieur à la phrase. |
| §6, règle de présence en phrase, préparation des cooccurrences et consignes de sauvegarde réunies. | Deux moments distincts en fin de séance. | Expliquer pourquoi une phrase où le pivot se répète compte une seule fois. Préparer la question du rapport sur *femme(s)/homme(s)* et le protocole M4 *femme/droit*. Récupérer son JSON et le rouvrir dans le cahier sur les cooccurrences avec le corpus nettoyé. |

Le cahier de comparaison des fréquences et son test de structure étaient déjà dépourvus de l’appel à `auditer_reapplication`. La reprise inscrit cette propriété dans le test. Le chargement passe par `preparer_atelier` pour accepter le TXT et le ZIP du corpus. Le cahier ne redemande aucune empreinte à l’étudiant. Les métadonnées des exports antérieurs restent utilisables.

## Ce que contient le JSON des fréquences

Le nom reste `resultats_02_<numero>.json`. Les 22 rubriques de premier niveau du JSON précédent sont conservées. Elles comprennent les mesures, classements de fréquences, champs, preuves, réponses personnelles et les deux questions dans `travail_03`. La preuve de champ conserve la forme et ses positions et fournit désormais la phrase où cette occurrence a été lue. Le cahier sur les cooccurrences y retrouve les deux calculs à mener. Le cahier d’audit relit notamment le nombre d’unités distinctes sous la clé `unites_distinctes`.

| Ajout | Ce qu’on peut vérifier en rouvrant le JSON |
|---|---|
| `decompte_tokens` | Mettre en regard le total brut de la bibliothèque, `len(doc)`, le nombre de tokens d’espacement et le volume hors espaces. |
| `logiciel_formes`, `meme_decoupage`, `formes_comparables` | Identifier le pipeline utilisé pour les formes, savoir si les tokens et les débuts de phrase coïncident et retrouver la mesure de référence qui sert à calculer l’écart avec les lemmes. |
| `abreviations`, `abreviation_choisie`, `preuves_abreviation` | Retrouver les décomptes par graphie, le choix personnel et les extraits avec leurs bornes. La réponse de l’étudiant se trouve dans `observations.abreviation`. |
| `variante_personnelle` | Relire les instructions du filtre et du comptage, les fréquences obtenues sur l’essai et les mesures du livre. |
| `preuve_vote` | Retrouver la phrase, la position du token, sa graphie, sa catégorie et son lemme lorsque l’occurrence a été retrouvée. |
| `essais_personnels.voix` | Relire la variante écrite pour repérer les mentions tout en conservant la phrase initiale utilisée pour le STTR dans `essais_personnels.lexique`. |

Après une correction, l’étudiant vérifie son numéro et la présence de sa réponse dans le dernier fichier téléchargé. Il conserve ce JSON dans son dossier personnel et le réimporte dans *Mesurer les cooccurrences par phrase et par fenêtre* avec le TXT ou l’archive du corpus nettoyé. La copie des trois JSON sur le dossier partagé intervient à la revue finale.

## Repères chiffrés pour le débriefing

Ces valeurs proviennent du TXT produit par le cahier 01 avec retrait des traits de soulignement (SHA-256 `ebb7e2aecf87ee716fcd2a6ebc636ae204ad3c1c38ed813b3810a5b3b41649fd`), avec spaCy 3.8.18 et `fr_core_news_sm` 3.8.0. Pour comparer une autre exécution, vérifiez l’empreinte du TXT, les versions et le filtre retenu.

| Convention | Occurrences retenues N | Phrases S | N/S | Unités distinctes V | Hapax | TTR |
|---|---:|---:|---:|---:|---:|---:|
| Formes minuscules, hors espaces | 93 795 | 3 512 | 26,707 | 8 824 | 4 713 | 0,09408 |
| Formes minuscules, hors espaces et ponctuation | 81 105 | 3 512 | 23,094 | 8 805 | 4 712 | 0,10856 |
| Formes minuscules, tokens alphabétiques | 74 192 | 3 494 | 21,234 | 8 397 | 4 424 | 0,11318 |
| Lemmes, mêmes tokens alphabétiques | 74 192 | 3 494 | 21,234 | 5 937 | 2 790 | 0,08002 |

`tokens_bruts_spacy` vaut ici 94 716, soit les 93 795 tokens hors espaces et 921 tokens pour lesquels `is_space` vaut vrai. En retirant la ponctuation, on retire 12 690 tokens et le nombre de phrases retenues reste le même. Le passage au filtre alphabétique écarte encore 6 913 tokens et 18 segments qui ne contiennent aucun token alphabétique. Le `sentencizer` détermine les frontières en amont de ces filtres.

| Champ lexical | Formes | Lemmes | Écart |
|---|---:|---:|---:|
| Genre et anthropologie | 1 033 | 1 825 | +792 |
| Droit et institutions | 340 | 412 | +72 |
| Mœurs et famille | 627 | 767 | +140 |
| Travail et éducation | 235 | 405 | +170 |
| Féminisme et idéologies | 313 | 385 | +72 |

Les cinq gains dépendent des listes de cibles et des lemmes attribués. Le lemme *lettre* réunit ici « gens de lettres » et « cette lettre » dans un passage sur un envoi. La lecture des deux passages permet de discuter leur rattachement au champ du travail et de l’éducation. Dans « J’écris des articles politiques et je vote aux élections », le passage à « nous votons » permet de retrouver l’infinitif *voter*. Pour l’occurrence après *je*, le modèle affiche la catégorie `VERB` et le lemme `vote`. Le compteur ajoute donc une occurrence à `vote`, alors que l’analyse grammaticale conduit à `voter`. Pour l’énonciation, les 75 unités comptées sous `m` sont des `m'` dans cette exécution. La graphie `M.` conserve son point et a un décompte distinct.

## Bibliothèque et références

| Ressource | Place dans la version révisée |
|---|---|
| [Fonctions de mesure](../src/tal_toolkit/metriques_globales.py) | Dans le cahier, `filtrer` sélectionne les tokens, `compter_formes_et_lemmes` compte les deux représentations et `mesurer` calcule les indicateurs. La fonction de bibliothèque `comparer_annonces` rapproche une mesure d’une valeur déclarée. |
| [Analyse des fréquences](../src/tal_toolkit/analyse_pt02.py) | Le cahier calcule le STTR avec `ttr_par_bloc` et appelle `analyser_lexique_pt02` pour relever les marques de voix, les locutions et les mentions. `CHAMPS_LEXICAUX` et `PERSONNES` rendent consultables les choix de vocabulaire. |
| [Entrées et sorties du PT](../src/tal_toolkit/atelier.py) | Même circuit. `preparer_atelier` ouvre le corpus nettoyé et fournit la fonction de sauvegarde. `charger_modele_francais` charge le modèle avec la segmentation en phrases utilisée dans l’atelier. |
| Manning, Raghavan et Schütze (2008), chapitre 2, et Bird, Klein et Loper (2009), chapitre 3 | Les deux lectures de la version précédente restent associées à la tokenisation et à la normalisation. [Manning et al.](https://www.cambridge.org/highereducation/books/introduction-to-information-retrieval/669D108D20F556C5C30957D63B5AB65C/the-term-vocabulary-and-postings-lists/ED26D3C6F7EBDC3E0FB53B160874AB72) · [Bird et al.](https://www.nltk.org/book/ch03.html) |
| Evert (2009), « Corpora and collocations » | Lecture conservée pour la transition vers le cahier sur les cooccurrences. Le chapitre publié est distingué du manuscrit étendu de 2007 déjà proposé. [Chapitre publié](https://doi.org/10.1515/9783110213881.2.1212) · [Manuscrit](https://stephanie-evert.de/PUB/Evert2007HSK_extended_manuscript.pdf) |
| Documentation spaCy | Deux accès directs ajoutés pour interpréter `is_space`, `is_punct`, `is_alpha`, `lemma_` et identifier le modèle français. [Attributs du token](https://spacy.io/api/token) · [Modèles français](https://spacy.io/models/fr) |
| Matériaux du projet | Le rapport chiffré, son [tableau d’annonces](../data/annonces_globales_gemini.json), la [conversation Gemini](https://share.gemini.google/43HURKzcfoet) et la [matrice du PT](matrice_pretraitements_gemini.md) restent les sources des affirmations à vérifier et des protocoles proposés. |
