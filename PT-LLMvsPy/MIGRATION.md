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
- Lors de l’import initial, le 01 résolvait la révision en SHA avant de charger
  la bibliothèque et l’annexe Gemini.
- Les documents de distribution et le lien vers le notebook de cadrage sont
  réorientés vers le nouveau répertoire.
- Tests exécutés depuis le sous-projet afin d'éviter toute collision avec les
  tests et scripts de l'application TAL principale.

Aucun changement n'est effectué au dépôt privé d'origine. Les corrections
postérieures à cet import devront être réintégrées intentionnellement : il
**n'existe aucune synchronisation automatique** entre les deux dépôts.

## Contrôle de reproductibilité

Les quatre cahiers utilisent désormais la branche `main` du dépôt public pour
installer la bibliothèque. Le 01 lit également les annonces de Gemini sur
`main`. Les métadonnées de son archive enregistrent le nom de la branche et
les versions du cahier et du paquet. Le texte source de Faguet conserve sa
référence historique. Les anciennes archives gardent leurs métadonnées d’origine.
