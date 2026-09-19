# Évaluation formative du TD2 S1

## Contrat et changement

Branche : `pedagogy/s1-td2-progressive`. Référence pédagogique : `docs/pedagogy/TD2_S1_SPECIFICATION.md`.

Le module dédié `app/app_correction_TD2_S1.py` conserve l'identifiant `td2-s1`, la signature `check_notebook(content_str, filename)`, le retour à cinq éléments et le plafond de 7 points. Il remplace pour ce seul TD la recherche globale de fragments et de marqueurs par une lecture locale des productions enregistrées. Aucun moteur partagé, route ou template n'est modifié.

Chaque groupe Q1–Q6 possède deux productions valant chacune 0,5 point : marqueur principal et sous-marqueur `b`. Q7 vaut 1 point pour le découpage enregistré conforme accompagné d'une tentative de commentaire non vide. La pertinence du commentaire n'est jamais certifiée ; même un groupe crédité demande explicitement une relecture avec l'enseignant. Le score mesure des traces formatives, pas une maîtrise globale des compétences.

## Analyse réalisée

- Le JSON et la structure des cellules sont contrôlés. Les erreurs donnent le même contrat de retour.
- Les flux stdout sont réunis par cellule avant lecture des lignes, y compris si Jupyter a segmenté un affichage.
- Chaque marqueur doit apparaître une seule fois dans un appel `print` reconnu et dans les sorties de cette même cellule. Les doublons ou une erreur d'exécution enregistrée empêchent le crédit de la trace concernée.
- L'AST décrit les affectations et les dépendances des arguments affichés. Commentaires, littéraux contenant du code et exemples enseignant en Markdown ne constituent pas une opération étudiante. Une opération présente dans une variable sans lien avec l'affichage ne suffit pas.
- Les valeurs attendues et l'ordre d'affichage sont comparés à la spécification. Les listes sont lues comme littéraux Python, avec vérification de leur type et de celui des éléments ; aucun `eval`, `exec`, compilation ou lancement de notebook n'est effectué.
- Q6 vérifie les trois éléments de la liste calculée : chacun doit être relié à son indice et aux deux opérations `strip` et `lower`. La présence des opérations pour un seul élément ne suffit pas.
- Chaînage de méthodes, étapes intermédiaires, alias de variables, `mot[:4]`, `mot[0:4]` et `mot[0:4:1]` sont acceptés. Le dernier élément accepte `-1`, son indice positif connu (11 pour `mot`, 4 pour `tokens`) ou `len(sequence)-1`. Une liste affichée avec des guillemets simples ou doubles est acceptée.
- Boucles, compréhensions, imports, conditions et définitions de fonctions rencontrés déclenchent un rappel du périmètre pédagogique, sans pénalité générale ajoutée.

## Limites explicites

Le correcteur **ne prouve pas que les sorties proviennent du code actuel**. Une sortie ancienne ou fabriquée qui ressemble au résultat attendu reste impossible à authentifier par cette lecture. Ce cas est couvert par un test qui montre la limite, et tous les retours rappellent de réexécuter les cellules dans l'ordre.

L'AST vérifie des opérations et des dépendances syntaxiques, pas la sémantique complète de Python. Il ne simule ni flot de contrôle, ni appels arbitraires, ni mutations. Les cellules sont parcourues dans l'ordre du document, pas dans l'ordre historique d'exécution. Le format d'affichage attendu est `print("Résultat Qn :", variable, ...)`, tel que fourni par le sujet ; un f-string fusionnant marqueur et valeur n'est pas reconnu. Le traitement n'est pas un mécanisme anti-fraude et ne remplace pas une appréciation humaine.

Le sujet vierge conserve des affichages commentés et aucune sortie ; il doit obtenir 0/7 jusqu'à ce que l'étudiant réalise et exécute ses manipulations.

## Validation technique

Commande : `/tmp/tal-test-venv/bin/python -m unittest discover -s tests -p 'test_*s1*.py' -v`.

Résultat lors du handoff Architecte : **19 tests réussis**, dont 16 propres au TD2. Cas couverts : référence complète ; variantes syntaxiques ; résultats erronés ; listes de mauvais type ; code seulement commenté ou sans rapport ; marqueur sans code ; doublons ; sorties dans une autre cellule ; nettoyage incomplet des trois chaînes ; erreur d'exécution ; absence de sorties ; JSON/cellules malformés ; stdout segmenté ; absence d'exécution ; limites sur sorties périmées et commentaire libre ; route Flask réelle et persistance notebook/rapport/CSV.

Le test commun S1 est ajusté pour exiger le rejet du faux positif historique du TD2 (« marqueur + ok » et fragments hors syntaxe), sans changer le comportement testé des six autres correcteurs.

Fichiers techniques modifiés : module dédié, `tests/test_td2_s1.py`, `tests/test_s1_formative.py`, cette note. Le changement exige une revue indépendante Code-Auditor et Pedagogy-Reviewer ainsi qu'une confrontation au corrigé Étudiant modèle. Le producteur ne délivre aucun verdict de conformité sur son propre travail.

## Correction d’intégration TAL-AUD-001

La revue indépendante a relevé l’absence du commentaire d’identification attendu par le moteur commun dans le sujet réel. Le Designer l’a ajouté au notebook. Les tests lisent désormais la cellule réelle, remplissent seulement les trois emplacements fictifs, vérifient l’extraction exacte et les chemins `td2-s1/S1/nb`, `rapport` et CSV avec les noms attendus. Ils ne reconstruisent plus une cellule idéale absente du sujet. Aucun changement du moteur partagé n’a été nécessaire.
