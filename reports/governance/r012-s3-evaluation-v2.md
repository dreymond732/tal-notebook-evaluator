# Audit de gouvernance — Révisions S3 R0, R1 et R2, version 2

## Verdict et périmètre

**CONFORME**, le 1er octobre 2026, sur la branche
`code/s3-revisions-evaluation-v2`, par comparaison avec `06cbd2a`.
La mission est la fiabilisation des trois évaluateurs de révision S3 et de leurs
sujets, avec refus explicite des anciennes versions. Ce verdict ne vaut ni
fusion ni déploiement ; le relais d’intégration est **MAINTAINER_REVIEW**.

L’enseignant a autorisé la fiabilisation et demandé le message exact
`mauvaise version du notebook` pour les anciennes copies, sans correction ni
migration. Les trois sujets passent au contrat v2 ; les copies v1 de `dist/`
ne doivent pas être redistribuées. Après fusion et déploiement, il faut
régénérer et vérifier les copies distribuables v2.

## Rôles et changement de contrat

Sources normatives lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et le rôle gouvernance.

- TAL-Prof a rédigé `docs/pedagogy/r012_v2_spec.md`, comprenant la matrice
  source → cible des douze questions. L’orchestrateur confirme l’avoir validée
  avant la conception. Aucune activité, donnée, durée indicative ni compétence
  n’est supprimée ; aucune bibliothèque nouvelle n’est introduite.
- TAL-Pedagogy-Designer a modifié uniquement les trois sujets. La révision
  renforce les traces observables et ajoute l’identification étudiante.
- TAL-Code-Architect a produit le moteur, les raccordements, les tests dédiés
  et `docs/revisions_s3_v2.md`. Le changement de contrat est explicitement
  déclaré et soumis à la double revue.
- TAL-Pedagogy-Reviewer indépendant a rendu **ACCEPT —
  COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** : douze activités, données et durées
  conservées ; schéma notebook, syntaxe, identifiants, quatre réponses,
  identité et tuteurs vérifiés. Aucun notebook étudiant exécuté.
- TAL-Code-Auditor indépendant a rendu **ACCEPT** après correction de ses
  observations, notamment retours constants, réaffectations, dépendances,
  réponses malformées et alias de lemme dans un filtre. Il a aussi relu les
  changements de tests produits par l’intégration et le stockage v2.
- TAL-Integration-Master a adapté six fichiers de tests ; étant producteur
  de cette partie du lot, il rend **MAINTAINER_REVIEW**, et non
  `READY_TO_MERGE`.
- TAL-Governance-Auditor a lu les normes, les changements et les preuves ; il
  écrit uniquement le présent rapport. Aucun producteur ne valide son propre
  produit. Les règles normatives restent inchangées.

Les verdicts spécialisés sont des preuves de session, transmis directement
par les agents ou relayés par l’orchestrateur. Ils ne sont pas présentés comme
des reviews GitHub déjà publiées.

## Preuves examinées

