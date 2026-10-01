# Consolidation des correcteurs S3 — contrats v2

La consolidation concerne quinze supports : TD0 à TD7 et les sept contrôles qui les suivent. Avec R0, R1 et R2 déjà révisés, les **18 correcteurs S3** exigent désormais un notebook v2 complet. Les identifiants et routes publiques restent identiques ; les 104 questions des quinze supports, les activités de deux heures et les barèmes sont conservés. La matrice et le contrat pédagogiques sont dans `docs/pedagogy/s3_complete_v2_coverage.md` et `s3_complete_v2_spec.md`.

## Distribution et mise en service

**Les quinze anciens supports doivent être remplacés après fusion et déploiement.** Une ancienne copie ne devient pas valide en changeant seulement son numéro de version. R0–R2 restent les supports v2 précédemment distribués ; la génération reconstruit néanmoins toute la distribution.

Depuis le nouveau clone du serveur, avec sa configuration d’environnement existante :

```sh
git pull
bash deploy.sh
```

`deploy.sh` régénère et vérifie les copies de `dist/` à partir de `TAL_PUBLIC_URL`, puis reconstruit le serveur. Redistribuer ensuite les quinze notebooks S3 v2 de cette distribution vérifiée. Les sources Git conservent leurs cellules et métadonnées pédagogiques sans adresse privée ni cellule de dépôt ; le générateur ajoute à chaque copie distribuée une cellule finale d’affichage HTML. La génération utilise une adresse neutre pendant les tests et ne constitue pas un déploiement de production.

Les chemins sources sont ceux du catalogue `app/notebook_catalog.json` : `Notebooks TD/S3/TD0_…` à `TD7_…` et `Notebooks contrôles finaux/S3/Controle_TD1_S3.ipynb` à `Controle_TD7_S3.ipynb`.

## Identification, refus et conservation des dépôts

Le contrat exige `metadata.tal` avec l’identifiant du sujet, son évaluateur et la version entière 2. Les cellules de réponse portent leur question et leur rôle ; l’ensemble attendu doit être complet, sans doublon. Une cellule présente mais vide reste une réponse non fournie. Les cellules peuvent être déplacées, et des cellules personnelles peuvent être ajoutées. Les exemples ne fournissent jamais la preuve d’une réponse.

Anciennes versions, métadonnées requises absentes ou contrat de cellules incomplet sont refusés par **« mauvaise version du notebook »**, avant correction ou sauvegarde, aussi bien sur `/submit` que sur les routes directes. Il n’existe pas de conversion automatique. Les routes historiques S1/S2 conservent leur compatibilité.

L’identité comprend quatre chaînes littérales non vides : `nom`, `prenom`, `classe` et `numero_etudiant`. Leur lecture AST reconnaît exactement les noms de variables et ignore les commentaires ; elle n’exécute aucune expression. Le numéro accepte 1 à 64 lettres ASCII, chiffres, tirets ou soulignements. Une identité incomplète reçoit une erreur explicite et n’est pas enregistrée.

Les nouveaux dépôts utilisent `soumissions/<identifiant>-v2/<classe>/`. Les fichiers notebook et rapport incluent le numéro étudiant, ce qui sépare les homonymes. Les anciens dossiers et CSV restent intacts ; ils ne sont ni déplacés ni fusionnés avec les résultats v2. Les contrôles renvoient uniquement un reçu public, avec détail et preuves dans le rapport privé enseignant.

## Mesures, références et limites

Les TD affichent un **score technique provisoire**, comme les contrôles. Les barèmes restent TD1 : 6 ; autres TD : 7 ; contrôles : 20 avec poids `2, 3, 3, 3, 3, 3, 3`. Ces points ne constituent pas une note globale de compétence linguistique.

TD1 et TD2 comparent maintenant les sorties sur les textes fixes à une référence indépendante du pipeline prescrit : Python 3.12.14, spaCy 3.8.7, modèle `fr_core_news_sm` 3.8.0. Les valeurs et leur provenance sont archivées dans `app/s3_spacy_reference.json`, produites à partir de code enseignant et des corpus fixes, séparément des notebooks étudiants. Aucun spaCy ni modèle n’est nécessaire au serveur de correction. Les annotations parfois discutables du modèle restent les sorties de référence ; la critique linguistique relève du travail étudiant et de la relecture humaine.

