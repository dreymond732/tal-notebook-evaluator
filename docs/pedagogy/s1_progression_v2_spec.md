# S1 — Contrat de correction et d’étayage v2

## Portée

Cette spécification accompagne `s1_progression_v2_coverage.md`, établie avant conception. Elle traduit la demande enseignante : réparer les faux positifs/faux négatifs de notation et étoffer la progression sans réduire aucun TD. Elle ne contient pas de corrigé à distribuer. Les valeurs ci-dessous sont des références du correcteur et de ses tests.

Sept contrats `td1-s1` à `td7-s1`, version2. Barèmes inchangés : TD1 6, TD2 7, TD3 6, TD4 7, TD5 6, TD6 6, TD7 7. Le résultat est un **score technique provisoire** : conformité des traces enregistrées, non certification d’une compétence ni note pédagogique définitive.

## Règles communes

- Racine `metadata.tal` conforme au catalogue ; une cellule identité unique ; une cellule `answer` pour chacune des Q attendues. Les réponses se rattachent à leur identifiant, jamais à la position de cellule ni à une recherche globale dans le notebook.
- Identité littérale complète : nom, prénom, classe, `numero_etudiant` non vides ; numéro de 1 à 64 caractères ASCII alphanumériques, `_` ou `-`. Les commentaires et noms de variables ressemblants ne constituent pas une identité. Copies homonymes distinguées par numéro ; persistance séparée par version.
- Ancien contrat ou métadonnées obligatoires absentes : « mauvaise version du notebook », sans correction ni sauvegarde. Cellule de réponse présente mais vide : preuve absente, et non ancienne version.
- Les prints historiques `Résultat Qn :` demeurent. Les traces complémentaires figurent dans la même cellule `answer` Qn. Un marqueur enregistré ailleurs, dans un exemple, une préparation, un entraînement ou la restitution ne rapporte aucun point.
- Sorties de conteneurs : représentation Python ordinaire, analysée sans exécution. `repr` pour la phrase libre Q6b du TD1 et le CSV multiligne Q6 du TD6. Types stricts : un booléen n’est pas un entier, liste/tuple/ensemble ne sont pas confondus sauf équivalence explicitement admise ci-dessous. Ordre des listes significatif ; ordre des dictionnaires/ensembles non significatif.
- Syntaxe : examiner l’AST de la cellule de réponse et les expressions participant à la production imprimée ; ne pas exiger une forme textuelle d’espacement, de guillemets ou de parenthèses. N’exiger une construction particulière que lorsqu’elle constitue l’objectif annoncé. Ne pas accorder un point pour un fragment placé dans un commentaire, une fonction inutilisée ou une chaîne.
- Une valeur fausse n’est pas rendue correcte par une structure de code plausible. Inversement, une variante équivalente autorisée n’est pas refusée pour des espaces ou des guillemets.
- Explications : relever présence et localisation pour relecture ; ne pas déduire qualité, pertinence ni compréhension d’un nombre de mots ou d’un mot-clé. Une production absente est signalée. Une production présente n’est pas déclarée « analyse correcte ».
- États de diagnostic distincts : conforme, résultat incorrect, preuve absente/illisible, construction demandée non repérée, non vérifiable (dépendance identifiée). Une erreur antérieure n’entraîne pas la déclaration de plusieurs erreurs indépendantes ; vérifier une sortie contre sa référence fixe dès que c’est possible.
- Aucun code étudiant n’est exécuté, aucun fichier mentionné par l’étudiant n’est ouvert sur le serveur. La sortie enregistrée ne prouve ni l’exécution réelle ni la généralité d’une fonction ; signaler cette limite.

## Références et preuves par question

### TD1 — Variables et types (six points)

