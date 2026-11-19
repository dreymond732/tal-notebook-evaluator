# Gouvernance — Validation enseignante du DM S1

**Verdict : `CONFORME`.**

Audit indépendant du 19 novembre 2026, rôle `TAL-Governance-Auditor`. Le réviseur n'a produit aucun des fichiers applicatifs ou tests du lot ; son écriture se limite au présent rapport. Ce verdict ne vaut ni fusion, ni déploiement, ni validation d'une copie réelle.

## Mandat et périmètre

L'accord enseignant « ok applique ce correctif », transmis dans le mandat, approuve quatre évolutions de l'interface de correction :

1. Cinq notes humaines obligatoires pour publier ; appréciations facultatives.
2. Conservation des saisies en cas d'erreur et signalement auprès de chaque champ concerné.
3. Retour à la file après validation réussie.
4. File distinguant les scores automatique /17,75, humain /2,25 et final /20, ainsi que les états « À corriger », « Brouillon » et « Validée ».

Branche observée : `code/dm-s1-validation`, base `2445c9e18357dc6a99a8e516bf0d7bd7e462fd42`. Ce lot est séparé de la révision du contrôle final S1 présentée dans la PR65 ; celle-ci n'est pas incorporée ici.

Fichiers examinés : `app/dm_hybrid.py`, `app/teacher_routes.py`, `app/templates/teacher_dm_review_template.html`, `app/static/teacher_progress.css`, `tests/test_dm_hybrid_workflow.py`, `docs/DM_HYBRIDE_S1.md` et `reports/editorial/dm-s1-validation.md`.

Sources normatives relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et fiche `TAL-Governance-Auditor`.

## Rôles et nature du changement

Le producteur technique et les réviseurs technique, pédagogique et éditorial sont distincts selon les relais de mission. Le rapport éditorial constate explicitement qu'il n'a pas écrit le produit. Le présent auditeur n'a modifié ni produit, ni tests, ni normes.

Le contrat de **validation et publication enseignante** change : une appréciation vide n'interdit plus de publier lorsque les cinq notes sont valides. Ce changement demandé est décrit dans la documentation. Le barème humain, le calcul automatique, les consignes et explications demandées aux étudiants ne changent pas.

Aucun notebook, correcteur d'exercice, métadonnée pédagogique, catalogue ou profil du tuteur n'est modifié. Aucune compétence ou activité étudiante n'est retirée. La matrice d'adaptation de notebook et une nouvelle copie Étudiant-Modèle sont donc **sans objet** pour cette correction d'interface ; leur absence n'est pas assimilée à une dérogation aux règles d'adaptation des supports.

Les actifs normatifs et la branche `main` ne sont pas modifiés. Aucun changement de schéma SQLite, migration, suppression d'archive, renotation ou modification de copie réelle n'est introduit dans ce lot.

## Constats et preuves

| Point audité | Observation dans les changements et tests | Conclusion |
|---|---|---|
| Notes obligatoires, commentaires facultatifs | `save_review` exige une valeur pour chaque note en publication, y compris zéro ; les commentaires peuvent rester vides | Conforme à la décision ; pas de modification du barème |
| Validation numérique | Virgule ou point admis ; valeurs non numériques, non finies, négatives, hors maximum ou à plus de deux décimales refusées | Contrôle côté serveur maintenu ; le champ texte n'abandonne pas la validation |
| Transaction | Les cinq questions sont contrôlées avant les écritures ; `ReviewValidationError` déclenche le rollback ; l'ancien brouillon est conservé | Pas d'enregistrement partiel ni de publication sur erreur |
| Saisie refusée | Route HTTP422 réaffichant les valeurs brutes de tous les champs, sans les enregistrer ; messages liés aux champs avec `aria-invalid` et `aria-describedby` | Erreur localisée, données de formulaire conservées pour correction |
| Échappement | Valeurs et commentaires réaffichés par les expressions Jinja ordinaires ; test de contenu script et guillemets échappé | Pas de HTML utilisateur rendu actif dans les scénarios testés |
| Publication et navigation | Après publication réussie, redirection303 vers la file ; après brouillon, retour à la fiche ; préfixe proxy conservé | Actions distinctes et navigation cohérente |
| File et notes | Scores automatique, humain et final affichés séparément ; finale en attente avant validation ; zéro reste distingué d'une absence | Pas de brouillon présenté comme résultat final publié |
| États et lecture seule | Ligne non commencée, brouillon et validation distingués ; après validation : lien « Consulter », fiche non modifiable | État explicite, verrou de validation conservé |
| Sécurité et concurrence | Session enseignante, CSRF, validation du reçu, `progression_lock` et contrôle de copie active conservés ; transaction `BEGIN IMMEDIATE` | Pas de contournement introduit dans le périmètre relu |
| Données existantes | Schéma, tables et données historiques inchangés ; notes et commentaires existants ne sont pas convertis | Mise à jour compatible avec les brouillons enregistrés |
| Informations perdues avant correctif | Documentation indique explicitement qu'une saisie refusée et perdue avant installation n'est pas récupérée | Limite correctement annoncée |

