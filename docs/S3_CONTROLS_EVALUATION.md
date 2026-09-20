# Évaluation privée des contrôles cumulatifs S3

Les sept nouveaux sujets `Notebooks contrôles finaux/S3/Controle_TD1_S3.ipynb` à `Controle_TD7_S3.ipynb` correspondent aux routes `controle-td1-s3` à `controle-td7-s3`. Chaque contrôle s’appuie sur le TD correspondant et sur les acquis antérieurs. Ils sont distincts des évaluations formatives TD et des contrôles historiques.

## Contrat de dépôt et de traces

Chaque module `app_correction_Controle_TDn_S3.py` expose `check_notebook(content_str, filename)` et retourne `(score, details, max_score, student_info, error_msg)`. Le maximum technique vaut 20 ; les sept vérifications valent respectivement 2, 3, 3, 3, 3, 3 et 3 points. Le critère indiqué dans chaque exercice s’applique au résultat calculé demandé, sans points automatiques pour une longueur d’argumentation, un mot-clé ou la qualité supposée d’une figure.

La cellule concernée contient un affichage explicite de premier niveau :

```python
print("S3_C1_Q1:", json.dumps(resultat_q1, ensure_ascii=False))
```

Le préfixe est propre au contrôle, de `S3_C1_` à `S3_C7_`. La sortie `stdout` enregistrée doit contenir une seule trace correspondante dans la même cellule. Une trace répétée, une erreur enregistrée, un affichage absent ou une sortie dans une autre cellule invalide la vérification. Les objets JSON aux clés répétées et les nombres non finis sont rejetés. Les nombres booléens ne sont pas assimilés à des comptages. Aucun code de la copie n’est exécuté par le serveur ; spaCy n’est pas une dépendance du correcteur.

Cette méthode ne garantit ni l’authenticité ni la fraîcheur d’une sortie, et ne démontre pas à elle seule l’existence d’une fonction réutilisable ou l’autonomie de son auteur. Ces limites figurent dans le rapport privé et les consignes de dépôt.

## Données et vérifications

Les corpus sont synthétiques et fournis dans les sujets. Leurs copies contractuelles sont dans `app/s3_controls_data.py` ; les tests comparent les littéraux des notebooks avec ces données, sans exécuter les notebooks.

Pour C1–C2, les annotations linguistiques produites par spaCy sont vérifiées par leurs positions et leur couverture du texte. Les filtres et fréquences doivent être cohérents avec ces annotations. Une catégorie grammaticale ou un lemme n’est pas présenté comme une vérité déterminée par le serveur. C2 comporte également une table d’annotations manuelle distincte, permettant un contrôle déterministe des fréquences, exclusions, unions de catégories et du cas vide. Les classements POS acceptent les permutations entre ex æquo.

Pour C3, les fragments, indices, concordances et citations exactes sont vérifiés contre la source. La normalisation est déclarée et possède son propre espace d’indices. Les passages candidats sont vérifiés comme présents dans la source ; leur pertinence sémantique et la validité des lemmes restent à la charge de la relecture humaine. Les listes identifiées par un identifiant autorisent un ordre différent lorsqu’il n’affecte pas le résultat.

Pour C4–C7, `s3_controls_quantitative.py` recalcule les références directement sur les corpus fixes : présences par contexte, marges, unions et sommes de paires, expressions contiguës, fenêtres positionnelles sans filtrage préalable, tableaux de contingence, proportions et taux, segments, positions et concordances, matrices et audit des annonces. Les références numériques sont confrontées à 28 résultats établis séparément dans le contrat Designer. Les quotients exacts et leur arrondi à six décimales sont acceptés avec une tolérance absolue de `1e-6` ; les effectifs restent des entiers stricts. Les listes de positions sont ordonnées selon les conventions des sujets.

Un dénominateur nul produit `null`, jamais un zéro numérique présenté comme une proportion. Une annonce dont le protocole est incomplet conserve le verdict « insuffisamment défini », même si une mesure exploratoire est proche de son intervalle. Le transfert final sur le second corpus est contrôlé quantitativement, en plus de la relecture du programme et du dossier.

## Confidentialité et portée du score

Les sept entrées du registre portent explicitement le mode `controle`. La page publique ne reçoit ni score, ni détails, ni réponse attendue ; elle retourne seulement un reçu après persistance réussie. Une erreur du correcteur ou de sauvegarde produit un message générique, sans transformer le dépôt en oracle de correction.

Le notebook, le rapport HTML privé et le CSV sont conservés dans `soumissions/<évaluation>/<classe>/`. Le rapport spécialisé `s3_controle_report_template.html` présente un **score technique provisoire**, les critères vérifiés et une grille de relecture à renseigner : raisonnement et transfert, qualité linguistique, interprétations et limites, figures et unités, réutilisabilité et autonomie. Ce résultat n’est pas une note globale.

Pour ces nouvelles évaluations seulement, le CSV nomme la colonne du score `Score technique provisoire` et ajoute `Nature du score`, `Maximum technique`, `Relecture humaine`. Les valeurs signalent `technique_provisoire`, `20.0` et `requise`. Le format des CSV des anciennes évaluations est préservé.

Les rapports échappent les traces étudiantes avant rendu. Aucune route publique de consultation des fichiers de soumission n’est ajoutée. Le dépôt conserve le fonctionnement sous le préfixe reverse proxy `/universite/tal/`.

## Validation

`tests/test_s3_controls.py` couvre le moteur, les pondérations, les cas de traces invalides, la distinction entre cohérence et validité linguistique, les calculs déterministes, la concordance des corpus, les sept modules/routes, le sélecteur, les formulaires sous proxy, le dépôt des sujets réels, la persistance privée, les métadonnées du CSV et l’échappement HTML. Les tests existants des TD et des contrôles historiques restent requis.

L’exécution complète des sujets dans Colab, la passation en classe et l’attribution de la note globale après lecture des copies restent des validations humaines distinctes. Les budgets de deux heures sont prévisionnels.

Validation locale de la version préparée : **97 tests passent** (`python -m unittest discover -s tests`), dont 20 nouveaux tests des contrôles cumulatifs. La revue technique indépendante a également calculé les 14 traces C1–C2 avec les versions spaCy prévues et vérifié l’alignement des deux flux C6 ; aucune cellule de copie étudiante n’a été exécutée.
