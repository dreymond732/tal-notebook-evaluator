# Distribution de la progression courante

Le S1 comporte quinze cahiers de TD en vigueur : TD1, TD2, les trois cahiers
A/B/C pour chacun des TD3 à TD6, puis TD7. Le [parcours détaillé](../Notebooks%20TD/S1/README.md)
indique leur ordre. Les quatre anciennes synthèses TD3 à TD6 et les anciens
corrigés sont regroupés dans [`historique/`](../historique/README.md), sans
modification de leurs octets. Ils ne sont ni mélangés aux dossiers de semestre,
ni exportés par le déploiement.

Leurs identifiants de correction restent reconnus pour les copies déjà
commencées. Ce rangement ne modifie aucun barème ni résultat enregistré et ne
change pas les fonctions de consolidation du suivi. Les liens du menu étudiant
présentent seulement les supports courants ; les routes directes historiques
restent disponibles.

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

Distribuer les cahiers du parcours courant depuis `dist/Notebooks TD/S1/`, selon `Notebooks TD/S1/README.md` (quinze cahiers TD pour le parcours renforcé). Les synthèses historiques restent compatibles avec les copies commencées.
Les anciens sujets S1 conservent leur contrat d'évaluation et ne sont pas rejetés
du seul fait du renommage. Le renommage historique, pris isolément, ne modifiait
ni les règles d’identification ni les correcteurs. Les neuf contrats additifs de
l’expansion Swinnen sont décrits ci-dessous et restent distincts des copies anciennes.

## Contrôles dans le même dossier de distribution

Depuis le rangement demandé le 19 novembre 2026, le sujet du contrôle final S1
est `Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb` ; sa copie
à distribuer est donc
`dist/Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb`.
Le DM reste dans le même sous-dossier S1. Les contrôles S2 et S3 sont rangés dans
leurs sous-dossiers respectifs.

La sélection de distribution est distincte de l'activation d'un correcteur :
`distribution_sources()` exclut les entrées `archived: true`, puis inclut les TD
courants et tous les sujets de contrôle courants du catalogue. Le lot actuel
comprend **43 notebooks**, pour **46 évaluateurs actifs**. Le contrôle final S2 est ainsi disponible dans `dist/`
sans modifier son état inactif ni ouvrir un dépôt.

Pour ce sujet sans dépôt actif, la cellule finale de restitution est remplacée,
dans la copie générée seulement, par une consigne Markdown de sauvegarde du
notebook avec ses sorties et de remise selon les modalités de l'enseignant.
Il n'y a ni adresse de dépôt ni marqueur non remplacé dans cette copie. Les
questions, données, identifiants et consignes du tuteur sont conservés. Les
sources restent identiques et les corrigés modèles ne sont jamais exportés.

Les anciens manifestes de 46 ou 47 fichiers restent reconnus : une nouvelle
génération retire les quatre synthèses remplacées, range le contrôle S1 dans
son semestre et conserve le final S2, pour un total de 43 fichiers courants. Les fichiers étrangers à une distribution gérée restent
protégés par le refus de remplacement ; aucun dossier de soumissions n'est lu
ou déplacé pour cette opération.

## Vérifications techniques

Les tests de distribution contrôlent la substitution unique, la conservation
exacte des sources, l'échappement de l'URL, le rejet des gabarits non canoniques,
les sorties contenant une adresse de dépôt, le remplacement atomique et le
retrait des anciens noms. Le test de `deploy.sh` remplace Python et Docker par
des commandes factices et vérifie l'ordre ainsi que l'arrêt sur erreur : il
n'effectue aucun déploiement réel. Le code exécuté pour contrôler le HTML est
uniquement le gabarit de confiance produit par le générateur ; aucun code de
notebook étudiant n'est exécuté par le serveur ou par ces tests.

## Historique du renforcement Swinnen des TD3, TD5 et TD6

Lors de cette étape, le parcours comportait treize cahiers TD, avec trois unités one → bis → ter pour chacun de ces thèmes. Les neuf nouveaux cahiers ont des contrats v2 distincts ; les trois anciens contrats restent disponibles pour les copies déjà distribuées. Ces anciens sujets sont désormais dans `historique/`, hors du sélecteur courant. Voir `Notebooks TD/S1/README.md` pour les fichiers exacts et `pedagogy/s1-swinnen-expansion.md` pour la matrice de couverture.

Chaque nouveau cahier contient ses attributions et une annexe repliable avec la notice, la préface et la licence intégrale de Swinnen (CC BY-NC-SA 2.0 France). Elle reste incluse dans chaque fichier distribué ; les adaptations pédagogiques ne sont pas placées sous la licence GPL du code serveur. Les cahiers sont générés par la même commande de distribution, sans modification manuelle de `dist/`.

## Historique de l’extension du parcours renforcé au TD4

Lors de cette extension, le TD4 a été décliné selon la même progression en trois cahiers : conditions et filtres, bornes et répétitions, comptages et compréhensions. Les trois sujets possèdent leurs contrats `td4-one-s1`, `td4-bis-s1`, `td4-ter-s1` en version 2 et un correcteur de six points chacun. Le sujet historique `td4-s1` et son barème restent compatibles avec les copies déjà distribuées. La progression actuelle comprend quinze cahiers de TD hors DM/contrôles ; les quatre synthèses historiques restent accessibles séparément. Matrice et références : `pedagogy/s1-td4-swinnen.md`.

## État d’archive et vérifications

Le champ de catalogue `archived` est booléen et doit correspondre à un chemin
commençant par `historique/`. Les archives conservent leurs métadonnées
embarquées d'origine comme provenance et leurs contrats de correction. Les
quatre anciens profils du tuteur sont classés comme exclusions figées, sans
synchronisation ni réécriture ; les profils des supports courants sont conservés.
Le recensement du tuteur inclut aussi `historique/` pour empêcher l'oubli d'une
archive, y compris celles dont le JSON était déjà tronqué.

Les tests comparent les douze fichiers à des empreintes extraites du parent Git
antérieur à l'archivage. Ils vérifient aussi les quinze cahiers S1 courants, les
43 fichiers générés, les anciennes routes, l'absence d'archives dans `dist/` et
la migration des anciennes distributions. Les fixtures historiques antérieures
ne sont pas recalculées.
