# Workflow multi-agents TAL

## Flux

- **Technique** : Code-Architect → Code-Auditor → Governance-Auditor → Integration-Master → mainteneur.
- **Pédagogique** : Pedagogy-Designer → Pedagogy-Reviewer → Governance-Auditor → Integration-Master → mainteneur.
- **Mixte** : tout `CHANGEMENT_DE_CONTRAT` déclenche Code-Architect + double revue Code-Auditor/Pedagogy-Reviewer avant gouvernance.
- **Intégration auto-produite** : Integration-Master → Code-Auditor → Governance-Auditor → `MAINTAINER_REVIEW`.

## Veille curriculaire TAL

TAL-Prof : veille et cadrage → validation explicite de l'enseignant → Pedagogy-Designer : TD → Pedagogy-Reviewer → flux mixte si contrat affecté → gouvernance → intégration → mainteneur.

La note de cadrage précise objectif de traitement, langues, données, bibliothèques, relation aux LLM, contraintes d'exécution et prérequis. Le TD est validé avant son contrôle associé.

## Branches

`code/<mission>`, `pedagogy/<mission>`, `governance/<mission>`, `integration/<mission>`, `agents/<mission>`.

Le mainteneur décide des bibliothèques introduites, barèmes, exceptions de gouvernance, fusion et production.
