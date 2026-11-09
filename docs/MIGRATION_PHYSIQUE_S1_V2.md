# Migration physique des dossiers S1 — version 2

Cette opération suit le renommage pédagogique de la PR #37 et la
consolidation historique de la PR #35. Elle porte sur les **19 TD du S1** ;
aucun changement de dossier S2, S3, de devoir maison ou de contrôle.

## Noms physiques attendus

- TD1_S1 à TD7_S1 deviennent S1_TD1 à S1_TD7.
- TD3_one_S1, TD3_bis_S1, TD3_ter_S1 deviennent
  S1_TD3_A, S1_TD3_B, S1_TD3_C dans la version actuelle.
  **Attention** : des déploiements antérieurs ont déjà archivé des données
  sous S1_TD3_one, S1_TD3_bis, S1_TD3_ter ; voir ci-dessous la
  migration complémentaire obligatoire si ces dossiers existent.
- TD4–TD6_one/bis/ter_S1 deviennent S1_TD4–TD6_A/B/C.

Exemple :

    soumissions/TD4_one_S1/notes_TD4_one_S1.csv
    soumissions/TD4_one_S1/nb/
    soumissions/TD4_one_S1/rapport/

sera copié vers :

    soumissions/S1_TD4_A/notes_S1_TD4_A.csv
    soumissions/S1_TD4_A/nb/
    soumissions/S1_TD4_A/rapport/

Les identifiants techniques des correcteurs, les URL de dépôt, les
versions de contrats des cahiers et les barèmes ne changent pas. Les
notebooks déjà distribués restent utilisables.

## Sécurité de la migration

Le script migrate_storage_s1.py effectue uniquement une simulation sans
option. Aucune écriture n'est alors réalisée dans le volume.

Avec --apply et --backup-confirmed, il :
- conserve intacts les dossiers et CSV originaux ;
- copie chaque cahier et rapport en contrôlant son SHA-256 ;
- préserve les collisions de noms, par suffixe déterministe ;
- fusionne le CSV canonique, avec provenance de chaque ligne et
  conservation du numéro d'étudiant, du score, du contrat et de la date ;
- refuse une source modifiée après migration, les liens symboliques et
  les fichiers inattendus ;
- peut être relancé sans créer de doublons ;
- recalcule les synthèses de progression.

Une identité d'essai est formée par le chemin d'origine et le numéro
de ligne de la source. L'ancienne provenance est conservée en suffixe.
Un CSV déjà migré partiellement est repris ; un CSV incompatible
interrompt la procédure. Ne jamais supprimer les archives source
avant une vérification humaine complète.

## Procédure sur serveur

1. Faire une sauvegarde complète et restaurable du volume soumissions,
   en dehors du dépôt, y compris suivi et la base SQLite éventuelle.
2. Planifier une interruption des dépôts étudiants.
3. Depuis le répertoire de docker-compose.yml, après fusion de la PR,
   exécuter dans cet ordre :

    git pull
    docker-compose build corrector-tal
    docker-compose stop corrector-tal

    docker-compose run --rm --no-deps corrector-tal python migrate_storage_s1.py

4. Lire le diagnostic (nouvelles lignes, fichiers à copier, erreurs).
   Après confirmation que la sauvegarde est indépendante et exploitable :

    docker-compose run --rm --no-deps corrector-tal python migrate_storage_s1.py --apply --backup-confirmed --annee 2026-2027

5. Redémarrer, vérifier les résultats et les archives :

    docker-compose up -d corrector-tal
    docker-compose exec corrector-tal python progression.py --annee 2026-2027

ATTENTION : l'ancienne commande migrate_storage.py --apply est désormais
désactivée lorsque le nouveau format S1 est actif. Elle visait une autre
migration (regroupement de classes et retrait des suffixes de versions).

## Contrôles

Vérifier : nombre d'étudiants, nombre d'essais, minimum et maximum de
chaque TD, nombre de cahiers/rapports, suivi/anomalies.csv. Les
résultats S2 et S3 ne doivent pas changer. Si des dossiers anciens
restent, ne pas les supprimer : c'est intentionnel et nécessaire pour
une éventuelle restauration.

Tests sur données fictives :

    python -m unittest discover -s tests -p test_storage_migration_s1.py -v
    python -m unittest discover -s tests -v

La PR ne réalise aucune migration sur le volume de production.

## Harmonisation complémentaire TD3 A/B/C (novembre 2026)

Cette étape couvre les anciennes destinations **S1_TD3_one**, **S1_TD3_bis**
et **S1_TD3_ter** créées par la première migration S1. Les correcteurs
utilisent maintenant comme dossiers canoniques :

- `S1_TD3_A` : listes, correcteur interne `td3-one-s1` ;
- `S1_TD3_B` : tuples, correcteur interne `td3-bis-s1` ;
- `S1_TD3_C` : dictionnaires et ensembles, correcteur interne `td3-ter-s1`.

**Ne jamais renommer manuellement les dossiers ou les CSV** : les noms
internes des journaux, les provenances et les noms de cahiers ont des
contraintes d'intégrité. Les identifiants techniques des correcteurs
restent stables pour permettre le dépôt des anciens cahiers distribués.

La commande `migrate_td3_variants.py` copie les fichiers `nb/`, `rapport/`
et fusionne les lignes du journal canonique sans supprimer les sources.
Elle vérifie les empreintes SHA-256, refuse les conflits et peut être
réexécutée sans compter deux fois la même soumission.

1. Effectuer une sauvegarde restaurable du volume `soumissions/`.
2. Depuis le répertoire du projet, après fusion de la PR :

```bash
git pull
docker-compose build corrector-tal
docker-compose stop corrector-tal
# Simulation, sans modifier les archives :
docker-compose run --rm --no-deps corrector-tal python migrate_td3_variants.py --annee 2026-2027
```

3. Après lecture du bilan et vérification de la sauvegarde :

```bash
docker-compose run --rm --no-deps corrector-tal python migrate_td3_variants.py --apply --backup-confirmed --annee 2026-2027
docker-compose up -d corrector-tal
docker-compose exec -T corrector-tal python audit_progressions.py --annee 2026-2027
```

Si aucun dossier intermédiaire `S1_TD3_one/bis/ter` n'existe,
la simulation annonce zéro ligne et zéro archive à copier.
Les scores ne sont jamais modifiés. Les fichiers de progression sont
recalculés à la fin de l'application de la migration.

Les **trois cahiers sources** du dépôt sont également renommés en
`S1_TD3_A_listes.ipynb`, `S1_TD3_B_tuples.ipynb` et
`S1_TD3_C_dictionnaires_ensembles.ipynb`. Il faut actualiser les
copies diffusées aux étudiants, sans imposer de nouvelle version de
contrat aux cahiers déjà distribués.