Les listes significativement ordonnées conservent les répétitions ; les entiers excluent les booléens. Les décomptes sont vérifiés indépendamment quand le corpus fermé le permet. Les choix d’exclusions de TD2 restent libres dans le contrat. TD1 Q6, qui porte sur un extrait libre, vérifie des invariants de positions et de préfixe sans prétendre certifier ses annotations linguistiques. TD3 contrôle les bornes exactes et les occurrences absolues distinctes du pivot, y compris lorsque plusieurs fenêtres de contexte se recouvrent.

Le serveur ne lance jamais le code soumis. Il inspecte les métadonnées, le code enregistré et les traces JSON, avec types et références explicites. Une trace fabriquée peut imiter une sortie correcte : le dispositif ne certifie ni l’exécution réelle, ni la fraîcheur des sorties, ni la généralité d’une fonction.

## Diagnostic et relecture

Quatre états sont distingués : conforme, incorrect, preuve absente, et non vérifiable faute d’une dépendance nécessaire. Une dépendance exploitable n’est pas invalidée par le seul score nul de sa question d’origine. À l’inverse, un schéma mal typé ne peut justifier un résultat aval.

Le rapport annonce les points attestés et les points non vérifiables à réexaminer, sans crédit automatique ni modification des poids. Il évite de présenter l’absence d’une annotation amont comme plusieurs erreurs de calcul indépendantes. Aucun score qualitatif n’est déduit d’un nombre de mots ou d’un mot-clé.

Les productions sont regroupées par question : code, commentaires, traces, analyses Markdown explicitement rattachées et formats visuels présents. Les 49 cellules « Votre analyse » des contrôles conservent leur texte et reçoivent seulement `metadata.tal_review.question`. Les cellules libres non identifiées restent séparées. Les extraits longs sont bornés et les troncatures signalées ; la copie complète reste conservée. La présence d’une figure ne note pas sa lisibilité ou son interprétation. Le HTML et les images soumis ne sont pas exécutés ou intégrés comme contenu actif ; leurs formats sont signalés et leur texte est échappé.

## Vérification et décision

Les tests couvrent les refus sans correction/persistance, l’identité et les homonymes, les contrats de cellules, les bornes et types, les fréquences de référence, les dépendances, le rendu privé et l’échappement. La fixture historique de migration reste inchangée. Les quinze nouvelles révisions sont explicitement déclarées et comparées à une seconde preuve figée du commit source `02f435dc770834b21e242592804d231e0836a4b7` : cellules, exemples, données, sorties, ordre, tuteurs et prose source hors enrichissements déclarés.

La validation complète exige la suite de régression, la compilation, les vérifications tuteurs/sources, une distribution neutre vérifiée, les routes derrière `/universite/tal/` et le smoke test Docker de CI. La double revue code/pédagogie et la gouvernance précèdent la décision de fusion du mainteneur. L’intégration ayant produit des tests et cette documentation, son verdict de clôture ne peut être que **MAINTAINER_REVIEW**, jamais une autorisation de fusion ou de production.

### Preuve locale d’intégration du 1er octobre 2026

Sur la branche de consolidation, avec l’environnement Python des exigences applicatives et `git-filter-repo` présent dans le PATH :

- `python -m unittest discover -s tests` : **199 tests réussis**, aucun ignoré, au passage d’intégration initial. Tout amendement de revue nécessite une nouvelle exécution sur la révision publiée.
- `python -m compileall -q app tests` et `git diff --check` : réussis.
- `python app/tutor_metadata.py --check` : **34 profils conformes**.
- `python app/prepare_student_notebooks.py check` : **33 sources conformes**.
- Rendu puis vérification dans `dist/integration-s3-v2`, avec l’adresse neutre `https://example.test/universite/tal` : **33 copies conformes**. Vérification supplémentaire : cellule HTML finale dans les 33 copies et version 2 dans les 18 copies S3.
- Client Flask : `/health` annonce 33 correcteurs ; `/` et `/submit` répondent 200 et proposent l’action `/universite/tal/submit` avec `X-Forwarded-Prefix`.

Docker n’est pas disponible dans cet environnement local : le build et le démarrage du conteneur restent à vérifier par le job `container-smoke` de CI sur le commit publié. Aucun notebook étudiant n’a été exécuté, et aucun déploiement en production n’a été effectué. La revue indépendante et la gouvernance sont encore requises avant le verdict global ; l’intégrateur est producteur des tests et de cette documentation.
