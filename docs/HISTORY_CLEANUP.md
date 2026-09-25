# Nettoyer les adresses de dépôt dans l’historique Git

L’outil `app/prepare_history_cleanup.py` prépare une réécriture contrôlée des branches et des tags légers. Il remplace les domaines ciblés par `example.invalid`, puis actualise le SHA des ressources figées dans les documents descendants. Il ne modifie ni le dépôt de travail ni le serveur pendant `prepare`. `publish` constitue une action distincte, explicite du mainteneur.

Ce nettoyage concerne les objets accessibles par les branches et tags ordinaires. Il ne retire pas les consignes pédagogiques historiques : le remplacement neutralise leurs adresses. Les consignes actuelles sont supprimées dans les notebooks par la PR pédagogique associée.

## Préparer depuis le poste du mainteneur

Fusionner d’abord la PR, récupérer cette version du script, puis interrompre les publications concurrentes pendant l’opération. Utiliser le transport Git déjà authentifié sur le poste, notamment son alias SSH habituel. Aucun jeton ne doit être copié dans le code ou la commande.

Prérequis : Python 3.10 ou ultérieur, Git, et la dépendance dédiée suivante. Elle n’est pas nécessaire à l’application Flask et ne figure pas dans ses dépendances de production.

```powershell
python -m pip install git-filter-repo==2.47.0
$talRemote = git remote get-url origin
$talCleanup = Join-Path $env:USERPROFILE 'tal-history-cleanup'
python app/prepare_history_cleanup.py prepare --source $talRemote --output $talCleanup --discover-deposit-hosts
```

Le dossier de sortie doit être nouveau et situé hors de tout dépôt Git. Choisir un emplacement privé : `original.bundle` conserve volontairement l’ancien historique, adresses comprises. Le script ne publie ni cette sauvegarde ni sa configuration.

L’option de découverte examine exclusivement les cellules Markdown des versions historiques de `Notebooks contrôles finaux/DevoirS1.ipynb` et `Notebooks TD/S3/TD0_S3_diagnostic_texte.ipynb`. Elle exige une mention de dépôt ou d’autoévaluation et l’un des deux chemins de dépôt connus. Les URLs de bibliothèques ou de ressources ne deviennent pas des cibles. Aucun nom de domaine découvert n’est affiché.

Pour un choix manuel des domaines, remplacer `--discover-deposit-hosts` par `--hosts-file CHEMIN_PRIVE`. Ce fichier privé contient soit un domaine par ligne, soit un tableau JSON de chaînes. La variable `TAL_PRIVATE_HOSTS` accepte également des domaines séparés par espaces ou virgules. Ne versionner aucun de ces paramètres.

Sous Linux, les mêmes commandes Python fonctionnent ; remplacer les affectations PowerShell par les variables du shell utilisé. Une source locale est possible, mais elle expose uniquement ses propres branches et tags : utiliser l’URL distante pour traiter toutes les branches partagées.

## Examiner le résultat

Une préparation réussie produit :

- `original.bundle` et `original-refs.json` : sauvegarde privée et références avant nettoyage ;
- `cleaned.bundle` : historique nettoyé, transportable ;
- `manifest.json` : références avant/après, empreinte du bundle et bilan des vérifications ;
- `commit-map.json` : correspondance des commits ;
- `rewritten.git` et `first-pass-mapping/` : objets de travail et correspondance intermédiaire.

Le script refuse de produire un manifeste de publication si une vérification échoue. L’audit contrôle tous les commits accessibles, leur nombre, l’ordre des parents, les auteurs, committers, dates et messages. Les substitutions autorisées sont les domaines et la référence complète du commit des ressources. Chaque chemin, mode de fichier et contenu est comparé ; les ressources pédagogiques restent identiques octet pour octet. La seconde passe doit laisser stable le nouveau commit des ressources. Un dernier parcours vérifie l’absence des domaines ciblés dans les objets accessibles.

