# TD S1 — Revue pédagogique et distribution

## Mission et référence

Revue du 1er octobre 2026, sur le commit `b12b40f` : sept TD S1 actifs, TD1 à TD7. La demande de l’enseignant autorise leur renommage selon le contenu, la vérification et la complétion des métadonnées, ainsi qu’une cellule finale de restitution HTML dont l’URL est injectée au déploiement. Le contrôle final et le devoir maison ne sont pas des TD et ne sont pas renommés par cette opération.

Matrice relue et validée par l’orchestrateur avant l’intervention du Designer, le 1er octobre 2026. La revue indépendante de la réalisation reste requise.

Cette fiche établit la matrice avant modification des notebooks. Elle autorise une adaptation de forme et de distribution, sans modifier les activités, les données, les productions demandées ni leur niveau d’autonomie. Les réserves pédagogiques ci-dessous constituent des constats à traiter dans un chantier distinct, pas des suppressions implicites.

## Matrice source → cible

Le répertoire reste `Notebooks TD/S1/`. Tous les sujets portent actuellement le suffixe `python_texte`.

| Source | Nom cible | Objectifs et activités conservés | Productions obligatoires | Charge et autonomie | Statut |
|---|---|---|---|---|---|
| `TD1_S1_python_texte.ipynb` | `TD1_S1_variables_types.ipynb` | Q1 calcul du coût ; Q2 type numérique ; Q3 comparaisons et conjonction ; Q4 f-string ; Q5 conversion ; Q6 longueur et appartenance | Six affichages Q1–Q6, variables construites par l’étudiant ; données de traduction et phrase personnelle | Prise en main, six tâches courtes ; absence de durée détaillée ; rappel bref | CONSERVÉ |
| `TD2_S1_python_texte.ipynb` | `TD2_S1_chaines_sequences.ipynb` | Q1 nettoyage/source ; Q2 transformations et vérifications ; Q3 indices/tranches ; Q4 chaîne/liste ; Q5 découpage/reconstruction ; Q6 trois normalisations explicites ; Q7 limite linguistique du découpage | Sept affichages Q1–Q7 et sept compléments Q1b–Q7b ; prédictions, observations et justifications ; données intégralement identiques | Budget explicite de 120 min ; exemples distincts puis essais personnels ; aucune boucle | CONSERVÉ |
| `TD3_S1_python_texte.ipynb` | `TD3_S1_collections.ipynb` | Q1 ajouter/retirer ; Q2 tuple et justification ; Q3 lexique bilingue ; Q4 parcours clé–valeur ; Q5 vocabulaire distinct ; Q6 intersection/différence | Six affichages Q1–Q6, explication du tuple, lexique et vocabulaires fournis | Six tâches ; rappel comparatif des collections ; parcours à étayer (voir réserves) | CONSERVÉ |
| `TD4_S1_python_texte.ipynb` | `TD4_S1_boucles_conditions_comptages.ipynb` | Q1 transformation par boucle ; Q2 filtre longueur ; Q3 filtre lettre ; Q4 positions paires ; Q5 boucle bornée ; Q6 fréquences ; Q7 compréhension | Sept affichages Q1–Q7 sur les listes et textes fournis ; deux filtrages distincts maintenus | Sept tâches cumulatives ; autonomie croissante ; temps non ventilé | CONSERVÉ |
| `TD5_S1_python_texte.ipynb` | `TD5_S1_fonctions_reutilisation.ipynb` | Q1 longueur et tests ; Q2 normalisation ; Q3 comptage composé ; Q4 traduction d’un mot ; Q5 traduction d’une phrase ; Q6 résumé structuré | Six affichages Q1–Q6, fonctions et appels demandés ; lexique inchangé | Six tâches progressives de définition puis composition ; temps non ventilé | CONSERVÉ |
| `TD6_S1_python_texte.ipynb` | `TD6_S1_fichiers_csv.ipynb` | Q1 lecture UTF-8 ; Q2 lignes utiles ; Q3 couples structurés ; Q4 normalisation d’identité ; Q5 dédoublonnage des affiliations ; Q6 écriture/relecture CSV | Six affichages Q1–Q6, fichier initial et CSV de sortie ; préparation fournie maintenue | Pipeline cumulatif ; distinction code fourni/travail étudiant ; temps non ventilé | CONSERVÉ |
| `TD7_S1_python_texte.ipynb` | `TD7_S1_expressions_regulieres_pipeline.ipynb` | Q1 recherche ; Q2 nombres ; Q3 mots accentués/comparaison ; Q4 dates ; Q5 nettoyage ; Q6 pipeline ; Q7 limite méthodologique | Sept affichages Q1–Q7, fonctions composées et interprétations ; textes inchangés | Synthèse des acquis ; recherche, extraction puis remplacement ; temps non ventilé | CONSERVÉ |

