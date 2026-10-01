# Révisions S3 R0, R1 et R2 — contrat d’évaluation v2

## Mission et décision

Branche `code/s3-revisions-evaluation-v2`, référence source `06cbd2a`. **CHANGEMENT_DE_CONTRAT** : fiabilisation conjointe des supports et des évaluateurs, autorisée par l’enseignant le 1er octobre 2026. L’enseignant demande de refuser les anciennes versions par le message exact **« mauvaise version du notebook »**, sans correction et sans migration. La matrice et le contrat ci-dessous ont été validés par l’orchestrateur avant conception. Aucune suppression, réduction substantielle, nouvelle bibliothèque ou extension de programme n’est proposée.

Sources pédagogiques lues : `Notebooks TD/S3/R0_S3_python_texte.ipynb`, `R1_S3_doc_spacy.ipynb`, `R2_S3_frequences_reutilisables.ipynb`, `TD1_S3_fondations_spacy.ipynb`, ainsi que les périmètres du tuteur associés. R0 prépare TD1 ; R1 et R2 consolident TD1 avant TD2. Les données, quatre questions par ressource et durées indicatives (25, 25, 30 minutes) sont conservées. Les traces deviennent plus précises ; ce travail de mise en forme reste guidé par des consignes et appels d’affichage commentés, sans fournir les solutions.

## Matrice de couverture source → cible, préalable à la conception

Toutes les activités ci-dessous restent obligatoires. Leur résolution demeure étudiante ; ni calcul ni annotation de référence ne sont fournis dans le sujet. Les listes d’annotations et traces remplacent les annonces non probantes (« terminé ») sans enlever l’observation.

| Source | Objectifs, notions et activité | Données et production cible | Charge, autonomie et statut |
|---|---|---|---|
| R0 Q1 | Écrire `compter_mots(texte)`, `split`, `len`, paramètre et retour ; tester | Texte original conservé ; trois appels : original, chaîne vide, `Un essai` | Fonction autonome ; deux petits tests explicités ; RENFORCÉ |
| R0 Q2 | Normaliser en minuscules puis segmenter ; construire une liste | Texte original ; `mots_normalises` complet, répétitions et ponctuation conservées | Même manipulation ; CONSERVÉ |
| R0 Q3 | Écrire `frequences(texte)`, parcourir et incrémenter un dictionnaire avec `.get()` | Texte original et `Mot mot autre` ; deux dictionnaires lowercase | Fonction autonome réutilisable ; test paramètre explicité ; RENFORCÉ |
| R0 Q4 | Identifier et expliquer une limite du comptage lexical | Commentaire personnel conservé ; `frequences('Python Python.')` et courte phrase de limite | Appui observable ajouté au regard critique ; explication relue humainement ; RENFORCÉ |
| R1 préparation | Charger spaCy et le modèle français | Texte original ; mêmes versions `spacy==3.8.7`, `fr_core_news_sm==3.8.0` ; installation fournie harmonisée TD1 | Préparation seulement, pas une nouvelle compétence ; CONSERVÉ |
| R1 Q1 | Construire `doc = nlp(texte)` et observer sa longueur | Nombre complet de tokens, ponctuation comprise | Même calcul autonome ; CONSERVÉ |
| R1 Q2 | Parcourir Doc ; lire forme, lemme et POS de chaque token | Liste ordonnée de triples ; affichage de tous les tokens conservé via cette liste | `for` et observation conservés ; trace vérifiable ; RENFORCÉ |
| R1 Q3 | Sélectionner NOUN et produire les lemmes | Liste ordonnée des lemmes de noms, répétitions conservées | Sélection autonome ; CONSERVÉ |
| R1 Q4 | Sélectionner VERB et produire les lemmes | Liste ordonnée des lemmes de verbes, répétitions conservées | Sélection autonome ; CONSERVÉ |
| R2 Q1 | Fonction `frequences_lemmas(texte, stopwords=None)`, `Counter`, NOUN et lemmes | Dictionnaire des fréquences nominales du texte original ; `stopwords` réservé à Q3 | Construction autonome ; portée clarifiée ; CONSERVÉ |
| R2 Q2 | Vérifier la sélection des noms et la lemmatisation | Liste ordonnée des triples forme/lemme/POS de tous les tokens ; confrontation au résultat Q1 | Preuve positive et négative du filtre ; RENFORCÉ |
| R2 Q3 | Réviser la fonction, utiliser `token.is_stop` et exclusions paramétrées | Deux résultats de la fonction révisée : sans exclusion personnelle puis avec `['texte']` | Fonction autonome, effet mesurable de l’exclusion ; RENFORCÉ |
| R2 Q4 | Comparer classements `most_common` avant/après filtrage | Deux classements complets ; courte observation des changements | Même comparaison autonome, pas de classement tronqué ambigu ; RENFORCÉ |
| Tutoriels R0–R2 | Guidance formative adaptée au S3 | Instructions métadonnées + première cellule ; périmètres ajustés aux traces et dépendances | Même politique TD, sans réponse complète ; CONSERVÉ |
| Identification et dépôt | Routage du bon correcteur, identité et retour | Identité complète ; métadonnées v2 ; cellule HTML injectée à la distribution | Infrastructure fournie ; RENFORCÉ |

