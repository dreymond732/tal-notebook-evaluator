# DM intermédiaire S1 — Circuit de correction hybride

## Contrat de notation (barème v2, contrat cahier inchangé)

L'identifiant `dm-intermediaire-s1` et le contrat `tal.version=1`
restent compatibles avec les cahiers déjà distribués. Le nouveau
barème de restitution du **prochain dépôt** est identifié séparément
par `HYBRID_RUBRIC_VERSION=2`.

- **17,75 points automatiques** sur les 18 questions ; les critères
  sont les mêmes que précédemment, sans exécuter le code étudiant.
- **2,25 points humains** pour Q2 (0,5), Q6 (0,5), Q12 (0,25),
  Q14 (0,5), Q17 (0,5).
- **20 points finaux** après validation de toutes les notes et
  appréciations. Avant validation, l'étudiant ne voit **que**
  la note automatique sur 17,75 et la mention « en attente ».
- La répartition exacte est appliquée **par question**, pas par un
  coefficient uniforme sur le score historique sur 20.

Les journaux des tentatives antérieures /20 restent inchangés.
Leurs scores ne sont ni convertis ni réévalués automatiquement.
Le tableau enseignant affiche toujours le relevé historique brut
pour ces anciennes copies. Le nouveau score /17,75 et le score final
apparaissent distinctement dans la file « DM S1 — Corrections humaines »,
et le portail étudiant utilise la dernière copie active.

## Redépôt et dernière copie

Le premier dépôt au barème v2 est enregistré avec un reçu unique.
Un **redépôt est autorisé** tant que :
1. la dernière note automatique est **strictement inférieure à
   8,875/17,75** (équivalent à 10/20) ;
2. la fiche n'a **pas** été validée par l'enseignant ;
3. l'étudiant s'est connecté à « Ma progression » avec la session
   individuelle correspondant au numéro de la copie déposée.

Le seuil exactement égal à 8,875 ferme le redépôt. Les redépôts
ne requièrent aucune justification supplémentaire.
Le dépôt accepté remplace le **pointeur courant** de l'étudiant ;
les anciens cahiers, journaux, rapports et éventuelles notes
humaines en brouillon restent conservés, mais ne sont ni proposés
à la correction ni publiés. Une ancienne URL de correction renvoie
404 et ne peut pas être réactivée.

Le redépôt reste possible après un brouillon non validé, mais pas
après la validation. L'application bloque un nouveau dépôt anonyme
visant à remplacer la copie d'un étudiant : l'utilisateur doit se
connecter au compte de progression du même numéro.

## Fiches enseignant

Adresse publique après connexion :

`/universite/tal/enseignant/progression/dm-s1`

La file liste une **unique copie courante par étudiant**.
La fiche montre les **énoncés intégraux canoniques** des cinq questions,
issus de `app/dm_hybrid_questions.json`, extraits du cahier source,
le code et les sorties réellement enregistrés, le score automatique
de la question, puis deux champs de saisie :
- score humain entre zéro et le maximum propre à la question,
  deux décimales maximum ;
- appréciation textuelle, 4 000 caractères maximum.

Le bouton « Enregistrer le brouillon » conserve une fiche inachevée.
« Valider et publier » exige les cinq notes **et** les cinq
appréciations. La validation n'est pas réversible depuis la page.
L'enregistrement et le redépôt sont sérialisés avec
`progression_lock`. Une session enseignante valide et le CSRF
sont obligatoires.

## Consultation personnelle : derniers rapports seulement

La route authentifiée
`/ma-progression/rapport/<evaluation>`
ne reçoit aucun nom de fichier ni chemin de stockage.

- Pour chaque **TD formatif**, le serveur vérifie le numéro étudiant
  de la session, le contrat actif, l'année universitaire et l'identifiant
  de réception `direct:<UUID>` dans le journal canonique, puis
  recherche une unique archive HTML portant cet identifiant.
  Le dernier dépôt seul est accessible. La restitution est sous
  `Content-Security-Policy: sandbox`, pour bloquer les scripts.
- Pour le **DM intermédiaire S1**, le serveur rend le bilan filtré
  depuis la dernière copie active en base privée ; il ne diffuse
  jamais le rapport enseignant, qui contient d'autres informations.
  Après validation, les cinq appréciations et le score final
  apparaissent immédiatement sur cette route.
- Les **contrôles sommatifs**, les rapports des autres étudiants,
  les fichiers bruts `.ipynb` et les rapports enseignants restent privés.
- Les anciens dépôts de DM non encore repris dans la base hybride
  n'obtiennent pas rétroactivement un nouveau rapport : une copie
  au barème v2 doit être soumise.

Aucun email automatique n'est déclenché.

## Stockage et sauvegarde

Base ajoutée : `soumissions/suivi/dm_hybride.sqlite3`
(mode 0600). Elle contient le reçu, numéro, identité, score automatique,
les 18 bilans filtrés, les cinq extraits de code/sorties, les brouillons
et la date de validation. Aucun cahier n'est exécuté par ce circuit.
Les anciennes archives restent dans `soumissions/DM_intermediaire_S1/`.

Avant déploiement : sauvegarder **tout le volume soumissions**, y compris
ses bases SQLite, cahiers, rapports et CSV. La PR n'exécute aucune
migration destructrice. Après fusion :

```bash
git pull
docker-compose up -d --build --force-recreate corrector-tal
python -m unittest discover -s tests -p test_dm_hybrid_workflow.py -v
docker-compose exec -T corrector-tal python audit_progressions.py --annee 2026-2027 --toutes-evaluations
```

La commande `python -m unittest` est à exécuter sur un environnement
de développement contenant les dépendances requises, pas sur les
données nominatives du NAS. Les tests utilisent uniquement des copies
synthétiques et un stockage temporaire.

## Limites et points d'attention

- Le rattachement d'email existant dans `student_access` suit encore
  le modèle « premier numéro revendiqué, email confirmé ». Il ne
  prouve pas l'identité administrative. **Vérifier la concordance
  des comptes avec les inscrits avant d'ouvrir largement les
  rapports individuels**, et corriger les rattachements litigieux
  par la procédure administrative existante.
- Les nouveaux dépôts au barème /17,75 et les anciens DM /20 coexistent
  dans le CSV historique ; les minima/maxima consolidés des DM ne
  constituent donc **pas** la note finale hybride. Consulter la
  file et la base hybride pour le score actuel et la validation.
- En cas d'erreur de disque après ajout au journal CSV mais avant
  enregistrement du pointeur SQLite, des archives orphelines
  peuvent subsister. Elles ne sont pas publiées : vérifier les
  journaux et réparer après sauvegarde plutôt que d'inventer un lien.
- Le dépôt initial du DM, comme précédemment, ne constitue pas
  une authentification étudiante. Le redépôt, lui, nécessite
  une session individuelle confirmée.
