# Origine de l'import PT-LLMvsPy

## Copie de travail conservée

Ce répertoire est une **importation des fichiers** de la bibliothèque et des
notebooks, et non une fusion des historiques Git. L'historique d'origine reste
disponible dans son dépôt initial, sans déplacement ni suppression.

| Élément | Référence |
|---|---|
| Dépôt source | `dreymond732/PT-LLMvsPy` (privé) |
| Branche source | `docs/td01-simplification-pedagogique` |
| Commit source | `90dfd4d335ffa177c06dc2d8375221c098afa6d3` |
| Destination | `dreymond732/tal-notebook-evaluator`, sous-dossier `PT-LLMvsPy/` |
| Branche d'intégration | `feat/pt-llmvspy-colab-integrated` |
| Nombre de fichiers importés | 36 |
| Fichier source non réimporté | `.github/workflows/tests.yml` (workflow du dépôt source, sans utilité dans un sous-dossier) |
| Nouvelle CI | `.github/workflows/pt-llmvspy.yml` à la racine du dépôt public |

Le code Python, les quatre notebooks, les tests, les scripts de validation, les
données Gemini et les documents de méthode sont conservés dans ce sous-dossier.

## Adaptations réalisées après import

- Notebook 01 : installation VCS `pip` depuis le dépôt **public**
  `tal-notebook-evaluator` en utilisant `#subdirectory=PT-LLMvsPy`.
- Révision Git résolue en SHA au début de la session, appliquée à la bibliothèque
  et à l'annexe Gemini, enregistrée avec le résultat de l'analyse.
- Les documents de distribution et le lien vers le notebook de cadrage sont
  réorientés vers le nouveau répertoire.
- Tests exécutés depuis le sous-projet afin d'éviter toute collision avec les
  tests et scripts de l'application TAL principale.

Aucun changement n'est effectué au dépôt privé d'origine. Les corrections
postérieures à cet import devront être réintégrées intentionnellement : il
**n'existe aucune synchronisation automatique** entre les deux dépôts.

## Contrôle de reproductibilité

La version du notebook est indépendante de la version des fonctions. Le choix
`REVISION_GIT="main"` est résolu en SHA-1 Git avant l'installation, ce qui
garantit une révision concrète pendant une exécution, même si `main` évolue
plus tard.

Pour expérimenter avant fusion, utiliser temporairement
`REVISION_GIT="feat/pt-llmvspy-colab-integrated"`. Après fusion, laisser
`main`. Les étudiants n'ont pas à connaître le dépôt privé d'origine.
