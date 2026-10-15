# S1 — Matrice préalable du nettoyage de présentation des sept TD

## Mission, autorisation et références

Cadrage TAL-Prof du 15 octobre 2026, avant intervention du Designer, sur la branche `pedagogy/s1-nettoyage-presentation`. Référence technique et source de comparaison : commit `590b9a6`, sept notebooks actifs sous `Notebooks TD/S1/`. La cible conserve les mêmes chemins, cellules, identifiants et ordre.

La demande enseignante « ok. opère ce nettoyage et fait une PR » autorise les quatre changements de présentation détaillés dans l'échange : retirer minutages et notices d'identification, expliquer une seule fois la procédure générale d'autoévaluation et présenter Gemini une seule fois au TD1. Elle n'autorise aucune réduction d'activité, de données, d'interprétation, de charge de travail ou d'autonomie. Les suppressions ci-dessous concernent donc uniquement ces notices et répétitions. Aucune nouvelle bibliothèque ni compétence n'est introduite.

Références normatives : `AGENTS.md`, règles 11 à 15 ; `docs/agents/WORKFLOW.md` ; fiches TAL-Prof et TAL-Pedagogy-Designer ; `docs/pedagogy/TUTORING_POLICY.md`. La matrice historique `docs/pedagogy/s1_editorial_complete_coverage.md` compare le premier état Git disponible `2a36752`, la référence technique `670e6c1` et les sources originales privées consultées lors de cette reprise. `docs/pedagogy/s1_td_review_distribution.md` documente les 45 questions et les sept traces complémentaires du TD2. Le présent cadrage préserve intégralement le support actuel ; il ne prétend ni avoir relu les archives privées non présentes dans le checkout ni avoir rétabli les lacunes historiques déjà signalées.

L'audit S1 du 14 octobre 2026 remis dans cet échange reste une référence de constats ; ses rapports locaux préexistants ne font pas partie de la PR de nettoyage. Cette opération limitée ne clôt pas les écarts du contrôle, du DM, des corrigés absents ou du modèle de corrigé TD2. Un avis favorable au nettoyage ne vaut pas conformité globale S1.

Les indices de cellules de ce document commencent à **1**. Les identifiants techniques de cellule constituent les repères stables pour la comparaison.

## Contrat de couverture et de présentation

| Élément source | Cible livrée | Statut et contrainte |
|---|---|---|
| Cours, exemples et exercices Q1 à Q45 cumulés | Même fichier, même cellule, même ordre | CONSERVÉ : notions, données, consignes, affichages, critères et niveau d'autonomie identiques. |
| Essais personnels, vérifications après réponse, synthèses | Même cellule et même statut | CONSERVÉ : aucune activité obligatoire ne devient facultative ; aucune remédiation n'est supprimée. |
| Budgets et minutages visibles | Retrait des seules durées et tableaux horaires | SUPPRIMÉ, décision enseignante ci-dessus : les activités listées restent dans leur support et leur ordre. La durée réelle n'est pas certifiée par ce nettoyage. |
| Notices décrivant les champs d'identification | Retrait des phrases de notice et de leur éventuel commentaire dans le code | SUPPRIMÉ, décision enseignante : les affectations des quatre champs restent identiques. |
| Procédure générale d'autoévaluation répétée | Explication regroupée en TD1, cellule 5 `tal-s1-td1-intro-v2` | DÉPLACÉ : cible immédiatement disponible dans le premier TD ; retirer les autres exposés généraux, conserver les indications nécessaires à chaque exercice. |
| Présentation générale répétée du tuteur | Présentation unique de Gemini dans cette même cellule du TD1 | DÉPLACÉ/RENFORCÉ : nommer Gemini, son aide au raisonnement dans les notions étudiées et l'absence de code écrit à la place de l'étudiant ; aucun élargissement des permissions cachées. |
| Limites locales du retour automatique | Cellules Q6 du TD1, Q7 du TD2 et Q7 du TD7 notamment | CONSERVÉ : ces limites décrivent une production propre à la question et ne sont pas une seconde procédure générale. |
| Titres, profils et contexte caché du tuteur | Première cellule Markdown et métadonnées Colab inchangées | CONSERVÉ : même titre, contexte HTML complet identique à la copie des métadonnées ; aucun changement de profil. |
| Contrat d'évaluation et restitution | Métadonnées, réponses, marqueurs, code et cellule finale inchangés | CONSERVÉ : versions, identifiants `tdn-s1`, Q, rôles, variables, types, formats, tolérances, barèmes et `__TAL_PUBLIC_URL__` restent identiques. |