Toutes les 45 questions principales et les sept traces complémentaires du TD2 sont conservées. Aucune activité obligatoire ne devient optionnelle. Les titres visibles actuels décrivent déjà les contenus : leur réécriture n’est pas nécessaire.

| Élément transversal | État source | Adaptation autorisée | Statut |
|---|---|---|---|
| Identification et réponse | Sept identifications et 45 réponses déjà balisées | Conserver leurs rôles et identifiants, leur source et leur ordre | CONSERVÉ |
| Instructions et ressources | Markdown non balisé ; deux cellules de préparation/import non balisées | Ajouter un rôle `prompt` et un identifiant unique aux Markdown, `infrastructure` au tuteur, `provided` aux cellules de préparation/import, sans les compter comme réponses | RENFORCÉ |
| Identifiants de cellules | Certains `cell.id` nbformat peuvent être absents | Ajouter des identifiants déterministes uniquement aux cellules qui en sont dépourvues ; préserver tous les identifiants existants | RENFORCÉ |
| Tuteur | Métadonnées de session et Colab, première cellule Markdown | Conserver le contenu des règles ; actualiser le chemin du notebook dans les fiches et métadonnées | CONSERVÉ |
| Restitution | Aucune cellule dédiée dans les sept sources | Ajouter une seule dernière cellule fournie, rôle `submission`, URL factice `__TAL_PUBLIC_URL__` ; substituer seulement dans les copies de `dist/` | RENFORCÉ |
| Bibliothèques | Aucune jusqu’au TD5 ; `pathlib` fourni au TD6, `csv` pour Q6 ; `re` au TD7 | `IPython.display` relève uniquement de la restitution fournie ; il ne devient pas un outil autorisé pour résoudre les exercices | CONSERVÉ |
| Routage | `td1-s1` à `td7-s1`, version 1 | Conserver ID, évaluateur, version et marqueurs Q ; seuls les chemins de ressources changent | CONSERVÉ |

## Constats vérifiables sur les sources

Les sept racines contiennent `metadata.tal.id`, `version: 1` et `evaluator`, en accord avec le numéro du TD. Les sept disposent d’un tuteur S1 en métadonnées et en première cellule Markdown : questionnement, absence de code fourni, aucun accès à une bibliothèque hors périmètre de l’exercice. Le nom de fichier générique apparaît aussi dans la session structurée du tuteur et doit suivre le renommage.

Les 123 cellules initiales comprennent 52 cellules déjà balisées `tal` (45 réponses et sept identifications). Les 71 autres cellules comprennent le tuteur, les introductions, rappels et énoncés, ainsi que la création du fichier au TD6 et l’import `re` au TD7. La présence des seules balises de réponse ne permet donc pas de déclarer que toutes les cellules étaient décrites. La cible décrit chaque cellule sans modifier sa fonction.

Les cellules d’identité contiennent actuellement nom, prénom et classe, sans numéro étudiant. La présente adaptation conserve ce contrat : l’ajout d’un identifiant obligatoire et son contrôle serveur nécessiteraient une évolution explicite, coordonnée avec les correcteurs et la persistance. Il ne faut pas annoncer que le renommage résout à lui seul les collisions d’identité.

## Revue des acquis et des points de vigilance

