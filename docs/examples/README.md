# Exemples synthétiques de restitution

Ces HTML illustrent la présentation des rapports, sans copie étudiante réelle.

- [TD1 S1 : six questions réussies](rapport_td1_s1.html).
- [TD1.a S3 : code retrouvé, erreur sauvegardée et résultats manquants](rapport_td1_s3.html).

Téléchargez les fichiers puis ouvrez-les dans un navigateur. La colonne « Résultat attendu » montre la solution dès l’ouverture ; la case permet de la masquer sans connexion. Une réponse validée reçoit seulement un ✓ vert dans le bilan. Les liens de nouvelle soumission pointent vers les routes de l'application et demandent une application déployée. Ces aperçus sont des instantanés de la version livrée, pas des rapports de production ni des évaluations d'étudiants.

Régénération depuis la racine du dépôt :

```bash
python tests/render_feedback_examples.py --output-dir docs/examples
```

Le script utilise les sorties sauvegardées des jeux de test et les sujets actuels ; il ne lance pas le programme d'une copie remise.
