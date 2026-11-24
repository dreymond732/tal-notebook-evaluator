# Notebook 03 — correspondance des tâches et repères pour le TD

Cette fiche compare le [cahier révisé](../notebooks/03_mesurer_les_cooccurrences_par_phrase_et_par_fenetre.ipynb) à la [version du 03 distribuée avant la reprise](https://github.com/dreymond732/tal-notebook-evaluator/blob/fcf8bdf152db52c26ec17f1ffc81618a3d9458a0/PT-LLMvsPy/notebooks/03_relations_lexicales.ipynb). Les chiffres ci-dessous proviennent d’une exécution sur le texte nettoyé du 01 avec spaCy 3.8.18 et `fr_core_news_sm` 3.8.0. Dans le cahier distribué, les étudiants les calculent eux-mêmes.

## Du découpage précédent au travail demandé

| Dans le 03 précédent | Dans le 03 révisé | Production attendue en TD |
|---|---|---|
| Reprise du 02 à l’ouverture. Segmentation du livre introduite au §2, deux filtres. | §0. Préparer les phrases et leurs représentations. | Comparer les formes et les lemmes du même document. Retrouver la place d’une virgule, d’un chiffre et d’une forme fléchie. Expliquer pourquoi le filtre alphabétique écarte davantage d’unités que le retrait de la ponctuation. |
| §1, classer cinq phrases d’essai, puis §2, vérifier les familles d’annonces de Studio. La mesure M4 ouvrait le §3. | §1. Mesurer la présence commune dans une phrase. | Prédire les effets d’une répétition sur un exemple personnel, confronter l’union des indices à la somme des couples de graphies, puis retrouver deux passages du livre. Garder les associations sur le mariage et le féminisme et les conventions de Studio et de M4. |
| Table de contingence introduite au §1, PMI en approfondissement après la lecture des passages au §5. | §2. Relier la table de présences, les marges et le PMI. | Reconstituer les quatre cases, vérifier leur somme et identifier le dénominateur d’une proportion ou d’un taux pour mille. Comprendre pourquoi une somme de couples ne peut alimenter cette table. Mettre le PMI en regard des effectifs. L’expérimentation supplémentaire reste facultative. |
| §3, fenêtres intra-phrase. Le franchissement des frontières était illustré sur un seul cas. | §3. Comparer les rayons ±5 et ±10 en phrase et en flux continu. | Numéroter les tokens d’une suite personnelle. Distinguer une position de pivot couverte de toutes les paires qu’elle forme. Sur le livre, faire varier un facteur à la fois et interpréter un écart ou une égalité. |
| §4, suites annoncées et affichage des cinq premières. §5, interprétation et transfert. | §4. Classer les bigrammes et trigrammes, puis interpréter et préparer le 04. | Prédire si deux mots séparés par une virgule deviennent consécutifs. Examiner les quinze premières suites d’une vue et vérifier les annonces sur des expressions précises. Justifier la conclusion par des passages. Un binôme peut aussi tester son propre couple de lemmes. |

## Trois unités à distinguer au tableau

Sur la suite **droit – femme – droit**, le lemme *femme* est le pivot. Dans cette seule phrase, l’union vaut **1**. Au rayon 1, **1 pivot est couvert**. Il forme **2 paires de positions**, l’une à gauche, l’autre à droite. En revanche, la somme des couples **d’expressions distinctes présentes** ne vaut que **1** avec les deux seules cibles *femme* et *droit*. Pour la faire varier, on peut autoriser plusieurs graphies ou plusieurs associés.

Les fenêtres s’arrêtent aux frontières de phrases en mode intra-phrase. Garder une virgule consomme une position dans la fenêtre. Elle peut éloigner deux mots au-delà du rayon choisi ou les laisser à portée. Pour un n-gramme, la contiguïté est stricte : retirer cette virgule peut créer un bigramme de mots qui n’étaient pas adjacents dans le texte.

## Repères chiffrés sur Faguet

Le 03 retient les **3 416** segments contenant au moins un token alphabétique, parmi les **3 433** segments de spaCy. Cette population reste fixe pour comparer les vues. Elle contient **94 618 tokens hors espaces**, **81 059 sans ponctuation** et **74 090 alphabétiques**. Le 02 comptait 94 654 tokens hors espaces sur l’ensemble des segments. Le choix des phrases explique les 36 tokens d’écart.

| Union de présences par phrase | Les deux | Pivot seul | Associé seul | Aucun | Pour 1 000 phrases | PMI, base 2 |
|---|---:|---:|---:|---:|---:|---:|
| Studio, graphies *femme(s)* et *homme(s)* | 199 | 512 | 131 | 2 574 | 58,26 | 1,535 |
| M4, lemmes *femme* et *droit* | 48 | 662 | 50 | 2 656 | 14,05 | 1,237 |

Studio annonce 208 phrases. Le protocole commun en retrouve 199, soit un écart de −9. La somme des couples de graphies vaut 223 sur **les mêmes 199 phrases**. M4 ne publie aucune valeur numérique à laquelle confronter les 48 phrases mesurées.

| Fenêtre sur les lemmes *femme* et *droit*, ponctuation retirée | Pivots couverts sur 955 | Paires de positions |
|---|---:|---:|
| Intra-phrase, ±5 | 24 | 25 |
| Intra-phrase, ±10 | 31 | 35 |
| Flux continu, ±5 | 25 | 26 |
| Flux continu, ±10 | 35 | 39 |

Dans le flux continu au rayon 10, conserver la ponctuation donne 34 pivots couverts et 38 paires. Pour les deux rayons intra-phrase, le retrait de la ponctuation laisse les effectifs du tableau identiques. Une différence de convention peut donc se vérifier sur une phrase personnelle même si elle ne change pas un total sur le livre.

En formes minuscules avec ponctuation, *union libre* fournit 22 bigrammes. *Divorce consentement mutuel* fournit zéro trigramme contigu. On peut retrouver *divorce* et *consentement mutuel* dans une même phrase et lire les mots qui les séparent.

**Pour discuter la portée du résultat.** Les phrases 20 et 3 387 ajoutent chacune une unité aux 199. Dans la première, une question sur l’égalité est suivie d’une réponse attribuée à Turgeon et d’une prise de position de Faguet. Dans la seconde, la négation dans « n’est pas tutoyée par lui » marque une asymétrie dans un propos cité. La coprésence ou un PMI élevé établit une proximité de surface dans l’unité choisie. Pour conclure à l’accord, à l’opposition, à la négation ou à l’ironie, il faut identifier qui parle et quels indices textuels étayent cette lecture.

## Ce que l’étudiant conserve et reprend au 04

Comme au 02, le cahier produit un seul fichier numéroté, `resultats_03_<numero>.json`. L’étudiant le télécharge depuis la session temporaire, ouvre le fichier pour y retrouver son commentaire, puis le range dans son dossier personnel `S3-PythonVsLLM`. Pour ouvrir le 04 dans une nouvelle session, il importe le TXT ou le ZIP du 01 et les JSON des 02 et 03. À la revue finale, il copie les trois JSON des 02 à 04 dans le dossier partagé.

Les 16 rubriques antérieures restent disponibles. Le 04 reprend l’annonce chiffrée et les passages de Studio sous `studio.principal`, puis la mesure indépendante de M4 sous `relation`. L’essai personnel facultatif figure sous `transfert`. Six rubriques documentent les nouveaux travaux :

| Rubriques ajoutées | Ce que l’étudiant peut retrouver |
|---|---|
| `unites`, `agregations` | Le nombre de phrases et de positions des six vues. Sur l’essai et sur Studio, l’union des phrases et la somme des couples d’expressions. |
| `statistiques_phrases`, `fenetres_continues` | Les quatre cases, les marges et le PMI. Les mesures en flux continu à rapprocher des fenêtres intra-phrase conservées sous `fenetres`. |
| `classements_ngrammes`, `observations` | Les quinze premiers bigrammes et trigrammes disponibles dans chaque vue, la prévision sur les phrases et les lectures personnelles du score et du classement. |

## Fonctions et références

| Référence | Ce qui évolue dans le 03 |
|---|---|
| [Outils de textométrie](../src/tal_toolkit/textometry.py) | L’ancienne bibliothèque comptait déjà les paires dans `bilan_fenetres` et les suites dans `frequences_ngrammes`. Les deux nouvelles entrées publiques rendent observables séparément le nombre de paires sur une suite, via `compter_paires_fenetre`, et les occurrences des suites avant classement, via `extraire_ngrammes` puis `frequences`. Les appels existants restent utilisables. |
| [Phrases et tokens](../src/tal_toolkit/linguistic.py) | `DocCache.analyser` et `tokeniser_phrases` existaient déjà. Le cahier construit ses vues sur le même document. Le filtre alphabétique porte sur la graphie initiale, y compris si l’on compte ensuite les lemmes. [Frontières des phrases dans spaCy](https://spacy.io/api/doc#sents) |
| Matériaux du projet | Le 03 renvoyait déjà au [rapport Studio, §4](../../app/static/PT_LLMvsPy_Analyse_Gemini_source_originale.md) et à la [conversation Gemini, M4](https://share.gemini.google/43HURKzcfoet). Ces deux sources précisent ce qui est annoncé et ce qui reste à mesurer. |
| Evert (2009), « Corpora and collocations » | Lecture déjà proposée en fin de 02, désormais reliée dans le 03 au choix du contexte de cooccurrence et de l’unité comptée. [Chapitre publié](https://doi.org/10.1515/9783110213881.2.1212) |
| Church et Hanks (1990), « Word Association Norms, Mutual Information, and Lexicography » | Lecture introduite dans le 03 pour discuter l’association lexicale et l’information mutuelle. Le calcul du PT utilise les présences par **phrase** et ses deux marges. [Article](https://aclanthology.org/J90-1003/) |
