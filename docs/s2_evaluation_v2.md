# Contrat d’évaluation S2 v2

La révision conserve les identifiants publics et leurs routes, y compris leur casse. Les supports ont désormais leur dossier par semestre ; les contrôles et le devoir maison sont classés avec les évaluations. Les six évaluateurs actifs passent au contrat v2. Le contrôle final, distinct des anciens exercices des modules `app_correction_controle_S2.py` et `app_correction_controle_Final_S2.py`, reste inactif : aucun correcteur ni dépôt n’est annoncé pour ce sujet.

| Identifiant | Questions | Barème | Mode |
|---|---:|---:|---|
| `td2-S2` | 13 | 20 | Contrôle |
| `td3-S2` | 30 | 30 | TD |
| `td4-S2` | 14 | 40 | Contrôle |
| `td5-S2` | 25 | 25 | TD |
| `td6-S2` | 10 | 20 | TD |
| `ControleDevoirMaisonS2` | 30 | 40 | Contrôle |

## Identification et refus des versions incompatibles

Le catalogue associe le notebook à son correcteur. Les métadonnées racine doivent fournir `metadata.tal.id`, `version: 2` et l’identifiant exact de l’évaluateur. Chaque question Q1 à QN correspond à une cellule de code unique de rôle `answer` ; une cellule `identity` de rôle `identification` contient les affectations littérales de `nom`, `prenom`, `classe` et `numero_etudiant`.

Une ancienne version, des questions manquantes ou dupliquées ou une identification des cellules incomplète sont refusées avec « mauvaise version du notebook ». Une identité personnelle incomplète reçoit un message explicite. Sur `/submit` comme sur la route historique de l’évaluation, ces contrôles interviennent avant correction et persistance.

## Traces, preuves et limites

Le moteur commun lit uniquement le code source et les sorties déjà enregistrées. Il n’exécute aucune instruction, ne charge aucun module indiqué par la copie et n’ouvre aucun fichier étudiant. Les valeurs littérales des traces sont décodées de façon bornée par `ast.literal_eval` ; les expressions soumises ne sont pas évaluées.

Les affichages v2 ont la forme `print("Résultat Qn :", valeur)` : le marqueur, la cellule Qn et la sortie enregistrée doivent correspondre. Les traces complémentaires Qnb appartiennent à la même question et ne créent pas de point supplémentaire. Les pratiques, exemples, cellules fournies et cellules de restitution ne valent pas réponse. Les imports fournis peuvent définir le nom d’une bibliothèque, jamais valider une compétence.

Les valeurs sont comparées avec leurs types (un booléen ne vaut pas un entier), avec des ensembles et dictionnaires indépendants de l’ordre. Lorsque la consigne vise une construction Python, le correcteur cherche celle-ci dans les dépendances syntaxiques de la valeur affichée. Une fonction inutilisée, un commentaire ou une branche littéralement morte ne suffisent pas. Pour les lectures placées dans `try`, seul le chemin nominal fournit une preuve de lecture ; le code d’un gestionnaire d’exception ne vaut pas preuve d’accès au fichier.

Le barème appartient à l’application, jamais à la copie. Les pondérations historiques sont conservées ; le maximum est calculé par leur somme. Le résultat reste un **score technique provisoire** : il ne certifie ni l’auteur, ni la fraîcheur des sorties, ni toutes les équivalences possibles de programmes Python. Les interprétations et justifications restent à relire humainement. Les diagnostics distinguent trace absente, valeur incorrecte et construction non repérée ; une dépendance absente peut rendre un résultat non vérifiable sans établir une erreur de calcul indépendante.

## Confidentialité et conservation

Les TD affichent le retour formatif. Les contrôles et le devoir maison présentent uniquement un accusé de dépôt ; le rapport détaillé est conservé pour l’enseignant, sans code HTML étudiant actif. Les copies, rapports et CSV v2 vont dans `soumissions/<identifiant>-v2/<classe>/`. Le numéro étudiant distingue les homonymes ; les historiques de l’ancien correcteur ne sont pas réécrits.

## Distribution

Les six sources actives se terminent par la cellule canonique de restitution HTML avec le marqueur `__TAL_PUBLIC_URL__`, sans sortie exécutée. Le contrôle final possède également sa cellule source, mais reste exclu de `dist` tant que son dépôt est inactif. `deploy.sh` lit l’environnement, produit les copies dans `dist`, vérifie leur contenu et injecte l’adresse uniquement dans ces copies. Après fusion et déploiement, redistribuer les six supports actifs : une ancienne copie v1 n’est pas automatiquement migrée ni corrigée.
