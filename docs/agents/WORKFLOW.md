# Workflow multi-agents TAL

## Flux

- **Technique** : Code-Architect → Code-Auditor → Governance-Auditor → Integration-Master → mainteneur.
- **Pédagogique** : Pedagogy-Designer → Pedagogy-Reviewer → Governance-Auditor → Integration-Master → mainteneur.
- **Mixte** : tout `CHANGEMENT_DE_CONTRAT` déclenche Code-Architect + double revue Code-Auditor/Pedagogy-Reviewer avant gouvernance.
- **Intégration auto-produite** : Integration-Master → Code-Auditor → Governance-Auditor → `MAINTAINER_REVIEW`.

## Adaptation non-dégradante

Avant de modifier un notebook existant :

1. **TAL-Prof** produit une matrice de couverture source → cible et classe les éléments obligatoires ou optionnels.
2. L’enseignant valide explicitement les suppressions, réductions substantielles ou déplacements sans équivalent immédiat.
3. **TAL-Pedagogy-Designer** réalise l'adaptation et joint le bilan de couverture à la PR.
4. **TAL-Pedagogy-Reviewer** contrôle l'équivalence substantielle et rend `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` ou `NON_DÉMONTRÉE`.
5. Si notebook et correcteur évoluent ensemble, appliquer aussi le flux mixte.
6. **TAL-Governance-Auditor** refuse la conformité si la matrice, les arbitrages requis ou le verdict de couverture manquent.
7. **TAL-Integration-Master** vérifie la présence des supports, activités déplacées et correcteurs déclarés avant son verdict.

Une adaptation peut condenser, réordonner ou enrichir un support, mais ne peut réduire implicitement l'objectif, la manipulation étudiante, l'interprétation ou l'évaluabilité. Le nombre de cellules ne constitue pas un critère de couverture.

## Veille curriculaire TAL

TAL-Prof : veille et cadrage → validation explicite de l'enseignant → Pedagogy-Designer : TD → Pedagogy-Reviewer → flux mixte si contrat affecté → gouvernance → intégration → mainteneur.

La note de cadrage précise objectif de traitement, langues, données, bibliothèques, relation aux LLM, contraintes d'exécution et prérequis. Le TD est validé avant son contrôle associé.

## Branches

`code/<mission>`, `pedagogy/<mission>`, `governance/<mission>`, `integration/<mission>`, `agents/<mission>`.

Le mainteneur décide des bibliothèques introduites, barèmes, exceptions de gouvernance, fusion et production.
