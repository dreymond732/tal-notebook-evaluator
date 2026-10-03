# Lecture des consignes — R1, TD1 et TD1B

Cette note du 3 octobre 2026 vous aide à repérer ce que les sujets demandent, où trouver les explications et quelles hésitations subsistent. Elle ne contient ni réponses aux exercices ni résultats attendus de spaCy.

## Ce qui a été lu

La lecture porte sur les versions présentes dans cette copie de travail, sans comparaison avec d'anciennes versions :

- `Notebooks TD/S3/README.md`, en entier ;
- `R1_S3_doc_spacy.ipynb` : les 26 cellules, indices 0 à 25 ;
- `TD1_S3_fondations_spacy.ipynb` : les 40 cellules, indices 0 à 39 ;
- `TD1B_S3_entites_similarite_regles.ipynb` : les 32 cellules, indices 0 à 31.

Les indices commencent à zéro et servent seulement à retrouver les passages dans cette note. Les textes des cellules Markdown, le code fourni et ses commentaires, ainsi que les instructions de restitution ont été lus. Les commentaires HTML destinés au tuteur ont été distingués des consignes visibles : ils ne constituent pas un cours à votre disposition.

Cela représente **98 cellules lues**. Après une modification signalée de l'introduction de R1, sa cellule 1 a été relue : elle précise désormais elle aussi que R2 répond à un autre besoin et ne suppose pas d'avoir refait R1.

`AGENTS.md` et la fiche du rôle `TAL-Étudiant-Modèle` ont été lus pour délimiter cette lecture. Aucun correcteur, test, corrigé existant, document de révision, fichier d'infrastructure ou autre ressource du dépôt n'a été consulté. Les liens externes et les ressources téléchargées par les notebooks n'ont pas été ouverts.

Les fichiers ont été ouverts comme des documents JSON pour en lire les cellules. Aucune cellule de notebook n'a été exécutée, aucun exercice résolu, aucune identité remplie et aucune copie soumise. Il n'y a donc aucune vérification des installations, annotations, scores, liens de dépôt ou retours automatiques réels.

## Vous situer dans le parcours

R1 est une remédiation facultative après TD1, annoncée pour environ 25 minutes. Son utilité est précise : reprendre la création d'un `Doc`, le parcours des tokens, la lecture des attributs et la construction de listes filtrées. Si vous maîtrisez déjà ces opérations, l'introduction vous invite à poursuivre sans refaire R1. Vous ne devez donc pas comprendre R1 comme une dixième séance obligatoire ni comme un prérequis imposé à R2. Le README précise explicitement que R2 poursuit un autre objectif, les fonctions et les fréquences, et ne suppose pas d'avoir refait R1.

TD1 est la découverte accompagnée ; Q6 demande un réinvestissement autonome. TD1B poursuit la découverte après TD1 et avant TD2. Son introduction annonce des exercices sans autocorrection et un dépôt sans note. Le README indique que les activités ajoutées dans TD1B n'ajoutent pas de questions aux contrôles associés à TD1 et TD2.

## R1 : ce que vous devez préparer

Les quatre questions utilisent la même phrase fournie dans « Chargement et données » (cellules 5–6). Les exemples utilisent d'autres textes et d'autres variables. Les rappels sont séparés des exemples, des essais et des questions. Les lignes d'affichage à décommenter et les noms des listes attendues sont annoncés avant les exercices.

| Question et cellules | Donnée et tâche comprises | Production demandée | Où retrouver les notions |
|---|---|---|---|
| Q1, 9–10 | Sur `texte`, construire le document et compter ses tokens, ponctuation comprise. | `doc` et affichage du nombre avec le libellé fourni ; explication personnelle de l'unité comptée, à voix basse ou en commentaire. | Rappel et exemple 7–8 : chaîne, `nlp()`, `Doc`, token et `len()`. TD1 3, 7–10 présente aussi le document et ses annotations. |
| Q2, 15–16 | Parcourir le `doc` de Q1 et relever tous ses tokens, dans l'ordre, sans retirer ponctuation ni répétitions. | Liste `annotations`, chaque élément comprenant forme, lemme et catégorie, dans cet ordre ; affichage complet ; observation si une annotation surprend. | Rappel 11 et exemple 12 : attributs, triple, tuple, liste et `append()`. L'essai 13–14 demande d'identifier ces informations sur un autre texte. |
| Q3, 19–20 | Sélectionner dans le même document les tokens dont la catégorie prédite vaut `NOUN`. | Liste `noms` de lemmes, dans l'ordre et avec les répétitions ; affichage fourni. | Rappel 17 et exemple 18 : condition, comparaison et ajout à l'intérieur de la condition. Q2 permet de contrôler la sélection. |
| Q4, 21–22 | Réutiliser la sélection avec la catégorie `VERB`. | Liste `verbes` de lemmes et affichage ; désaccord linguistique éventuel en commentaire, sans modifier les prédictions. | Q3 et rappel 17 ; Q4 explique explicitement qu'une liste vide peut être valide. |