La procédure unique au TD1 doit dire comment travailler sur sa copie, conserver les cellules et libellés, activer les affichages après avoir préparé les variables, enregistrer les sorties, utiliser le retour automatique puis vérifier soi-même explications et critères. Les exemples et essais font partie du travail même sans points supplémentaires. Demander une aide précise reste possible. Les instructions de navigation propres à un TD, aux essais après définition d'une fonction et à sa restitution restent présentes ; il ne s'agit pas de reconstituer ailleurs un guide général.

## Matrice des cellules de présentation

Toutes les cellules non désignées pour une modification de source sont conservées intégralement. Les cellules de code sont immuables sauf le commentaire de notice identifié au TD2 ; son AST et ses affectations doivent rester identiques.

| Fichier sous `Notebooks TD/S1/` | Cellules et passages source | Cible précise | Statut |
|---|---|---|---|
| `TD1_S1_variables_types.ipynb` | 3, dernière phrase sur les points de suspension de l'identification ; 5, notice d'identité, budget et explication générale ; 7, 12, 17, 22, 27, 32, suffixes chronométrés ; 37, titre et rappel général du retour automatique | Retirer la notice en 3 ; garder le cours sur `#`. En 5, supprimer identité et budget, conserver et réunir la procédure générale puis ajouter l'unique présentation de Gemini. Retirer uniquement les durées dans les six titres. En 37, garder les questions de synthèse, l'activité de reprise d'un essai et le dépôt ; condenser le rappel général déjà traité en 5. | CONSERVÉ pour les activités ; SUPPRIMÉ pour notices/durées ; RENFORCÉ pour la présentation initiale. |
| `TD2_S1_chaines_sequences.ipynb` | 2, budget ; 3, titre chronométré et procédure répétée ; 4, premier commentaire d'identification ; 5, notice et rappel général ; 6, 10, 14, 18, 22, 26, 30, titres ; 32, titre et dépôt | Retirer budget et durées. En 3, garder le rappel actif des variables, types, `=`, `==`, `len()` et le renvoi au TD1. Retirer uniquement `# Complétez les informations entre les guillemets.` en 4 ; conserver `# Mes réponses au rappel du TD1 :` et les affectations. En 5, garder les indications locales sur les réponses, observations et cellules d'exemple, sans répéter le guide général. En 32, préserver la liste Q1–Q7/Q1b–Q7b, la réflexion de synthèse et le dépôt spécifique TD2. | Activités CONSERVÉES ; guide général DÉPLACÉ au TD1 ; notices/durées SUPPRIMÉES. |
| `TD3_S1_collections.ipynb` | 3, seconde phrase sur l'identification ; 5, notice, procédure et budget ; 7, 12, 17, 23, 28, 33, titres ; 38, titre et rappel général | En 3, garder le partage du lexique entre Q3 et Q4 et l'ordre du travail. En 5, conserver l'organisation locale exemples/essais/réponses sans la notice ni l'exposé général d'autoévaluation. Retirer durées et budget. En 38, garder les activités de reprise et de comparaison des collections, ainsi que restitution et difficultés formulées. | Activités CONSERVÉES ; guide général DÉPLACÉ ; notices/durées SUPPRIMÉES. |
| `TD4_S1_boucles_conditions_comptages.ipynb` | 5, budget, notice d'identité et dernier paragraphe général de retour/tuteur ; 7, 12, 17, 22, 27, 32, 37, titres ; 42, titre | Retirer budget, identité, durée des titres et présentation générale répétée. Conserver la progression cours–exemple–entraînement–exercice, les manipulations obligatoires, les prédictions, commentaires, critères locaux et la synthèse sur bornes, filtres et initialisation. | Activités CONSERVÉES ; présentation générale DÉPLACÉE ; notices/durées SUPPRIMÉES. |
| `TD5_S1_fonctions_reutilisation.ipynb` | 5, tableau horaire, notice d'identité et dernier paragraphe général ; 43, phrase « Vérifiez votre identification » | Retirer tableau, notice et présentation répétée ; conserver les étapes de travail et l'obligation d'effectuer les essais après définition des fonctions. En 43, conserver le choix d'un test, son explication dans la cellule 44, la difficulté ouverte et l'enregistrement des sorties. | Activités CONSERVÉES ; présentation générale DÉPLACÉE ; notices/durées SUPPRIMÉES. |
| `TD6_S1_fichiers_csv.ipynb` | 5, tableau horaire, notice d'identité et dernier paragraphe général ; 40, phrase « Vérifiez votre identification » | Même nettoyage limité ; conserver données fournies, préparation du fichier, essais après Q4 et Q5, choix d'un test expliqué en 41, difficulté ouverte et enregistrement des sorties. La notion d'identité des personnes de Q4 est une donnée métier, pas une notice du formulaire : elle reste intégrale. | Activités CONSERVÉES ; présentation générale DÉPLACÉE ; notices/durées SUPPRIMÉES. |
| `TD7_S1_expressions_regulieres_pipeline.ipynb` | 5, tableau horaire, notice d'identité et dernier paragraphe général ; 47, phrase « Vérifiez votre identification » | Même nettoyage limité ; conserver avertissement d'exécuter les essais après définition des fonctions, conventions regex, ordre du pipeline, critères de Q7, test expliqué en 48 et restitution. | Activités CONSERVÉES ; présentation générale DÉPLACÉE ; notices/durées SUPPRIMÉES. |