La somme humaine en file peut être partielle lorsqu'une fiche est un brouillon ; elle ne devient une note finale qu'après validation des cinq notes. Les explications étudiantes de Q2/Q6/Q12/Q14/Q17 restent à apprécier par l'enseignant : rendre son commentaire facultatif ne rend pas ces travaux facultatifs.

## Revues indépendantes reçues

- **Technique : `ACCEPT`.** Relais de l'auditeur indépendant : tests du circuit DM, validation sous proxy et fiche en lecture seule réussis ; aucune réserve bloquante. Sa suggestion CSS a été intégrée dans les sélecteurs de saisie courants. Ce relais est distinct du résultat de la suite complète.
- **Pédagogique : `ACCEPT` / `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`.** Le commentaire facultatif est celui de l'enseignant ; aucune consigne, réponse ou justification étudiante n'est retirée.
- **Éditoriale : `ACCEPT` / `LISIBILITÉ_INTERFACE_ENSEIGNANTE_VALIDÉE`.** Rapport `reports/editorial/dm-s1-validation.md`, avec lecture des textes et des états de l'interface. Il ne revendique pas un essai visuel de navigateur ni une validation des transactions.

Le verdict éditorial porte volontairement le nom du destinataire enseignant. Il n'attribue pas artificiellement un verdict de lisibilité à un support étudiant inchangé. Aucun verdict négatif non résolu n'a été reçu.

## Vérifications effectives

Reproduites par le présent auditeur, avec la dépendance Python de test disponible, données fictives et stockage temporaire :

- `python -m unittest discover -s tests -p test_dm_hybrid_workflow.py -q` : **16 tests, OK**.
- `python app/tutor_metadata.py --check` : réussi, code de sortie 0.
- `python app/prepare_student_notebooks.py check` : **46 notebooks, check OK**.
- `git diff --check` : réussi.
- Inspection des chemins du diff : uniquement les six fichiers du lot, hors rapports ajoutés ; aucun notebook ni actif normatif modifié.

Observé dans le journal final fourni par le producteur, sans revendiquer une seconde exécution par la gouvernance :

- `python -m unittest discover -s tests -v` : **478 tests en 16,995 s, OK**, journal de session `dm-validation-tests-final.log`.
- Relais de l'architecte : compilation, contrôle du tuteur, génération et vérification d'une distribution neutre de 46 notebooks réussis. Le présent auditeur a reproduit le contrôle des sources et du tuteur, pas la génération.

Le test d'un reçu erroné a été stabilisé : il choisit maintenant un dernier caractère effectivement différent, au lieu de risquer de conserver le reçu initial lorsque celui-ci se terminait déjà par 0. L'attente HTTP404 est conservée ; ce changement ne masque pas une erreur de produit.

## Limites et décision d'intégration

Aucune copie réelle, aucun commentaire réel ni aucune note réelle n'a été saisi ou publié pendant cet audit. Aucun code étudiant n'est exécuté. Les tests couvrent le rendu HTML, les erreurs et les transactions sur des données synthétiques ; ils ne constituent pas un test visuel mobile, une vérification avec lecteur d'écran ou un essai du serveur de production.

Le correctif conserve les saisies refusées **après son installation** ; il ne récupère pas les valeurs déjà perdues auparavant. Une actualisation du navigateur seule ne déploie pas le code serveur, comme le précise la documentation.

Le lot peut poursuivre vers la PR et l'intégration avec **`MAINTAINER_REVIEW`** puisque l'intégration est auto-produite. Le présent auditeur ne rend pas `READY_TO_MERGE`. Fusion, reconstruction du service et mise en production restent sous décision du mainteneur.
