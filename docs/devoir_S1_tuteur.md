# devoir_S1_tuteur — Édition de révision guidée

La demande enseignante du 15 octobre 2026 est réalisée sur la branche
`pedagogy/devoir-s1-tuteur`, à partir de `590b9a6c78fc6b27f8985e060c6ea2325367f652`.
Le nouveau [notebook](../Notebooks%20contr%C3%B4les%20finaux/S1/devoir_S1_tuteur.ipynb)
reprend intégralement les 18 questions du devoir maison S1 avec un profil LLM
spécifique, `devoir_S1_tuteur`.

## Utilisation

Ouvrir cette nouvelle version dans Colab et indiquer au tuteur le numéro,
l'intitulé ou l'énoncé de la question à réviser, par exemple :
« Je souhaite réviser les notions nécessaires à Q14. »
Le tuteur doit identifier cette question puis vérifier toutes les notions de
sa fiche, prérequis et dépendances compris. Il pose une seule question à la fois
et attend la réponse. En cas d'hésitation, il fournit une courte explication
conceptuelle et un exemple sur d'autres données, puis vérifie la compréhension.
Il suit les notions vérifiées et restantes avant de revenir à un essai autonome.

Les instructions interdisent code à recopier, correction, pseudocode, résultat
attendu ou solution du devoir. Elles interdisent aussi toute modification ou
exécution de cellule par le tuteur. La révision reste limitée à la fiche de la
question choisie, sans réunir les permissions de toutes les questions.

## Périmètre livré

- Le [DM original](../Notebooks%20contr%C3%B4les%20finaux/S1/DM_intermediaire_S1.ipynb)
  reste inchangé, en mode LLM `controle`, sans assistance.
- La copie conserve 45 cellules, les 18 questions, leurs données, toutes les
  cellules de code, les essais, explications demandées et le barème. Seuls le
  titre, les conditions d'accompagnement et les contextes du tuteur diffèrent.
- Les 18 fiches fermées couvrent les prérequis nécessaires, dont division et
  priorités, ordre d'insertion et sûreté des indices lorsque requis. Les notions
  absentes du cours antérieur sont explicitement à introduire dans cette révision.
- Le contexte complet de 4 256 caractères est identique dans le commentaire
  HTML de la première cellule Markdown et dans les métadonnées Colab.
- Les 35 supports originaux, leurs contextes et le catalogue restent inchangés.
  Aucun nouvel évaluateur n'est créé. La copie utilise le contrat de notation
  du DM original ; un dépôt produit toujours un reçu privé, sans note publique.
- La source peut être ouverte directement dans Colab. Elle n'est pas ajoutée
  à la distribution automatique des 34 sujets actifs du catalogue.

Le barème et le paragraphe d'évaluation hérités sont conservés. Cette édition
n'établit pas de nouvelles modalités de remise ou d'attribution de note.

## Vérifications et preuves

La suite complète compte **308 tests réussis**, après la dernière synchronisation
du prompt. La revue technique indépendante a aussi exécuté 36 tests ciblés,
inclus dans ces 308. Le contrôle des 36 profils du tuteur, celui des 34 sujets
actifs, la validation nbformat, l'idempotence de la migration et la compilation
des modules réussissent. Un POST indépendant vérifie la persistance et le reçu
privé de la nouvelle copie. Aucun code étudiant n'a été exécuté.

Journaux locaux : `/tmp/devoir-s1-tuteur-tests-verified.log` et
`/tmp/devoir-s1-tuteur-contexts-verified.log`. Le comportement réel de Gemini
dans Colab, sa régularité sur plusieurs tours et la maîtrise d'étudiants réels
ne sont pas testés. Le prompt donne des instructions ; il ne constitue pas un
verrou technique garantissant les réponses du LLM.

Empreinte SHA-256 du notebook final :
`e67df7e49ea623346cc50964002ef0473359649b3fa3b13af7353ae9a80ac25b`.
Contexte :
`1ce982aa091861a5550f50721f30e68d0eb0ae5b6f4c85cb7ff29b9752d3306b`.

## Revue indépendante

Répartition des productions : TAL-Prof a établi le cadrage et le manifeste ;
TAL-Pedagogy-Designer a créé la copie ; TAL-Code-Architect (agent principal)
a modifié `app/tutor_metadata.py`, ajouté `tests/test_devoir_s1_tuteur.py` et
adapté `tests/test_notebook_migration_integrity.py`. Les réviseurs indépendants
n'ont modifié aucun de ces produits. Le même agent principal assure ensuite
l'intégration documentaire sous le rôle TAL-Integration-Master.

Le [cadrage et la matrice](pedagogy/devoir_s1_tuteur_spec.md) ont été acceptés
avant conception. Les livrables de revue sont distincts :

- [Revue pédagogique](devoir_S1_tuteur_pedagogy.md) : ACCEPT,
  `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`.
- [Revue rédactionnelle](../reports/editorial/devoir-s1-tuteur.md) : ACCEPT,
  `LISIBILITÉ_ÉTUDIANTE_VALIDÉE`.
- [Lecture étudiante par question](../Corrig%C3%A9s%20mod%C3%A8les/TD/devoir-s1-tuteur/lecture_etudiante.md).
- [Audit technique](devoir_S1_tuteur_code_review.md) : ACCEPT technique.
- [Gouvernance](../reports/governance/devoir-s1-tuteur.md) : `CONFORME` pour
  cette édition, son profil et les adaptations techniques associées.

L'intégration est réalisée par un producteur du changement : le statut final
est `MAINTAINER_REVIEW`, après avis de gouvernance `CONFORME`. Aucune fusion
ni mise en production n'est effectuée. Cette livraison ne clôt pas les constats
de l'audit global S1, notamment ceux du moteur de correction préexistant.
