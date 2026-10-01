# Gouvernance — consolidation des évaluateurs S3 v2

## Verdict et autorisation

**CONFORME**, le 1er octobre 2026, sur l’arbre de travail final de la branche
`code/s3-evaluation-complete-v2`, comparé à
`02f435dc770834b21e242592804d231e0836a4b7`. Ce verdict porte sur les changements
examinés et leurs preuves locales ; il ne vaut ni fusion ni déploiement.
Le relais d’intégration est **MAINTAINER_REVIEW**. La CI, notamment
`container-smoke`, reste un contrôle à observer sur le commit publié.

L’enseignant a autorisé les quatre lots proposés après l’audit complet :
identification et contrat de cellules ; bornes, occurrences, types et ordre ;
diagnostics et rapport de relecture ; conformité quantitative de TD1–TD2.
Il a demandé que les anciennes copies soient refusées avec le message exact
`mauvaise version du notebook`, sans correction ni migration. Le lot traite
quinze supports, TD0–TD7 et leurs sept contrôles, soit 104 questions.
Les trois révisions R0–R2 étaient déjà v2 : leurs sujets restent inchangés,
mais bénéficient du contrôle d’identité partagé. Les 18 évaluateurs S3
exigent maintenant le contrat v2 complet. S1/S2 ne sont pas reconçus.

## Séparation des rôles et couverture

Les sources normatives ont été lues : `AGENTS.md`,
`docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`,
`docs/agents/WORKFLOW.md` et le rôle de gouvernance. La vérification propre de
la gouvernance confirme la branche dédiée et l’absence de modification de
ces actifs ou de `tests/fixtures/notebook_migration_baseline.json`.

| Rôle et relais de session | Production, contrôle et verdict |
|---|---|
| TAL-Prof | Matrice préalable `docs/pedagogy/s3_complete_v2_coverage.md` et contrat `s3_complete_v2_spec.md`. Validation de la matrice par l’orchestrateur avant conception, attestée dans les handoffs et les documents. Aucun barème, corpus, durée, compétence ou activité supprimé ; aucune bibliothèque nouvelle. |
| TAL-Code-Architect, missions `complete_v2_core`, `complete_v2_quant`, `complete_v2_reports` | Contrats, identité et stockage ; références et validateurs ; moteurs, diagnostics et rapports. Fichiers applicatifs, tests et documentation technique dans les permissions du rôle. |
| TAL-Pedagogy-Designer, `complete_v2_designer` | Quinze notebooks et bilan `docs/s3_v2_notebook_coverage.md` ; ne valide pas son propre produit. |
| TAL-Code-Auditor, `complete_v2_independent_review` | Revue indépendante en lecture seule des changements applicatifs, nouveaux tests et adaptations, générateur de référence et stockage. **ACCEPT**, après correction et recontrôle de deux observations P2. |
| TAL-Pedagogy-Reviewer, `complete_v2_pedagogy_review` | Revue indépendante en lecture seule des sujets, matrice, barèmes, tuteurs et concordance des contrats. **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** après relecture finale des précisions TD1 Q4 et TD2 Q5. |
| TAL-Integration-Master, `complete_v2_integration` | Tests de régression, protection de migration, fixtures et documentation technique. Étant producteur de cette partie, relais **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. Le code-auditeur indépendant a également examiné cette production. |
| TAL-Governance-Auditor, `complete_v2_governance` | Lecture des normes, diff, moteurs, collecteur et templates, documents et preuves spécialisées ; seule écriture : le présent rapport dans `reports/governance/`. Aucun changement produit, commit, publication, fusion ou déploiement par ce rôle. |

Ces verdicts sont des preuves de session transmises par les agents,
directement ou par l’orchestrateur ; ce ne sont pas des reviews GitHub
prétendument déjà publiées. Aucun producteur ne délivre son propre verdict
spécialisé. Aucun Étudiant-Modèle n’a été sollicité pour accéder aux
correcteurs ou aux références.

La revue pédagogique indépendante a comparé les quinze notebooks au commit
source : **420 cellules, 104 réponses, 49 cellules de relecture rattachées**,
**37 sources enrichies par suffixe et 383 sources intactes**. Toutes les
sources enrichies conservent leur ancien texte comme préfixe. Les données,
exemples, interprétations, manipulations, essais, transferts, figures,
exports, autonomie et durées de deux heures sont préservés. Les compteurs
et sorties n’ont pas été produits en exécutant les notebooks. Les quinze
introductions et identités précisent le nouveau contrat ; sept consignes
sont enrichies. Le tuteur reste dans les métadonnées et la première cellule,
avec guidance en TD et aucune assistance en contrôle.

