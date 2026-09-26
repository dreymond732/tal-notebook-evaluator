# Intégration de la consolidation TAL

Mission : `TAL-Integration-Master`, producteur des gardes de non-régression et de la CI, sur `integration/tal-metadata-submit`. Référence initiale : `2a367529963f66a186dff1658b5951d0dbc27642`.

## Preuves d'intégrité

`tests/fixtures/notebook_migration_baseline.json` contient des SHA256 calculés depuis les objets Git de la référence initiale, jamais depuis les notebooks migrés :

- 32 empreintes du JSON canonique des sujets actifs. Le test retire uniquement les nouvelles clés `metadata.tal` du notebook et de ses cellules avant comparaison. Sources, sorties, ordre, identifiants de cellules, métadonnées Colab et instructions du tuteur restent inclus dans la comparaison.
- 10 empreintes des octets d'origine : neuf notebooks exclus de la distribution et le contrôle final S2 sans correcteur actif. Cette vérification couvre également le fichier enseignant dont le JSON était déjà tronqué.

Le test compare aussi catalogue, manifeste des tuteurs et registre des modes/semestres. Les fichiers de référence ne sont pas régénérés par la CI. Une future révision pédagogique légitime devra mettre à jour la preuve dans la même PR, avec justification et revue pédagogique ; un échec ne doit pas être masqué en recalculant automatiquement les empreintes.

## Vérifications automatisées

`.github/workflows/ci.yml` s'exécute sur les PR et sur les publications dans `main`, avec accès GitHub en lecture seule :

1. Python 3.12, dépendances applicatives et `git-filter-repo==2.47.0`, pour exécuter aussi les tests de l'outil historique.
2. Compilation de l'application et des tests, puis toute la suite `unittest`.
3. Contrôle des 33 contextes tuteur et des 32 sujets distribuables.
4. Génération et vérification d'une distribution sous `dist/ci`, avec l'adresse neutre `https://example.test/universite/tal`, puis vérification qu'aucun fichier suivi n'a été modifié.
5. Construction de l'image Docker, démarrage isolé, contrôle de `/health`, `/` et `/submit`, avec simulation du préfixe de proxy `/universite/tal`. Le conteneur est supprimé même en cas d'échec.

Les notebooks étudiants ne sont jamais exécutés par ces vérifications. La cellule de dépôt générée est comparée structurellement ; aucun notebook distribué n'est publié comme artefact CI. Les tests existants du contrat, de la distribution et des évaluateurs couvrent notamment le routage, les réponses privées des contrôles, la persistance et les anciennes copies.

## Limites et passage au mainteneur

Vérification locale du 26 septembre 2026 : **143 tests réussis, aucun test sauté** ; compilation Python réussie ; 33 contextes tuteur conformes ; vérification, génération et contrôle des 32 notebooks distribuables réussis. Le YAML du workflow a été chargé et chaque bloc shell vérifié par `bash -n`. Ces résultats ne préjugent pas de l'exécution du job Docker sur GitHub Actions.

Docker n'est pas disponible dans l'environnement local de production de cette PR : construction et démarrage du conteneur sont **NOT_TESTED localement**, et leur résultat doit être contrôlé dans GitHub Actions. Le smoke test avec en-tête de préfixe ne remplace pas un essai derrière le proxy réel du serveur.

Lors de la [première exécution CI de la PR 15](https://github.com/dreymond732/tal-notebook-evaluator/actions/runs/36246038374), au commit `f55fcc`, le job de tests et la construction Docker ont réussi. Le smoke test a échoué sur une réinitialisation de connexion immédiatement après le démarrage du conteneur, avant disponibilité de Gunicorn. L'attente de disponibilité réessaie désormais aussi ces erreurs de connexion, avec délais bornés ; les assertions sur le contenu de `/health` et les formulaires sous préfixe restent inchangées. Le résultat du smoke test après cette correction reste à vérifier dans une nouvelle exécution CI.

L'intégration est productrice des tests et du workflow : son verdict est **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. La revue indépendante du code a recalculé les 42 empreintes et examiné ces ajouts sans anomalie bloquante. Les verdicts pédagogiques et de gouvernance restent nécessaires avant la décision du mainteneur. Aucun déploiement ni fusion n'est effectué par cette mission.
