# Revue éditoriale indépendante — Formulaire de correction du DM S1

## Périmètre et verdict

- Branche : `code/dm-s1-validation`, référence `2445c9e18357dc6a99a8e516bf0d7bd7e462fd42` ; diff courant relu.
- Mandat transmis : cinq notes obligatoires, appréciations facultatives, conservation de la saisie refusée, erreurs à côté des champs, retour à la file après publication, distinction des trois scores et des trois états.
- Destinataire de cette interface : enseignant chargé de corriger les copies ; aucun sujet étudiant ni notebook modifié dans ce lot.
- Réviseur : agent indépendant `editorial_review`. Aucun texte du produit n’a été écrit ou modifié par le réviseur.
- Fichiers relus : `app/templates/teacher_dm_review_template.html`, messages de `app/dm_hybrid.py`, section DM de `app/teacher_routes.py`, modifications de `app/static/teacher_progress.css`, `docs/DM_HYBRIDE_S1.md` et noms des tests de `tests/test_dm_hybrid_workflow.py`.

**Verdict : `ACCEPT` — `LISIBILITÉ_INTERFACE_ENSEIGNANTE_VALIDÉE`.**

Aucune confusion essentielle ni formulation bloquante relevée dans ce périmètre. Le verdict concerne la compréhension des actions et des états ; il ne remplace pas la revue technique des transactions ou les tests du formulaire.

## Preuves de lecture

| Situation | Texte et comportement rendus compréhensibles | Constat |
|---|---|---|
| Ouvrir une copie non validée | « Les cinq notes sont obligatoires pour valider. Les appréciations sont facultatives. » | La distinction répond directement à la règle attendue ; le statut facultatif est aussi présent dans chaque libellé d’appréciation |
| Commencer sans terminer | « Vous pouvez enregistrer un brouillon incomplet » ; bouton « Enregistrer le brouillon » | Enregistrer et publier sont deux actions distinctes, sans obligation implicite de remplir les cinq notes pour un brouillon |
| Oublier une note avant publication | « Saisissez une note, y compris 0. » | L’absence de note est distinguée d’une note nulle ; le message est rattaché au champ concerné |
| Saisir une valeur refusée | Messages dédiés : note numérique, intervalle de points, deux décimales ; appréciation limitée à 4 000 caractères | Les messages indiquent ce qu’il faut corriger sans exposer une exception ou une règle d’implémentation |
| Revenir après erreur | « La correction n’a pas été enregistrée. Vérifiez les champs signalés. Les valeurs saisies sont conservées ci-dessous. » | Le refus d’enregistrement est explicite et le maintien des champs est annoncé. Le formulaire relu réaffiche les valeurs brutes reçues, y compris les valeurs invalides ; cette lecture statique ne vaut pas test d’exécution |
| Repérer le champ en erreur | Message immédiatement après le champ ; `aria-invalid` et association `aria-describedby` | L’information ne dépend pas uniquement d’une couleur et peut être reliée au champ par les technologies d’assistance |
| Publier | Bouton « Valider et publier la note finale », puis message « Correction validée et publiée. » et retour à la file | La publication est nommée dans l’action et dans sa confirmation. La route relue distingue le retour à la file après validation du retour à la fiche après brouillon |
| Lire une copie publiée | « Correction validée et publiée. Note finale … / 20. Cette fiche n’est plus modifiable. » | L’état publié et la lecture seule sont annoncés sans demander une nouvelle action |
| Lire la file | « Auto / 17,75 », « Correction / 2,25 », « Finale / 20 » | Les trois bases de notation sont visibles côte à côte ; une somme humaine partielle en brouillon n’est pas présentée comme une note finale publiée |
| Distinguer les états | « À corriger », « Brouillon », « Validée » ; finale « En attente » avant publication | Les états et la note finale permettent de repérer ce qui reste à faire ; une finale nulle reste affichable après validation |
| Consulter une copie publiée depuis la file | Libellé « Consulter » après validation, « Ouvrir » sinon | Le lien ne promet pas une modification de la fiche publiée |
| Lire la procédure | Documentation : cinq notes requises, commentaires facultatifs, décimales point/virgule, saisie conservée après erreur et liste des trois états | Le texte de procédure et le formulaire décrivent la même règle ; les détails de stockage et de déploiement demeurent dans la documentation, hors du parcours de saisie |

## Limites de la revue

- Lecture intégrale du template courant et des changements de messages et de navigation ; aucune modification du produit.
- Aucun accès à une copie réelle, aucune saisie de note réelle, aucune publication ni action en production.
- Pas de test visuel dans un navigateur, pas d’essai mobile ni de vérification avec un lecteur d’écran. Les propriétés d’accessibilité constatées sont celles du HTML relu.
- Les tests couvrant saisies brutes refusées, publication sans appréciations, états de file et conservation du préfixe proxy sont présents dans `tests/test_dm_hybrid_workflow.py`. Ils n’ont pas été réexécutés par ce réviseur ; leur résultat est à rattacher au rapport technique.
- Pas de retour Étudiant-Modèle requis : la mission concerne une interface de correction enseignante, sans modification d’une activité pédagogique ni du barème.

## Relais

Aucune reprise rédactionnelle nécessaire avant clôture dans ce périmètre. Transmettre avec les résultats techniques au réviseur de gouvernance et au responsable d’intégration. La décision de fusion et de déploiement reste celle du mainteneur.