| Q | Trace attendue | Construction/critère et variantes |
|---|---|---|
| Q1 | `15.0` (nombre réel 15 accepté avec tolérance de représentation numérique) | Affectation de `cout_total`, produit des données prix et quantité ; syntaxe de multiplication, pas une simple constante recopiée. |
| Q2 | `<class 'float'>` | Appel à `type` sur `note`, pas type affiché comme chaîne littérale. |
| Q3 | `True True` | Comparaison d’égalité et conjonction `and`, valeur de chaque booléen vérifiée séparément. |
| Q4 | `Traduction du français vers l’anglais.` | f-string (AST JoinedStr) liée à la phrase imprimée ; apostrophe typographique ou droite acceptée ; guillemets de code indifférents. |
| Q5 | `100 <class 'int'>` | Conversion `int` à partir de la chaîne, addition20, résultat entier et `type`. |
| Q6 | `len(phrase)` puis booléen de présence exacte de `TAL` | Nouvelle Q6b = `repr(phrase)` ; comparer longueur et appartenance à cette chaîne libre. `len` et opérateur d’appartenance dans la production. Une phrase sans TAL est parfaitement valide si False est imprimé. |

Q6b est une sérialisation de vérification, présentée comme affichage fourni ; elle n’introduit pas une compétence évaluée sur `repr`.

### TD2 — Chaînes et séquences (sept points)

Contenu pédagogique, tous Q/Qb, données et explications intacts. Le contrat historique détaillé de `TD2_S1_SPECIFICATION.md` est conservé ; changement transversal d’identité, version et isolation des preuves seulement. Respecter notamment Q1 longueurs 35 et29, Q2 transformations et booléens, Q3 bornes, Q4 chaîne/liste, Q5 reconstruction, Q6 trois indices sans boucle, Q7 liste et commentaire. Si une divergence apparaît entre une valeur de ce document et les chaînes exactes du notebook, les chaînes originales font référence et leurs valeurs doivent être recalculées dans les tests de référence. Aucune réduction des sept questions ni de leur interprétation.

### TD3 — Collections (six points)

| Q | Trace attendue | Construction/critère et variantes |
|---|---|---|
| Q1 | Nouvelle Q1a `['corpus','lexique','concordancier','tokeniseur']` immédiatement après ajout ; Q1 `['corpus','lexique','concordancier']` après retrait | Deux états conservés et manipulation de liste ; `append`/`pop` présentés, variantes d’ajout/retrait sémantiquement admissibles si le correcteur peut les identifier. Ne pas noter la seule liste finale inchangée. |
| Q2 | Q2 `<class 'tuple'>` puis justification personnelle ; nouvelle Q2b `('français','italien','espagnol')` | Construction tuple littérale ou `tuple(...)`, appel `type`; justification non vide, qualité humaine. |
| Q3 | Q3 `langue` ou `langage` ; nouvelle Q3b dictionnaire à quatre clés `book`, `language`, `data`, `corpus` | Valeurs `livre`, (`langue` ou `langage`), `données`, `corpus`. Deux traductions de language admises explicitement. Ajout de corpus après construction initiale, accès à language. Ordre des clés libre. |
| Q4 | Liste des quatre chaînes `book -> livre`, `language -> langue` ou `language -> langage`, `data -> données`, `corpus -> corpus` | Boucle sur `lexique.items()` présentée avant activité ; chaîne par concaténation ou f-string ; ordre des entrées libre, unicité et contenu exacts. Cohérence avec Q3 lorsqu’il est vérifiable ; sans Q3, les deux traductions admises restent connues. |
| Q5 | Q5 `6 4` ; nouvelle Q5b ensemble `{'texte','corpus','donnée','analyse'}` | Conversion de la liste en ensemble, deux `len`. Ordre de repr libre. |
| Q6 | Ensembles communs `{'langue','corpus'}` et seulement_a `{'texte','analyse'}` | Intersection/différence : opérateurs `&`/`-` ou méthodes `.intersection`/`.difference` également valides. |

### TD4 — Boucles, conditions et comptages (sept points)

