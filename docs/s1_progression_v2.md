# TD du S1 : progression et évaluation v2

Les sept TD du S1 passent au contrat de notebook v2. Les 45 questions et leurs maxima restent inchangés : 6, 7, 6, 7, 6, 6 et 7 points. Les nouveaux entraînements servent à préparer les activités originales ; ils ne constituent pas des réponses notées supplémentaires. TD2 conserve intégralement son contenu pédagogique et son correcteur détaillé.

La matrice de conservation et les attendus techniques figurent dans `docs/pedagogy/s1_progression_v2_coverage.md` et `docs/pedagogy/s1_progression_v2_spec.md`. Les noms thématiques adoptés dans la PR précédente demeurent.

## Contrats et identification

Chaque source comporte le contrat `metadata.tal` de version 2, une cellule d’identification et toutes les cellules de réponses identifiées Q1 à Qn. Le nom du fichier téléchargé et la position des cellules ne déterminent pas la correction. Les réponses doivent être dans leur cellule identifiée ; les traces présentes dans un exemple, un entraînement ou la restitution ne sont pas des preuves pour la note.

L’étudiant renseigne nom, prénom, classe et numéro étudiant dans la cellule d’identification. Les valeurs doivent être des chaînes littérales non vides ; le numéro accepte de 1 à 64 caractères ASCII alphanumériques, `_` et `-`. Les numéros distinguent les homonymes dans les noms de copies et de rapports. Le numéro est un identifiant de dépôt, pas un mécanisme d’authentification.

Une copie v1, sans contrat ou sans les cellules requises est refusée avec « mauvaise version du notebook », sans correction ni persistance. Une cellule requise existante mais laissée vide demeure une question sans preuve ; ce n’est pas une erreur de version. Ne pas modifier simplement le numéro de version d’une ancienne copie : certains TD demandent désormais des traces complémentaires.

Les résultats et les fichiers des nouveaux TD sont rangés dans `soumissions/tdN-s1-v2/`, séparément des anciens résultats. Les anciens dossiers ne sont ni migrés ni effacés. Les contrôles du S1, le S2 et les contrats S3 restent hors de cette révision.

## Portée du résultat

Le résultat est un **score technique provisoire**, obtenu à partir du code et des sorties enregistrées. Le serveur analyse la syntaxe Python et les représentations de valeurs sans exécuter le code étudiant ni ouvrir ses fichiers. Il compare les types et les valeurs, accepte les variantes explicitement admises et conserve les pondérations des questions.

Les retours distinguent résultat incorrect, preuve manquante ou illisible, construction demandée non repérée et dépendance non vérifiable. Les productions textuelles sont repérées pour relecture ; leur présence n’établit pas leur pertinence. Les sous-critères permettent de comprendre les points obtenus sans assimiler une preuve absente à plusieurs erreurs conceptuelles.

L’analyse statique ne garantit pas que les sorties ont été produites par le code actuel. Elle ne prouve pas la généralité des fonctions sur toutes les entrées. Les sorties périmées ou falsifiées, les variantes complexes non reconnues et la qualité des analyses linguistiques restent des limites explicites : l’enseignant peut relire le notebook et réviser son appréciation.

## Distribution après fusion

Conserver `TAL_PUBLIC_URL` dans la configuration locale du serveur, puis lancer :

```bash
git pull
bash deploy.sh
```

Le déploiement génère les 33 notebooks actifs de distribution et remplace le substitut `__TAL_PUBLIC_URL__` uniquement dans `dist/`. Les sept TD S1 sont à redistribuer depuis `dist/Notebooks TD/S1/`. Leur cellule HTML de restitution reste finale et unique ; les sources Git ne contiennent pas l’adresse du serveur.

Les tuteurs restent présents dans les métadonnées et la première cellule Markdown. Ils guident les TD du S1 sans fournir de solution codée ; les contrôles gardent leur interdiction d’assistance.

## Preuves de conservation et tests

La fixture `tests/fixtures/s1_progression_v2_source_baseline.json` est extraite du commit `322abf53b4a1ff96c1652acfa21b4d27185bfa1a`, antérieur aux enrichissements. Elle conserve aussi la preuve de la PR précédente : seules dénomination, métadonnées et cellule de restitution avaient alors changé. La fixture historique de migration n’a pas été régénérée.

Les tests vérifient la conservation ordonnée des cellules originales, les 45 réponses, l’ajout des entraînements, les identifiants, l’exclusion des cellules non notées, le refus des anciens contrats et la persistance versionnée. Les références positives et les variantes négatives contrôlent les correcteurs ; les sorties des fixtures sont des preuves synthétiques, jamais l’exécution de copies étudiantes. La vérification de distribution porte sur l’ensemble des 33 sujets, y compris les niveaux non modifiés.