La cellule 3 des TD4 à TD7 conserve son instruction d'ordre et d'affichage. Les cellules `tal-submission` restent canoniques, y compris le commentaire technique d'injection de l'URL : cette exception contractuelle à l'allègement des explications de fabrication est documentée ici pour protéger la distribution. Leurs sources et commentaires restent inchangés. Les rappels locaux « pour vérifier », exemples à prédire et contraintes de résultat restent dans chaque question, même lorsqu'ils contiennent les termes « retour automatique » ou « autoévaluation ».

## Matrice par question et par activité

Chaque ligne ci-dessous est **obligatoire** et **CONSERVÉE** dans le même fichier et les mêmes cellules. Les données, productions et critères sont ceux des énoncés sources : aucune paraphrase de cette table ne les remplace. Les notions sont introduites dans les cellules de cours précédentes, avec les exemples et essais associés ; le nettoyage ne modifie ni ces prérequis ni l'autonomie demandée. Toutes les cellules Markdown locales non chronométrées et toutes les sources de code d'activité restent identiques.

| Fichier | Question, objectif/activité | Énoncé (cellule) | Réponse (cellule et identifiant) | Exemples / essais / vérifications conservés (cellules) |
|---|---|---|---|---|
| `TD1` (`TD1_S1_variables_types.ipynb`) | Q1 — Exercice 1 — Calculer un coût de traduction | 10 | 11, `td1-s1-answer-q1` | 8 (example) ; 9 (practice) |
| `TD1` (`TD1_S1_variables_types.ipynb`) | Q2 — Exercice 2 — Identifier un type | 15 | 16, `td1-s1-answer-q2` | 13 (example) ; 14 (practice) |
| `TD1` (`TD1_S1_variables_types.ipynb`) | Q3 — Exercice 3 — Affectation ou comparaison | 20 | 21, `td1-s1-answer-q3` | 18 (example) ; 19 (practice) |
| `TD1` (`TD1_S1_variables_types.ipynb`) | Q4 — Exercice 4 — Insérer des valeurs dans une phrase | 25 | 26, `td1-s1-answer-q4` | 23 (example) ; 24 (practice) |
| `TD1` (`TD1_S1_variables_types.ipynb`) | Q5 — Exercice 5 — Convertir avant de calculer | 30 | 31, `td1-s1-answer-q5` | 28 (example) ; 29 (practice) |
| `TD1` (`TD1_S1_variables_types.ipynb`) | Q6 — Exercice 6 — Décrire une phrase personnelle | 35 | 36, `td1-s1-answer-q6` | 33 (example) ; 34 (practice) |
| `TD2` (`TD2_S1_chaines_sequences.ipynb`) | Q1 — Exercice 1 — À vous de travailler | 8 | 9, `td2-s1-answer-q1` | 7 (example) |
| `TD2` (`TD2_S1_chaines_sequences.ipynb`) | Q2 — Exercice 2 — À vous de travailler | 12 | 13, `td2-s1-answer-q2` | 11 (example) |
| `TD2` (`TD2_S1_chaines_sequences.ipynb`) | Q3 — Exercice 3 — À vous de travailler | 16 | 17, `td2-s1-answer-q3` | 15 (example) |
| `TD2` (`TD2_S1_chaines_sequences.ipynb`) | Q4 — Exercice 4 — À vous de travailler | 20 | 21, `td2-s1-answer-q4` | 19 (example) |
| `TD2` (`TD2_S1_chaines_sequences.ipynb`) | Q5 — Exercice 5 — À vous de travailler | 24 | 25, `td2-s1-answer-q5` | 23 (example) |
| `TD2` (`TD2_S1_chaines_sequences.ipynb`) | Q6 — Exercice 6 — À vous de travailler | 28 | 29, `td2-s1-answer-q6` | 27 (example) |
| `TD2` (`TD2_S1_chaines_sequences.ipynb`) | Q7 — Exercice 7 — Observer et interpréter une limite | 30 | 31, `td2-s1-answer-q7` | Observation/interprétation dans l’énoncé et la réponse |
| `TD3` (`TD3_S1_collections.ipynb`) | Q1 — Exercice 1 — Ajouter, observer, retirer | 10 | 11, `td3-s1-answer-q1` | 8 (example) ; 9 (practice) |
| `TD3` (`TD3_S1_collections.ipynb`) | Q2 — Exercice 2 — Choisir une référence stable | 15 | 16, `td3-s1-answer-q2` | 13 (example) ; 14 (practice) |
| `TD3` (`TD3_S1_collections.ipynb`) | Q3 — Exercice 3 — Construire un lexique bilingue | 20 | 22, `td3-s1-answer-q3` | 18 (example) ; 19 (practice) |
| `TD3` (`TD3_S1_collections.ipynb`) | Q4 — Exercice 4 — Parcourir le lexique | 26 | 27, `td3-s1-answer-q4` | 24 (example) ; 25 (practice) |
| `TD3` (`TD3_S1_collections.ipynb`) | Q5 — Exercice 5 — Distinguer occurrences et formes | 31 | 32, `td3-s1-answer-q5` | 29 (example) ; 30 (practice) |
| `TD3` (`TD3_S1_collections.ipynb`) | Q6 — Exercice 6 — Comparer deux vocabulaires | 36 | 37, `td3-s1-answer-q6` | 34 (example) ; 35 (practice) |
| `TD4` (`TD4_S1_boucles_conditions_comptages.ipynb`) | Q1 — Exercice 1 — Transformer chaque mot | 10 | 11, `td4-s1-answer-q1` | 8 (example) ; 9 (practice) |
| `TD4` (`TD4_S1_boucles_conditions_comptages.ipynb`) | Q2 — Exercice 2 — Filtrer selon la longueur | 15 | 16, `td4-s1-answer-q2` | 13 (example) ; 14 (practice) |
| `TD4` (`TD4_S1_boucles_conditions_comptages.ipynb`) | Q3 — Exercice 3 — Filtrer selon une lettre | 20 | 21, `td4-s1-answer-q3` | 18 (example) ; 19 (practice) |
| `TD4` (`TD4_S1_boucles_conditions_comptages.ipynb`) | Q4 — Exercice 4 — `range` et positions | 25 | 26, `td4-s1-answer-q4` | 23 (example) ; 24 (practice) |
| `TD4` (`TD4_S1_boucles_conditions_comptages.ipynb`) | Q5 — Exercice 5 — `while` avec condition d’arrêt | 30 | 31, `td4-s1-answer-q5` | 28 (example) ; 29 (practice) |
| `TD4` (`TD4_S1_boucles_conditions_comptages.ipynb`) | Q6 — Exercice 6 — Compter des formes | 35 | 36, `td4-s1-answer-q6` | 33 (example) ; 34 (practice) |
| `TD4` (`TD4_S1_boucles_conditions_comptages.ipynb`) | Q7 — Exercice 7 — Compréhension de liste | 40 | 41, `td4-s1-answer-q7` | 38 (example) ; 39 (practice) |
| `TD5` (`TD5_S1_fonctions_reutilisation.ipynb`) | Q1 — Exercice 1 — Première fonction | 10 | 11, `td5-s1-answer-q1` | 8 (example) ; 9 (practice) ; 12 (practice) |
| `TD5` (`TD5_S1_fonctions_reutilisation.ipynb`) | Q2 — Exercice 2 — Normaliser | 16 | 17, `td5-s1-answer-q2` | 14 (example) ; 15 (practice) ; 18 (practice) |
| `TD5` (`TD5_S1_fonctions_reutilisation.ipynb`) | Q3 — Exercice 3 — Compter les mots | 22 | 23, `td5-s1-answer-q3` | 20 (example) ; 21 (practice) ; 24 (practice) |
| `TD5` (`TD5_S1_fonctions_reutilisation.ipynb`) | Q4 — Exercice 4 — Traduire un mot | 28 | 29, `td5-s1-answer-q4` | 26 (example) ; 27 (practice) ; 30 (practice) |
| `TD5` (`TD5_S1_fonctions_reutilisation.ipynb`) | Q5 — Exercice 5 — Traduire une phrase | 34 | 35, `td5-s1-answer-q5` | 32 (example) ; 33 (practice) ; 36 (practice) |
| `TD5` (`TD5_S1_fonctions_reutilisation.ipynb`) | Q6 — Exercice 6 — Composer un résumé | 40 | 41, `td5-s1-answer-q6` | 38 (example) ; 39 (practice) ; 42 (practice) |
| `TD6` (`TD6_S1_fichiers_csv.ipynb`) | Q1 — Exercice 1 — Lire sans oublier de fermer | 11 | 12, `td6-s1-answer-q1` | 9 (example) ; 10 (practice) |
| `TD6` (`TD6_S1_fichiers_csv.ipynb`) | Q2 — Exercice 2 — Lignes utiles | 16 | 17, `td6-s1-answer-q2` | 14 (example) ; 15 (practice) |
| `TD6` (`TD6_S1_fichiers_csv.ipynb`) | Q3 — Exercice 3 — Lire une ligne structurée | 21 | 22, `td6-s1-answer-q3` | 19 (example) ; 20 (practice) |
| `TD6` (`TD6_S1_fichiers_csv.ipynb`) | Q4 — Exercice 4 — Normaliser une personne | 26 | 27, `td6-s1-answer-q4` | 24 (example) ; 25 (practice) ; 28 (practice) |
| `TD6` (`TD6_S1_fichiers_csv.ipynb`) | Q5 — Exercice 5 — Affiliation(s) unique(s) | 32 | 33, `td6-s1-answer-q5` | 30 (example) ; 31 (practice) ; 34 (practice) |
| `TD6` (`TD6_S1_fichiers_csv.ipynb`) | Q6 — Exercice 6 — Écrire un CSV | 38 | 39, `td6-s1-answer-q6` | 36 (example) ; 37 (practice) |
| `TD7` (`TD7_S1_expressions_regulieres_pipeline.ipynb`) | Q1 — Exercice 1 — Rechercher | 12 | 13, `td7-s1-answer-q1` | 10 (example) ; 11 (practice) |
| `TD7` (`TD7_S1_expressions_regulieres_pipeline.ipynb`) | Q2 — Exercice 2 — Extraire plusieurs nombres | 17 | 18, `td7-s1-answer-q2` | 15 (example) ; 16 (practice) |
| `TD7` (`TD7_S1_expressions_regulieres_pipeline.ipynb`) | Q3 — Exercice 3 — Extraire des suites de lettres | 22 | 23, `td7-s1-answer-q3` | 20 (example) ; 21 (practice) |
| `TD7` (`TD7_S1_expressions_regulieres_pipeline.ipynb`) | Q4 — Exercice 4 — Remplacer des dates | 27 | 28, `td7-s1-answer-q4` | 25 (example) ; 26 (practice) ; 29 (practice) |
| `TD7` (`TD7_S1_expressions_regulieres_pipeline.ipynb`) | Q5 — Exercice 5 — Fonction de nettoyage | 33 | 34, `td7-s1-answer-q5` | 31 (example) ; 32 (practice) ; 35 (practice) |
| `TD7` (`TD7_S1_expressions_regulieres_pipeline.ipynb`) | Q6 — Exercice 6 — Pipeline de synthèse | 39 | 40, `td7-s1-answer-q6` | 37 (example) ; 38 (practice) ; 41 (practice) |
| `TD7` (`TD7_S1_expressions_regulieres_pipeline.ipynb`) | Q7 — Exercice 7 — Limite méthodologique | 45 | 46, `td7-s1-answer-q7` | 43 (example) ; 44 (practice) |

