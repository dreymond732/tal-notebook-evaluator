# PT-LLMvsPy — développement de la bibliothèque et dépôts étudiants

## Deux circuits distincts

**Développement enseignant (GitHub)** : les fonctions Python, les tests automatisés,
les versions de la bibliothèque et les notebooks modèles sont maintenus dans ce
dépôt. La modification du code partagé reste soumise à une pull request examinée
et à des tests de régression.

**Travail étudiant.** Chaque étudiant crée le dossier `S3-PythonVsLLM` dans son Drive. Les quatre notebooks travaillent dans le stockage temporaire de Colab. Après chaque séance, l’étudiant télécharge les fichiers portant son numéro sur son ordinateur, puis les importe dans son dossier personnel. À la séance suivante, il remet les pièces demandées dans le volet **Fichiers** de Colab.

Le partage se fait dans l’interface de Drive. À la première revue, l’étudiant copie son ZIP du corpus nettoyé depuis son dossier personnel dans le dossier partagé. En fin de S3, il y copie les trois JSON des fréquences, des cooccurrences et de l’audit pour la synthèse du projet tuteuré. Il conserve les originaux dans son dossier personnel. Les anomalies observées sont consignées dans le cahier et discutées en revue.

[Procédure de sauvegarde, de reprise et de remise](docs/deploiement_colab_drive_td01.md)

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
- Préciser quelles occurrences sont retenues, si les unités distinctes sont des formes ou des lemmes, et si le calcul inclut les mots vides.
- Conserver le corpus brut et, pour le texte épuré, un manifeste et une correspondance des indices.
- Le calcul des métriques original/épuré doit employer la même configuration spaCy.
- L'approbation étudiante et la validation du protocole commun par l'enseignant sont distinctes.

## Vérifier

```bash
python -m pip install -e ".[test,nlp]"
python -m pytest -q
```
