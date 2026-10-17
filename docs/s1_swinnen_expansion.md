# Renforcement Swinnen du S1 — intégration

Mission `pedagogy/s1-swinnen-renforcement`, base `c81c38641ecddb66c5ea65c78eafbd2d8d3cbbc5`. Les rôles existants ont été utilisés : Prof, trois Designers, Étudiant-Modèle, réviseurs pédagogique et éditorial, Architecte, auditeur code et gouvernance. Aucun rôle normatif ajouté ou modifié.

## Résultat et contrat

Neuf nouveaux cahiers (six questions chacun) remplacent les trois étapes TD3/5/6 dans le parcours renforcé, sans effacer les trois synthèses historiques. Le parcours comprend treize cahiers TD, plus DM et contrôle distincts. Les noms visibles suivent one, bis, ter ; les chemins et identifiants techniques emploient uniformément des tirets. Le sélecteur distingue les anciens cahiers comme synthèses historiques.

Chaque nouveau correcteur `td{3,5,6}-{one,bis,ter}-s1` possède un contrat v2 indépendant, six cellules-réponses, une identification canonique et un maximum technique de 6 points. Les anciens barèmes, variables, questions et identifiants ne sont pas modifiés. Il s'agit d'un **CHANGEMENT_DE_CONTRAT additif**, pas d'une migration des copies anciennes.

Le moteur `check_saved_notebook` reste inerte : analyse syntaxique et comparaison des sorties déjà enregistrées. Aucun programme soumis, fonction, import ou fichier étudiant n'est exécuté ni ouvert par le serveur. Le JSON applicatif `s1_expansion_rubrics.json` définit les références, appels/structures demandés et tolérances ; les données soumises ne peuvent pas définir un barème ou une fonction de correction.

Les imports présents dans les exemples enseignés et les préparations sont lus comme contexte d'alias uniquement, jamais exécutés ni crédités comme production. Le lecteur CSV rejoint les opérations de lecture suivies par le graphe de dépendances afin de relier les écritures aux lignes relues. Comme auparavant, ce graphe est une approximation syntaxique : la trace ne prouve ni fraîcheur, ni auteur, ni comportement pour toute entrée.

Tolérances conservées : traduction langue/langage avec cohérence entre traduction, lexique et liste des entrées ; ordre libre des entrées du lexique ; couples liste ou tuple pour les fiches autorisées, sans relâchement des types des champs ; ordre libre des personnes et affiliations dans l'export historique, avec en-tête, effectifs et unicité stricts. Les compréhensions restent acceptées pour la composition lorsque la consigne laisse ce choix. Les exercices nouveaux qui demandent explicitement une boucle ou un tri conservent cette contrainte.

## Sources et distribution

Matrice préalable et références : `docs/pedagogy/s1-swinnen-expansion.md`. Manuel fourni par l'enseignant : Gérard Swinnen, *Apprendre à programmer avec Python*, copyright 2000–2012. Chaque adaptation indique section/exercice et page imprimée. Les neuf cahiers contiennent notice, préface et licence intégrale du manuel dans une annexe repliable, également disponible dans `docs/swinnen/NOTICE_PREFACE_LICENCE.txt`. Ces adaptations restent CC BY-NC-SA 2.0 France ; la licence du serveur n'est pas modifiée.

La cellule canonique de restitution conserve `__TAL_PUBLIC_URL__`. La commande habituelle `prepare_student_notebooks.py` génère les copies distribuables et injecte l'URL seulement dans `dist/`. Les neuf corrigés de référence sont explicitement exclus de la distribution et du manifeste des sujets tutorés. Aucun `dist/` généré n'est suivi dans Git.

## Validation et limites

Revue pédagogique indépendante : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` sur les 54 questions, cours, exemples, essais et vérifications ; les deux demandes de reprise (alternative compréhension et affichage texte CSV historique) ont été levées. Revue rédactionnelle indépendante : `reports/editorial/s1-swinnen-expansion.md` avec les preuves par question.

L'Étudiant-Modèle a lu uniquement les sujets et les acquis autorisés, puis produit neuf corrigés non exécutés et une lecture préalable : `Corrigés modèles/TD/s1-swinnen/lecture.md`. L'Architecte a ensuite testé des copies temporaires de ces références synthétiques en local, chacune dans un dossier vide distinct, avec capture réelle des affichages puis passage dans son correcteur : neuf exécutions sans erreur et neuf scores de 6/6. Cette QA locale n'ajoute aucune exécution au serveur. Les fichiers de référence suivis dans Git restent non exécutés, sans sorties ; certains essais personnels demeurent à compléter comme indiqué dans leur note.

Les tests dédiés portent sur les neuf contrats, versions incorrectes, questions manquantes, absence d'exécution, variantes positives/négatives, imports et écritures CSV, routage automatique et neuf répertoires de persistance distincts. Les suites historiques, la concordance des tuteurs, le schéma nbformat et la génération de la distribution complètent ces vérifications.

La charge accrue n'est pas mesurée en classe ; les treize cahiers ne sont pas assimilés à treize séances. L'enseignant répartira les activités entre présentiel et travail personnel sans suppression implicite. Les contrôles et le DM ne sont pas remaniés par cette PR. Le comportement réel du tuteur dans Colab et le serveur de production ne sont pas testés ici. Le score demeure formatif et limité ; la relecture individuelle des explications reste facultative.

L'intégration a été produite par le rôle Architecte principal : verdict final **MAINTAINER_REVIEW**, pas d'auto-validation d'intégration ni de fusion.