Une modification de parent ou de contenu invalide une signature de commit : les signatures retirées sont comptées. Les auteurs et dates restent conservés ; les anciens badges de signature ne le sont pas. Les tags annotés sont explicitement refusés avant réécriture, car ils demandent un audit distinct de leurs métadonnées et signatures. Le dépôt examiné pour cette mission ne possède aucun tag.

La préparation n’est utilisable que tant que les références distantes n’ont pas changé. Toute fusion, création, suppression ou modification d’une branche ou d’un tag impose une nouvelle préparation dans un autre dossier. Un bundle préparé avant fusion de la PR ne convient donc pas à une publication après cette fusion.

## Publier explicitement

Après examen du manifeste, le mainteneur lance :

```powershell
python app/prepare_history_cleanup.py publish --output $talCleanup --remote $talRemote
```

Le script vérifie l’empreinte du bundle, compare exactement les références distantes à l’état initial, reconstruit un dépôt temporaire à partir du bundle, puis publie les références explicitement avec `--atomic` et un `--force-with-lease` par référence. Aucune suppression de référence n’est demandée. Si une référence existante avance entre le contrôle et le push, le bail fait refuser l’opération entière. Une nouvelle branche créée après le contrôle préalable ne peut pas être protégée par ces baux : le contrôle final la détecte après publication. Le gel des contributions doit donc couvrir toute l’opération. Le serveur doit accepter les mises à jour atomiques et la politique de protection doit autoriser l’opération du mainteneur ; le script ne contourne aucune protection.

Pour transporter la préparation vers un autre poste, copier au minimum `cleaned.bundle` et `manifest.json` dans le même dossier et disposer de cette version du script. Conserver séparément la sauvegarde privée originale. Le poste de publication utilise sa propre configuration Git authentifiée.

## Après publication

Vérifier les liens de ressources des TD et les références distantes. Avant de remplacer le dépôt sur le serveur, préserver les soumissions et autres données non versionnées, les fichiers de configuration locaux, les fichiers `.env` et les volumes Docker ; les sauvegarder séparément et conserver leurs montages lors du redéploiement. Re-cloner le dépôt sur les postes et le serveur de travail avant de reprendre les contributions. Ne pas fusionner ni pousser les anciennes branches locales : cela pourrait réintroduire les objets nettoyés. Les travaux non publiés doivent être conservés séparément et réappliqués après inspection.

Une réécriture des branches ne garantit pas l’effacement mondial des anciennes adresses. Les anciennes copies, forks, caches et références de pull requests peuvent conserver les objets. GitHub précise notamment que les références de PR ne sont pas modifiables par un push ordinaire et que son assistance ne supprime pas les données non sensibles dans ce cadre. Une URL de dépôt publique ne doit donc pas être présentée comme définitivement effacée de GitHub.

Références techniques : [procédure GitHub de retrait de données sensibles](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository), [documentation de git-filter-repo](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt), [documentation de git push](https://git-scm.com/docs/git-push).

## Vérification de l’outil

```text
python -m unittest discover -s tests -p test_history_cleanup.py -v
```

Les tests utilisent des dépôts locaux synthétiques : graphe avec fusion, deux dates distinctes, ressources avec fins de ligne conservées, pin vers un ancêtre, découverte ciblée, sauvegarde, publication explicite, refus d’une source avancée et refus d’un bundle modifié. Ils sont ignorés si la dépendance optionnelle `git-filter-repo` n’est pas installée.

### Validation sur le dépôt du projet

Le 25 septembre 2026, une préparation locale a réussi sur l’état distant comprenant six branches, aucun tag et 111 commits. L’audit a examiné 283 versions de blobs ; 15 signatures de commits ont été retirées. Le commit des ressources a été remappé vers `b92e92b6c216014283056c83aa545881a447b3a5`, avec contenu des ressources inchangé. La sauvegarde originale, le bundle nettoyé, le manifeste et la correspondance des commits ont été produits. Aucune publication distante n’a été effectuée lors de cette validation.

Cette préparation constitue une preuve de fonctionnement sur cet état précis. La branche de la présente PR et sa fusion changent les références : le mainteneur doit exécuter une nouvelle préparation après fusion avant de publier. Une divergence de référence provoque un refus explicite de `publish`.
