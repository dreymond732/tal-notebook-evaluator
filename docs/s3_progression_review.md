# Revue des TD du S3 et distribution

La revue porte sur les huit TD de deux heures, de TD0 à TD7, ainsi que sur les trois ressources de révision R0, R1 et R2. Ces dernières conservent leur format court de 25, 25 et 30 minutes. Les sept contrôles du S3 sont hors modification pédagogique. Le point de départ est le commit `933b0df6565fbd7d64f02db941eda5e8358eb16e`, après fusion des PR 19 et 20.

## Conservation et dénomination

Les onze noms existants décrivent déjà le contenu : diagnostic texte, fondations spaCy, analyse de corpus, concordances et citations, cooccurrences, associations, visualisations, audit LLM, puis les trois ressources de révision Python texte, document spaCy et fréquences réutilisables. Ils sont conservés, ainsi que les identifiants des évaluateurs et les contrats en version 2.

Le renforcement ajoute des explications, exemples et entraînements ; il ne retire aucune des 67 questions évaluées ni aucune activité originale. Les anciens identifiants de cellules et leur ordre relatif sont conservés. Le tuteur reste la première cellule et son contenu est synchronisé avec les métadonnées du notebook et le manifeste pédagogique.

La fixture `tests/fixtures/s3_progression_review_source_baseline.json` a été extraite directement du commit de départ avant modification. Le test de conservation vérifie les sources originales comme préfixes exacts, tous les autres champs, les contrats des questions et les ajouts de métadonnées manquantes. Les 28 cellules originales d’interprétation de TD4 à TD7 et la cellule de reprise personnelle de TD7 reçoivent également un lien `tal_review.question` sur une liste fermée d’identifiants : leurs analyses restent visibles dans le rapport enseignant après classification des cellules. Les énoncés et exemples ne sont pas collectés comme analyses étudiantes. Seule la régénération ciblée du tuteur bénéficie d'une comparaison distincte par le vérificateur de politique. Les empreintes des sept contrôles interdisent une modification incidente. L'ancienne preuve de migration reste figée : sa comparaison passe par cette nouvelle référence parent pour les TD enrichis, tandis que les contrôles restent comparés directement.

## Restitution et déploiement

Chaque source des onze TD et ressources de révision se termine par la même cellule canonique de restitution HTML que les TD du S1. Elle porte le rôle `submission`, n'a ni sortie enregistrée ni compteur d'exécution et contient uniquement le marqueur `__TAL_PUBLIC_URL__`. Les imports de cette cellule relèvent de l'infrastructure ; ils ne constituent pas une réponse pédagogique.

La commande habituelle `bash deploy.sh` vérifie les sources, génère les notebooks dans `dist/`, contrôle le résultat, puis lance Docker. `TAL_PUBLIC_URL` est lu dans l'environnement ou dans le fichier de configuration fourni à la commande. L'adresse n'est jamais réécrite dans les notebooks sources. Le rendu remplace la dernière cellule sans en ajouter une seconde ; toutes les autres données du notebook sont identiques. La génération des 33 sujets actifs demeure unique et exclut les corrigés modèles.

Après fusion et déploiement, redistribuer les onze notebooks S3 depuis `dist/`. Les copies v2 antérieures conservent le même contrat d'évaluation ; elles n'acquièrent pas automatiquement les nouveaux appuis et la cellule de restitution. Les copies v1 restent refusées avec « mauvaise version du notebook » avant évaluation et enregistrement.

## Portée des vérifications

Les tests vérifient l'identification des questions, l'isolement des cellules d'entraînement et d'infrastructure, les identités étudiantes obligatoires, le refus des versions incompatibles, les résultats enregistrés et la conservation des activités. Le serveur n'exécute pas le code étudiant. Le score reste technique et provisoire : il ne certifie ni une exécution effective de toute la copie ni la qualité d'une interprétation linguistique. Les analyses et choix méthodologiques appellent une relecture humaine.

La durée annoncée est une organisation pédagogique prévue, à ajuster après observation en séance. L'intégration, productrice des tests et de cette documentation, fournit un avis `MAINTAINER_REVIEW` après les revues indépendantes et les contrôles de CI ; elle ne s'attribue pas une validation indépendante.

## Preuves d'intégration locales

Au terme de la production, le 1er octobre 2026 :

- `python -m unittest discover -s tests` : 254 tests réussis, sans test ignoré ;
- `python -m compileall -q app tests` : réussi ;
- `python app/tutor_metadata.py --check` : 34 profils synchronisés ;
- contrôle des sources, génération puis vérification : 33 sujets actifs conformes, avec l'adresse neutre `https://example.test/universite/tal` ;
- `/health` : 33 évaluateurs ; formulaires `/` et `/submit` correctement préfixés par `/universite/tal`.

La CI GitHub et la construction Docker sont à confirmer sur le commit publié ; leurs liens et résultats sont à joindre à la PR. Avis de l'intégration productrice : **MAINTAINER_REVIEW**, sous réserve des revues indépendantes et de ces contrôles distants.