| Q | Trace attendue | Construction/critère et variantes |
|---|---|---|
| Q1 | `['TAL','CORPUS','ANALYSE','IA']` | Boucle `for`, conversion `upper`, constitution d’une liste dans l’ordre. |
| Q2 | `['corpus','analyse']` | Boucle `for` et condition de longueur strictement supérieure à5. |
| Q3 | `['TAL','analyse','IA']` | Recherche de `a` sans casse, données originales conservées dans la liste ; boucle/filtre cohérent. |
| Q4 | `[0,2,4,6,8,10]` | Utilisation de `range` ; pas de2 ou filtre de parité admis ; `list(range(...))` admis puisque la consigne exige range, pas une boucle écrite. |
| Q5 | `[7,14,21,28,35,42,49,56,63,70]` | Boucle `while`, progression de la variable ; `multiple += 7` et `multiple = multiple + 7` admis. Le passage à77 explique l’arrêt ; ne pas exiger qu’il soit dans la sortie. |
| Q6 | `{'le':3,'tal':1,'traite':1,'langage':1,'et':1,'texte':1}` | Parcours et accumulation ; `.get` OU test d’appartenance avec branches if/else, comme la consigne l’autorise. Ordre des clés libre ; compteurs entiers positifs. |
| Q7 | `[6,7]` | Compréhension de liste filtrée, longueurs des mots de plus de5 caractères ; ordre original. |

Les entraînements supplémentaires couvrent range inverse et frontière while sur des données distinctes, sans nouvelle question notée.

### TD5 — Fonctions (six points)

| Q | Trace attendue | Construction/critère et variantes |
|---|---|---|
| Q1 | `3 6` | Définition `longueur_texte`, paramètre, retour de longueur ; appels demandés. |
| Q2 | `bonjour tal` | `normaliser` combine suppression des espaces de bord et minuscules, retourne le résultat. |
| Q3 | `5` | `nombre_mots` appelle `normaliser`, découpe et compte les fragments. |
| Q4 | `langage unknown` | `traduire_mot` normalise avant recherche, utilise son paramètre lexique ; branche conditionnelle ou `lexique.get` avec valeur de repli normalisée admises. |
| Q5 | `langage données` | `traduire_phrase` réutilise `traduire_mot` pour chaque fragment, recompose par join. Boucle ou compréhension admise. |
| Q6 | `{'texte_normalise':'le tal avance','nb_caracteres':13,'nb_mots':3}` | `resume_texte` compose les fonctions ; longueur du texte normalisé (convention désormais explicite), trois clés exactes, ordre libre. |

Entraînements distincts obligatoires : appels sur chaîne vide pour Q1–Q3, connu en majuscules et inconnu pour Q4, phrase vide pour Q5, résumé vide pour Q6. Attendus conceptuels : 0, chaîne vide,0, conservation de l’inconnu normalisé, chaîne vide, résumé 0/0. Ils sont des essais à expliquer, non de nouveaux points. Introduire un paramètre à valeur par défaut avec exemple distinct ; ne pas ajouter de paramètre obligatoire aux six signatures existantes. Aucune dépendance à une bibliothèque nouvelle.

### TD6 — Fichiers et CSV (six points)

Jeu fourni inchangé, cinq lignes terminées par `\n`, longueur156. Il ne devient pas une réponse à évaluer.

| Q | Trace attendue | Construction/critère et variantes |
|---|---|---|
| Q1 | `156` | `with open(..., encoding='utf-8')` et lecture vers texte_affiliations ; espacement/guillemets libres. |
| Q2 | `5` | Découpage splitlines et traitement des lignes utiles ; ne pas exiger un rejet artificiel quand aucune ligne vide interne n’existe. |
| Q3 | Q3 premier couple `['durand alice','Laboratoire TAL']` ou tuple équivalent ; nouvelle Q3b liste complète des cinq couples dans l’ordre | `split(';',1)`, maxsplit positional ou keyword, blancs/guillemets libres ; liste/tuple admis pour chaque paire, liste externe ordonnée. |
| Q4 | Q4 `Durand Alice` ; nouvelle Q4b trois résultats `Durand Alice` sur `durand alice`, `Durand Alice`, `  Durand   Alice  ` | Fonction normalisant espaces de bord/intérieurs puis title ; trois graphies initiales toujours testées, ajout du cas à espaces multiples. |
| Q5 | Q5 ensemble `{'Laboratoire TAL','Centre de traduction'}` ; nouvelle Q5b dictionnaire complet | Clés `Durand Alice` avec ces2 affiliations, `Martin Bob` avec `{'Centre de traduction'}` ; valeurs ensembles non ordonnés. |
| Q6 | `repr` du fichier CSV relu ; décodage sans lecture serveur du fichier étudiant | En-tête `personne,nb_affiliations,affiliations`, deux lignes, virgule CSV, cellules affiliations réunies par ` | ` ; ensembles logiques identiques àQ5, comptes2/1. Ordre des personnes et des affiliations libre ; LF/CRLF admis, syntaxe de quoting CSV gérée par csv. Écriture avec csv, encodageUTF-8, newline vide, puis relecture. |

