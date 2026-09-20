# Gouvernance — rappel Markdown du tuteur TD2 S1

## Périmètre et décision

Branche : `pedagogy/td2-markdown-tutor-reminder`, référence : `8a6f2bc`, destination proposée : `main`.

L'enseignant demande explicitement d'essayer un rappel en commentaire Markdown après une résolution immédiate rapportée dans Colab. Cette demande autorise l'exception à la politique initiale de métadonnées seules. Le pilote ajoute uniquement un commentaire HTML au début de la première cellule du TD2 S1 ; il ne généralise pas ce mécanisme aux autres notebooks.

Fichiers du lot :

- `Notebooks TD/S1/TD2_S1_python_texte.ipynb` ;
- `docs/pedagogy/TD2_TUTOR_REMINDER.md` ;
- `docs/pedagogy/TUTORING_POLICY.md` ;
- `docs/TUTOR_METADATA.md` ;
- le présent rapport.

Aucun `CHANGEMENT_DE_CONTRAT` : code, données, marqueurs, productions attendues, identification, barème et métadonnées sont conservés. Aucun fichier applicatif, test, corrigé modèle ou actif de gouvernance n'est modifié.

## Rôles et preuves

Le Prof `markdown_prof` a produit la matrice source → cible et la mise à jour de politique dans `docs/pedagogy/`. L'Integration-Master a validé la matrice avant le relais au Designer `markdown_designer`, seul auteur du changement de notebook. La matrice conserve les sept exercices, les activités de prédiction, manipulation, interprétation et dépôt ; aucune réduction ne requiert d'arbitrage supplémentaire.

L'Integration-Master a adapté la documentation technique. Les agents indépendants `markdown_review` et `markdown_code_review` ont rendu respectivement `ACCEPT` avec `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, et `ACCEPT`. Aucun producteur n'a validé son propre travail. Le présent audit écrit uniquement dans `reports/governance/`.

| Vérification | Résultat et portée |
|---|---|
| Comparaison structurelle à `8a6f2bc` | PASS : retirer le seul préfixe ajouté restitue exactement le JSON source ; 18 cellules, dont 8 de code, et toutes les métadonnées conservées. Vérification reproduite par la gouvernance. |
| Identité du notebook audité | SHA-256 `021a8355749c0a3cf2349646e331a3e279573d9c3187ced64df58c9e37c365ff`. |
| Vérification du générateur | PASS : `--check` conforme pour les quatre profils ; 11 tests de métadonnées réussis, attestés par les revues indépendantes. |
| Conservation du rappel | PASS : l'auditeur code vérifie que `migrate_notebook` restitue le notebook entier, rappel compris. Le rappel est manuel et non synchronisé automatiquement. |
| Intégrité du diff | PASS : `git diff --check`, reproduit par la gouvernance. |
| Exécution de code étudiant | Aucune : seules lectures, comparaisons structurelles et vérifications du générateur ont été réalisées. |
| Comportement réel du nouveau pilote dans Colab | `NOT_TESTED`. L'échec de la version précédente rapporté par l'enseignant n'est pas un essai de cette version. |

## Limites et verdict

Le commentaire peut ne pas être transmis au modèle ou ne pas être respecté. Il ne constitue pas un verrou technique. Sa cohérence avec les métadonnées devra être revue lors de toute évolution des règles. Le protocole manuel documenté doit être appliqué dans Colab avant de conclure à son efficacité.

**CONFORME** pour ce périmètre et ces preuves. L'Integration-Master ayant produit la documentation technique, le statut d'intégration est **MAINTAINER_REVIEW**, pas `READY_TO_MERGE`. Une PR en brouillon vers `main` est appropriée ; fusion et production restent sous décision du mainteneur.
