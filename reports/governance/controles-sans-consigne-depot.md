# Audit de gouvernance — contrôles sans consigne de dépôt

## Verdict et référence

**CONFORME**, le 25 septembre 2026, pour le commit `61cf77b`, branche
`pedagogy/controles-sans-consigne-depot`, comparé à `origin/main` `2572972`.
Ce verdict concerne le retrait logistique demandé par l'enseignant ; il ne
vaut ni fusion, ni déploiement, ni verdict d'intégration.

## Autorisation, rôles et flux

Sources normatives lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et le rôle
`TAL-Governance-Auditor`.

- L'enseignant demande explicitement le contrôle de tous les contrôles et la
  suppression des consignes de dépôt. Le script futur d'injection par variable
  d'environnement est hors de ce lot.
- `/root/deposit_prof_scope`, TAL-Prof, a établi la matrice source → cible
  `docs/pedagogy/CONTROLS_DEPOSIT_REMOVAL.md`, avec verdict
  `PÉRIMÈTRE_VALIDÉ`, avant l'édition, selon le handoff de production.
- `/root`, TAL-Pedagogy-Designer, a modifié les huit notebooks autorisés.
- `/root/deposit_pedagogy_review`, TAL-Pedagogy-Reviewer indépendant, a transmis
  directement **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** après comparaison
  JSON et recherche sur les 17 fichiers. Cette preuve de session n'est pas
  présentée comme une review GitHub déjà publiée.
- `/root/deposit_governance` a audité les preuves et écrit uniquement ce rapport.

Le flux pédagogique s'applique. Les modifications portent sur douze sources
Markdown : aucun changement de contrat de correction, aucune activité,
compétence, donnée, trace évaluée ou pondération ne sont modifiés. Une revue
technique du serveur n'est donc pas requise pour ce lot.

## Preuves examinées

| Exigence | Preuve et constat |
|---|---|
| Branche dédiée | Branche et HEAD contrôlés directement ; espace de travail propre avant ce rapport. Aucun changement direct de `main` observé. |
| Matrice et autorisation | Matrice lue intégralement : distinction entre logistique supprimable et éléments pédagogiques obligatoires ; demande enseignante autorisant le retrait logistique. |
| Exhaustivité | Inventaire de 17 fichiers confirmé par le réviseur : 11 dans le dossier des contrôles, trois contrôles rangés dans les TD et leurs trois variantes corrigées. Huit fichiers modifiés et neuf inchangés. |
| Absence de régression | Comparaison JSON indépendante effectuée par la gouvernance : huit notebooks, douze sources Markdown seules ; nombre de cellules et tous les autres champs identiques à la base. Le réviseur confirme la conservation des exercices, grilles, barèmes, sauvegardes, exports et cinq minutes finales. |
| Retrait des consignes | Recherche indépendante du réviseur et journal d'audit : aucune consigne de dépôt ni adresse du serveur enseignant restante dans les 17 fichiers. Les quatre rappels de refus du tuteur « y compris après un dépôt » restent légitimement présents. |
| Tuteur | Journal `/tmp/tal-controls-tutor-tests.log` examiné : 22 tests réussis. Journal `/tmp/tal-controls-tutor-after.log` examiné : 33 profils conformes. Métadonnées et premières cellules inchangées. |
| Sécurité et contrat | Aucun code applicatif, marqueur, sortie, dépendance, route, persistance ou infrastructure modifié. Aucune exécution de code étudiant ni aucun envoi de copie ; aucune adresse personnelle recopiée dans la nouvelle documentation. |
| Qualité du diff | `git diff --check origin/main...HEAD` exécuté par la gouvernance : succès sans diagnostic. |

La gouvernance a lu les journaux et le handoff indépendant, sans relancer les
tests du tuteur. Le journal `/tmp/tal-controls-deposit-audit.log` confirme les
assertions sémantiques de production ; il complète la revue indépendante.

## Limites et relais

- `DevoirS2.ipynb` possède un JSON tronqué préexistant à la ligne 382 ; il est
  déjà exclu du manifeste comme ancien corrigé enseignant. Son texte brut a
  été audité et demeure inchangé. Sa validation structurelle n'est pas revendiquée.
- Les TD ordinaires et l'historique Git sont hors du retrait demandé. Des
  références de dépôt peuvent y subsister ; aucun effacement historique n'est
  annoncé.
- Suite Flask complète, exécution des notebooks et déploiement : **NOT_TESTED**.
  Le périmètre est limité à des sources Markdown et à leur documentation.

Aucun veto de gouvernance. Relais à un Integration-Master indépendant pour
le verdict d'intégration ; fusion et production restent sous décision du
mainteneur. Si l'intégrateur a participé à la production, la règle
`MAINTAINER_REVIEW` s'applique.
