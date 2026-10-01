# Consolidation complète du semestre 2

Base de revue : `b7650e3d035846a67014b94e463a08cd43b67fb5`, après fusion de la PR 21. Les sept sujets S2 sont désormais regroupés dans leurs dossiers de semestre : trois TD dans `Notebooks TD/S2/`, trois évaluations actives et le contrôle final inactif dans `Notebooks contrôles finaux/S2/`.

## Progression et conservation

La [matrice avant conception](pedagogy/s2_complete_review_coverage.md) et les bilans [TD](s2_review_td_coverage.md) et [contrôles](s2_review_controls_coverage.md) documentent les activités. Les numéros historiques sont conservés, mais le parcours suit les prérequis : TD3, contrôle TD2, TD5, contrôle TD4 et devoir maison, puis TD6. TD3 et TD5 se déploient chacun sur deux séances de deux heures ; TD6 sur une séance de deux heures. Aucun exercice n’est retiré.

Les sept sujets comptent 140 questions : 65 dans les TD, 57 dans les trois évaluations actives, 18 dans le contrôle final. Les six correcteurs actifs traitent donc 122 questions. Les maxima historiques restent 20, 30, 40, 25, 20 et 40 points respectivement pour contrôle TD2, TD3, contrôle TD4, TD5, TD6 et devoir maison.

Les fichiers `tests/fixtures/s2_complete_review_source_baseline.json` et `tests/test_s2_progression_preservation.py` fixent les sources d’avant conception et vérifient leur conservation, l’ordre des cellules, les contrats et la distribution. Les seules substitutions de contenu historique autorisées sont le tuteur, l’identification, le titre erroné « Contrôle S3 » du contrôle TD4 et les lignes d’affichage de résultats. Les calculs et données restent intacts ; la mention monétaire du TD3 Q1 reste dans l’exercice, son affichage canonique n’ajoute plus de suffixe après la valeur. Les anciennes sorties exécutées du sujet TD3 sont effacées pour distribuer un sujet vierge.

Les fixtures historiques de migration restent inchangées : la nouvelle preuve s’y rattache explicitement. Les 37 autres notebooks, dont les S1, S3, corrigés et l’archive `Notebooks contrôles finaux/DevoirS2.ipynb`, sont protégés par leur empreinte complète.

## Contrat d’évaluation et tutorat

Voir le [contrat S2 v2](s2_evaluation_v2.md). Chaque sujet porte une identité de notebook, des identifiants uniques de cellule, les rôles des cellules et une question canonique par réponse. Nom, prénom, classe et numéro étudiant sont nécessaires pour déposer une copie active. Les anciennes versions sont refusées avec « mauvaise version du notebook », sans note ni sauvegarde.

Les sorties enregistrées sont comparées par valeur et type ; les preuves syntaxiques doivent dépendre de la réponse de la bonne question. Le serveur ne lance jamais le code soumis. Le score est technique et provisoire ; les justifications restent soumises à relecture humaine. Les TD montrent leur retour formatif ; contrôles et devoir maison ne montrent qu’un accusé de réception.

Le tuteur apparaît à la fois dans les métadonnées et dans la première cellule Markdown. Au S2, un exemple minimal distinct peut accompagner le dialogue après une tentative ; la résolution complète immédiate reste exclue. Contrôles, devoir maison et final refusent toute assistance. Les essais, exemples, consignes et cellules techniques ne constituent pas des réponses évaluées.

## Déploiement et redistribution

La dernière cellule HTML contient `__TAL_PUBLIC_URL__` dans les sources. Le déploiement lit `TAL_PUBLIC_URL` dans l’environnement ou le fichier `.env` local et injecte l’adresse dans les seules copies distribuées. Le HTML rend le lien lisible ; l’adresse est nécessairement accessible dans le notebook distribué.

Après fusion, mettre à jour le dépôt, conserver le fichier d’environnement et le volume des soumissions, puis lancer :

```bash
bash deploy.sh
```

Pour générer uniquement les supports, y compris depuis PowerShell :

```powershell
python app/prepare_student_notebooks.py render --env-file .env
python app/prepare_student_notebooks.py verify --env-file .env
```

Redistribuer obligatoirement les **six nouveaux supports S2 actifs** depuis `dist/Notebooks TD/S2/` et `dist/Notebooks contrôles finaux/S2/`. Une ancienne copie v1 n’est pas migrée automatiquement. La distribution générale conserve 33 sujets et 34 profils de tuteur. Le contrôle final S2 possède ses métadonnées et sa cellule HTML, mais reste inactif et exclu de `dist` : son correcteur et son barème par question devront faire l’objet d’une mission explicite avant utilisation via le dépôt.

Les résultats v2 sont isolés dans `soumissions/<identifiant>-v2/<classe>/`. Le numéro étudiant distingue les homonymes ; les CSV et rapports historiques restent conservés.

## Vérifications et intégration

La suite vérifie les contrats, les six familles de correction, les variantes acceptées, les faux positifs, la confidentialité des contrôles, l’identité, les versions refusées, la conservation pédagogique et les deux parcours de dépôt. La vérification de distribution contrôle 33 sources puis les 33 copies rendues, y compris le préfixe de proxy. La CI ajoute le démarrage Docker et les sondes HTTP.

Vérification locale du 1er octobre 2026 : 281 tests réussis, compilation Python réussie, 34 tuteurs synchronisés, 33 sources contrôlées, 33 copies générées et vérifiées avec une adresse neutre. La sonde Flask annonce 33 évaluateurs ; les formulaires de l’accueil et de `/submit` respectent le préfixe `/universite/tal`. Docker n’est pas disponible dans cet environnement local ; le résultat du test conteneur doit être confirmé par la CI de la PR.

Les revues indépendantes technique et pédagogique précèdent la gouvernance. L’Integration-Master ayant produit les tests et cette documentation, son verdict final est `MAINTAINER_REVIEW` ; fusion et déploiement restent à la décision de l’enseignant.