Pour les TD1 à TD5, aucune bibliothèque n'est ajoutée aux réponses ; le TD6 conserve `csv` et la préparation fournie avec `pathlib`, le TD7 conserve `re`. `IPython.display` reste seulement un outil de restitution fourni. Au TD2, toutes les traces Q1b–Q7b, prédictions, observations et justifications sont conservées. Les 45 questions principales comprennent 6+7+6+7+6+6+7 questions ; les 44 exemples fournis, 52 cellules d'essai/vérification/synthèse, deux préparations fournies et sept restitutions restent présents. Les réponses conceptuelles et essais figurant dans une même cellule de réponse restent également exigés.

Les synthèses spécifiques sont intégralement conservées : TD1 cellule 37 (valeur/type, affectation/comparaison, chaîne/nombre), TD2 cellule 32 (chaîne/liste, borne exclue, limite de `split()`), TD3 cellule 38 (choix de collection, intersection/différence), TD4 cellule 42 (bornes, filtres, initialisation), TD5 cellules 43–44, TD6 cellules 40–41 et TD7 cellules 47–48 (choix d'un test, explication, difficulté persistante). Aucune durée n'est un critère d'acceptation pédagogique.

## Vérifications et relais

Avant conception : cette matrice doit être relue et acceptée par un intervenant distinct du Prof ; l'accord de l'utilisateur constitue l'arbitrage sur les notices et durées, sans suppression d'activité. Le Designer peut ensuite appliquer uniquement les transformations définies ici.

Après conception, les preuves attendues sont : comparaison JSON avec `590b9a6` des identifiants/ordre/types/métadonnées/sorties, identité de toutes les cellules de code hors seul commentaire de notice TD2 (AST identique), conservation des 45 réponses et des 44 exemples/52 essais, conservation des préparations et restitutions, identité des deux contextes cachés et du profil tuteur de chaque support. Aucun code étudiant n'est exécuté. La validation nbformat, les vérifications de distribution et les tests existants pertinents complètent ces preuves sans les remplacer.

TAL-Pedagogy-Reviewer vérifie indépendamment toutes les questions et essais, puis rend son verdict de couverture. TAL-Editorial-Reviewer relit tous les passages visibles, commentaires inclus, et rend son verdict distinct de lisibilité. L'Étudiant-Modèle relève les ambiguïtés de lecture par question avec les seuls supports autorisés. Les preuves techniques sont auditées indépendamment. La gouvernance vérifie la matrice préalable, l'arbitrage déjà fourni et les verdicts spécialisés ; l'intégration qualifie la préparation de la PR, sans fusionner ni valider les autres écarts de l'audit S1.

Risques à surveiller : supprimer par recherche globale une consigne locale légitime ; effacer le rappel actif du TD2 en même temps que sa notice d'identité ; altérer l'identité métier de Q4 au TD6 ; déplacer implicitement les essais après réponse ; multiplier les présentations générales en voulant ajouter un renvoi. Aucun de ces changements n'est autorisé.

Statut de ce document : **CADRAGE PRÉALABLE ACCEPTÉ**, le 15 octobre 2026, par TAL-Pedagogy-Reviewer (`/root/s1_pedagogy_review`), intervenant distinct du Prof, avant toute modification de notebook. Le reviewer a lu la matrice intégralement et vérifié physiquement les 45 réponses, 44 exemples, 52 cellules d'essai, deux préparations et sept restitutions. La première étape de prévalidation porte sur l'empreinte `fbfcc1238b461d6cabe141f8404def7c32e23177e991d43cb87a9ae004ba72ab`. Le même reviewer a ensuite relu la correction de provenance de l'audit local non livré et maintenu son ACCEPT, sur l'empreinte `fa9483e94fdd06992d745033e29110ae326e709dad9794b02692bb352c82dca4`, avant ajout du présent paragraphe d'attribution. Le Designer a été lancé après l'ACCEPT initial et cette correction de provenance. Aucun ajustement de périmètre demandé. Cette acceptation autorise la conception dans le périmètre défini ; elle ne valide pas les notebooks futurs et ne lève pas le verdict global NON_CONFORME de l'audit S1.