Les vérifications personnelles sont concrètes : relier le nombre de Q1 à la longueur de Q2, vérifier les trois informations d'un triple, puis confronter les sélections aux catégories déjà affichées. Elles donnent un moyen de relire votre construction sans révéler les annotations attendues. Le bilan 23 vérifie les mêmes compétences. L'introduction annonce quatre points techniques et précise que la qualité des observations linguistiques n'est pas notée par ce retour. Aucune relecture individuelle n'est promise.

## TD1 : ce que chaque question demande

`texte` et `doc` sont préparés en cellules 7–8 ; les exemples portent sur d'autres documents. Les cellules 14–15 expliquent comment conserver les résultats et activer les affichages JSON fournis. Les acquis Python sont déclarés dans l'introduction ; leur apprentissage antérieur n'a pas été vérifié dans cette lecture.

| Question et cellules | Donnée et tâche comprises | Production demandée | Où retrouver les notions |
|---|---|---|---|
| Q1, 16–17 | Prédire deux lemmes, lire les tokens de `doc` sauf ponctuation, vérifier leurs positions, puis comparer séparément cinq entrées d'une référence manuelle. | Prédictions et commentaires ; `resultat_q1` avec une liste de dictionnaires à six champs sous `annotations`, calculée sur `doc`. La comparaison manuelle ne remplace pas cette liste. | 3, 9–13 : document, annotations, indice en caractères et tranches ; 14–15 : dictionnaire et affichage. La référence est désignée par `exemples["annotation_manuelle"]` ; son contenu n'a pas été ouvert. |
| Q2, 20–21 | Relever les phrases de `doc` et leurs nombres de tokens ; recompter une phrase ; essayer séparément une abréviation et une citation interrogative ; indiquer une frontière à vérifier dans une lecture de Faguet. | `resultat_q2` contenant les phrases de `doc` dans leur ordre, avec texte et nombre de tokens ; essais et explications dans la même cellule. | 18–19 : `Span`, `doc.sents`, texte et bornes des phrases, exemple d'abréviation. |
| Q3, 24–25 | Prédire puis comparer trois sélections sur `doc` : noms, verbes, et catégories demandées hors mots usuels ; justifier l'intérêt et la perte d'information d'un filtre. | Trois listes de lemmes sous les clés annoncées de `resultat_q3`, avec ordre et répétitions ; prédictions et interprétation. | 22–23 : filtre, `is_stop`, convention locale des « mots pleins » et exemple de sélection. |
| Q4, 28–29 | Afficher la première phrase de `doc`, examiner un verbe et un mot qui lui est relié, confronter figure et attributs, puis expliquer un risque d'attribution d'une citation. | Figure et `resultat_q4` avec les deux formes, leurs positions, la relation et l'interprétation. | 26–27 : dépendance, tête, racine et displaCy ; 11–13 : positions ; 28 : accès à la première phrase et possibilité d'une citation inventée explicitement signalée. |
| Q5, 32–33 | Comparer trois comptages sur le seul `texte_td0`, dans un nouveau document ; expliquer deux différences précises. | `resultat_q5` : trois entiers et une interprétation avec formes citées. La comparaison à l'ancien export TD0 est facultative s'il manque. | 30–31 : `split()`, tokenisation, `is_punct`, `is_space` et visualisation des limites. Le texte nécessaire est fourni en 8. |
| Q6, 34–35 | Choisir un extrait de 2 à 4 phrases et d'au moins cinq tokens, l'analyser séparément, conserver les cinq premiers tokens, les listes complètes de noms et verbes, et formuler une question de corpus. | `resultat_q6` avec les sept clés annoncées ; cinq annotations avec positions locales à l'extrait ; vérification manuelle et limite en commentaire. | Q1 : annotations et positions ; Q2 : phrases ; Q3 : sélections ; 34 : conservation de la ponctuation parmi les cinq premiers tokens, bornes locales et fin exclue. |

Q6 ne promet pas une correction du fond linguistique. Dès le début de la question, le sujet précise que le retour porte sur la structure et certains repères textuels, sans juger la justesse des lemmes ou catégories ni la pertinence de la question ou de l'interprétation. La vérification manuelle reste votre tâche. Le bilan 36 décrit le score comme technique et provisoire et n'annonce aucune relecture individuelle systématique. Vous pouvez donc distinguer un retour technique réussi d'une analyse linguistique justifiée.

