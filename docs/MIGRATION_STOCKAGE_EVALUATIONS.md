# Migration du stockage TAL : un dossier par évaluation

## Résultat attendu

Par exemple pour la route /eval/td2-s1, le nom stable du module
app_correction_TD2_S1 donne le dossier physique TD2_S1 :

    soumissions/TD2_S1/
        notes_TD2_S1.csv
        nb/
            MARTIN_Alice_00123_<id unique>_TD2_S1.ipynb
        rapport/
            MARTIN_Alice_00123_<même id unique>_td2-s1.html

Les noms de classe (M1_TILT, M1_TILT_Programmation, Master_TILT, etc.)
ne créent plus de répertoire. La valeur déclarée par l'étudiant est
conservée dans la colonne Classe du CSV : elle n'a aucun effet sur le
chemin physique. Les contrats notebook (v2/v3) continuent d'exister
pour identifier et valider les copies ; seul le suffixe de stockage
-v2/-v3 disparaît.

Chaque réception a un identifiant unique commun aux noms de copie,
de rapport et à l'origine du journal. Aucune copie ne remplace un
essai antérieur, même si le nom et le fichier ont été réutilisés.

Le CSV porte toujours les données personnelles, le score, sa nature,
le contrat versionné et l'origine de la ligne, sous un en-tête uniforme.
Des contrats v1 et v2 d'une même route peuvent être archivés dans
le même CSV sans être considérés équivalents : le suivi ne retient
que les lignes du contrat actuellement en vigueur.

## Migration non destructive : procédure recommandée

**Faire une sauvegarde intégrale du dossier soumissions avant la migration.**
Aucune ancienne arborescence n'est supprimée par le script.

La migration et le changement de code doivent être réalisés dans
la même fenêtre de maintenance : l'ancienne application écrit dans
les dossiers avec classes, et la nouvelle écrit directement au niveau
de l'évaluation. Éviter tout dépôt concurrent pendant l'opération.

1. Faire le pull et construire la nouvelle image, sans la démarrer.
2. Arrêter le service corrector-tal (un ancien conteneur en cours
   d'écriture ne doit pas rester actif).
3. Exécuter le script une première fois sans --apply pour voir le
   bilan des groupes, des copies et des lignes à fusionner.
4. Après examen du diagnostic, exécuter --apply sur la même copie
   de soumissions. Le script vérifie tous les schémas et toutes les
   collisions avant les premiers changements.
5. Vérifier le résultat et les indicateurs de progression, puis
   démarrer la nouvelle application.

Exemple de commandes dans le répertoire docker-compose.yml :

    docker compose build corrector-tal
    docker compose stop corrector-tal
    docker compose run --rm corrector-tal python migrate_storage.py
    docker compose run --rm corrector-tal python migrate_storage.py --apply
    docker compose up -d corrector-tal

Une vérification autonome des indicateurs est disponible :

    docker compose exec corrector-tal python progression.py --annee 2026-2027

La migration ne modifie ni les fichiers sources ni les journaux
historiques. Elle copie les archives dans des dossiers indépendants
des groupes, attribue un suffixe déterministe aux fichiers ayant
le même nom mais des contenus différents, et fusionne les CSV
en conservant l'origine et la ligne d'origine de chaque essai.

En cas d'interruption, une nouvelle exécution de --apply peut reprendre
sans recompter les essais déjà importés. Une ligne source modifiée
depuis l'importation provoque un arrêt au lieu d'être écrasée.
Un CSV inconnu ou une collision non résoluble interrompt la migration.

Attention : le script ne supprime pas les anciens dossiers. **Ne pas
les supprimer avant sauvegarde et vérification manuelle de la migration.**
La suppression éventuelle est volontairement hors périmètre.

## Impact sur le suivi de progression

Le module progression.py lit maintenant uniquement les journaux
plats notes_<évaluation>.csv ; les copies et journaux source encore dans
les anciens dossiers de groupes ne sont donc plus comptés avant
la migration --apply. Après migration, les différentes déclarations de
classe pour un même étudiant sont regroupées par numéro étudiant.

Le rapport de suivi reste dans soumissions/suivi/ et les correspondances
manuelles restent dans correspondances_validees.csv ; ces fichiers
ne sont pas modifiés ni supprimés par le migrateur, hormis la
régénération normale du suivi.

L'année TAL_ACADEMIC_YEAR=2026-2027 est conseillée pour ne pas mélanger
des promotions. Les noms de classes ne doivent jamais servir de clé
d'identité étudiante ; celle-ci repose sur le numéro étudiant.

## Validation avant déploiement

    python -m unittest discover -s tests -p test_storage_migration.py -v
    python -m unittest discover -s tests -p test_progression.py -v
    python -m unittest discover -s tests -v

Tests ciblés : trois libellés de classe, archives de versions antérieures,
préservation des notes/essais, collisions de noms, idempotence,
fichiers source intacts, refus d'un schéma invalide, et enregistrement
sans dossiers de groupe. Tous les exemples utilisent des données fictives.
