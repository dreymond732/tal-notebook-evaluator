# PT-LLMvsPy — développement de la bibliothèque et dépôts étudiants

## Deux circuits distincts

**Développement enseignant (GitHub)** : les fonctions Python, les tests automatisés,
les versions de la bibliothèque et les notebooks modèles sont maintenus dans ce
dépôt. La modification du code partagé reste soumise à une pull request examinée
et à des tests de régression.

**Travail étudiant (Google Colab → Drive)** : les étudiantes n'ont besoin ni de
compte GitHub ni d'accès en écriture au dépôt. Elles installent la bibliothèque directement depuis un commit GitHub public,
complètent le TD01 avec le protocole commun, contrôlent leurs résultats et déposent
une archive dans le dossier Google Drive identifié dans le notebook. Les anomalies repérées dans la bibliothèque sont décrites dans
leur rapport, puis traitées séparément par l'équipe enseignante.

Pour la publication du dépôt, l'autorisation Drive et les livrables : voir
[Guide TD01 Colab et Drive](docs/deploiement_colab_drive_td01.md).

## Cycle d'une correction de code par l'équipe enseignante

1. Partir de la branche principale, créer une branche de correction.
2. Définir les entrées/sorties et les cas limites indépendamment de Faguet.
3. Écrire un test qui aurait échoué avant la correction.
4. Préserver les positions et empreintes du texte source.
5. Ouvrir une PR précisant objectifs, conventions, tests et limites.
6. Vérifier les tests et approuver explicitement avant fusion.

## Conventions

- Ne jamais faire correspondre artificiellement une mesure aux chiffres de Gemini.
- Ne jamais considérer une citation rapprochée comme vérifiée sans contrôle.
- Le token, le type, le lemme et le mot vide sont des représentations ou des filtres, pas des suppressions implicites.
- Conserver le corpus brut et, pour le texte épuré, un manifeste et une correspondance des indices.
- Le calcul des métriques original/épuré doit employer la même configuration spaCy.
- L'approbation étudiante et la validation du protocole commun par l'enseignant sont distinctes.

## Vérifier

```bash
python -m pip install -e ".[test,nlp]"
python -m pytest -q
```
