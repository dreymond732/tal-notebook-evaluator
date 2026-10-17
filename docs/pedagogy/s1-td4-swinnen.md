# TD4 S1 — Cadrage et couverture du renforcement Swinnen

## Décision et références

Demande enseignante du 15 octobre 2026 : poursuivre sur TD4 le renforcement des TD3, TD5 et TD6. L'autorisation porte sur une adaptation plus étayée, sans réduction de couverture ni introduction d'une bibliothèque. Le présent cadrage est établi avant la conception des nouveaux cahiers ; sa conformité effective sera contrôlée sur les supports livrés par des relecteurs indépendants.

Référence historique et technique : `c81c386`, `Notebooks TD/S1/TD4_S1_boucles_conditions_comptages.ipynb`. La version `126cf63` (base PR #31) conserve ce fichier sans modification. Le TD historique et son contrat `td4-s1` (version 2) restent disponibles ; les nouveaux cahiers ont leurs propres contrats `td4-one-s1` (version 2), `td4-bis-s1` (version 2), `td4-ter-s1` (version 2), chacun comprenant six questions et six points. Aucun des 54 exercices des neuf cahiers de la PR #31 ne doit être altéré.

Trois cibles : `TD4-one_S1_conditions_filtres.ipynb`, `TD4-bis_S1_bornes_repetitions.ipynb`, `TD4-ter_S1_comptages_comprehensions.ipynb`, sous `Notebooks TD/S1/`.

## Acquis et périmètre

Les TD1 et TD2 apportent variables, chaînes, opérations, méthodes de chaînes et affichages. Les trois nouveaux TD3 travaillent listes, tranches, `append`, `pop`, parcours `for`, initialisation hors boucle, tuples et déballage, dictionnaires, clés/valeurs, `items`, appartenance, ensembles et distinction formes/occurrences. Ces prérequis sont rappelés et ne constituent pas une preuve de maîtrise.

TD4-one introduit ou consolide comparaison, booléen, `if/else`, indentation imbriquée et filtre. TD4-bis introduit explicitement `range` (un, deux et trois arguments), borne exclue, pas positif ou négatif, modulo, boucle `while` et progression vers l'arrêt. TD4-ter introduit compteurs, accumulation, recherche d'un maximum par parcours, fréquences avec `if/else` puis `get`, et compréhension de liste. Toute notion requise par une question doit être expliquée et montrée sur d'autres données avant cette question.

Aucune bibliothèque dans les réponses ; pas de fonction définie, de saisie interactive, de `Counter`, d'expression régulière ni de bibliothèque de TAL. Les imports de la cellule de restitution sont une préparation fournie et n'élargissent pas les notions autorisées.

## Matrice source → cible établie avant conception

Les références de cellules sont numérotées depuis zéro. Chaque ligne conserve cours, prédiction, manipulation et vérification ; le nombre de nouvelles questions ne suffit pas à démontrer l'équivalence. Toutes les lignes sont **RENFORCÉES** : aucune notion, activité ni vérification de fond n'est supprimée. Les activités historiques sont obligatoires ; les essais d'appui font partie du travail sans point supplémentaire. Le nombre de points ne constitue pas une estimation de charge.

| Source historique | Objectif, notions et activité à conserver | Données, production, autonomie et vérification | Cible prévue | Statut |
|---|---|---|---|---|
| Q1, cellules 6–10 | Cours : `for`, élément courant, liste résultat initialisée avant le parcours, `append`, `upper` ; prédire et observer les états intermédiaires ; essayer sur trois villes et expliquer l'erreur d'initialisation dans la boucle. | Exemple revue/livre ; exercice `mots = ["TAL", "corpus", "analyse", "IA"]` ; construire `majuscules` dans l'ordre, conserver la source, afficher ; autonomie après exemple distinct. | one : transformer une liste ; entraînement villes et comparaison source/résultat. | RENFORCÉ |
| Q2, cellules 11–15 | Cours `if` imbriqué dans `for`, longueur et comparaison ; distinguer strict et inclusif ; prédire un filtre court, puis l'essayer. | Exemple un/livre/des/poèmes ; essai ici/ailleurs/là ; liste historique `mots`, produire `mots_longs` de longueur strictement supérieure à 5, ordre et graphie conservés ; cas exactement égal à 5 explicitement exclu. | one : filtre par longueur ; renforcement par partition des longueurs Swinnen 5.15. | RENFORCÉ |
| Q3, cellules 16–20 | Comparer sur une chaîne normalisée sans modifier la donnée conservée ; prédire et essayer l'appartenance ; distinguer casse et accent. | Exemple ÉTUDE/livre/Revue ; rechercher `e` et vérifier que `é` est distinct ; essai trois chaînes avec `o` ; sur `mots`, produire `mots_avec_a` insensible à la casse mais graphie/ordre d'origine conservés. | one : recherche d'une lettre puis sélection de mots ; appui Swinnen 5.6. | RENFORCÉ |
| Q4, cellules 21–25 | Cours `range` à un/deux/trois arguments, début inclus, fin exclue, pas implicite 1, pas négatif et `list(range(...))` ; modulo comme reste, test de parité ; confronter parcours par pas et sélection par condition. | Exemples `range(2, 9, 3)`, `range(9, 1, -2)`, `range(3)` et reste de 13 par 5 ; prédire `range(8, 2, -2)`, construire 5→1 inclus ; prédire les restes de 8/9/10 par 2 ; exercice `positions_paires` 0→10 inclus, ordre croissant. | bis : bornes croissantes puis parcours inverse ; parité travaillée en one avant partition de nombres si nécessaire, puis réinvestie en bis. | RENFORCÉ |
| Q5, cellules 26–30 | Cours `while` : état initial, condition, traitement, mise à jour, terminaison ; prévoir sur papier une boucle privée de mise à jour sans l'exécuter. | Exemple 3→12 pas 3 avec valeur de sortie ; essai 2/4/6/8 et première rejetée ; exercice `multiple = 7`, liste `multiples` ≤70, prédire première/dernière retenue et première rejetée ; progression observable. | bis : boucle conditionnelle, arrêt et états ; renforcement Swinnen 4.2/4.8. | RENFORCÉ |
| Q6, cellules 31–35 | Cours incrémentation d'un effectif ; comparer `get(cle, 0)` et `if/else` ; prédire les états successifs et expliquer pourquoi une réinitialisation à 1 perd les occurrences. | Exemple revue/livre/revue ; essai oui/non/oui/oui avec états imprimés ; `mots_a_compter = "le TAL traite le langage et le texte".lower().split()` ; produire `frequences`, ordre des clés libre, comparer total des effectifs et nombre de mots. | ter : compteur puis fréquences conditionnelles et avec `get` ; deux écritures effectivement manipulées, conservation du corpus historique. | RENFORCÉ |
| Q7, cellules 36–40 | Cours compréhension : transformation, parcours, filtre ; lire dans l'ordre parcours→filtre→transformation ; comparer à une boucle explicite. | Exemple doubles des valeurs ≥4 de `[2, 5, 1, 4]` ; essai carrés des valeurs >2 de `[1, 3, 6]` en deux écritures ; exercice historique `longueurs_mots_longs` : longueurs des mots >5, ordre préservé, comparaison avec `mots_longs`. | ter : compréhension simple puis filtre et transformation ; données historiques fournies localement pour une exécution autonome. | RENFORCÉ |
| Rappel, cellules 1–5 | Parcourir puis décider, indentation, travail dans l'ordre et sorties conservées. | Identifier les données, prédire avant d'exécuter, observer et commenter ; cours/exemple/exercice/vérification distingués. | Trois cahiers, avec rappels ciblés ; le minutage et la notice d'identification anciens sont retirés conformément à AGENTS §15. | RENFORCÉ |
| Synthèse et restitution, cellules 41–43 | Reprendre une prédiction erronée et expliquer la correction ; contrôler bornes, conditions, initialisation ; réexécuter et conserver les sorties. | Bilan étudiant et procédure de dépôt existante ; problème précis et essai à identifier en cas de blocage. | Bilan des trois cahiers et cellule de restitution ; ne pas répéter la présentation du tuteur ni la procédure générale d'autoévaluation. | RENFORCÉ |

Le déplacement des activités entre cahiers ne vaut couverture que lorsque les trois cibles sont effectivement livrées. Les titres, numéros définitifs et cellules livrées sont consignés dans le tableau de réalisation ci-dessous ; la matrice ci-dessus reste le critère de contrôle.

## Exercices de Swinnen authentifiés dans le PDF fourni

Source : Gérard Swinnen, *Apprendre à programmer avec Python*, copyright 2000–2012, exemplaire fourni par l'enseignant (`apprendre_python3_5.pdf`). Les numéros de pages suivants sont les pages **imprimées**, distinctes du rang de page dans le PDF (décalage +20). Les consignes seront adaptées, avec données fournies en cellule et résultats enregistrables ; elles ne seront pas présentées comme des citations littérales.

| Exercice | Page imprimée (PDF) | Objectif source et adaptation autorisée |
|---|---|---|
| 4.2 | 31 (51) | Vingt premiers termes de la table de 7 ; liste et affichage plutôt qu'une suite d'affichages seule ; expliciter les bornes et l'arrêt. |
| 4.8 | 35 (55) | Parmi les cinquante premiers multiples de 13, sélectionner les multiples de 7 ; réinvestir modulo et filtre. |
| 5.6 | 44 (64) | Déterminer la présence de `e` dans une chaîne ; traiter ensuite plusieurs chaînes et préciser la casse et les accents. |
| 5.7 | 44 (64) | Compter les occurrences de `e` dans une chaîne ; compteur explicite, puis transfert aux fréquences de mots. |
| 5.13 | 47 (67) | Rechercher le maximum d'une liste ; parcours et mise à jour, liste non vide et cas de nombres négatifs ; ne pas remplacer le travail algorithmique par `max`. |
| 5.14 | 47 (67) | Répartir les nombres entre pairs et impairs ; préserver l'ordre de chaque sous-liste et vérifier l'exhaustivité. |
| 5.15 | 47 (67) | Répartir les mots entre moins de 6 caractères et au moins 6 ; tester explicitement 5 et 6 caractères et relier au filtre historique >5. |
| 6.8 | 58 (78) | Additionner entre deux bornes les multiples de 3 **et** de 5, puis de 3 **ou** de 5 ; expliquer les deux conditions et le comptage unique des valeurs communes. |

Chaque cahier adapté attribue les exercices concernés avec numéro et page, explicite les modifications et inclut l'annexe existante `docs/swinnen/NOTICE_PREFACE_LICENCE.txt` sans altération. La licence de l'ouvrage fournie avec cette notice reste applicable aux adaptations ; aucune nouvelle politique de droits n'est introduite.

## Charge, contrats et acceptation

Le parcours passe de 13 à 15 cahiers de TD, hors devoirs maison et contrôles : TD1, TD2, trois TD3, trois TD4, trois TD5, trois TD6 et TD7. Une découpe en cahiers ne constitue pas une mesure du temps nécessaire. La faisabilité dans huit séances de deux heures n'est pas mesurée ; aucune activité obligatoire n'est supprimée pour donner artificiellement l'impression de tenir ce volume. La répartition des séances reste un arbitrage enseignant.

Le tuteur garde son contexte complet et identique dans les métadonnées et le commentaire HTML sous le titre de la première cellule Markdown ; chaque question a son périmètre explicite et fermé, sans code donné au S1. Les nouveaux contrats sont des ajouts, sans modification des contrats historiques. L'évaluateur observe les productions enregistrées et les constructions demandées sans exécuter le code étudiant côté serveur. Les vérifications humaines requises incluent essais, explications et pertinence des comparaisons ; un score de 6/6 ne suffit pas à les attester.

Critères d'acceptation : couverture de toutes les lignes de la matrice ; dix-huit questions au total, chacune avec appui, exemple distinct, essais et critères vérifiables ; exécution locale des copies modèles et six points sur six ; conservation des neuf cahiers précédents ; verdicts pédagogique et rédactionnel indépendants puis audit technique et de gouvernance selon le workflow.

## Réalisation livrée après conception

Les trois cahiers ont été lus dans leur état livré : chacun contient 43 cellules, numérotées ci-dessous depuis zéro. Chaque question conserve six fonctions distinctes : cours, exemple, essai, énoncé, réponse et vérification. Pour Q1, ces fonctions occupent respectivement les cellules 4, 5, 6, 7, 8 et 9 ; l’écart entre deux questions successives est de six cellules. Les marqueurs de réponse sont `metadata.tal.question = Q1` à `Q6`, et `metadata.tal.role = answer`.

| Cahier | Question et objectif livré | Source couverte ou appui authentifié | Cellules finales (cours → vérification) | Identifiant de réponse |
|---|---|---|---|---|
| one | Q1 — Transformer chaque mot | Historique Q1 : `upper`, ordre, source conservée, initialisation hors boucle, états intermédiaires. | 4–9 | `td4-one-s1-07` |
| one | Q2 — Filtrer selon la longueur | Historique Q2 : longueur strictement >5 ; essai effectif sur un mot de cinq caractères. | 10–15 | `td4-one-s1-13` |
| one | Q3 — Filtrer selon une lettre | Historique Q3 : recherche de `a` sans casse, graphie source conservée ; entraînement casse/accent et lettre `o`. | 16–21 | `td4-one-s1-19` |
| one | Q4 — Distinguer présence, casse et accent | Swinnen 5.6, p. 44 : présence de `e` ; adaptation trois chaînes, booléens, casse, accent et chaîne vide. | 22–27 | `td4-one-s1-25` |
| one | Q5 — Répartir les mots selon leur longueur | Swinnen 5.15, p. 47 : prénoms répartis entre <6 et ≥6 ; seuil 5/6, occurrences et ordre conservés. | 28–33 | `td4-one-s1-31` |
| one | Q6 — Répartir les nombres pairs et impairs | Swinnen 5.14, p. 47 : partition par modulo, liste numérique reprise, essais sur zéro, négatifs et répétitions. | 34–39 | `td4-one-s1-37` |
| bis | Q1 — Choisir les bornes de range | Historique Q4 : formes de `range`, borne exclue, pas implicite, parité, liste des pairs 0→10 inclus ; essais historiques conservés. | 4–9 | `td4-bis-s1-07` |
| bis | Q2 — Parcourir dans le sens inverse | Renforcement du cours et des essais historiques Q4 : pas négatif, bornes incluses/exclues, parcours vide si pas incompatible. | 10–15 | `td4-bis-s1-13` |
| bis | Q3 — Garantir l’arrêt d’une boucle while | Historique Q5 : multiples de 7 ≤70, première valeur rejetée affichée, état initial/condition/traitement/mise à jour ; boucle sans mise à jour examinée sans exécution. | 16–21 | `td4-bis-s1-19` |
| bis | Q4 — Produire exactement vingt termes | Swinnen 4.2, p. 31 : vingt premiers multiples positifs de 7 par `while` ; compteur distinct et valeur finale contrôlée. | 22–27 | `td4-bis-s1-25` |
| bis | Q5 — Sélectionner parmi cinquante multiples | Swinnen 4.8, p. 35 : cinquante multiples positifs de 13 examinés ; conserver ceux divisibles par 7, distinguer candidats et sélection. | 28–33 | `td4-bis-s1-31` |
| bis | Q6 — Distinguer « et » de « ou » | Swinnen 6.8, p. 58 : deux sommes sur bornes incluses ; données fixées à 1 et 30, conditions `and/or`, pas de double ajout des multiples communs. | 34–39 | `td4-bis-s1-37` |
| ter | Q1 — Compter un caractère exact | Swinnen 5.7, p. 44 : compteur de `e`, texte adapté, casse neutralisée et accents distincts. | 4–9 | `td4-ter-s1-07` |
| ter | Q2 — Rechercher un maximum par parcours | Swinnen 5.13, p. 47 : liste numérique source et liste négative ajoutée ; candidat initial correct, listes non vides, sans `max` ni tri. | 10–15 | `td4-ter-s1-13` |
| ter | Q3 — Mémoriser des fréquences par condition | Renforcement propre au cours de l’historique Q6 : un compteur par animal avec `if/else`, répétitions et total des observations. | 16–21 | `td4-ter-s1-19` |
| ter | Q4 — Comparer deux écritures du comptage | Historique Q6 complet : corpus `le TAL traite le langage et le texte`, exemples `get`/`if-else`, essais oui/non et états ; les deux écritures sont désormais obligatoires, puis total par parcours des effectifs. | 22–27 | `td4-ter-s1-25` |
| ter | Q5 — Transformer par compréhension | Appui propre au cours préparant l’historique Q7 : une longueur par mot, ordre et répétitions, source conservée. | 28–33 | `td4-ter-s1-31` |
| ter | Q6 — Combiner filtre et transformation | Historique Q7 : longueurs des mots >5 ; boucle/compréhension comparées, essai des carrés et exemple historique des doubles conservés ; reconstruction locale de `mots_longs`. | 34–39 | `td4-ter-s1-37` |

Dans chaque cahier, le bilan occupe la cellule 40, l’annexe Swinnen avec notice/préface/licence la cellule 41 et la restitution la cellule 42. Le titre et le contexte complet du tuteur sont dans la cellule 0 ; l’introduction et l’identification précèdent le cours. Les numéros Swinnen ne sont attribués qu’aux huit adaptations documentées ; les fréquences de mots et les compréhensions sont explicitement identifiées comme des renforcements propres au cours.

## État des validations et limites

- **Cadrage adopté avant conception** par le coordinateur, dans le périmètre autorisé par l’enseignant.
- **Supports livrés** : trois cahiers, dix-huit questions et trois contrats de six points, sans remplacement du TD4 historique.
- **Revue pédagogique indépendante** : `TAL-Pedagogy-Reviewer` a transmis au coordinateur le verdict `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`. Correspondances contrôlées : historiques Q1→one Q1, Q2→one Q2, Q3→one Q3, Q4→bis Q1/Q2, Q5→bis Q3, Q6→ter Q4, Q7→ter Q6. Ce verdict est celui du relecteur indépendant, non une autovalidation de `TAL-Prof`.
- Les verdicts rédactionnel, technique, de gouvernance et d’intégration ainsi que les résultats d’exécution sont consignés séparément par les rôles responsables ; le présent document ne les anticipe pas.
- La durée nécessaire aux étudiants et la répartition dans les huit séances de deux heures restent non mesurées. Un score automatique ne valide pas à lui seul les prédictions, explications et essais.

Statut : **CADRAGE ET MATRICE DE RÉALISATION LIVRÉS ; COUVERTURE PÉDAGOGIQUE ACCEPTÉE PAR REVUE INDÉPENDANTE ; AUTRES VERDICTS DANS LES HANDOFFS DISTINCTS**.
