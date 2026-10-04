# Reprise éditoriale des sept TD S1 — vérification technique

## Périmètre et référence

Branche `pedagogy/s1-editorial-complete`, référence exacte `670e6c104a6d0228fcad8a91cfc8776117b038bb` (main intégrant le lot S3). Rôle producteur : TAL-Code-Architect. Ce rapport fournit des preuves techniques à soumettre au Code-Auditor ; il ne constitue pas une validation indépendante ni une validation pédagogique.

Les sept TD ont déjà leur correcteur actif. Aucun nouveau correcteur, changement de version, barème, jeu de données, marqueur ou règle de validation n’est nécessaire pour la réécriture. Les 45 questions restent sous contrat v2.

## Alignement relu

| Support | Contrôle des productions enregistré par question | Limite explicitée |
|---|---|---|
| TD1, Q1–Q6 | Prix numérique avec tolérance ; type float ; deux booléens ; f-string ; conversion int ; longueur/appartenance cohérentes avec la phrase personnelle et son repr | Les références portent sur les exemples imposés ; aucune preuve de compréhension |
| TD2, Q1–Q7 | Deux traces par question ; valeurs, types, index/tranches, méthodes strip/lower/replace/split/join reliées aux affichages ; Q6 traite explicitement trois indices | Q7 vérifie découpage et présence du commentaire, jamais son sens |
| TD3, Q1–Q6 | États append/pop ; tuple/type ; lexique avec langue ou langage ; parcours items ; cardinalités et ensembles ; intersection/différence | Justification du tuple : présence seulement ; ordre d’ensembles libre |
| TD4, Q1–Q7 | for/upper ; filtres ; range ; while/incrément ; comptage ; compréhension filtrée | Une trace juste sur ces données ne démontre pas la généralité du programme |
| TD5, Q1–Q6 | Fonctions appelées et return ; strip/lower ; réutilisation de normaliser ; traduction connue/inconnue ; split/join ; dictionnaire de synthèse typé | Analyse statique des dépendances, pas exécution ni exploration exhaustive des entrées |
| TD6, Q1–Q6 | Lecture with/UTF-8 ; splitlines ; split limité ; title et tests de graphie ; dictionnaire d’ensembles ; CSV relu, colonnes et effectifs | Normaliser un nom ne garantit pas l’identité ; ordre des personnes/affiliations libre |
| TD7, Q1–Q7 | Recherche insensible à la casse ; nombres ; lettres accentuées ; date ; étapes de nettoyage ; pipeline ; présence d’une limite | La qualité des commentaires Q3/Q7 n’est pas autocorrigée |

Les tests indépendants existants couvrent 38 réponses des TD1 et TD3–TD7, ainsi que les sept questions de TD2. Les variantes déjà acceptées comprennent ordre des ensembles, langue/langage, apostrophe droite/courbe, incrément simple/augmenté, comptage avec if/get, split positionnel/nommé, recherche avec option ou texte normalisé. Les constructions expressément exigées (for, while, f-string, items…) restent exigées : une autre construction peut produire le même résultat sans remplir cet objectif. Aucune nouvelle variante valide refusée n’a été établie dans cette revue ; ceci ne démontre pas l’exhaustivité du moteur.

## Défaut concret corrigé : charge de relecture annoncée

Le correcteur TD2 disait que le commentaire « reste à relire avec l’enseignant » ; les sept TD annonçaient `relecture_humaine='requise'`. Cela contredisait le principe de travail autonome demandé. Les retours orientent maintenant vers les critères du TD et une sollicitation en cas de difficulté. La valeur persistée devient `facultative`, déjà utilisée par le rendu des productions S3. Les traces restent disponibles à l’enseignant.

Fichiers concernés : `app/app_correction_TD2_S1.py`, `app/s1_revision.py`, `app/s1_reference.py`. Modification de messages et d’un indicateur de restitution, sans modification des valeurs acceptées, constructions vérifiées ni points. Le moteur partagé ne change cet indicateur que pour les sept identifiants S1 : les TD et contrôles S2 conservent `requise`. Le DM S1 et les autres contrôles sont hors de cette modification.

## Conservation mesurée et adaptation du test antérieur