| TD | Cohérence observée | Réserve précise et priorité d’un chantier ultérieur |
|---|---|---|
| TD1 | Distingue affectation/comparaison, valeurs/types et conversion ; contexte traduction pertinent | Six tâches brèves, seulement un rappel succinct ; `and`, f-string, conversion et appartenance sont demandés sans exemples distincts dans le sujet. La tenue de deux heures dépend d’un apport enseignant non mesuré. Priorité : exemples et essais de transfert, sans retirer les tâches. |
| TD2 | Étayage explicite pour chaque notion, prédire–essayer–expliquer, distinction chaîne/liste ; aucun recours prématuré aux boucles | Les sept durées d’exercice totalisent 106 min, plus 8 min de démarrage et 6 min de restitution : 120 min prévisionnelles, non une mesure de séance. Préserver les explications, qui dépassent la simple sortie numérique. |
| TD3 | Collections complémentaires et application au lexique/vocabulaire ; ensemble utilisé pour des valeurs distinctes | Q4 demande de parcourir `items()` avant la séance consacrée aux boucles. Le tuteur déclare `for` introduit ici, mais le sujet ne l’enseigne pas explicitement. Q1 ajoute puis retire le même dernier élément : la sortie finale seule ne prouve pas les deux opérations. Priorité : étayer Q4 et faire observer les états intermédiaires dans une future révision coordonnée. |
| TD4 | Deux filtrages successifs ; séparation `for`, `range`, `while`, puis fréquences et compréhension | Rappels très courts pour plusieurs syntaxes nouvelles ; aucune mise en pratique distincte de l’arrêt d’une boucle hors l’exemple de multiples. Renforcer les exemples et les prédictions, en conservant les sept objectifs. |
| TD5 | Réinvestissement des chaînes et collections ; distingue `print`/`return`, paramètres et composition | La normalisation avant recherche dans le lexique reste implicite en Q4, alors que Q5 teste « Language » avec une majuscule. Clarifier lors d’une révision des consignes et vérifier la compatibilité du correcteur. Les tests ne couvrent pas explicitement le cas vide. |
| TD6 | Cas métier complet : lecture, nettoyage, dédoublonnage, export ; réutilise collections et fonctions | Le sujet décrit peu `csv.writer` avant son usage. Une valeur `set` n’a pas d’ordre garanti : ne pas imposer implicitement un ordre d’affiliations ou `sorted()` sans introduction. La préparation `Path` est fournie, non un prérequis. |
| TD7 | Pipeline cohérent avec TD4–TD5 ; comparaison avec `split()` et limite linguistique explicitement demandées | Classes de caractères, répétitions et échappements peu étayés. Le nettoyage remplace les dates par `[DATE]` : l’ordre avec la mise en minuscules peut modifier ce marqueur ; convention à expliciter lors d’une future révision. La prise en charge des lettres accentuées ne vaut pas tokenisation linguistique générale. |

Ces observations reposent sur les cellules des sujets, pas sur une mesure des apprentissages. La revue présente ne certifie ni le temps effectif de réalisation ni l’exhaustivité des correcteurs. Les révisions de fond proposées ne sont pas implémentées dans une modification de dénomination/métadonnées/distribution.

## Cohérence des correcteurs : limites héritées vérifiées

Complément de revue demandé après le signalement du réviseur pédagogique indépendant. La lecture des six modules `app_correction_TD1_S1.py`, `app_correction_TD3_S1.py` à `app_correction_TD7_S1.py` confirme leur délégation au moteur `formative_s1`, alias de `formative_s3.check_formative_notebook`. Le TD2 utilise un autre correcteur et n’est pas inclus dans ce constat collectif.

Dans ce moteur, `_sources(cells)` et `_outputs(cells)` concatènent les cellules évaluables. Chaque contrôle recherche des fragments littéraux de code et la présence d’un marqueur de sortie dans ces ensembles. Il ne compare pas la valeur affichée à une référence et ne rattache pas chaque preuve à sa cellule `metadata.tal.question`. Les métadonnées nouvellement complétées ne corrigent donc pas automatiquement ces limites de notation.

