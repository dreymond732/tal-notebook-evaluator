# Gouvernance — Contrôle final S1, périmètre TD1 à TD5

**Verdict : `CONFORME`.**

Audit indépendant du 19 novembre 2026, rôle `TAL-Governance-Auditor`, agent `governance`. Ce réviseur n'a produit ni sujet, ni correcteur, ni tests, ni corrigé ; son écriture est limitée au présent rapport. Le verdict porte sur le lot de travail examiné, avant publication de la PR. Il ne vaut ni fusion, ni déploiement, ni `READY_TO_MERGE`.

## Mandat et référence

- Branche observée : `pedagogy/controle-s1-td1-5`.
- Base observée : `2445c9e18357dc6a99a8e516bf0d7bd7e462fd42`.
- Décision enseignante : après présentation des quatre substitutions Q5/Q24/Q25/Q30 et des incohérences du sujet et du correcteur, l'enseignant demande « oK Applique ces corrections ». Cette autorisation couvre les retraits ciblés de notions au profit des TD1–TD5 et du DM.
- Sources normatives lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/agents/WORKFLOW.md`, `docs/agents/TAL-Governance-Auditor.md` et `docs/EVALUATOR_CONTRACT.md`.
- Matrice préalable examinée : `docs/pedagogy/controle_s1_td1_5_coverage.md`. Elle identifie les références historiques et techniques, les 30 questions, les quatre objectifs retirés, leurs remplacements approuvés, les poids conservés et les limites de la preuve technique. Sa rédaction avant adaptation est déclarée dans le relais du Prof/Designer ; aucune nouvelle approbation sur une réduction non annoncée n'est inférée.

## Lot et séparation des rôles

| Zone | Production et revue constatées | Conclusion |
|---|---|---|
| Sujet `Notebooks contrôles finaux/DevoirS1.ipynb` et matrice | Agent `subject`, rôles Prof puis Designer ; revues indépendantes `pedagogy_review` et `editorial_review` | Séparation producteur/réviseurs respectée |
| Correcteur, catalogue et validation du contrat | Architecte principal ; revue indépendante `code_audit` | Flux mixte appliqué |
| Tests nouveaux et adaptations des tests existants | Architecte et agent `integration_tests` ; auditeur code indépendant | Contrats v2 et protections historiques conservés explicitement |
| Modèle et lecture préalable | Agent `model_solution`, sans accès au correcteur ni aux tests selon son relais ; écritures dans `Corrigés modèles/Contrôles finaux/controle-s1-v2/` | Modèle séparé de la distribution, sans sortie fabriquée |
| Rapport éditorial | Écriture limitée à `reports/editorial/controle-s1-td1-5.md` par `editorial_review` | Permission du rôle respectée |
| Gouvernance | Présent rapport, sans modification des fichiers audités | Indépendance respectée |

Les actifs normatifs `AGENTS.md`, la matrice de permissions et `docs/agents/` ne figurent pas dans le diff. Les règles auditées n'ont pas été changées pour lever un blocage. La branche principale n'a pas été modifiée dans cette mission. Les données de test ajoutées emploient une identité fictive et une adresse de distribution neutre ; aucun secret n'est introduit dans les changements examinés.

## Contrat déclaré et observations

Le changement est un **`CHANGEMENT_DE_CONTRAT`**, explicitement documenté dans `docs/controle_s1_v2.md` et la matrice : sujet et catalogue `Controletilt-s1` passent ensemble en version 2 ; l'identifiant de l'évaluateur reste stable.

- Les substitutions Q5/Q24/Q25/Q30 correspondent aux propositions acceptées ; aucune correction rédigée supplémentaire n'est demandée.
- Les incohérences Q3/Q4/Q15/Q18/Q22/Q29 sont corrigées dans le même lot. Les autres retouches sont des clarifications locales, sans nouveau cours ou bibliothèque exigés.
- Le total est cohérent : Q1–Q25 à 1 point, Q26–Q30 à 2 points, identification à 1 point, soit **36 points**. Les poids des questions ne sont pas réduits.
- Les 70 identifiants de cellules sont identiques à la base. La première cellule, le profil `tal_tutor` et les contextes Colab sont identiques à la base : titre visible et refus de toute assistance de contrôle restent conservés.
- Le contrôle v2 exige sa cellule d'identité et ses 30 cellules de réponse. Les anciennes copies v1 ou sans métadonnées sont refusées sur les deux routes, avant correction et persistance. Aucun numéro étudiant nouveau n'est imposé.
- Q2 lit la trace canonique, puis vérifie la tranche sur une chaîne de référence connue. Les bornes négatives ou calculées ne sont pas exclues par un critère caché ; cette évolution est maintenant décrite dans la matrice et la documentation technique.
- Les booléens ne sont pas assimilés aux entiers ; effectifs et longueurs sont comparés exactement. Les listes gardent leur ordre et les dictionnaires n'imposent pas celui des clés.
- La correction ne contient aucun appel exécutant le code déposé. Les fixtures comportent volontairement un code inerte qui échouerait s'il était exécuté ; seules leurs traces synthétiques sont lues.
- Le retour public demeure un reçu. Les essais de routes vérifient le rapport privé et l'absence de score ou solution dans le reçu.
- L'ancien corrigé `Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` reste un historique v1 inchangé, explicitement distingué du modèle v2 dans la documentation. Les archives de soumission ne sont ni migrées ni renotées.

## Revues spécialisées reçues

Ces verdicts viennent des agents indépendants nommés ; le présent audit ne les remplace pas :

| Revue | Verdict | Preuve et clôture |
|---|---|---|
| Pédagogique, `pedagogy_review` | `ACCEPT` / `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` | Lecture des 30 questions et des acquis TD1–TD5/DM ; complément après lecture du modèle. Le faux négatif Q2 a été corrigé et le blocage levé. La réserve Q28 est non bloquante : les stratégies brute ou normalisée satisfont les seuls cas annoncés et sont admises. |
| Éditoriale, `editorial_review` | `ACCEPT` / `LISIBILITÉ_ÉTUDIANTE_VALIDÉE` | Rapport `reports/editorial/controle-s1-td1-5.md`, lecture des 70 cellules et rapprochement de la lecture étudiante ; coquille Q10 et tournure Q17 constatées corrigées. |
| Technique, `code_audit` | `ACCEPT` | Relais indépendant : 14 tests ciblés et 56 tests de régression réussis ; constats sur nombres proches mais faux et sorties mal formées corrigés puis revérifiés ; 30 solutions du modèle concordantes à lecture statique. |

Aucun verdict négatif non résolu ne subsiste dans les relais reçus. Les verdicts de couverture et de lisibilité sont distincts de la réussite des tests.

## Vérifications observées et reproduites

**Reproduites par le présent auditeur**, sans exécution des cellules d'un notebook :

- `python -m unittest discover -s tests -p test_controle_s1_v2.py -q` : **14 tests, OK**.
- `python app/tutor_metadata.py --check` : sortie de contrôle du tuteur réussie, code de sortie 0.
- `python app/prepare_student_notebooks.py check` : **46 notebooks, check OK**.
- `TAL_PUBLIC_URL=https://example.test/universite/tal python app/prepare_student_notebooks.py verify --output-dir .../distribution-s1` : **46 notebooks, verify OK** sur la distribution de contrôle fournie.
- `git diff --check` : réussi.
- Comparaison JSON indépendante sujet/base : 70 identifiants, première cellule et deux contextes du tuteur conservés.
- Source et modèle : toutes les cellules de code sont sans sorties et avec `execution_count=null` ; les 31 cellules de code résolues du modèle se parsèment par AST. Cette analyse ne les exécute pas.

