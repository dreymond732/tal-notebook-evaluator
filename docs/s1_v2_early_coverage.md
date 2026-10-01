# S1 v2 — Réalisation pédagogique des TD1 à TD4

## Mission et base

Rôle : TAL-Pedagogy-Designer. Branche `pedagogy/s1-progression-evaluation-v2`, référence `322abf53`. Mise en œuvre de la matrice `docs/pedagogy/s1_progression_v2_coverage.md` après validation explicite de l’orchestrateur. Contrat détaillé : `docs/pedagogy/s1_progression_v2_spec.md`. L’enseignant interdit toute réduction de l’étayage existant.

## Couverture livrée

| TD | Cellules avant → après | Activités originales | Ajouts obligatoires non notés |
|---|---:|---|---|
| TD1 | 16 → 36 | Six questions, données et productions conservées | Six blocs notion → exemple distinct → prédiction et essai : affectation/calcul, types, comparaison/conjonction, interpolation, conversion, longueur/présence. |
| TD2 | 20 → 21 | Sept questions et sept traces complémentaires ; tous textes pédagogiques mot pour mot | Seulement une notice de contrat ; aucune activité ni explication réécrite. |
| TD3 | 17 → 38 | Six questions et données conservées | Six blocs : états append/pop, tuple, dictionnaire, introduction de for/items/déballage avant Q4, occurrences/types, comparaison d’ensembles ; convention bilingue explicite. |
| TD4 | 19 → 42 | Sept questions et données conservées | Sept blocs : accumulation, filtres, casse, bornes de range et parcours inverse, terminaison while, deux écritures du comptage, équivalence boucle/compréhension. |

Les exemples utilisent d’autres données que les questions notées. Les cellules d’essai ne sont pas optionnelles : elles demandent une prédiction, une manipulation courte et une explication. Les trois TD enrichis annoncent 8 minutes de démarrage, 102 minutes d’activités (exemples et essais inclus), 10 minutes de synthèse/restitution. Les 120 minutes du TD2 sont inchangées. Ces durées restent une hypothèse à éprouver en classe.

## Conservation et contrats

- Identifiants et ordre relatif de toutes les cellules originales conservés. Leur source demeure un préfixe exact, sauf le contexte tuteur géré synchronisé sur le manifeste. Le TD2 conserve aussi son contexte tuteur puisque sa session n’a pas changé.
- Identité : ajout de `numero_etudiant` en suffixe de la cellule originale, y compris après les commentaires de rappel du TD2. Racines TAL v2, mêmes identifiants d’évaluateurs.
- TD1 Q6 : ajout de l’affichage fourni `Résultat Q6b` avec `repr(phrase)` ; la phrase reste libre. `repr` est expliqué comme trace de vérification, sans nouveau point.
- TD3 : ajout Q1a immédiatement après l’ajout et avant le retrait ; Q2b tuple complet ; Q3b lexique complet ; Q5b ensemble complet. Les instructions originales restent intégrales, les traces sont ajoutées en suffixe de leur cellule.
- Convention TD3 Q3 : les traductions retenues sont précisées dans une cellule distincte, avec les deux possibilités « langue » et « langage » ; la limite contextuelle de cette convention est indiquée.
- Les 19 cellules `practice` portent une liaison `tal_review.question` vers Qn. Leurs identifiants TAL sont distincts (`essai-qN`), comme ceux des `example` et des compléments `prompt`. Elles ne fournissent aucune preuve à la notation automatique.
- Tuteur synchronisé uniquement pour ces quatre notebooks : métadonnées et première cellule, règle S1 sans code fourni par le tuteur maintenue, exercices et entraînements reliés au périmètre.
- Dernière cellule de restitution HTML conservée exactement, avec `__TAL_PUBLIC_URL__`. Aucun hôte ajouté aux sources ; aucune exécution ni sortie préremplie.

Aucun élément pédagogique historique supprimé, déplacé ou rendu facultatif. Les nombres de questions notées restent 6, 7, 6 et 7.

## Vérifications du producteur et relais

Vérifications locales : syntaxe Python des cellules (sans exécuter les notebooks), unicité des identifiants, présence des métadonnées, conservation par comparaison au JSON source, absence de sorties préremplies. Les tests du correcteur et les contrôles de distribution relèvent de l’intégration.

Risque restant : une durée de préparation ne garantit pas le rythme effectif d’un groupe ; aucun temps étudiant n’a été mesuré. La correction automatique contrôle des traces et ne remplace pas la relecture des explications. Les exemples rédigés par l’enseignant dans le support ne modifient pas l’interdiction pour le tuteur S1 de donner du code.

Verdict demandé aux réviseurs indépendants : conformité de la conservation, progressivité, couverture des nouvelles notions, distinction entraînements/preuves notées et adéquation des traces au contrat v2. Ce document est un handoff de réalisation, pas une auto-validation pédagogique.

## Reprise après revue TAL-PED-001

TD4 Q4 : l’atelier introduit désormais explicitement `%` comme reste de division, puis la parité par reste nul modulo 2. L’exemple emploie 13 (division par 5 puis test de parité) et l’essai demande les restes de 8, 9 et 10. Ces observations sont incluses dans les 15 minutes prévues pour Q4. Aucun contenu, essai ou objectif préexistant n’est réduit ; sources historiques et métadonnées conservées. Ce complément rend enseignée l’alternative déjà admise par le contrat et le périmètre du tuteur.
