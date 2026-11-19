# Gouvernance — Archives et progression courante

**Verdict : `CONFORME`.**

Audit indépendant du 19 novembre 2026, rôle `TAL-Governance-Auditor`. Le réviseur n'a produit ni rangement, ni code, ni tests ; son écriture se limite au présent rapport. Ce verdict ne vaut ni fusion, ni déploiement réel, ni diffusion aux étudiants.

## Mandat et référence

L'enseignant demande : « Place les dans un dossier historique pour ne laisser dans les dossiers de semestre que les dernières versions en vigueur ». Ce mandat autorise le classement physique des versions remplacées et anciens corrigés ; il n'autorise pas une suppression d'exercices, de copies remises ou de notes.

- Branche observée : `code/archives-progression`.
- Référence immédiate observée : `501413c3e5c216138595e68bee714d7902e9a393`, stade de la PR67 consacré à la distribution des contrôles.
- Cadrage préalable et matrice source → archive : `docs/pedagogy/archives_progression.md`.
- Tableau des douze déplacements et empreintes : `historique/README.md` et `tests/fixtures/archives_progression_source_sha256.json`.
- Normes relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et fiche du rôle `TAL-Governance-Auditor`.

Le rapport antérieur `reports/governance/distribution-controles.md` reste une preuve datée du stade de distribution à 47 fichiers. Il n'est pas réécrit pour faire croire que ce stade antérieur comptait 43 fichiers. Le présent rapport documente la réduction de la sélection courante après archivage, sans réduction des contenus conservés.

## Périmètre et décision de classement

| Famille | Traitement constaté | Conservation et effet |
|---|---|---|
| Quatre synthèses S1 TD3/4/5/6 | Déplacement sous `historique/Notebooks TD/S1/` | Octets identiques ; hors menu et distribution courants ; correcteurs de compatibilité maintenus |
| Huit anciens corrigés déjà exclus | Déplacement sous `historique/`, avec arborescence d'origine | Aucune diffusion nouvelle ; contenus et défauts d'origine conservés |
| Douze cahiers A/B/C S1 + TD1/TD2/TD7 | Emplacements courants inchangés | Quinze cahiers S1 courants ; aucun exercice ni contrat modifié |
| R0, R2 et TD1.b S3 | Conservation dans la progression courante | Activités distinctes, dont bonus facultatif ; pas d'archivage sur le seul nom R ou ancien numéro |
| Contrôle final S2 à 18 questions | Conservation dans les contrôles et la distribution | Sujet distinct, correction automatique toujours inactive, sauvegarde locale conservée |
| Modèles actuels | Conservation dans `Corrigés modèles/` | Hors distribution, inchangés |

Les quatre synthèses ne sont pas remplacées par des supports futurs à produire : les douze cahiers A/B/C existent déjà. La matrice de classement ne prétend pas démontrer une nouvelle équivalence de chaque ancien exercice ; elle distingue ce rangement explicitement demandé des revues pédagogiques de fond antérieures.

Deux archives sont déjà invalides en JSON à la référence : `Notebooks TD/TD6_S2-corrigé.ipynb` et `Notebooks contrôles finaux/DevoirS2.ipynb`. Leur conservation porte sur leurs octets, sans reconstruction de cellules ni assimilation à un sujet courant.

## Preuves indépendantes de conservation

Le présent auditeur a comparé les fichiers au parent Git, sans les exécuter :

- **12 archives strictement identiques en octets** aux douze sources de la référence ; leurs SHA-256 correspondent au manifeste de preuve.
- Les douze anciens chemins physiques ont disparu ; les archives conservent les chemins internes d'origine comme provenance figée.
- Les **63 autres notebooks** suivis à la référence sont présents à leur emplacement courant et strictement identiques en octets.
- Le manifeste de synchronisation du tuteur retire exactement les sessions `TD3_S1`, `TD4_S1`, `TD5_S1` et `TD6_S1` des sessions courantes. Tous les autres profils de session sont identiques à la référence.
- Les archives deviennent des exclusions explicites. L'inventaire technique inclut `historique/`, ce qui permet de vérifier leur présence sans les réécrire ou les redistribuer.

Aucun barème, exemple, donnée, sortie, identifiant, rôle de cellule ou contexte de tuteur n'est modifié dans un notebook. Aucun fichier normatif n'est modifié pour faire accepter le rangement.

## Contrats, distribution et stockage

Le changement porte sur le statut de visibilité et le chemin physique des quatre synthèses. Le catalogue ajoute un indicateur `archived` booléen cohérent avec le préfixe `historique/`. Il conserve leur activation de correction afin que les copies déjà commencées restent recevables.