Liste Q3b complète : `[['durand alice','Laboratoire TAL'], ['DURAND ALICE','Laboratoire TAL'], ['Durand Alice','Centre de traduction'], ['Martin bob','Centre de traduction'], ['MARTIN BOB','Centre de traduction']]`.

Le tri peut être choisi par un étudiant qui le connaît, mais il n’est ni introduit implicitement ni exigé pour réussir. La cellule `Path` reste une préparation fournie ; seuls csv et les constructions enseignées sont nécessaires.

### TD7 — Regex et pipeline (sept points)

| Q | Trace attendue | Construction/critère et variantes |
|---|---|---|
| Q1 | `True` | Recherche regex insensible à la casse : flag IGNORECASE/I, motif inline ou normalisation explicite cohérente admis ; conversion en booléen. |
| Q2 | `['2','14','3','250']` | `re.findall`, chiffres regroupés ; `\d+` ou `[0-9]+` valides sur les données de l’exercice. |
| Q3 | `['L','analyse','c','est','déjà','étapes']` puis commentaire non vide | Lettres accentuées incluses, chiffres exclus, ordre exact ; classe adaptée ou classe Unicode pertinente admise. Commentaire comparatif conservé pour relecture, pas jugé par mot-clé. |
| Q4 | `Le [DATE], Alice a relu 12 segments.` | `re.sub` sur forme JJ/MM/AAAA ; classe chiffrée et répétitions équivalentes admises ; le12 hors date reste intact. |
| Q5 | `le [DATE] comporte exemples.` | `nettoyer_texte` : minuscules puis remplacement dates, retrait chiffres restants, espaces normalisés, return. Marqueur DATE reste majuscule. |
| Q6 | `{'texte_nettoye':'le tal, le tal : exemples.','mots':['le','tal','le','tal','exemples'],'frequences':{'le':2,'tal':2,'exemples':1}}` | Composition via nettoyer_texte, extraction regex, accumulation ; ordre de mots conservé, ordre des clés libre. |
| Q7 | Chaîne limite_regex non vide | Un point de présence technique uniquement, **interprétation à relire** ; situation linguistique + information manquante demandées, non certifiées automatiquement. |

Sur d’autres textes, le marqueur `[DATE]` peut devenir le mot `DATE` lors de l’extraction des lettres : conserver ce comportement explicite et demander à l’étudiant d’en discuter la limite. Les motifs de dates vérifient une forme, pas l’existence calendaire de la date. Une classe comprenant des lettres accentuées ne garantit pas une tokenisation linguistique générale.

## Mise en œuvre pédagogique

Pour chaque nouvelle notion : un exemple commenté sur données différentes, une prédiction, un essai court puis l’activité originale. Les cellules d’essai portent un rôle `practice` et un identifiant distinct rattaché à l’exercice pour le tuteur ; aucune n’est une cellule `answer` supplémentaire. Les exemples de code du support sont autorisés par l’enseignant ; le tuteur S1 ne fournit toujours pas de code aux demandes de solution, y compris pendant les entraînements.

Les notebooks annoncent : score technique sur sorties enregistrées, justifications à relire, nouvelle version nécessaire. Les sources distribuées restent sans réponse, sans exécution ni sorties préremplies, avec tuteur d’abord et restitution HTML en dernier. Le dépôt n’embarque que le substitut d’adresse ; dist est généré au déploiement.

## Vérification attendue

Cas positifs sur chaque Q ; variantes f-string apostrophes, incrémentation longue, if/else de comptage, maxsplit sans espaces, opérateurs/méthodes d’ensembles, ordre arbitraire des affiliations. Cas négatifs : valeur fausse malgré bonne syntaxe, marqueur dans une autre Q/exemple/practice, commentaires trompeurs, booléens pris pour compteurs, manque de cellules/v1, identité vide, dépendances absentes, CSV incohérent, commentaire vide. Les contrôles TD2 existants restent couverts sans réduire ses exigences.
