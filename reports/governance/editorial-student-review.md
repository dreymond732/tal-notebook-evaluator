# Gouvernance — règles de révision éditoriale et inventaire intégral

## Mission et indépendance

- Date : 3 octobre 2026.
- Rôle : `TAL-Governance-Auditor`, agent indépendant du producteur des règles et du rédacteur de l'inventaire.
- Branche : `agents/editorial-student-review`.
- Base examinée : `4b79943f0a59a3e05eedc89d3783988682254a80`, avec les modifications de travail de la présente PR.
- Autorisation : demande explicite de l'enseignant de vérifier les règles des agents et de proposer une PR, en couvrant l'intégralité des TD et contrôles.
- Écriture du réviseur : ce rapport uniquement. Aucun fichier audité, notebook, profil du tuteur ou correcteur modifié par le réviseur.

Cette mission audite des **règles et un registre de reprise**. Elle ne prononce aucun verdict de qualité sur les contenus des notebooks inchangés et ne vaut ni validation de la progression ni autorisation de redistribution.

## Périmètre et preuves

Lecture de `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, de toutes les fiches de `docs/agents/`, de leur diff, de `docs/agents/EDITORIAL_REVIEW_TEMPLATE.md`, de `docs/pedagogy/editorial_revision_inventory.md` et du diff de `docs/pedagogy/TUTORING_POLICY.md`. Vérification indépendante des fichiers suivis avec `git ls-files -z '*.ipynb'`, lecture JSON des notebooks et du catalogue, contrôle des cellules citées dans les deux sondages. Aucun code de notebook exécuté.

| Point contrôlé | Preuve dans la proposition | Résultat |
|---|---|---|
| Autorisation et périmètre de changement | Mission `agents/` demandée par l'enseignant ; exception circonscrite dans la matrice et le workflow | Conforme ; ne permet pas de modifier les règles pour débloquer une mission de contenu |
| Séparation producteur/réviseur | `AGENTS.md` règle 2 ; fiche éditoriale, rubrique « Mission et indépendance » ; workflow pédagogique | Le Designer produit ; les réviseurs pédagogique et éditorial rendent des avis distincts et indépendants |
| Permissions du nouveau rôle | Colonne Réviseur éditorial de la matrice ; WRITE limité à `reports/editorial/` et verdict de PR | Aucun droit d'écriture sur les supports, contrats, profils, correcteurs ou règles auditées |
| Destinataire des passages | `AGENTS.md` règle 12 ; fiches Editorial-Reviewer, Designer, Prof et Étudiant-Modèle ; inventaire | Étudiant pour tous les passages visibles, y compris commentaires de code ; seule exception pédagogique : corrigés de DM pour l'enseignant ; contexte caché du tuteur explicitement distinct |
| Lisibilité et exhaustivité | Fiche éditoriale, tableau des fonctions et preuve par question ; workflow « Reprise de tous les supports » | Distinction cours, exemple, exercice guidé, problème autonome, vérification et restitution ; lecture de toutes les cellules, pas seulement des introductions |
| Bibliothèque nouvellement présentée | Fiches Editorial-Reviewer, Prof et Pedagogy-Reviewer | Introduction, objets nécessaires, exemples manipulables et réemploi ; un import de préparation ne devient pas un acquis |
| Tuteur en double | `AGENTS.md` règle 14 ; fiche éditoriale « Tuteur » ; Designer et Integration-Master | Contexte complet identique dans les métadonnées Colab et le commentaire HTML de première cellule Markdown ; profil structuré conservé ; aucune garantie inférée quant au comportement de Colab |
| Acquis et contrôle sans aide | Fiche éditoriale « Périmètre de la question » et « Contrôles » ; protocole A/T de l'inventaire | Restrictions par question et selon les acquis antérieurs ; S1 sans code ; S2/S3 fragment distinct après échange ; aucune assistance, quiz ou indice en contrôle |
| Absence de réduction implicite | Fiches Prof, Designer, Pedagogy-Reviewer et Editorial-Reviewer ; workflow d'adaptation | Référence historique et version technique comparées ; cible déplacée effectivement livrée ; enrichissement des suivants plutôt qu'appauvrissement des précédents |
| Préservation technique et confidentialité | Fiche éditoriale « Conservation » ; Designer ; protocole M/H de l'inventaire | Métadonnées, identifiants et contrat de correction préservés sauf changement déclaré ; marqueur public dans Git, injection d'URL dans la distribution |
| Absence de validation mensongère | Gouvernance, Integration-Master, workflow ; introduction et conclusion de l'inventaire | Recensement et CI explicitement séparés des verdicts de couverture et de lisibilité ; aucun support annoncé comme réécrit ou validé |
| Preuves opératoires de relecture | `EDITORIAL_REVIEW_TEMPLATE.md` | Révision et périmètre identifiés ; une ligne par question, y compris ateliers non marqués ; passages hors question et limites explicités ; aucun verdict positif sur une simple checklist ou un échantillon |
| Cohérence de la politique de tutorat | Diff de `TUTORING_POLICY.md` | Ancien compte de 21 sujets identifié comme historique, renvoi au catalogue et à l'inventaire actuels ; revue des acquis et des deux copies du tuteur ajoutée sans changer les règles d'assistance |

## Vérification indépendante de l'inventaire

- **44 notebooks suivis, 44 chemins présents dans l'inventaire.** Aucun fichier suivi omis.
- **34 entrées au catalogue : 33 actives et une inactive.** S1 : 7 TD et 2 évaluations actives ; S2 : 3 TD, 3 évaluations actives et un contrôle inactif ; S3 : 11 TD/révisions et 7 contrôles actifs. Ces comptes concordent avec les tableaux.
- **10 fichiers hors catalogue**, conservés dans le périmètre sans activation ni distribution implicite.
- **42 notebooks JSON lisibles, 2 invalides**, tous deux explicitement signalés : `Notebooks TD/TD6_S2-corrigé.ipynb` et `Notebooks contrôles finaux/DevoirS2.ipynb`. Leur réparation n'est pas prétendue effectuée.
- Aucun notebook `dist/` suivi dans ce recensement ; les copies distribuées sont à régénérer et à vérifier depuis les sources après reprise.
- Les indices et identifiants des passages cités dans les sondages R2 et TD1 spaCy concordent avec les cellules observées. Cette concordance atteste la localisation, pas la qualité pédagogique intégrale de ces deux supports.
- Les références historiques absentes sont déclarées comme limites ; l'inventaire ne se présente pas comme une matrice détaillée validée et ne conclut pas à une restauration accomplie.

Le diff du produit examiné contient uniquement les règles, fiches et documents de suivi annoncés ; aucun notebook ni code applicatif n'est modifié. `git diff --check` passe lors de cette revue. Le producteur rapporte également les contrôles existants du tuteur sur 34 profils et de distribution sur 33 sujets actifs réussis ; ces résultats techniques sont distincts de la présente relecture de gouvernance. Le réviseur n'a pas exécuté de tests applicatifs ; aucune réussite de test n'est invoquée comme preuve éditoriale.

## Verdict et suites obligatoires

**CONFORME — règles des agents et inventaire de reprise.** Aucun écart bloquant identifié dans ce périmètre. La proposition rend les exigences de l'enseignant explicites et les relie aux permissions, au workflow et aux preuves attendues.

La relecture complète, les matrices détaillées, la réécriture, l'essai novice et les verdicts indépendants restent à produire pour chaque lot de supports. Aucun notebook ne reçoit ici `LISIBILITÉ_ÉTUDIANTE_VALIDÉE` ou `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`. Les deux archives invalides restent un obstacle identifié à leur lecture complète, sans bloquer une PR qui les recense honnêtement.

Le présent rapport n'est pas un `READY_TO_MERGE` ; la vérification d'intégration et la décision de fusion restent distinctes et la fusion appartient au mainteneur.
