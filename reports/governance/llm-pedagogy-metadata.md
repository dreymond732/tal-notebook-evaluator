# Audit de gouvernance — tutorat dans les métadonnées

## Périmètre et verdict

**Verdict : CONFORME pour la préparation d'une PR en brouillon.** Ce verdict
ne vaut ni validation effective du comportement de Colab, ni `READY_TO_MERGE`,
ni autorisation de fusion ou de déploiement.

Audit du lot `code/llm-pedagogy-metadata`, sur la base S1
`639a0481e03a215750d641b1d35d0801fd58012e` de
`origin/pedagogy/s1-complete-tds` (PR #6). La future PR doit cibler cette branche
S1 pour isoler ce lot des changements antérieurs. La branche de travail est
distincte de `main` ; l'auditeur n'a effectué aucun commit, push ou déploiement.

L'enseignant a validé le pilote TD1 S1, TD0 S3 et contrôle S1, avec protection
du retour de l'application en contrôle. Son dernier arbitrage impose la fusion
des instructions dans les métadonnées seules, un questionnement simplificateur
après demande de solution ou copie d'énoncé, et la possibilité d'un mini-cours
avec exemple conforme aux notions déjà introduites. L'interdiction de produire
du code au S1 et le refus de toute assistance en contrôle restent applicables.

Références normatives lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et
`docs/agents/TAL-Governance-Auditor.md`.

## Séparation des rôles et relais

| Rôle et agent | Production ou contrôle | Preuve du relais |
|---|---|---|
| TAL-Prof — `prof_audit` | Politique, manifeste des séances et index dans `docs/pedagogy/` | Matrice source → cible dans `TUTORING_POLICY.md`, règles et correspondances par exercice ; aucune modification des sujets |
| TAL-Pedagogy-Designer — `designer_metadata` | Génération des métadonnées des trois notebooks pilotes | Relais final : régénération réussie, `--check` réussi, cellules identiques à la base |
| TAL-Code-Architect — agent parent | Générateur, tests structurels et documentation technique | `app/tutor_metadata.py`, `tests/test_tutor_metadata.py`, `docs/TUTOR_METADATA.md` ; pas de validation de sa propre production |
| TAL-Code-Architect — `architect_audit` | Routes, reçu public, tests et documentation du retour de contrôle | Relais de production : quatre fichiers assignés, 19 tests alors réussis, limites de persistance et restitution décrites |
| TAL-Code-Auditor — `review_code` | Revue technique indépendante en lecture seule | `ACCEPT` final après nouvelle exécution des 30 tests et vérifications décrites ci-dessous ; aucun fichier modifié |
| TAL-Pedagogy-Reviewer — `review_pedagogy` | Revue pédagogique indépendante en lecture seule | `ACCEPT` final et `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` après correction TAL-PED-001 ; aucun fichier modifié |
| TAL-Governance-Auditor — `governance_review` | Audit des règles, preuves et relais | Écriture limitée au présent rapport ; aucune modification du produit audité |

Ces relais ont été reçus dans la session de travail. Le présent rapport en
consigne le contenu utile ; il ne prétend pas qu'ils ont déjà été publiés comme
revues GitHub. Les deux verdicts spécialisés proviennent d'agents distincts des
producteurs. La restitution des contrôles change le comportement de
l'application : le lot a donc suivi le flux mixte avec les deux revues.
Les fichiers structurants de gouvernance et les signatures des correcteurs
ne sont pas modifiés.

## Preuves examinées

| Vérification | Résultat et provenance |
|---|---|
| Matrice et arbitrages avant adaptation | Matrice source → cible présente dans `docs/pedagogy/TUTORING_POLICY.md`, contrôlée par le Reviewer et relue par la Gouvernance. Les anciennes autorisations génériques sont remplacées selon la décision de l'enseignant ; aucune activité étudiante supprimée |
| Conservation des sujets | Comparaisons indépendantes Reviewer, Code-Auditor et Gouvernance : égalité profonde de toutes les cellules avec `HEAD`, soit 14 cellules TD1 S1, 17 TD0 S3 et 69 DevoirS1. La preuve porte sur leur contenu complet, pas seulement sur leur nombre |
| Métadonnées exclusives | Un contexte `metadata.colab.aiContexts` par pilote, complété par la fiche `metadata.tal_tutor`. Aucun bloc d'instructions ajouté aux cellules. Le Code-Auditor constate la conservation des métadonnées étrangères au tutorat |
| Synchronisation des profils | `python app/tutor_metadata.py --check` observé par les trois réviseurs : succès, respectivement 3 648, 4 106 et 955 caractères. Le budget de 4 400 caractères est explicitement une précaution du projet, sans revendication d'une limite Colab documentée |
| Correspondance titre d'exercice / marqueur de réponse | Réserve indépendante TAL-PED-001 corrigée : Exercice 2 S3 → Q2/Q3, Exercice 3 → Q4, Exercice 4 → Q5, Exercice 5 → Q6, Exercice 6 → Q7. Politique, manifeste et métadonnées régénérées ; test ciblé ajouté. Reviewer : `ACCEPT` après relecture |
| Politique pédagogique | Reviewer : quiz à une question par échange, diagnostic et retour aux bases, mini-cours, aucun code S1, exemple distinct et borné après échange au S2/S3, refus sans quiz en contrôle. Pas de réponse ou corrigé ajouté. R0 conditionnel conservé |
| Tests techniques | Code-Auditor : 30 tests `unittest` observés réussis après le dernier correctif. Couverture ciblée : génération, migration, périmètres, routes GET/POST, erreurs, persistance, TD et préfixe proxy |
| Absence d'exécution du code étudiant | Code-Auditor : revue du chemin de traitement et essai ad hoc sur quatre routes de contrôle avec leurs vrais correcteurs ; une cellule contenant `raise AssertionError` n'est pas exécutée. La Gouvernance constate que le générateur manipule uniquement du JSON et du texte |
| Retour des contrôles | Code-Auditor : essais réels sans mocks sur quatre routes, reçu public seul et rapport privé conservé. Une métadonnée étudiante `activity=td` ne change pas le mode serveur. Masquage des erreurs et échecs de persistance vérifié par les tests |
| Secrets et périmètre | Aucun ajout de secret ou d'identité étudiante constaté dans les fichiers audités. Pas de nouvelle route publique de rapport. Aucune modification de fichier de gouvernance, d'infrastructure ou de déploiement dans le lot |

Les résultats techniques détaillés ci-dessus sont les observations transmises
par l'auditeur indépendant. La Gouvernance a elle-même relu les règles, la
politique, le manifeste, les modifications des routes, le reçu et le générateur,
et a exécuté la vérification de synchronisation et les comparaisons des cellules.
Elle n'a pas réexécuté l'intégralité de la suite ou les essais POST ad hoc.

## Risques et conditions restant ouverts

- **Colab réel : `NOT_TESTED`.** Ni activation du profil, ni persistance après
  copie/import/export, ni obéissance effective du LLM n'ont été constatées dans
  Colab. Le protocole manuel figure dans `docs/TUTOR_METADATA.md`. Les tests
  Python ne peuvent remplacer ces essais. Les métadonnées modifiables par un
  étudiant ne constituent pas un verrou d'examen.
- **Progression globale : hors de ce pilote.** La refonte complète S1, son
  articulation S2/S3 et l'alignement du contrôle historique avec cette future
  progression ne sont pas certifiés par le verdict pédagogique présent.
- **Deux supports S2 ambigus : arbitrage enseignant restant.** `td2-S2` et
  `td4-S2` portent des titres de contrôle dans leurs notebooks ; le serveur les
  traite provisoirement comme des contrôles. Leur statut et le semestre annoncé
  sont documentés dans `docs/CONTROL_FEEDBACK.md`. Toute reclassification exige
  une décision explicite avant activation en enseignement.
- **Persistance historique non transactionnelle.** Un échec tardif peut laisser
  des éléments partiels ; le reçu positif est réservé au succès. La restitution
  après clôture reste manuelle et individuelle, sans nouvelle authentification
  ou route publique.
- **Reverse proxy extérieur non audité.** L'absence de route Flask publique ne
  prouve pas que les répertoires de soumissions sont inaccessibles par une autre
  configuration du serveur. Aucun déploiement n'a été effectué.

## Relais demandé à l'intégration

Conserver la PR en brouillon, porter les deux verdicts spécialisés et les limites
ci-dessus dans son descriptif, et vérifier que le diff cible bien la branche S1.
Un Integration-Master indépendant devra contrôler les pièces avant son propre
verdict. Si l'intégration est assumée par un producteur de ce lot, utiliser
`MAINTAINER_REVIEW`, conformément à `AGENTS.md`. La fusion et la mise en
production restent sous décision du mainteneur. Aucun `READY_TO_MERGE` n'est
émis par la Gouvernance.
