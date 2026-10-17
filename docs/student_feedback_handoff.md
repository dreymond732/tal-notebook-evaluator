# Restitution étudiante S1/S3 — livraison et vérifications

Mission : PR #33, branche `code/rapports-pedagogiques-s1-s3`. La reprise du 17 octobre intègre `main` (`992108a`, PR #31 et #32 fusionnées par le mainteneur) sans fusionner cette PR dans `main`.

## Comportement livré

Le rapport distingue le code réellement retrouvé, ses sorties sauvegardées (erreurs comprises), le résultat attendu et le bilan. La colonne **Résultat attendu** montre un exemple de solution dès l’ouverture ; une case permet de la masquer, y compris dans le HTML sauvegardé. Pour une réponse validée, le bilan contient seulement un **✓ vert**, accompagné d’un libellé accessible.

Les résultats incorrects, absents ou non vérifiables conservent un retour pour reprendre la question. Un calcul validé dont un champ rédigé obligatoire manque reste signalé « À compléter ». Les explications et interprétations non notées restent à autoévaluer ; les productions complémentaires et la portée du score sont repliables.

Périmètre : **31 correcteurs formatifs S1/S3, 188 questions**. Les 116 exemples de la première livraison sont conservés ; 72 exemples propres aux douze nouveaux TD3/4/5/6 one/bis/ter S1 sont ajoutés. Le S2 bénéficie de la présentation commune avec ses attendus historiques ; ses exemples complets restent le lot suivant. Les contrôles restent des reçus publics, sans solution cachée dans leur HTML.

Les sujets, activités, tuteurs, versions, barèmes, tolérances et règles de validation ne changent pas. Le serveur n’exécute jamais le programme remis ni les solutions affichées.

## Fichiers et contrat

- `app/report_evidence.py` extrait les cellules de réponse sans exécution. Code et sorties textuelles sont échappés ; HTML/SVG soumis ne sont pas rendus.
- `app/s1_feedback.py`, `app/s1_expansion_feedback.py` et `app/s3_feedback.py` fournissent les exemples applicatifs de confiance. Le nouveau catalogue est autonome, sans dépendance de déploiement aux corrigés modèles.
- L’enrichissement conserve `student_code`, `student_output`, `answer_cells`, `diagnostic`, `action`, `solution_code`, `solution_explanation` et les champs historiques. Les consommateurs de scores ne changent pas.
- `s1_revision.py` conserve ensemble `enrich_s1_details(notebook, evaluator, details)` et `optional_review = evaluator in STRICT_S1` : le conflit des deux séries de changements est résolu.
- `corrector_template.html` regroupe état et retour dans « Bilan » et retire leur répétition en cas de réussite. Les diagnostics internes restent disponibles sans être affichés pour les réussites.

La [matrice de restitution](pedagogy/restitution_simplifiee.md) conserve les éléments de rapport et les activités. Le [plan initial](pedagogy/plan_restitution_etudiante_s1_s3.md) documente l’inventaire historique de 116 questions ; le lot actuel y ajoute les 72 questions désormais stabilisées.

## Vérifications

- Suite complète : **352 tests réussis** ; les résultats finaux et les éventuelles limites d’environnement sont indiqués dans le rapport de gouvernance et la PR.
- **62 dépôts HTTP** : les 31 correcteurs via leur route et `/submit`, sous préfixe proxy. Vérification des extraits réels, erreurs, échappement, solution présente, affichage initial, copie, CSV et HTML sauvegardé.
- **117 exemples S1 exécutés localement comme code applicatif de confiance**, dans des répertoires temporaires, puis vérifiés par les correcteurs existants. Les douze nouvelles copies obtiennent 6/6 ; cas limites des fonctions, collections et fichiers vérifiés. L’évaluation de ces copies est exécutée avec `exec` interdit.
- Les 71 exemples S3 sont compilés ; 44 ont été exécutés dans la livraison initiale. Les 27 exemples nécessitant les modèles spaCy fixés restent relus statiquement, sans nouvelle exécution de ces modèles ici.
- Tests du tableau : ✓ seul et accessible, absence de vert pour les états non vérifiables ou incomplets, solutions visibles d’emblée et masquables sans dépendance externe, confidentialité des contrôles préservée.
- Deux [aperçus anonymes](examples/README.md) régénérés : succès TD1 S1 et erreur sauvegardée TD1.a S3.

## Revues indépendantes et limites

Code-Auditor : **ACCEPT**, avec 29 tests et 94 sous-tests ciblés, plus comparaison des scores/statuts des 72 nouvelles réponses avec et sans enrichissement. Pedagogy-Reviewer : **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, 72 énoncés et solutions comparés, exécution indépendante et matrice relue. Les rapports [éditorial](../reports/editorial/rapports-simplifies.md) et [gouvernance](../reports/governance/rapports-simplifies.md) consignent leurs verdicts propres. Le producteur ne prononce pas sa propre validation.

Une source préremplie peut ne pas être une production de l’étudiant ; les sorties sauvegardées peuvent être périmées. Aucun rapport ne certifie l’auteur ni l’actualité des sorties. Les anciens HTML archivés nécessitent une nouvelle soumission ou leur notebook original pour être régénérés.

Le navigateur interactif, Colab et la production ne sont pas testés ici. Docker n’est pas disponible localement ; la construction et le démarrage du conteneur restent contrôlés par la CI GitHub.

Intégration auto-produite : **MAINTAINER_REVIEW**. La fusion et la mise en production restent sous décision du mainteneur.