L’ancien `test_s1_progression_preservation.py` imposait que chaque prose révisée commence par toute la prose historique ; il exigeait également que toutes les sources de TD2 restent identiques. Ces deux assertions empêchaient directement la séparation cours/exemples/énoncés autorisée par le mainteneur. Elles sont remplacées par des contrôles ciblés, et non supprimées au motif de faire passer des tests :

- la fixture historique `s1_progression_v2_source_baseline.json` demeure intacte et les IDs/métadonnées TAL de ses activités sont vérifiés ;
- la nouvelle fixture `s1_editorial_source_baseline.json` contient les sept fichiers exacts de main au commit de référence, extraits par `git show` avant rédaction ;
- tous les anciens IDs restent dans leur ordre, sans doublon ; les 45 cellules de réponse et les métadonnées restent intactes ;
- l’AST de **tout code préexistant**, et pas uniquement des réponses, demeure identique ; les affichages commentés fournis dans les réponses sont également comparés par AST ;
- la restitution générée et les champs racine restent identiques, hors emplacements dédiés du tuteur soumis à leurs contrôles indépendants.

Ce test ne mesure pas l’équivalence du texte du cours. Celle-ci exige la matrice et les revues pédagogiques/éditoriales par question. Les commentaires de code peuvent être clarifiés ; les données et opérations exécutables ne peuvent pas être changées silencieusement.

Une exception précise concerne `td6-s1-answer-q6` : l’ancien affichage multiligne commenté, que le sujet demandait déjà de laisser désactivé, est retiré pour supprimer une consigne contradictoire. L’affichage `repr(...)` fourni pour le contrat v2 demeure inchangé et vérifié. Le test autorise seulement la suppression de l’AST exact de cet ancien `print`, dans ce fichier et cette cellule ; aucun autre affichage ne bénéficie de cette exception. Cet ajustement de test a été produit par l’intégration et accepté séparément par le Code-Auditor.

## Vérifications réalisées

Avec `/tmp/tal-check-venv/bin/python` : 34 tests `test_s1*.py`, 16 tests `test_td2_s1.py` et 29 tests `test_s2*.py` réussissent lors du contrôle initial. Les deux tests ajoutés vérifient les sept vrais correcteurs (score Q1 conservé, relecture facultative, preuves accessibles) et tous les identifiants S2 du moteur partagé (relecture obligatoire inchangée).

Ces nombres sont des résultats techniques initiaux ; le lot éditorial final doit repasser ces contrôles et la suite complète après intégration. Le serveur n’exécute jamais les réponses soumises. La fraîcheur/authenticité des sorties, la compréhension, la durée réelle et le comportement du tuteur Colab ne sont pas certifiés.

## Validation finale d’intégration — 4 octobre 2026

La suite complète réussit : **295 tests**. Les 35 profils du tuteur passent le contrôle de synchronisation ; les 34 supports actifs passent `check`, puis `render` et `verify` avec une adresse neutre. Les sept TD S1 passent nbformat et l’analyse syntaxique de toutes leurs cellules de code. Les sorties des sources restent vides.

L’intégration a exécuté **44 exemples et deux préparations fournis**, dans un répertoire temporaire distinct pour chaque notebook. Aucune réponse ni cellule d’entraînement à compléter n’a été exécutée. Les fichiers des démonstrations CSV restent hors dépôt. Le Code-Auditor a reproduit indépendamment cette vérification et 79 tests ciblés.

**TAL-AUD-001 résolu :** le test de conservation historique S2 comparait encore les sept TD S1 à leurs anciennes empreintes. Il compare désormais ces mêmes empreintes aux snapshots du parent `670e6c1`, dont la reconstruction exacte a été vérifiée contre les sept blobs Git. Les chemins admis sont exactement ceux des sept TD S1 ; la fixture historique S2 n’a pas été modifiée et les autres fichiers restent contrôlés. La conservation des versions courantes S1 est assurée séparément par les tests d’IDs, métadonnées, AST et affichages. Cette adaptation a été produite par l’intégration et validée indépendamment par le Code-Auditor.

Le Code-Auditor rend **ACCEPT** sur le lot final. Le bilan pédagogique, la lecture étudiante et le rapport éditorial constituent des preuves distinctes ; leurs limites concernant le cours historique de 2025 restent explicites. L’intégration a participé à la production et soumet le lot sous **MAINTAINER_REVIEW**, sans fusion ni déploiement. Le résultat de CI distante doit être contrôlé après publication ; les vérifications locales ne constituent pas un succès Docker distant.
