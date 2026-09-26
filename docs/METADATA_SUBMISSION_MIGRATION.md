# Consolidation TAL : identification et dépôt automatique

Mission : transposer la refonte TQR (#51, #54 et correction #56) au cours TAL.
Branche : `integration/tal-metadata-submit`. Base : `2a367529963f66a186dff1658b5951d0dbc27642`.
Il s'agit d'un changement de contrat rétrocompatible, sans changement de barème.

## Catalogue et périmètre

`app/notebook_catalog.json` inventorie les 33 sujets du tuteur. Les 32 actifs
(8 S1, 6 S2, 18 S3) correspondent exactement aux correcteurs enregistrés.
`ControleFinalS2.ipynb` reste inactif et inchangé : aucun correcteur ni bouton
n'est activé implicitement. Les neuf corrigés exclus du manifeste tuteur
restent inchangés, y compris les deux fichiers historiquement non valides en JSON.

Les valeurs `id`, `version` et `evaluator` de `metadata.tal` désignent une entrée
du catalogue serveur. La version 1 est la version du contrat d'identification.
Le semestre et le mode viennent du serveur ; les champs fournis par le notebook
ne donnent aucun droit d'import, d'exécution ou d'accès aux rapports enseignants.
En particulier `td2-S2` et `td4-S2` restent des contrôles.

Les cellules évaluées portent `metadata.tal.question` et `role: answer` ;
l'identification existante porte `question: identity`, `role: identification`.
Les nouvelles métadonnées n'écrasent ni `tal_tutor`, ni `colab.aiContexts`,
ni le commentaire du tuteur en première cellule. Les 313 réponses et les
28 cellules d'identification déjà présentes sont identifiées. Aucun exercice,
exemple, sortie, compteur, identifiant Jupyter ou ordre de cellule n'est modifié.
TD5 S2 et R0–R2 S3 n'avaient pas de cellule d'identification : cette migration
n'en ajoute pas et ne résout pas cette limite pédagogique historique.

## Résolution et compatibilité

Le formulaire de l'accueil et `/submit` reconnaissent le sujet sans utiliser
le nom du fichier. Une copie renommée conserve son correcteur. La cohérence
identifiant/version/évaluateur est vérifiée avant correction et sauvegarde.
Un identifiant inconnu, une version non supportée ou des métadonnées ambiguës
produisent un refus explicite, sans tentative de deviner le sujet.

Les anciennes routes `/eval/<nom>` et les pages par semestre restent utilisables
pour les copies sans identification automatique. Une copie identifiée déposée
sur la mauvaise ancienne route est refusée. Les deux parcours partagent le même
traitement de persistance et de confidentialité : retour formatif pour un TD,
accusé de dépôt seulement pour un contrôle. Les rapports S3 conservent la
distinction entre score technique provisoire et appréciation enseignante.

Les moteurs ciblent les réponses identifiées tout en gardant leurs preuves
existantes (code statique, sorties enregistrées, traces). Une copie comportant
des identifiants d'exercices explicites ne peut pas récupérer une réponse dans
une autre cellule non identifiée en cas d'absence : cela empêche un exemple de
remplacer une réponse manquante. Les copies sans ces identifiants gardent leur
recherche historique. Un doublon explicite est toujours une erreur.

Les contrôles formatifs qui analysent historiquement plusieurs cellules
conservent cette agrégation. Les sous-sorties Qnb du TD2 S1 et les fonctions
auxiliaires du S3 restent prises en compte. Les cellules de service
`submission` et `infrastructure` sont exclues de l'évaluation.

L'identification par métadonnées permet aussi de retrouver huit cellules dont
le commentaire historique n'était pas reconnu. Elle lit les valeurs écrites
dans le code, jamais des noms/prénoms fournis comme métadonnées. Les valeurs
non renseignées des sujets restent à compléter par les étudiants.

## Copies distribuables et adresse du serveur

Le dépôt Git ne contient pas l'adresse de production. Le script
`app/prepare_student_notebooks.py` ajoute le bloc HTML uniquement dans les copies
de `dist/`, en lisant `TAL_PUBLIC_URL` dans l'environnement ou dans un fichier
`.env` local. Il ne dépend pas d'une variable d'environnement dans Colab.

Le script ne source pas le fichier `.env`, n'exécute aucune de ses expressions
et ne lit que la clé concernée. L'environnement du processus a priorité sur ce
fichier. Les URL avec identifiants, paramètres ou fragment sont refusées.
La valeur doit être la racine publique complète, préfixe du proxy compris,
sans ajouter `/submit`.

Exemple fictif de ligne à ajouter au `.env` existant :

```dotenv
TAL_PUBLIC_URL=https://example.invalid/universite/tal
```

Le HTML rend le bouton lisible ; il ne rend pas son adresse secrète pour les
étudiants. L'adresse est présente dans les copies distribuées, qui ne doivent
pas être replacées dans Git. `dist/` et les répertoires temporaires de génération
sont ignorés. Les sorties enregistrées des cellules sont aussi contrôlées.

La génération prépare puis vérifie un répertoire temporaire complet avant de
remplacer l'ancienne distribution. Elle refuse de remplacer un dossier existant
non reconnu ou contenant des fichiers étrangers. Elle ne distribue ni corrigés
ni sujet inactif et laisse tous les fichiers sources intacts.

## Déploiement et distribution

Déployer le serveur compatible avant d'envoyer les nouveaux supports.
Conserver le `.env` et le volume `soumissions/` du serveur existant.
La génération nécessite Python 3.10 ou supérieur ; l'image utilise Python 3.12.

Sur le serveur, depuis le nouveau clone :

```bash
bash deploy.sh
```

Le script prépare et vérifie les 32 copies, lance `docker compose up -d --build`
avec le fichier d'environnement, puis vérifie `/health` à l'intérieur du
conteneur. Ce contrôle local ne remplace pas une vérification de l'URL publique
à travers le reverse proxy. Un fichier d'environnement externe peut être passé
comme premier argument, sans être copié dans le dépôt.

La génération seule fonctionne aussi dans PowerShell :

```powershell
python app/prepare_student_notebooks.py render --env-file .env
python app/prepare_student_notebooks.py verify --env-file .env
```

Distribuer les fichiers de `dist/Notebooks TD/` et
`dist/Notebooks contrôles finaux/` par le canal pédagogique habituel (Moodle,
Drive puis Colab). Les sources ouvertes directement depuis GitHub contiennent
les métadonnées mais pas le bouton privé ; le formulaire du serveur reste
utilisable. Cette mission n'expose pas automatiquement `dist/` sur le Web.
Les ressources S3 restent téléchargées depuis leur référence Git figée.

Les anciennes routes restant disponibles, les copies déjà distribuées ne
nécessitent aucune modification. Un retour à la version précédente du serveur
reste possible avec ces routes : ses correcteurs ignorent les métadonnées
ajoutées. Ne pas supprimer `soumissions/` lors d'un retour arrière.

## Revues et limites

La matrice du Prof est dans `docs/pedagogy/metadata_migration_coverage.md`.
Les revues indépendantes technique et pédagogique, puis la gouvernance,
conditionnent l'intégration. La fusion et le déploiement appartiennent au
mainteneur. Les sources TQR sont des références de conception, pas des fichiers
copiés en bloc : leurs marqueurs et règles de confidentialité diffèrent de TAL.

Un défaut de barème préexistant a été constaté pendant la revue : le contrôle
S1 peut renvoyer 36 points pour un maximum déclaré de 35. Il est conservé pour
ne pas changer la notation au cours de cette migration ; son arbitrage doit
faire l'objet d'une correction distincte validée par l'enseignant.

Références :
- https://github.com/dreymond732/TQR/pull/51
- https://github.com/dreymond732/TQR/pull/54
- https://github.com/dreymond732/TQR/pull/56
