# Suivi longitudinal privé S1 / S2 / S3

## Périmètre et sources

Les CSV canoniques regroupés par évaluateur sont la source du suivi,
en lecture seule dans soumissions/. Le migrateur conserve en parallèle
les journaux source sans les modifier. Chaque ligne correctement journalisée constitue
un essai (même si le score est 0). Min/max sont les scores bruts et ne sont
pas normalisés sur 20.

Les tableaux couvrent les TD, devoirs maison (DM) et contrôles actifs
du catalogue. Les synthèses initiales td3-s1, td4-s1, td5-s1 et td6-s1
sont **comptabilisées**, distinctement des approfondissements one/bis/ter.
Seul le contrôle historique Controletilt-s1 reste exclu. Les versions
anciennes de chaque évaluateur sont filtrées par la colonne Version du contrat,
sans devoir séparer les dossiers physiques. Le DM S1 v1 reste inclus.

Un score technique provisoire ne constitue pas une note académique
définitive ; aucune correction ni aucun barème n'est modifié.

## Sorties nominatives privées

Les exports recalculés dans soumissions/suivi/ sont :

- progression_S1.csv, progression_S2.csv, progression_S3.csv :
  une ligne par numéro étudiant, nom, prénom et trois colonnes par évaluation
  (identifiant__min, identifiant__max, identifiant__essais).
  Absence de dépôt : min/max vides et zéro essai.
- catalogue_evaluations.csv : liste des évaluations, type, version et nature
  du score, pour interpréter les colonnes.
- correspondances_a_valider.csv : identités sans numéro et suggestions
  fondées sur une correspondance exacte (nom, prénom, classe) avec
  numéro unique déjà observé.
- anomalies.csv : erreurs de CSV, identifiants absents et conflits.

Les fichiers utilisent le séparateur point-virgule et la virgule décimale.
Les numéros étudiants sont des chaînes : lors de l'import dans Excel,
imposer le format Texte pour conserver les zéros initiaux.

Ces fichiers sont dans le volume Docker persistant, ignoré par Git.
Aucune route publique de consultation ou de téléchargement n'est créée.
Il s'agit de données personnelles : ne jamais les commiter ni les
diffuser aux étudiants.

## Correspondances à valider

Aucune suggestion n'est appliquée automatiquement. Après contrôle dans
la source administrative, créer dans soumissions/suivi/ un fichier
correspondances_validees.csv avec les colonnes exactes :

    Nom;Prénom;Classe;Numéro étudiant

Exemple fictif :

    Martin;Léa;G1;00012345

Une correspondance est indexée sur les trois premiers champs, même si la
classe a changé au cours de l'année : dans ce cas ajouter les lignes
correspondantes après vérification. Toute correspondance contradictoire
est signalée et ignorée. Les CSV d'origine ne sont jamais modifiés.

Les modifications de la table validée sont reprises au prochain dépôt
accepté ou lors d'un recalcul manuel.

## Mise à jour et période

Après chaque soumission acceptée, l'application écrit le cahier, le rapport
et enfin le CSV, puis recalcule les exports sous un verrou interprocessus
sur le même volume que les CSV. Chaque export est remplacé atomiquement.
Une erreur de consolidation n'annule pas un dépôt étudiant déjà écrit ;
elle est signalée dans les journaux du serveur.

Premier calcul, ou recalcul à la demande dans le conteneur :

    docker compose exec corrector-tal python progression.py --annee 2026-2027

Recalcul sur une copie privée hors production :

    python app/progression.py --root /chemin/prive/soumissions --annee 2026-2027

La variable TAL_ACADEMIC_YEAR (format 2026-2027), si configurée, est
utilisée par défaut. Sans année, tous les historiques compatibles sont
lus et plusieurs promotions peuvent être mêlées. La fenêtre annuelle
va du 1er septembre au 31 août, d'après les dates des CSV serveur.

## Limites et validation

- Un essai correspond à une ligne, non à un identifiant de dépôt unique.
  Les journaux historiques de l'ancien mécanisme peuvent contenir des lignes
  sans fichier associé ; le migrateur les conserve sans altération.
- Les scores ne sont pas agrégés entre correcteurs à barèmes différents.
  Min/max n'indiquent pas à eux seuls le sens chronologique des progrès.
- Les soumissions destinées à la relecture humaine seule ne reçoivent
  pas de score et ne sont pas ajoutées artificiellement au suivi noté.
- Un recalcul intégral est effectué après chaque dépôt. Mesurer son coût
  si les historiques deviennent volumineux avant un déploiement massif.

Vérifications prévues :

    python -m unittest discover -s tests -p test_progression.py -v
    python -m unittest discover -s tests -v

Les tests de suivi reposent sur des noms, identifiants et scores fictifs.

La structure physique et la migration non destructive sont décrites dans
MIGRATION_STOCKAGE_EVALUATIONS.md. Une migration --apply est obligatoire
avant que le nouveau suivi puisse reprendre les anciens dépôts.

La nouvelle nomenclature des dossiers physiques du S1 est `S1_TD1` à `S1_TD7`, avec déclinaisons `S1_TD3_one/bis/ter` et `S1_TD4_A/B/C` à `S1_TD6_A/B/C`. Voir [MIGRATION_PHYSIQUE_S1_V2.md](MIGRATION_PHYSIQUE_S1_V2.md) avant d'activer le stockage sur le serveur.

## Diagnostic d'une évaluation manquante

Le nombre de fichiers dans nb/ et rapport/ **ne permet pas** de déduire
le nombre d'étudiants et d'essais. Le consolidateur compte les lignes
CSV conformes : date de l'année, version de contrat actuelle,
score numérique, identité complète et numéro étudiant valide ou
correspondance validée manuellement.

La commande suivante est en lecture seule et n'affiche pas les
identités des étudiants :

    docker-compose exec -T corrector-tal python diagnostic_progression.py --evaluation td4-s1 --annee 2026-2027

Elle compare le nombre de cahiers, de rapports, de lignes source,
d'essais exploitables et de lignes retenues dans progression_S1.csv.
Les causes de non-prise en compte (année, contrat, score, numéro) sont
ventilées sans divulguer de noms. Une régénération manuelle peut se
faire avec :

    docker-compose exec -T corrector-tal python progression.py --annee 2026-2027

Si le diagnostic indique un contrat ancien, ne pas attribuer
automatiquement ses scores à la nouvelle version sans vérifier
la correspondance pédagogique des barèmes. La présence de fichiers
sources conserve la preuve du travail, indépendamment de leur
évaluabilité automatique.

## Audit de l'ensemble des TD

Après le rétablissement des TD3–TD6 initiaux dans la PR #40,
le contrôle exhaustif est documenté dans
[AUDIT_PROGRESSIONS_TOUS_TD.md](AUDIT_PROGRESSIONS_TOUS_TD.md).
Il couvre 34 TD actifs : 19 S1, 3 S2 et 12 S3.
La commande audite les CSV et les relevés sans les réécrire :

    docker-compose exec -T corrector-tal python audit_progressions.py --annee 2026-2027

Ajouter --toutes-evaluations pour inclure les DM et contrôles.
