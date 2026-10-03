# Workflow multi-agents TAL

## Flux

- **Technique** : Code-Architect → Code-Auditor → Governance-Auditor → Integration-Master → mainteneur.
- **Pédagogique** : Pedagogy-Designer → revues indépendantes Pedagogy-Reviewer et Editorial-Reviewer → Governance-Auditor → Integration-Master → mainteneur.
- **Mixte** : tout `CHANGEMENT_DE_CONTRAT` déclenche Code-Architect + revues Code-Auditor, Pedagogy-Reviewer et Editorial-Reviewer avant gouvernance. Une revue rédactionnelle ne peut modifier le contrat silencieusement.
- **Intégration auto-produite** : Integration-Master → Code-Auditor → Governance-Auditor → `MAINTAINER_REVIEW`.

## Adaptation non-dégradante

Avant de modifier un notebook existant :

1. **TAL-Prof** produit une matrice de couverture source → cible et classe les éléments obligatoires ou optionnels. Il identifie à la fois la référence historique disponible et la version technique actuelle ; une référence manquante reste signalée.
2. L’enseignant valide explicitement les suppressions, réductions substantielles ou déplacements sans équivalent immédiat.
3. **TAL-Pedagogy-Designer** réalise l'adaptation et joint le bilan de couverture à la PR.
4. **TAL-Pedagogy-Reviewer** contrôle l'équivalence substantielle et rend `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` ou `NON_DÉMONTRÉE`. **TAL-Editorial-Reviewer** relit tous les passages visibles en tant qu'étudiant, distingue les fonctions des passages et rend séparément `LISIBILITÉ_ÉTUDIANTE_VALIDÉE` ou `NON_DÉMONTRÉE`. Aucun des deux ne révise sa propre production.
5. Si notebook et correcteur évoluent ensemble, appliquer aussi le flux mixte.
6. **TAL-Governance-Auditor** refuse la conformité si la matrice, les arbitrages requis ou l'un des deux verdicts positifs manquent.
7. **TAL-Integration-Master** vérifie la présence des supports, activités déplacées et correcteurs déclarés avant son verdict. Une activité annoncée dans un futur support non livré reste non couverte.

Une adaptation peut condenser, réordonner ou enrichir un support, mais ne peut réduire implicitement l'objectif, la manipulation étudiante, l'interprétation ou l'évaluabilité. Le nombre de cellules ne constitue pas un critère de couverture.

## Reprise de tous les supports

L'inventaire `docs/pedagogy/editorial_revision_inventory.md` couvre tous les TD, révisions, contrôles, devoirs, corrigés et archives suivis dans le dépôt, tous semestres. Le catalogue actif ne suffit pas à définir ce périmètre. Les fichiers `dist/` sont générés à partir des sources ; ne pas les corriger séparément.

Pour chaque lot cohérent TD → contrôle associé : cadrage et matrice validée avant conception, réécriture par le Designer, lecture indépendante par question, vérifications techniques, gouvernance, intégration. Commencer par R2 et l'introduction spaCy comme pilotes de la méthode ; poursuivre l'intégralité de la progression sans considérer ces pilotes comme une validation des autres notebooks.

Faire intervenir l'Étudiant-Modèle sur les supports révisés et les seules ressources autorisées pour relever les ambiguïtés avant de résoudre. Archiver la lecture par question, pas seulement une copie réussie. En contrôle, cet essai de validation se fait hors épreuve, sans activer le tuteur. Aucune exécution de code étudiant sur le serveur.

Les statuts de suivi sont distincts : `RECENSÉ`, `À_REPRENDRE`, `RÉÉCRIT`, `REVU`, `VALIDÉ`. Passer à `VALIDÉ` exige les preuves et verdicts de la révision concernée. Le recensement, le tutorat synchronisé et une CI verte ne valident pas la rédaction. Une archive illisible est signalée ; elle n'est ni ignorée dans l'inventaire ni réactivée implicitement.

Tous les passages visibles ont pour destinataire l'étudiant, sauf les corrigés de devoirs maison identifiés pour l'enseignant. Les corrigés de TD ne sont pas une seconde exception. Déplacer les notes de fabrication et de maintenance dans la documentation. Préserver le double contexte caché du tuteur, les permissions par exercice et le refus complet d'aide en contrôle.

## Évolution des règles des agents

Une mission `agents/` explicitement demandée par le mainteneur peut modifier les actifs normatifs et les fiches de rôles. Une revue indépendante de ces changements vérifie leur cohérence avec les permissions et les décisions enseignantes. Ce n'est pas une autorisation générale pour un producteur de modifier les règles pendant une mission de contenu. La présente mission ne vaut pas verdict pédagogique sur les notebooks qu'elle recense ; leurs reprises suivent le flux ci-dessus.

## Veille curriculaire TAL

TAL-Prof : veille et cadrage → validation explicite de l'enseignant → Pedagogy-Designer : TD → Pedagogy-Reviewer et Editorial-Reviewer → flux mixte si contrat affecté → gouvernance → intégration → mainteneur.

La note de cadrage précise objectif de traitement, langues, données, bibliothèques, relation aux LLM, contraintes d'exécution et prérequis. Le TD est validé avant son contrôle associé.

## Branches

`code/<mission>`, `pedagogy/<mission>`, `governance/<mission>`, `integration/<mission>`, `agents/<mission>`.

Le mainteneur décide des bibliothèques introduites, barèmes, exceptions de gouvernance, fusion et production.