Les barèmes restent **6 points pour TD1, 7 pour les autres TD**, et
**20 pour chaque contrôle**, avec poids `2, 3, 3, 3, 3, 3, 3`. Le statut
provisoire, la présence d’une rédaction ou d’une figure et les points à
réexaminer ne créent ni note qualitative automatique ni changement de poids.

## Exigences et preuves examinées

| Exigence | Preuve et résultat |
|---|---|
| Contrat complet et anciennes copies | Lecture de `notebook_contract.py`, des routes et moteurs ; tests couvrant les 18 S3. Métadonnées racines v2, identité unique et toutes les cellules Q attendues requises. Version absente/périmée ou ensemble de cellules incompatible : `mauvaise version du notebook`, avant appel de correction et persistance, sur `/submit` et route directe. Aucun repli vers les cellules d’exemple ni conversion automatique. Réponses présentes mais vides distinguées d’un contrat absent. |
| Identité | Affectations littérales lues par AST, noms exacts, commentaires ignorés, champs non vides et numéro étudiant obligatoire ; doubles affectations rejetées. Numéro de 1 à 64 caractères ASCII lettres/chiffres/tiret/soulignement. Absence d’identité valide : refus sans enregistrement. |
| Conservation et homonymes | Stockage `soumissions/<évaluateur>-v2/<classe>/`, numéro dans les noms de copie et rapport, CSV v2 séparés. Tests automatisés et sonde indépendante avec les 18 vrais moteurs : 36 copies d’homonymes `E1`/`_E1` distinctes, rapports distincts, anciennes données conservées. Le code-auditeur a également constaté 36 refus v1 sans mutation des fichiers. |
| Bornes, ordre et occurrences | Régressions sur booléens interdits comme entiers, types des tags, débordements de tranches, listes ordonnées avec répétitions et préfixes attendus. TD3 exige des positions absolues valides et trois occurrences distinctes du pivot, sans confondre plusieurs fenêtres du même pivot avec plusieurs occurrences. |
| TD1–TD2 | Référence JSON figée sur les corpus prescrits, avec versions et SHA-256 ; fréquences, tailles et listes comparées aux résultats effectifs du pipeline au lieu de la seule cohérence interne. Exclusions et ex æquo autorisés conservés ; les choix libres de tokens incluent la ponctuation lorsque la consigne le permet. |
| Provenance de référence | `tests/build_s3_spacy_reference.py` est du code enseignant séparé, sur `TEXT0`, `TEXT1`, `TEXT2`, sans entrée notebook ni appel serveur. L’auditeur a recalculé toutes les références par son propre code enseignant : concordance exacte, y compris les tables complètes ajoutées après revue. Python 3.12.14, spaCy 3.8.7, `fr_core_news_sm` 3.8.0 ; dépendances et méthode documentées dans `docs/s3_spacy_reference.md`. Aucune installation spaCy ajoutée au serveur. |
| Limite linguistique | Conformité au modèle explicitement distinguée de la vérité linguistique. TD1 Q4 repère deux tokens distincts de la première phrase, mais l’analyse syntaxique reste humaine ; Q6 libre n’est soumis qu’à des invariants. La critique du modèle, les alternatives valables et les interprétations restent des activités étudiantes. |
| Diagnostics de dépendances | États conforme, incorrect, preuve absente et non vérifiable distincts. Une dépendance structurellement exploitable n’est pas bloquée uniquement parce que son score est nul. Tests : C1 avec annotation absente indique 9 points aval à réexaminer ; C2 avec annotation inexploitable en indique 12. Aucun crédit automatique ni conclusion de plusieurs erreurs indépendantes. |
| Relecture humaine | Regroupement de code, traces, commentaires et analyses associées aux questions ; 49 cellules rédigées des contrôles rattachées par `tal_review.question`. Cellules libres séparées, limites de taille et troncatures annoncées. Inventaire des formats visuels, absence d’affichage signalée sans conclure à sa qualité. Aucun appel LLM ni jugement qualitatif fondé sur des mots-clés ou la longueur. |
| Confidentialité des contrôles et HTML | Reçu public uniquement pour les contrôles ; détails et preuves dans le rapport enseignant sauvegardé. Sources et sorties textuelles échappées ; HTML/SVG soumis jamais injecté comme contenu actif. Régressions de rendu et vérification indépendante des vrais moteurs réussies. |
| Non-exécution | Moteurs lus par la gouvernance et l’auditeur : lecture JSON, AST inerte, comparaison des traces sauvegardées. Le collecteur ne lance pas le code étudiant ; exemples et préparations ne fournissent pas une réponse. Les références de modèle ont été produites uniquement par code enseignant séparé. |
| Intégrité de migration | Fixture historique originale inchangée, quinze exceptions de révision déclarées explicitement et seconde baseline figée au commit source. Les autres sujets continuent à être protégés ; les enrichissements sont testés sans réécrire la preuve historique. |
| URL et distribution | Les sources distribuables passent le contrôle sans cellule de dépôt ni adresse privée. Génération finale puis vérification de 33 copies avec adresse neutre ; cellule HTML finale présente dans les copies et 18 contrats S3 v2 vérifiés par l’intégration. L’adresse réelle est injectée depuis l’environnement lors du déploiement, sans être ajoutée aux sources Git. |

