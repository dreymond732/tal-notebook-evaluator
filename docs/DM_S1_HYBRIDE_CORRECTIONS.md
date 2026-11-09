# DM intermédiaire S1 — Circuit hybride (17,75 + 2,25 points)

## Périmètre de la PR

Le DM S1 demeure dans le catalogue et utilise le même cahier (contrat
`dm-intermediaire-s1`, version 1), les mêmes identifiants étudiants et
le même journal CSV. **Seul le barème des nouvelles analyses automatiques
change (version de notation 2)**. Aucune note déjà enregistrée en CSV
n'est recalculée ou remplacée.

Le correcteur attribue désormais **17,75 points automatiques**. Les
cinq questions ciblées comportent un maximum humain supplémentaire :

| Question | Maximum automatique | Maximum humain | Total |
|---|---:|---:|---:|
| Q2 | 0,50 | 0,50 | 1,00 |
| Q6 | 0,50 | 0,50 | 1,00 |
| Q12 | 0,75 | 0,25 | 1,00 |
| Q14 | 0,50 | 0,50 | 1,00 |
| Q17 | 1,00 | 0,50 | 1,50 |
| 13 autres questions | 14,50 | 0 | 14,50 |
| **Total** | **17,75** | **2,25** | **20** |

Les cinq corrections humaines portent uniquement sur les explications et
essais complémentaires des Q2, Q6, Q12, Q14 et Q17. Ne pas les confondre
avec les critères techniques des mêmes questions : aucun point ne peut
être obtenu deux fois.

## Dépôt et redépôt

Les nouveaux dépôts du DM sont enregistrés dans les mêmes répertoires
`soumissions/DM_intermediaire_S1/{nb,rapport}/`. Chacun reçoit un
identifiant de réception aléatoire inscrit dans la colonne `Origine`
du CSV `notes_DM_intermediaire_S1.csv`. Un enregistrement séparé
`soumissions/suivi/dm_s1_corrections.sqlite3` sert uniquement à la
correction humaine et ne modifie pas la source.

Un nouvel essai est autorisé **strictement** si :
- le score automatique de la copie active est inférieur à 8,875/17,75,
  équivalent de 10/20 ;
- la correction humaine n'est pas publiée ;
- l'étudiant utilise une session de `Ma progression` liée au même
  numéro pour toute nouvelle soumission (un premier dépôt sans
  précédent reste possible sur la route existante).

Les anciennes copies et corrections partielles conservent leurs
fichiers originaux et leurs entrées en SQLite marquées `superseded`,
mais disparaissent de la **file active** de relecture. Une ancienne fiche
ouverte devient non modifiable (HTTP 409). La validation d'une fiche
fixe la note finale et ferme les redépôts. Aucun calcul de moyenne ou
choix automatique de la « meilleure note » n'est effectué.

## Espace enseignant

Le lien « DM S1 — Corrections humaines » dans
`/enseignant/progression/` ouvre une file privée triée par état.
Pour chaque dernière copie :
- score automatique /17,75 ;
- cinq énoncés ciblés provenant du cahier de référence ;
- code, commentaires et sorties enregistrées, **lus sans exécution** ;
- champ de points borné par la part humaine de la question ;
- champ d'appréciation, sauvegardable en brouillon.

La publication exige **tous les points et toutes les appréciations**,
y compris la note 0 explicitement saisie, puis rend la note finale
sur 20 disponible dans `Ma progression`. L'état `published` est
protégé contre les modifications ou redépôts ultérieurs. Les formulaires
et la liste exigent la session enseignant et le CSRF déjà déployés.

## Rapports individuels : accès privé et contrôle initial

Le rapport automatique /17,75 est affiché immédiatement au déposant.
Depuis sa session personnelle, l'étudiant peut consulter :
- le **dernier rapport de TD** correspondant à un reçu `direct:<uuid>`
  dans le journal canonique, une année et une version de contrat valides ;
- le **dernier bilan DM**, et après publication sa note finale sur 20
  et les cinq appréciations.

Les archives sont servies **uniquement par les routes Flask** sous
`/ma-progression/rapport/<evaluation>`. Les contrôles sommatifs
restent exclus. Le chemin physique du NAS ne figure ni dans l'URL ni
dans les paramètres transmis par l'étudiant. Les anciens rapports TD
sont servis avec une politique CSP sandbox interdisant les scripts.

**Attention** : le premier rattachement du numéro étudiant à un email
ne certifie pas l'identité administrative. Pour cette raison, les liens
vers les rapports détaillés sont **désactivés par défaut**. Vérifier
administrativement les comptes déjà associés avant d'ajouter dans le
`.env` du correcteur :

    TAL_STUDENT_REPORTS_ENABLED=1

Recréer ensuite le conteneur. Même quand les rapports sont désactivés,
la synthèse de progression continue d'afficher les scores habituels
et, après dépôt du DM, le score automatique ou final du DM.

Il n'y a **aucun envoi de mail de notification** pour les notes.

## Reprise des DM historiques

Les dépôts existants restent dans le journal d'origine avec le barème
sur 20. Si l'on veut les placer dans la nouvelle file enseignant, la
commande `bootstrap_dm_hybrid.py` indexe uniquement les copies de la
**dernière tentative** identifiable avec reçu `direct:<uuid>`
et cahier complet. Elle calcule, sans exécuter le notebook, un nouveau
score automatique selon la version de notation 2 et le conserve
**uniquement dans la nouvelle base privée**. Le score original du CSV,
le rapport HTML et le cahier ne sont jamais réécrits.

Sauvegarder le volume `soumissions/`, après fusion et reconstruction :

```bash
docker-compose exec -T corrector-tal python bootstrap_dm_hybrid.py
```

La simulation affiche les nombres de copies éligibles, non exploitables
et candidates. Pour appliquer, seulement après vérification d'une
sauvegarde indépendante :

```bash
docker-compose exec -T corrector-tal python bootstrap_dm_hybrid.py --apply --backup-confirmed
```

La commande est idempotente, n'affiche ni noms ni numéros d'étudiants,
et ignore les tentatives sans reçu fiable ou identité exploitable.
Si aucune archive correspondant à la tentative n'est disponible, une
nouvelle soumission sera nécessaire ; ne pas inventer de correspondance.

## Déploiement et vérifications

```bash
git pull
docker-compose up -d --build --force-recreate corrector-tal
docker-compose exec -T corrector-tal python audit_progressions.py --annee 2026-2027 --toutes-evaluations
```

Vérifier ensuite :
1. Un premier DM affiche son résultat automatique sur 17,75.
2. L'enseignant voit les cinq questions, peut enregistrer un brouillon
   et publier une note humaine sur 2,25.
3. Un redépôt sous le seuil rend l'ancienne fiche non modifiable ;
   un redépôt après validation ou au-dessus du seuil est refusé.
4. Le portail étudiant n'expose pas d'autres copies et ne propose
   jamais un rapport de contrôle sommatif.
5. Une nouvelle consultation du portail affiche la note finale
   publiée, sans que l'étudiant ait besoin de solliciter un email.

L'authentification étudiante du portail `Ma progression` reste le
modèle de premier rattachement du projet, avec ses limites identifiées.
Les tests sont uniquement sur des copies fictives, et la PR ne
modifie pas les données sur le NAS.
