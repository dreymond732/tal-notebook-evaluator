# Suivi longitudinal privé S1 / S2 / S3

## Périmètre et sources

Les CSV originaux des évaluateurs restent la source de vérité, en lecture
seule dans soumissions/. Chaque ligne correctement journalisée constitue
un essai (même si le score est 0). Min/max sont les scores bruts et ne sont
pas normalisés sur 20.

Les tableaux couvrent les TD, devoirs maison (DM) et contrôles actifs
du catalogue. Les synthèses historiques td3-s1, td4-s1, td5-s1, td6-s1
et le contrôle historique Controletilt-s1 sont exclus. Les anciennes
versions des sujets sont également exclues : seul le répertoire correspondant
au contrat actuel est lu. Le DM intermédiaire S1 conserve son contrat v1
actuel et est inclus.

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

Après chaque soumission acceptée, l'application écrit le CSV, le cahier
et le rapport, puis recalcule les exports sous un verrou interprocessus
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
  L'ancien mécanisme peut laisser une ligne si la sauvegarde du cahier
  échoue ensuite ; rien n'est supprimé ni réécrit.
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