| Exigence | Preuve et résultat |
|---|---|
| Branche, normes et fixture | Vérification propre : branche dédiée ; `git diff --exit-code 06cbd2a` sur `AGENTS.md`, matrice, contrat, `docs/agents/` et fixture historique sans changement. `git diff --check` réussi. |
| Périmètre des sujets | Vérification propre : seuls les trois notebooks R0–R2 sont modifiés. Chacun possède `metadata.tal` v2, une identité et Q1–Q4 `role: answer`. Toutes les sorties sont vides et tous les compteurs d’exécution nuls. |
| Intégrité historique | Lecture des adaptations et revue indépendante : les trois révisions sont déclarées explicitement, les 39 autres notebooks de la référence historique restent protégés par leurs empreintes. La fixture des 42 originaux n’est pas réécrite. Le DM ajouté antérieurement conserve ses contrôles séparés. |
| Anciennes copies | Lecture du routage et tests : version absente ou périmée refusée avec `mauvaise version du notebook`. Les routes S3 explicites exigent les métadonnées et ne contournent pas `/submit`. Aucune correction ni persistance lors du refus ; aucune migration automatique. Les routes historiques S1/S2 conservent leur compatibilité. |
| Localisation et calcul | Lecture du moteur : seules les réponses identifiées et leurs dépendances prévues sont examinées, avec analyse AST et comparaison de traces sauvegardées. Les exemples et les sorties d’autres cellules ne fournissent pas les points. Le score reste borné à quatre points techniques. |
| Non-exécution | Lecture et tests : JSON, AST et `ast.literal_eval` sur littéraux bornés uniquement ; aucun lancement de code étudiant. Les tests utilisent des sources et sorties synthétiques sans exécuter les solutions. |
| Référence spaCy | L’orchestrateur puis l’architecte ont produit/reproduit les références avec du code enseignant indépendant, spaCy 3.8.7 et `fr_core_news_sm` 3.8.0. Versions et protocole copiables dans `docs/revisions_s3_v2.md`. L’installation fournie reprend les épinglages Typer du TD1. Aucune dépendance spaCy n’est ajoutée au serveur. |
| Interprétation linguistique | Spécification et sujets : les prédictions ADV pour `analysent` et PRON pour `corpus` sont assumées comme résultats du modèle, non comme vérité grammaticale. Les observations Q4 restent visibles à la relecture et ne sont pas notées par leur longueur ou des mots-clés. |
| Identité et persistance | Lecture et sonde indépendante : identité complète obligatoire ; stockage séparé `td-r*-s3-v2` pour conserver les CSV historiques. Deux homonymes avec numéros distincts produisent deux copies et deux rapports ; CSV v2 à deux lignes et dix colonnes, numéros corrects ; ancien CSV intact. Échappement HTML testé. |
| Tests ciblés indépendants | Code-Auditor : 13 tests dédiés réussis ; variante avec alias de lemme à 4/4 ; 72 cas de refus web et 48 cas de cellules malformées réussis. Les anciennes copies n’appellent ni correction ni persistance. |
| Tests globaux | Intégration : 168 tests réussis avant la dernière adaptation. Orchestrateur : suite complète relancée après les derniers correctifs, **169 tests réussis**, sans omission des tests de nettoyage d’historique ; compilation et contrôle du diff réussis. |
| Tuteurs et distribution | Intégration et orchestrateur : 34 tuteurs vérifiés ; 33 sources vérifiées, 33 copies générées et vérifiées sous `dist/` avec `TAL_PUBLIC_URL=https://example.test/universite/tal`. Les trois copies v2 ont la cellule HTML finale ; les sources n’exposent pas l’adresse serveur privée. |

## Limites et relais mainteneur

L’analyse statique et les sorties enregistrées ne prouvent ni une exécution
réelle ni l’authenticité d’une réponse ni sa validité sur toute entrée. Le
retour et la documentation présentent donc un score technique provisoire et
prévoient une relecture des alternatives valables non reconnues. La qualité
des explications linguistiques reste à apprécier humainement.

Les références spaCy ont été exécutées comme code enseignant séparé ; cela
ne constitue pas une exécution des notebooks étudiants. Colab, proxy et
serveur de production sont **NOT_TESTED**. Docker est indisponible dans
l’environnement local ; la CI, y compris le conteneur, doit être observée
après publication et ne doit pas être considérée comme déjà réussie.

L’adresse injectée reste hors du dépôt source, mais elle est nécessairement
lisible dans la copie distribuée : le mécanisme n’est pas une dissimulation
vis-à-vis de son destinataire. Les trois anciens fichiers `dist/` doivent
être remplacés par les fichiers v2 régénérés après mise à jour ; il n’y a pas
de migration des réponses anciennes.

Absence de veto de gouvernance sur le lot examiné. Relais
**MAINTAINER_REVIEW** : fusion et production restent sous décision du
mainteneur. Aucun commit, aucune publication, fusion ou mise en production
n’a été effectué par la gouvernance. Une modification substantielle
ultérieure exige de réexaminer les preuves concernées.