La cellule 37 fournit l'export après les six exercices. Le bilan explique comment conserver cet export et le notebook avec ses sorties et sa figure, et précise que TD2 reste faisable sans l'export.

## TD1B : ce que chaque question demande

Le modèle `md`, différent de celui de TD1, est présenté avant son chargement (3–6). Chaque notion nouvelle dispose d'un cours et d'un exemple avant la question correspondante. Les cellules « Observations » servent aux prédictions et aux interprétations ; les cellules de réponse servent au code et à ses sorties.

| Question et cellules | Donnée et tâche comprises | Production demandée | Où retrouver les notions |
|---|---|---|---|
| Q1, 9–11 | Sur le texte fourni à propos d'Apple, relever d'abord les informations à la lecture, puis comparer ce repérage aux entités détectées. | Observations avant/après et liste `entites_q1` de couples forme/label conservant toutes les prédictions dans leur ordre. | 7–8 : mention, délimitation, labels disponibles, `Span`, `doc.ents`, forme et label. Le cours distingue une erreur d'une catégorie non proposée. |
| Q2, 14–16 | Sur le texte fourni puis un texte personnel, comparer les entités complètes à une extraction limitée à `PER` et `ORG`. | Sorties complètes et filtrées, liste `personnes_organisations_q2`, texte personnel affiché, justification et discussion d'une limite. | 12–13 : extraction, faux positif, absence, distinction entre label d'entité et POS, exemple de filtre ; TD1 Q3 pour l'appartenance à plusieurs catégories. |
| Q3, 19–21 | Prédire la proximité de deux couples de mots ; calculer les scores et vérifier les vecteurs ; comparer les phrases fournies, puis une phrase à une variante choisie. | Scores accompagnés des textes, prédictions, effet de la modification sur le sens et interprétation appuyée sur les sorties. | 17–18 : vecteurs, moyenne pour les documents, `.similarity()`, `has_vector`, avertissements et limites du score. Aucun ordre chiffré prédéfini n'est imposé. |
| Q4, 25–27 | Comparer le même texte avant/après une règle dans un pipeline distinct ; ajouter trois règles choisies ; éprouver les quatre expressions sur au moins cinq textes incluant une variante et une ambiguïté. | Code, textes et sorties ; tableau des attentes humaines et des résultats avec/sans règles ; bilan de trois ou quatre phrases. | 22–24 : dictionnaires de règles, `add_patterns()`, `EntityRuler`, placement avant `ner`, pipeline rechargeable, labels personnalisés et limites de la correspondance exacte. |

Le bilan 28–29 demande en plus l'apport et une erreur possible de chacune des trois méthodes, ainsi qu'un moyen de la repérer. Les critères reprennent les travaux attendus. Le dépôt conserve les observations sans correction ni note automatiques ; aucun export JSON n'est demandé, et aucune relecture individuelle n'est garantie.

## Hésitations à garder visibles

Aucun blocage de compréhension empêchant de commencer les activités n'a été repéré dans le périmètre lu. Les réserves suivantes restent utiles :

1. L'espace d'essai de R1, cellule 14, emploie « trace évaluée ». Le contexte permet de comprendre qu'il s'agit de la réponse affichée dans la cellule dédiée, mais ce terme est moins direct que les autres consignes.
2. TD1 Q6 distingue les 2 à 4 phrases de l'extrait choisi et le nombre de phrases proposé par spaCy, mais n'explique pas explicitement quoi faire si ce dernier diffère du découpage que vous aviez prévu. Le cours de Q2 rappelle que ces frontières sont des prédictions ; le sujet permet de les discuter sans les remplacer. Cette situation mérite néanmoins d'être signalée si elle se présente.
3. TD1 Q1 dépend du contenu d'une référence manuelle téléchargée. La consigne décrit où la trouver et ce qu'elle contient, mais cette lecture limitée ne permet pas de vérifier ses cinq entrées, son accessibilité ou son alignement avec spaCy. Il s'agit d'une limite de vérification, pas d'un défaut constaté de la ressource.

Le commentaire technique « URL injectée lors du déploiement », présent dans les trois cellules finales, n'appelle aucune action de votre part. Les instructions visibles de restitution sont compréhensibles ; la validité du lien n'a pas été vérifiée.

Les cours, exemples et exercices sont identifiables sans utiliser les instructions cachées du tuteur. Aucun résultat automatique n'est présenté comme une preuve suffisante de justesse linguistique. Cette note établit seulement la compréhension des demandes : elle ne valide ni leur exécution, ni leur durée réelle, ni le fonctionnement de l'évaluation.
