> **Historique — TD1B version 2 retirée.** Depuis sa version 3, TD1B dispose d’un correcteur technique automatique. L’ancienne copie est refusée avec « mauvaise version du notebook ». Aucun sujet actif ne relève du dépôt manuel décrit ci-dessous. Les anciens fichiers enregistrés restent intacts. Voir [le contrat actuel](s3_next_correctors.md).

# Dépôt sans correction automatique du TD1B S3

Cette évolution est un **CHANGEMENT_DE_CONTRAT** : le catalogue peut désigner un support distribué et déposable, sans évaluateur automatique. Elle ne modifie aucun barème ni contrat des 33 correcteurs existants. Le premier sujet concerné est `td1b-s3`, version 2.

## Routage et validation

Le catalogue serveur déclare `assessment: "human_review"`, `evaluator: null`, `active: true`. Ce type est réservé aux sujets explicitement enregistrés dans `HUMAN_REVIEW_QUESTION_COUNTS`. Un champ envoyé par l’étudiant ne peut pas changer le type d’évaluation d’un autre sujet. Les sujets automatiques existants conservent leur comportement, sans obligation d’ajouter un champ `assessment`.

Le notebook TD1B porte `metadata.tal = {"id": "td1b-s3", "evaluator": null, "version": 2}`. Son contrat exige exactement les réponses de code Q1 à Q4, identifiées par `metadata.tal`, et une cellule de code `identity` / `identification`. La cellule d’identité contient les quatre chaînes littérales `nom`, `prenom`, `classe`, `numero_etudiant`, non vides et non ambiguës. Le numéro étudiant utilise uniquement lettres, chiffres, tiret ou soulignement. Les versions anciennes et contrats de cellules incomplets renvoient `mauvaise version du notebook`.

Le dépôt utilise `/submit`, avec le même formulaire et la même infrastructure de réception que les autres notebooks. Aucune route `/eval/td1b-s3`, aucun module de correction factice, aucun contournement de l’authentification ou des limites de taille de l’infrastructure ne sont ajoutés. `/health` continue à annoncer 33 évaluateurs automatiques. Les limites d’upload et l’authentification dépendent de l’infrastructure existante ; cette évolution n’ajoute pas de nouvelle protection de ce type à Flask.

## Conservation et reçu

Sous `soumissions/td1b-s3-v2-human-review/<classe nettoyée>/` sont enregistrés :

- `nb/<identifiant réception>_<nom fichier nettoyé>` : copie originale du notebook ;
- `rapport/<identifiant réception>.html` : code et sorties textuelles enregistrées, regroupés par question et échappés ;
- `receptions.csv` : journal des réceptions, sans colonne de note, de score ni de bonus.

Chaque réception reçoit un UUID, ce qui conserve plusieurs dépôts du même étudiant. Aucun code soumis n’est exécuté. Les sorties HTML, SVG ou images ne sont pas rendues dans le rapport ; leur présence est signalée. Le rapport borne les extraits, signale les troncatures et renvoie à l’original conservé. Les sorties déposées ne sont pas authentifiées et ne prouvent pas la justesse du travail. Les chaînes d’identité à risque de formule sont neutralisées dans le CSV.

Le reçu public indique « Travail reçu ; aucune note automatique. » Il confirme la conservation des productions, sans promettre une relecture individuelle ni un retour enseignant systématique. Le type technique `human_review` et la persistance restent inchangés : les productions sont consultables si l’enseignant le souhaite. Il n’est envoyé qu’après l’écriture du notebook, du rapport et du journal. Toute erreur d’écriture empêche la confirmation et donne une réponse 503 sans détail interne. Des fichiers partiels peuvent subsister en cas d’échec intermédiaire : le journal réussi constitue la preuve d’une réception confirmée. Il n’existe pas de transaction globale entre ces trois fichiers ni de verrou interprocessus sur le journal, conformément au stockage sur fichiers existant.

## Distribution et vérification

Le sujet actif participe à `prepare_student_notebooks.py` comme les autres supports : la cellule HTML finale est canonique dans la source, puis son URL est injectée seulement dans la distribution. Le double tuteur relève des mêmes contrôles existants.

`tests/test_human_review_submission.py` vérifie routage, refus des versions et contrats invalides, absence d’appel d’un correcteur et du journal de notes, conservation de l’original, échappement HTML, journal sans score, échecs de persistance et génération distribuable. Les tests historiques gardent 33 correcteurs et distinguent ce nouveau support manuel des 11 TD S3 historiques. La modification des tests de conservation de R2, TD1 et R1 autorise uniquement la réécriture de leur prose et des commentaires, en préservant ordre, identifiants, métadonnées, cellules originales et AST du code fourni, à la seule exception du pin de compatibilité décrit dans `docs/s3_spacy_runtime.md`. La couverture et la lisibilité sont établies séparément par les revues pédagogique et éditoriale.
