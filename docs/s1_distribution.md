# TD S1 : identification et distribution

Les sept TD S1 sont renommés selon leur contenu, conformément à la matrice
[du Prof](pedagogy/s1_td_review_distribution.md). Le catalogue conserve les
identifiants `td1-s1` à `td7-s1`, les mêmes évaluateurs, versions de contrat et
barèmes. L'identification du correcteur repose sur les métadonnées, pas sur le
nom téléchargé. Les autres supports ne sont pas renommés.

| TD | Fichier dans `Notebooks TD/S1/` |
|---|---|
| 1 | `TD1_S1_variables_types.ipynb` |
| 2 | `TD2_S1_chaines_sequences.ipynb` |
| 3 | `TD3_S1_collections.ipynb` |
| 4 | `TD4_S1_boucles_conditions_comptages.ipynb` |
| 5 | `TD5_S1_fonctions_reutilisation.ipynb` |
| 6 | `TD6_S1_fichiers_csv.ipynb` |
| 7 | `TD7_S1_expressions_regulieres_pipeline.ipynb` |

## Cellule source et adresse injectée

Les sources S1 comportent une dernière cellule fournie `tal-submission`, avec
`metadata.tal.question = submission` et `role = submission`. Son seul paramètre
d'adresse est `__TAL_PUBLIC_URL__`. Elle reprend l'encadré « Restitution de votre
travail », ses trois étapes et le bouton HTML demandé. `html.escape` protège
l'attribut du lien ; `rel="noopener noreferrer"` accompagne son ouverture dans
un nouvel onglet. Ces imports servent uniquement à la restitution et sont
exclus des preuves évaluées.

`app.prepare_student_notebooks.submission_cell()` définit ce gabarit. La
validation refuse une cellule altérée, déplacée, dupliquée, exécutée ou contenant
des sorties enregistrées. Le marqueur ne peut pas apparaître ailleurs. Les
contrôles d'URL inspectent tous les champs des sources, sorties et métadonnées
comprises. Cette vérification repère les chemins de dépôt connus et le domaine
configuré pendant la génération ; elle ne prétend pas identifier automatiquement
toute adresse privée inconnue qui aurait un chemin arbitraire.

Lors du rendu, le générateur substitue cette cellule dans une copie du notebook.
Pour les autres supports, qui n'ont pas ce gabarit source, il ajoute une seule
cellule finale selon le même modèle. Il conserve intégralement les autres
champs. Les sources Git ne sont jamais réécrites.

Le HTML rend l'accès plus lisible ; il ne dissimule pas l'adresse aux étudiants.
L'adresse réelle figure nécessairement dans leur notebook distribué. Ne pas
reverser ces copies dans Git : `dist/` reste ignoré.

## Déployer et distribuer

Après fusion, depuis le dépôt du serveur :

```bash
git pull
bash deploy.sh
```

Le script lit le `.env` existant par défaut ; un chemin externe peut être fourni
par `bash deploy.sh /chemin/configuration.env`. Il vérifie les sources, génère et
vérifie la distribution, puis lance Docker Compose et contrôle `/health`.
Un échec avant Docker interrompt le déploiement. La clé `TAL_PUBLIC_URL` désigne
la racine publique de l'application, préfixe de proxy compris, sans `/submit`.
L'environnement du processus a priorité sur `.env` ; le fichier n'est jamais
exécuté ou chargé par `source`.

Pour générer sans lancer Docker, notamment depuis PowerShell :

```powershell
python app/prepare_student_notebooks.py check
python app/prepare_student_notebooks.py render --env-file .env
python app/prepare_student_notebooks.py verify --env-file .env
```

La génération vérifie une distribution temporaire complète avant de remplacer
la précédente. Le manifeste autorise la suppression des anciens chemins gérés,
donc les anciens noms `python_texte` ne restent pas dans la nouvelle distribution.
Un dossier inconnu, des fichiers étrangers ou des liens symboliques font refuser
le remplacement. Les données de soumission restent hors de cette opération.

Distribuer ensuite les sept fichiers renommés de `dist/Notebooks TD/S1/`.
Les anciens sujets S1 conservent leur contrat d'évaluation et ne sont pas rejetés
du seul fait du renommage. Le changement n'ajoute pas un numéro étudiant
obligatoire ni ne refond les correcteurs : ces évolutions nécessiteraient un
contrat coordonné avec l'identification et la persistance.

## Vérifications techniques

Les tests de distribution contrôlent la substitution unique, la conservation
exacte des sources, l'échappement de l'URL, le rejet des gabarits non canoniques,
les sorties contenant une adresse de dépôt, le remplacement atomique et le
retrait des anciens noms. Le test de `deploy.sh` remplace Python et Docker par
des commandes factices et vérifie l'ordre ainsi que l'arrêt sur erreur : il
n'effectue aucun déploiement réel. Le code exécuté pour contrôler le HTML est
uniquement le gabarit de confiance produit par le générateur ; aucun code de
notebook étudiant n'est exécuté par le serveur ou par ces tests.