## Contrat commun des notebooks

- `metadata.tal.id` et `metadata.tal.evaluator` : respectivement `td-r0-s3`, `td-r1-s3`, `td-r2-s3` ; `metadata.tal.version` entier **2**. Il s’agit de la version du contrat évaluateur, distincte de celle de la politique du tuteur.
- Chaque question possède exactement une cellule de code `metadata.tal = {"question": "Qn", "role": "answer"}`. Les consignes, préparations, données et exemples ne sont pas des réponses. Les déplacements de cellules ne changent pas leur identification.
- Une cellule `metadata.tal = {"question": "identity", "role": "identification"}` comporte les affectations littérales `nom`, `prenom`, `classe`, `numero_etudiant`, initialisées à des chaînes vides. L’identité manquante/incomplète produit une erreur explicite et non une soumission `NON_RENSEIGNE`.
- Les anciennes versions, les métadonnées de version absentes, erronées ou incohérentes sont refusées avant attribution d’un score, y compris sur les routes directes. Le parcours automatique ne doit pas contourner ce refus en retrouvant un titre ancien. Aucun ancien contenu n’est réécrit ou migré.
- Les sources Git ne contiennent pas la cellule de dépôt ni l’adresse serveur privée. Le générateur produit dans `dist/` une cellule HTML finale depuis la configuration d’environnement ; les trois copies v2 doivent être régénérées et vérifiées après modification. **Les copies actuelles v1 de `dist/` ne doivent pas être redistribuées.**
- Affichages : un marqueur `Résultat Qn :` suivi d’un littéral Python lisible (entier, liste, dictionnaire, chaînes et couples), enregistré dans la sortie de la cellule concernée. Aucune nouvelle bibliothèque de sérialisation. Les dictionnaires et `Counter` sont affichés au moyen de `dict(...)` lorsque demandé.
- Le correcteur recherche des opérations dans l’AST, accepte les espaces et variantes structurelles valides, puis confronte les sorties enregistrées aux références. Il n’exécute jamais le notebook. Un marqueur seul, des sorties dans une autre cellule, un exemple fourni, une sortie non analysable ou une erreur d’exécution dans la réponse ne valent pas réussite.
- Les fonctions définies dans une question antérieure sont des dépendances autorisées : R0 Q4 → Q3, R2 Q2 → Q1, R2 Q3 révise Q1, R2 Q4 → Q3. Cette portée ne permet pas de créditer à Qn un résultat enregistré dans une autre cellule. La version révisée pertinente de la fonction prévaut.

## R0 — données et preuves exactes

Texte conservé : `Python est utile. Python sert au TAL et le TAL sert à analyser des textes.`