## Observations closes et vérification finale

- **TAL-AUD-001, P2** : TD2 Q5 écartait la ponctuation malgré le choix libre
  de cinq tokens. Correction avec la table complète et multiplicité des
  occurrences ; l’auditeur confirme qu’un ou trois points réellement présents
  sont acceptés, quatre refusés.
- **TAL-AUD-002, P2** : TD1 Q4 écartait un dépendant ponctuation.
  Correction avec la table complète de la première phrase, relue et testée
  indépendamment ; aucune solution n’est donnée dans le sujet.
- **TAL-PED-001, mineur** : absence d’affichage visuel non signalée.
  Mention neutre ajoutée et relue, sans transformer la présence en note de qualité.

Après ces correctifs, l’orchestrateur et le code-auditeur attestent
**200 tests réussis**, sans test ignoré. Le réviseur pédagogique a également
repassé indépendamment les **17 tests quantitatifs et 7 tests de rapport**.
Compilation, contrôles de sources et de tuteurs, et contrôle du diff réussis.
Commandes de vérification locale depuis la racine du dépôt :

```sh
env PATH=/tmp/tal-r012-venv/bin:$PATH python -m unittest discover -s tests
/tmp/tal-r012-venv/bin/python -m compileall -q app tests
/tmp/tal-r012-venv/bin/python app/tutor_metadata.py --check
/tmp/tal-r012-venv/bin/python app/prepare_student_notebooks.py check
git diff --check
TAL_PUBLIC_URL=https://example.test/universite/tal /tmp/tal-r012-venv/bin/python app/prepare_student_notebooks.py render --output-dir dist/final-s3-v2
TAL_PUBLIC_URL=https://example.test/universite/tal /tmp/tal-r012-venv/bin/python app/prepare_student_notebooks.py verify --output-dir dist/final-s3-v2
```

Résultats : **34 profils de tuteur**, **33 sources**, **33 copies générées
et vérifiées**. L’intégration a contrôlé via le client Flask `/health`
(33 évaluateurs), `/` et `/submit`, statut 200 et action de formulaire
`/universite/tal/submit` avec `X-Forwarded-Prefix`. Ce contrôle simulé du proxy
ne constitue pas un test du serveur de production.

## Limites, distribution et relais

Les traces sauvegardées ne prouvent ni leur fraîcheur, ni une exécution réelle,
ni la généralité des fonctions, ni l’autonomie de l’étudiant. Le score reste
technique provisoire ; annotations, argumentation, figures et interprétations
requièrent une relecture. L’inventaire visuel n’intègre pas les images ou le
HTML étudiants comme contenu actif : consulter la copie pour le rendu.

Docker est indisponible localement : **NOT_TESTED localement**. Les jobs CI
`contracts-and-notebooks` et `container-smoke` doivent réussir sur le commit
publié avant clôture de l’intégration. Colab réel et production sont également
**NOT_TESTED**. Aucune fusion ni mise en production n’est autorisée par le
présent verdict, et aucune n’a été effectuée pendant cette revue.

Après fusion et déploiement décidés par le mainteneur, régénérer la distribution
et **redistribuer les quinze supports révisés**. R0–R2 restent les copies v2
précédemment révisées ; la génération reconstruit néanmoins les 33 copies.
Ne pas convertir une ancienne réponse en changeant seulement son numéro de
version. L’adresse injectée est absente des sources Git, mais nécessairement
lisible dans la copie distribuée : ce mécanisme ne la masque pas au destinataire.

Absence de veto de gouvernance sur le lot examiné. Relais
**MAINTAINER_REVIEW**, sous contrôle CI et décision du mainteneur pour fusion
et production. Toute modification substantielle ultérieure exige de réexaminer
les preuves et verdicts concernés.
