# Référence technique spaCy des TD1–TD2 v2

`app/s3_spacy_reference.json` est calculé par le code enseignant indépendant
`tests/build_s3_spacy_reference.py` sur les constantes `TEXT0`, `TEXT1`, `TEXT2`
de `app/s3_audit_data.py`. Le script ne lit aucun notebook, n'accepte aucun fichier
soumis et n'est jamais appelé par le serveur. Le correcteur ne charge pas spaCy :
il compare seulement les traces enregistrées à cette référence figée.

Versions observées lors de la génération du 1er octobre 2026 : Python 3.12.14,
spaCy 3.8.7, `fr_core_news_sm` 3.8.0, thinc 8.3.11, numpy 2.5.3,
typer 0.16.1 et typer-slim 0.16.1. Les versions spaCy/modèle sont vérifiées par
le script. Les empreintes SHA-256 des trois textes figurent dans le JSON et sont
vérifiées par les tests. Aucune sortie de modèle n'a été corrigée manuellement.

Dans un environnement enseignant séparé avec ces versions installées, depuis
la racine du dépôt :

```bash
python tests/build_s3_spacy_reference.py
git diff -- app/s3_spacy_reference.json
```

La génération est déterministe pour ce pipeline fixé ; le diff doit être vide.
Une divergence doit être examinée et revue, jamais publiée automatiquement en
remplacement des valeurs attendues. Le script fixe explicitement l'ordre des
annotations et des listes, les filtres et les comptages. Les dictionnaires de
fréquences sont comparés sans tenir compte de l'ordre des clés ; les ex æquo du
top 3 restent libres.

La conformité au modèle n'est pas une vérité linguistique. Sur `TEXT1`, le modèle
étiquette notamment `analysent` ADV et prend `étudiantes` comme ROOT. C'est un objet
de critique, pas une erreur à masquer en réécrivant la référence. TD1 Q4 contrôle
uniquement deux tokens distincts repérés dans la première phrase, ponctuation
comprise dans la table `all_annotations`, et une relation
renseignée ; l'analyse syntaxique et le rendu displaCy restent humains. TD1 Q5
compte 56 tokens, dont 41 hors ponctuation **et** espaces (43 si l'on conservait les
deux sauts de ligne, convention exclue par le contrat v2).

Pour TD1 Q6, l'extrait est libre : le serveur vérifie les bornes et l'absence
d'omission dans le préfixe des cinq segments, mais ne certifie pas leur segmentation
spaCy ni leurs annotations. Pour TD2 Q5, cinq triplets sont comparés à tous les tokens du Doc, ponctuation
comprise (`all_annotations`), avec leurs multiplicités ; les dix annotations Q1
restent filtrées hors ponctuation (`annotations`). Ainsi les trois points sont
éligibles au contrôle manuel, sans pouvoir en déclarer quatre. Des occurrences au triplet identique ne sont pas distinguables
sans positions supplémentaires. Les commentaires et figures sont relus humainement.