| Question | Trace attendue après `Résultat Qn :` | Obligations et critères |
|---|---|---|
| Q1 | `{'principal': 15, 'vide': 0, 'essai': 2}` | Valeurs produites par `compter_mots(texte)`, `compter_mots('')`, `compter_mots('Un essai')`. Fonction paramétrée, `split()`, `len()`, retour effectif. |
| Q2 | `['python', 'est', 'utile.', 'python', 'sert', 'au', 'tal', 'et', 'le', 'tal', 'sert', 'à', 'analyser', 'des', 'textes.']` | Liste `mots_normalises` calculée sur `texte` par minuscules et segmentation ; aucun nettoyage supplémentaire de ponctuation. |
| Q3 | `{'principal': {'python': 2, 'est': 1, 'utile.': 1, 'sert': 2, 'au': 1, 'tal': 2, 'et': 1, 'le': 1, 'à': 1, 'analyser': 1, 'des': 1, 'textes.': 1}, 'essai': {'mot': 2, 'autre': 1}}` | Deux appels de `frequences` sur le texte original puis `Mot mot autre`. Minuscules, split, boucle, accumulation avec `.get()`, retour du dictionnaire. L’ordre des clés n’est pas un critère. |
| Q4 | `{'comptes': {'python': 1, 'python.': 1}, 'limite': <courte phrase personnelle>}` | Calcul par réemploi de `frequences('Python Python.')` ; commentaire explicatif dans la cellule conservé. Le score technique porte sur le calcul et sa trace, jamais sur des mots-clés ou la longueur de l’explication. L’interprétation doit rester visible dans le retour pour relecture. |

## R1 — annotations et sélection

Texte conservé : `Les traducteurs analysent rapidement les nouveaux documents.`

- Q1 : `doc = nlp(texte)` puis `Résultat Q1 : 8` (ponctuation comprise).
- Q2 : `annotations`, liste ordonnée de triples `(token.text, token.lemma_, token.pos_)` construite par parcours de `doc`, puis `print('Résultat Q2 :', annotations)`. Les couples/listes ou tuples de taille trois ont la même signification ; les triples contiennent tous les tokens, ponctuation comprise.
- Q3 : `noms`, liste des lemmes de tokens de POS `NOUN`, ordre et répétitions conservés ; sortie `Résultat Q3 : ['traducteur', 'document']`.
- Q4 : `verbes`, liste des lemmes de tokens de POS `VERB`, ordre et répétitions conservés ; sortie `Résultat Q4 : []`. La référence épinglée classe ici `analysent` comme `ADV`, avec le lemme `analyser` : ne pas corriger manuellement le modèle pour satisfaire une intuition grammaticale. Demander une courte observation non notée de cette divergence ; une liste vide est un résultat possible et valide.

L’orchestrateur a généré les annotations avec du code enseignant indépendant et confirmé les valeurs ci-dessus le 1er octobre 2026. L’architecte conserve une référence canonique indépendante produite avec spaCy 3.8.7 + fr_core_news_sm 3.8.0 sur le texte exact, au moyen de code enseignant séparé. Cette référence, son protocole et sa provenance sont requis avant acceptation ; ne pas substituer une simple auto-cohérence des déclarations étudiantes. Les annotations du modèle constituent une référence technique reproductible, pas une vérité linguistique universelle.

## R2 — fonction réutilisable et effets des filtres

Texte conservé : `Les corpus contiennent des textes. Les textes contiennent des termes et des répétitions.`