| Point audité | Observation | Conclusion |
|---|---|---|
| Sélection courante | Le générateur exclut les entrées archivées, puis conserve les TD actifs et contrôles courants | **43 fichiers : 30 TD et 13 contrôles**, sans archive ni modèle |
| S1 courant | Quinze cahiers dans le dossier et la distribution ; noms A/B/C et liens documentaires corrigés | Le parcours à commencer est distinct des synthèses historiques |
| Compatibilité | Les quatre correcteurs restent enregistrés, leurs routes directes accessibles et leurs contrats identiques | **46 évaluateurs** conservés, dont 4 de compatibilité ; aucune réévaluation historique |
| Menu | Les quatre éditions archivées sont masquées dans le menu de semestre, sans suppression de route | Le menu courant ne propose pas d'anciennes versions à commencer |
| Final S2 | Sujet toujours exporté ; catalogue inactif et évaluateur nul inchangés | Distribution et activation restent distinctes |
| Remplacement de `dist/` | Tests de génération depuis les manifestes antérieurs de 46 ou 47 fichiers ; anciens chemins retirés | Les synthèses ne restent pas dans la nouvelle distribution gérée |
| Migration du stockage S1 | Sélection par semestre, mode TD et évaluateur actif plutôt que par chemin physique de source | Le périmètre reste de **19 jeux de stockage : 15 courants + 4 historiques** |
| Données remises | Aucun migrateur exécuté sur un volume réel, aucune copie ou note réelle déplacée ou recalculée | Le rangement de sources ne devient pas une migration de résultats |

La modification de `migrate_storage_s1.py` évite précisément qu'un classement des sources réduise le périmètre à préserver. Le stockage d'une ancienne copie n'est pas supprimé parce que son notebook source se trouve désormais dans `historique/`.

Les protections des distributions gérées, de leur liste autorisée et des fichiers étrangers restent en place. Le générateur et le manifeste ne diffusent pas automatiquement les archives ou corrigés présents dans l'inventaire.

## Rôles et revues reçues

La production, les revues code/pédagogique/éditoriale et le présent audit sont distincts selon les relais de mission. Le réviseur de gouvernance n'a modifié aucun des fichiers examinés. La publication de la branche et la mise à jour de la PR sont dans le mandat ; elles ne valent pas approbation de fusion ou de mise en production.

- **Technique : `ACCEPT`.** Relais de l'auditeur indépendant : 56 tests et 8 POST synthétiques réussis, dont dépôts automatiques et directs des quatre copies historiques ; aucune réserve bloquante. Les essais utilisent des données et stockages temporaires, sans exécution du code étudiant.
- **Pédagogique : `ACCEPT` / `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`.** Rangement et conservation des contenus, distinction des remédiations S3 et du final S2 courant ; aucun objectif retiré sur le seul critère du nom du fichier.
- **Éditoriale : `ACCEPT` / `LISIBILITÉ_DOCUMENTATION_PROGRESSION_VALIDÉE`.** Rapport `reports/editorial/archives-progression.md` relu : tableau de classement, noms A/B/C, distinction des 19 jeux de stockage et 15 cahiers courants, correspondances prudentes des corrigés et statut des archives JSON invalides. Les trois observations documentaires signalées ont été corrigées et relues.

Le verdict éditorial est nommé selon son périmètre documentaire ; il n'attribue pas une nouvelle lisibilité à des questions de notebook inchangées. Aucun verdict négatif non résolu n'est transmis.

## Vérifications effectives

Reproduites par le présent auditeur :

- `python -m unittest discover -s tests -p test_notebook_archives.py -q` : **6 tests, OK**.
- `python -m unittest discover -s tests -p test_storage_migration_s1.py -q` : **11 tests, OK**.
- `python app/tutor_metadata.py --check` : réussi.
- `python app/prepare_student_notebooks.py check` : **43 notebooks, check OK**.
- Génération et vérification en répertoire temporaire avec adresse neutre : **43 fichiers, render/verify réussis**, dont 15 TD S1, sans `historique/` ni `Corrigés modèles/`.
- Comparaisons au parent Git : 12 déplacements et 63 autres notebooks byte-identiques ; empreintes et suppression des anciens emplacements confirmées.
- Comparaison des profils du manifeste : seules les quatre sessions déclarées sont retirées de la synchronisation courante.
- Vérification des comptes : 46 évaluateurs actifs, 19 entrées TD S1 de stockage, 15 cahiers S1 courants.
- `git diff --check` : réussi.

Observé dans le journal final du producteur, sans revendiquer une seconde exécution complète par la gouvernance :

- `python -m unittest discover -s tests -v` : **504 tests en 18,553 s, OK**, journal de session `archives-tests-final.log`.
- Relais complémentaire : appel de `bash deploy.sh` avec Docker uniquement simulé, check/render/verify 43 réussis ; quinze TD S1 et treize contrôles, sans les quatre synthèses. Ce message ne démontre aucun démarrage de service réel.

Les anciens fichiers de fixtures gelées ne sont pas régénérés : les tests adaptent explicitement les mappings de chemins, puis conservent les assertions de contenu et de contrat.

## Limites et relais d'intégration

Les deux archives JSON invalides restent invalides ; leur archivage ne les rend pas utilisables. La couverture de fond d'anciens corrigés par rapport à un sujet courant n'est pas revalidée par ce classement. Les chemins internes historiques sont conservés intentionnellement ; ils ne sont pas des références courantes à distribuer.

Aucun code de copie étudiante n'est exécuté et aucune copie réelle, note ou base de production n'est modifiée. Aucun notebook n'est testé visuellement dans Colab ; aucun déploiement réel ou transfert aux étudiants n'est effectué par cet audit.

Le lot peut poursuivre vers la branche et la PR67 avec **`MAINTAINER_REVIEW`**, l'intégration étant auto-produite. Le présent auditeur ne rend pas `READY_TO_MERGE`. Le mainteneur garde la décision de fusion, de déploiement réel et de choix des fichiers à diffuser.