| Question et source de preuve | Variante compatible avec la consigne | Condition réellement imposée par `CHECKS` | Résultat du sondage statique et impact |
|---|---|---|---|
| TD1 Q4, consigne « avec une f-string » ; `app/app_correction_TD1_S1.py` | f-string délimitée par apostrophes `f'…'` | Fragment `f"` | 0/1 malgré une f-string et une sortie correcte : dépendance injustifiée au type de guillemets. |
| TD4 Q5, consigne « La variable doit progresser » ; `app/app_correction_TD4_S1.py` | `multiple = multiple + 7` | Fragment `+=`, en plus de `while ` | 0/1 malgré une progression bornée compatible : seule une variante d’affectation est reconnue. |
| TD4 Q6, consigne « `.get(mot, 0)` ou une condition `if` » ; même module | Comptage avec test d’appartenance et branches `if/else` | Fragment `.get(`, en plus de `for ` | 0/1 pour l’alternative explicitement autorisée : contradiction entre consigne et vérification. |
| TD6 Q3, séparation avec `split(";", 1)` ; `app/app_correction_TD6_S1.py` | Même appel écrit `split(';',1)` | Fragment exact `split(";", 1)` | 0/1 pour une syntaxe équivalente : dépendance injustifiée aux espaces et aux guillemets. |
| TD1 Q1, calcul du coût ; moteur commun `app/formative_s3.py` | Sonde volontairement fausse : `cout_total=2*2` dans une cellule balisée Q2 et sortie enregistrée `Résultat Q1 : faux` | Présence globale de `cout_total`, `*` et du marqueur Q1 | 1/1 : ni la valeur du coût ni le rattachement à Q1 ne sont vérifiés. |

Sondages reproduits le 1er octobre 2026 en appelant le correcteur sur des JSON synthétiques et leurs sorties enregistrées : aucun code étudiant n’est exécuté. Pour les quatre faux négatifs, seul le critère de la question concernée est appelé, avec le code complet correspondant et une sortie correcte fournie ; les quatre renvoient « élément de code attendu ». Dans un notebook complet, un fragment trouvé ailleurs peut masquer le défaut, précisément parce que la recherche est globale. Le dernier sondage montre un faux positif à valeur manifestement incorrecte.

Ces défauts préexistent au renommage et à la restitution HTML. Le score de ces six correcteurs renseigne actuellement la présence de traces et de fragments, sans garantir la correction quantitative ni la couverture effective des compétences. Il ne faut pas présenter cette livraison comme une fiabilisation des notes S1.

Prochain chantier prioritaire : définir une preuve par question et par cellule de réponse, reconnaître les constructions équivalentes au moyen d’une analyse statique adaptée, vérifier les valeurs et types des sorties enregistrées, puis distinguer résultat incorrect, trace absente et dépendance non vérifiable. Conserver les alternatives explicitement admises par les consignes, le refus d’exécuter le code déposé et la relecture humaine des justifications. Cette évolution devra faire l’objet d’une matrice de contrat, de cas positifs/négatifs issus des défauts ci-dessus et des revues spécialisées ; les correcteurs et barèmes ne sont pas modifiés dans la présente opération de distribution.

## Critères d’acceptation pour le Designer et les revues

1. La matrice est relue avant le début des modifications et les sept noms cibles sont repris dans le catalogue, les fiches du tuteur et les références actives ; les rapports historiques conservent leurs anciens noms lorsqu’ils décrivent l’état antérieur.
2. Une comparaison source → cible démontre l’égalité des sources et types de toutes les cellules initiales, dans le même ordre ; seul l’enrichissement des métadonnées et l’ajout de la dernière cellule sont attendus.
3. Le premier Markdown du tuteur reste à sa place. Les règles S1 restent identiques, notamment aucun code fourni par le tuteur et aucune bibliothèque supplémentaire pour les réponses.
4. La cellule de restitution suit le modèle HTML demandé, porte un identifiant stable et le rôle `submission`, sans marqueur Q, sortie enregistrée ni exécution préalable. Elle ne reçoit ni point ni activité évaluée.
5. Les sources Git contiennent seulement le substitut `__TAL_PUBLIC_URL__`. Le déploiement rend une seule cellule finale résolue dans les copies distribuées ; les chemins renommés sont utilisés, et aucune ancienne copie distribuée gérée par le manifeste ne demeure proposée en parallèle.
6. Les sept notebooks restent reconnus par le même évaluateur, indépendamment de leur nom de fichier. Aucun changement des réponses attendues, barèmes ou versions de contrat n’est justifié par un renommage et une cellule fournie de restitution.
7. Les revues pédagogique et technique sont indépendantes des producteurs. Ce document est une spécification et un constat du Prof ; il ne vaut pas auto-validation du travail réalisé.