**Observé dans le journal final du producteur**, sans revendiquer une seconde exécution par la gouvernance :

- `python -m unittest discover -s tests -v` : **486 tests en 16,540 s, OK**, journal `controle-s1-tests-final.log` de la session.
- Le relais de l'architecte indique également compilation `compileall`, génération de 46 notebooks et vérification de la distribution neutre réussies. Le présent audit a reproduit la vérification de distribution, pas sa génération.

Empreintes observées après les derniers ajustements cosmétiques du modèle :

- Sujet : SHA-256 `033339bc1e14ced85638919998df45aed92c6c74e14426d66e90902f7aa9d13d`.
- Modèle : SHA-256 `d0626cecf6cb8e86286e0704a833b9237e47b12524bf1dbd6d5c16c7b470b744`.
- `lecture_etudiante.md` contient bien l'empreinte courante du sujet.

## Limites et relais d'intégration

La suite vérifie des données synthétiques, des traces injectées et des dépôts temporaires. Elle ne démontre ni l'authenticité d'une sortie étudiante, ni la généralité d'une fonction, ni le comportement du tuteur dans Colab. Le sujet et le modèle n'ont pas été exécutés dans Colab ; aucune durée réelle en classe n'a été mesurée. La réserve Q28 demeure une limite de généralisation annoncée, sans nouveau critère rétrospectif.

Aucun essai sur le serveur de production, fusion ou déploiement n'est réalisé par cette revue. L'intégration auto-produite doit conserver le statut **`MAINTAINER_REVIEW`** ; seul le mainteneur décide de fusionner et de redistribuer le sujet v2. Le présent `CONFORME` autorise la poursuite vers cette revue d'intégration sans constituer cette décision.
