# Gouvernance — Progression et évaluation S1 v2

## Mission et verdict

Revue indépendante du 1er octobre 2026 sur la branche `pedagogy/s1-progression-evaluation-v2`, référence `322abf53b4a1ff96c1652acfa21b4d27185bfa1a` (PR19). L’enseignant demande de traiter les limites des TD et de leurs correcteurs, en interdisant toute réduction de l’étayage existant. Le TD2 sert de référence conservée ; les autres supports sont enrichis.

**Verdict : CONFORME**, pour l’état relu et les preuves ci-dessous. Il s’agit d’un **CHANGEMENT_DE_CONTRAT** : les sept TD S1 passent en v2, exigent quatre champs d’identité et des preuves rattachées aux questions ; six correcteurs génériques sont remplacés. Les 45 questions principales et leurs maxima restent 6, 7, 6, 7, 6, 6 et 7. Aucun exercice, donnée, explication ou objectif historique n’est supprimé ni rendu facultatif.

## Séparation des responsabilités

| Rôle | Production ou contrôle | Résultat |
|---|---|---|
| TAL-Prof (`s1v2_prof`) | Matrice source → cible, spécification et périmètres du tuteur dans `docs/pedagogy/` | Matrice validée par l’orchestrateur avant toute conception ; aucune réduction autorisée |
| TAL-Pedagogy-Designer (`s1v2_designer_early`, `s1v2_designer_late`) | Sept notebooks et bilans pédagogiques, dans leurs périmètres respectifs | Réalisation soumise à revue indépendante |
| TAL-Code-Architect (`s1v2_engine`, `s1v2_checks`) | Moteur inerte, références, six correcteurs, porte d’entrée TD2, contrat, routes, catalogue et tests techniques | Réalisation soumise à revue indépendante |
| TAL-Code-Auditor (`s1v2_code_audit`) | Analyse technique, tests et sondes indépendants, produit en lecture seule | ACCEPT / CONFORME après reprises |
| TAL-Pedagogy-Reviewer (`s1v2_pedagogy_audit`) | Comparaison à la base, progressivité et adéquation des preuves, produit en lecture seule | ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE après reprises |
| TAL-Integration-Master (`s1v2_integration`) | Fixture de conservation, adaptation des tests et documentation technique | Producteur : relais MAINTAINER_REVIEW, jamais auto-validation READY_TO_MERGE |
| TAL-Governance-Auditor (`s1v2_governance`) | Contrôle des permissions, contrats et preuves ; écriture du présent rapport uniquement | CONFORME |

La branche est dédiée. Les actifs normatifs `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md` et `docs/agents/` ne sont pas modifiés. Aucune modification directe de `main`, fusion ou mise en production n’est réalisée. Le mainteneur reste décisionnaire de la fusion et du déploiement.

## Conservation et pédagogie

La matrice `docs/pedagogy/s1_progression_v2_coverage.md` a précédé les modifications des notebooks. La spécification précise les valeurs attendues, les traces complémentaires, les alternatives admises et la portée du score. Les bilans `docs/s1_v2_early_coverage.md` et `docs/s1_v2_late_coverage.md` décrivent les ajouts. L’autorisation enseignante porte sur l’enrichissement ; elle n’autorise aucune réduction.

La gouvernance a comparé indépendamment les sept objets de `tests/fixtures/s1_progression_v2_source_baseline.json` aux notebooks récupérés par `git show` au commit source : ils sont exactement identiques. La fixture historique de migration n’a pas été régénérée. Les contrôles de conservation et la lecture indépendante confirment les mêmes identifiants, le même ordre relatif et les sources pédagogiques historiques préservées comme préfixes. Le TD2 conserve mot pour mot ses activités, explications et traces ; seuls le contrat, l’identité et une notice sont ajoutés.

Les nouveaux exemples emploient d’autres données que les réponses notées. Les entraînements restent obligatoires, non notés et distincts des cellules `answer`. Ils préparent notamment `for/items`, les parcours inverses et le modulo, les paramètres par défaut et cas vides, la lecture/écriture CSV et l’ordre des transformations regex. Les sept tuteurs restent dans les métadonnées et la première cellule ; le tuteur S1 ne fournit toujours pas de code aux demandes de solution. La cellule finale de restitution est conservée, unique, fournie et hors évaluation.

La revue pédagogique a clôturé ses deux réserves : introduction explicite du modulo et synchronisation des périmètres TD5/TD7 ; acceptation des phrases construites par concaténation ou f-string en TD1 Q6 et du filtre par `upper()` en TD4 Q3. Son verdict final est **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, avec 2 tests de conservation et 13 tests de correcteurs réussis. Les durées annoncées de 120 minutes sont cohérentes avec le découpage, mais ne sont pas des temps observés en classe.