- Q1 : écrire `frequences_lemmas(texte, stopwords=None)`, sélectionner `NOUN`, compter les lemmes avec `Counter`, retourner le `Counter`. À cette étape le paramètre optionnel est réservé à Q3 ; on n’utilise pas encore `is_stop`. Sortie dict sur le texte original : `{'texte': 2, 'terme': 1, 'répétition': 1}`. La référence épinglée classe ici `corpus` comme `PRON` : le filtre NOUN l’exclut. Le sujet demande de suivre les annotations observées, d’en noter les limites sans les corriger manuellement.
- Q2 : produire `annotations`, liste ordonnée des triples forme/lemme/POS de **tous** les tokens du texte. Cette trace permet de contrôler la présence de tous les noms, leurs lemmes et l’absence des non-noms dans Q1. Aucune auto-déclaration booléenne « tous sont des noms » n’est probante.
- Q3 : réécrire `frequences_lemmas` pour ne conserver que les NOUN non `token.is_stop` dont le lemme n’appartient pas aux exclusions personnelles. `None` signifie aucune exclusion personnelle. Les exclusions portent explicitement sur les **lemmes**, pas les formes fléchies. Produire `{'sans_exclusions': dict(frequences_lemmas(texte)), 'avec_exclusions': dict(frequences_lemmas(texte, ['texte']))}`. Le filtre personnel doit retirer les deux occurrences du lemme `texte` ; les autres comptes restent identiques. L’inspection AST doit vérifier l’usage effectif du paramètre dans le filtrage, pas sa simple présence dans la signature.
- Q4 : appeler la fonction révisée de Q3 puis `.most_common()` sans limite pour les cas sans et avec `['texte']`. Trace `{'avant': <classement sans exclusion personnelle>, 'apres': <classement avec exclusion personnelle>}`. Les fréquences décroissent ; les ex æquo peuvent figurer dans n’importe quel ordre (même multiensemble attendu). Une courte observation des changements est demandée, sans notation automatique de sa qualité.

La référence canonique indépendante doit inclure forme, lemme, POS et `is_stop` pour le texte original. Sur un texte où aucun nom retenu n’est un stopword spaCy, le filtre `is_stop` peut n’enlever aucun élément : le notebook le précise et ne fabrique pas d’effet. Le correcteur distingue (a) preuve syntaxique de l’application de ce filtre et (b) effet quantifié réellement observable des exclusions personnelles. Cette ressource ne prétend pas démontrer tous les cas possibles de filtrage.

## Barème, interprétation et limites

Barème formatif conservé : quatre questions de 1 point, total **4 points techniques**. Un point exige une trace conforme et des éléments de code correspondant à l’opération demandée ; aucun point sur la seule présence d’un marqueur. Les réponses manquantes ou invalides reçoivent un retour localisé. L’explication R0 Q4 et l’observation R2 Q4 restent demandées et visibles ; le score ne mesure pas leur qualité. Ne pas présenter 4/4 comme une validation de l’ensemble du raisonnement linguistique.

La combinaison code source + sorties stockées réduit les faux positifs connus ; elle ne prouve ni l’exécution réelle, ni l’authenticité, ni la généralité d’une fonction pour toute entrée. Les étudiants doivent pouvoir expliquer et reproduire leur démarche. Une autre solution correcte refusée par l’analyse statique doit pouvoir être signalée à l’enseignant ; ne jamais exécuter sa copie pour tenter de la valider.

## Critères d’acceptation

1. Sujets v2, identité et Q1–Q4 reconnus ; données, objectifs et tuteurs conservés ; sources sans dépôt, copies distribuées avec cellule HTML finale.
2. Ancienne version et version absente refusées avec `mauvaise version du notebook`, sans correction, persistance de note ni migration automatique.
3. Réponses de référence exactes acceptées ; sorties fausses avec marqueurs, réponses vides avec exemples fournis, erreurs de calcul, répétitions oubliées, mauvais POS, faux lemmes et exclusions inefficaces refusés.
4. Espaces syntaxiques, ordre des cellules, ordre des clés de dictionnaires et ordre des ex æquo ne provoquent pas de faux échec ; métadonnées de réponses dupliquées/incohérentes rejetées explicitement.
5. Absence d’exécution du code étudiant attestée ; références spaCy générées par code enseignant séparé, versions attestées.
6. Revue pédagogique indépendante de cette matrice, revue technique, gouvernance et intégration avant décision de fusion du mainteneur.