## Contrat technique et sécurité

- Les sept contrats v2 exigent une identité unique et toutes les cellules de réponses attendues. Les quatre valeurs d’identité sont des affectations littérales non vides ; le numéro étudiant distingue les homonymes dans les noms de fichiers. Les anciennes versions et cellules obligatoires manquantes renvoient « mauvaise version du notebook » avant correction et persistance. Une cellule existante mais vide reste une preuve absente.
- Les copies acceptées sont enregistrées dans `soumissions/tdN-s1-v2/`. Les anciens fichiers et CSV ne sont ni réécrits ni supprimés. Les contrôles S1, le devoir maison, le S2 et les contrats S3 gardent leur comportement attendu, couvert par la suite de régression.
- L’analyse porte uniquement sur le code source et les sorties enregistrées. Le moteur relie les marqueurs aux cellules de réponse et aux dépendances syntaxiques des valeurs imprimées. Il compare les valeurs et les types, sans assimiler booléens et entiers ni imposer l’ordre des ensembles et dictionnaires. Les cellules d’exemple, d’entraînement ou de restitution ne donnent aucun point.
- Aucun code de notebook étudiant n’est exécuté et aucun fichier désigné par ce code n’est ouvert sur le serveur. Les littéraux enregistrés sont décodés avec `ast.literal_eval` après bornage ; le CSV enregistré est analysé en mémoire. Les tests utilisent des preuves synthétiques. Les sept notebooks sources ne contiennent aucune cellule exécutée ni sortie préremplie, vérification effectuée indépendamment par la gouvernance.
- Les résultats sont présentés comme **scores techniques provisoires**. Les diagnostics distinguent résultat incorrect, preuve absente, construction non repérée et dépendance non vérifiable. La présence d’une justification ne certifie jamais sa pertinence. Le rapport échappe les productions à relire.
- Le dispositif de restitution conserve seulement `__TAL_PUBLIC_URL__` dans les sources. L’adresse est injectée dans `dist/` lors du déploiement ; aucune adresse réelle de serveur n’a servi aux vérifications. Cette protection concerne le dépôt Git, pas la visibilité du lien dans les copies distribuées.

L’auditeur code a clôturé les réserves sur le code mort, les fonctions réaffectées, les textes de remplacement et les dernières variantes valides. Son verdict final est **ACCEPT / CONFORME** : 64 tests ciblés lors de la première revue, puis 24 tests de références et moteur après reprises. Des sondes indépendantes sur d’autres données confirment l’acceptation des phrases construites, le rejet d’une longueur fausse et l’acceptation du filtre `upper()` avec un autre nom de variable. Aucun défaut bloquant résiduel n’est identifié dans ce périmètre.

## Gates finaux et relais

Après toutes les reprises, l’orchestrateur a exécuté et communiqué les résultats consolidés :

| Vérification | Résultat |
|---|---|
| Suite complète `unittest discover -s tests` | **236 tests PASS**, 4,408 secondes |
| Compilation Python `app` et `tests` | PASS |
| Synchronisation des tuteurs | **34/34 PASS** |
| Vérification des sources distribuables | **33/33 PASS** |
| Génération des copies avec une URL neutre sous `/universite/tal` | **33/33 PASS** |
| Vérification de la distribution générée | **33/33 PASS** |

La suite inclut les contrats, routes, persistance, rendu et comportement sous proxy. Les gates portent sur l’état après les dernières corrections des variantes et des périmètres pédagogiques.

**Docker local : NOT_TESTED. CI distante : en attente de publication au moment de ce rapport.** La CI, dont le build et le contrôle de santé Docker, doit être constatée sur le commit exact de la PR et consignée dans son relais avant fusion. Une réussite locale ne constitue ni un déploiement réel ni une validation en séance Colab.

Les limites résiduelles sont explicites : les sorties peuvent être périmées ou fabriquées, l’analyse statique ne reconnaît pas toutes les variantes Python valides et ne démontre pas la généralité d’une fonction, les commentaires demandent une relecture humaine et la charge réelle doit être observée en classe. Ces limites ne sont pas présentées comme résolues par la conformité des traces.

Le relais reste **MAINTAINER_REVIEW** après CI : l’intégration est productrice de tests et ne peut s’auto-déclarer prête à fusionner. Après fusion décidée par le mainteneur, `bash deploy.sh` régénère la distribution. **Les sept TD S1 v2 doivent être redistribués depuis `dist/Notebooks TD/S1/`** ; changer seulement la version des anciennes copies ne leur ajoute pas les traces et le contrat requis.
