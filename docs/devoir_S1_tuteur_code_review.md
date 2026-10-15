# devoir_S1_tuteur — Audit technique indépendant

## Handoff et verdict

Mission du 15 octobre 2026 : révision guidée distincte du DM S1, avec profil spécifique du tuteur, sans changement de l'original ni de son contrat de notation. Branche `pedagogy/devoir-s1-tuteur`, référence `590b9a6c78fc6b27f8985e060c6ea2325367f652`. Rôle : TAL-Code-Auditor, indépendant du Designer, du Code-Architect et de l'intégration.

**ACCEPT technique** au périmètre et aux empreintes ci-dessous. Aucun nouveau TAL-AUD dans le diff audité. Ce verdict ne certifie pas le comportement effectif de Gemini et ne lève aucun constat de l'audit S1 sur le moteur DM, les contrôles ou les corrigés.

L'auditeur a lu le cadrage et la matrice préalablement acceptés `docs/pedagogy/devoir_s1_tuteur_spec.md`, la nouvelle édition, le manifeste, le générateur, les six nouveaux tests et le test d'inventaire adapté. Aucun fichier source, test, notebook ou document du dépôt modifié par l'auditeur ; seule sortie personnelle : ce rapport `/tmp/devoir-s1-tuteur-code-review.md`. Aucun commit, changement de branche, publication ou déploiement.

## Conservation indépendante du DM et des autres supports

Vérification des octets actuels contre **les blobs Git de 590b9a6 et les SHA-256 du snapshot `/tmp/devoir-s1-tuteur-before.json`** : les 35 notebooks originaux et `app/notebook_catalog.json` sont identiques, soit 36 objets contrôlés. L'original `Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb` garde notamment l'empreinte `6fd62ebefdb8e8cd1a7673edf1dbfca2b26a02745dd2ab98a6183f9ea46122f1`.

Le manifeste ajoute exactement la séance `devoir_S1_tuteur` ; ses autres champs et chacune des 35 sessions existantes sont identiques. Pour ces 35 sessions, le contexte régénéré par le nouveau code est exactement égal au contexte Colab actuellement enregistré et la migration est idempotente. Les octets des notebooks comprenant le contexte HTML et celui de Colab n'ont pas été changés.

Nouvelle copie `Notebooks contrôles finaux/S1/devoir_S1_tuteur.ipynb` :

- 45 cellules, mêmes types, IDs et ordre que le DM ; cellules 3 à 45, en base 1, intégralement identiques à l'original.
- Toutes les cellules de code, tous les énoncés Q1–Q18, données, sorties, marqueurs, essais et barème sont donc conservés, sans exécution.
- Seules les sources des deux premières cellules Markdown changent : titre et contexte caché en première ; paragraphe « Conditions de travail » de l'introduction en deuxième. Les autres champs de ces deux cellules restent identiques.
- Métadonnées racines hors `tal_tutor` et `colab.aiContexts` identiques ; `metadata.tal` de notation inchangé, avec l'identifiant `dm-intermediaire-s1`.
- Nouvelle métadonnée de tutorat : `id` et `tutor_profile` `devoir_S1_tuteur`, activité `td`, semestre 1. Elle ne crée pas de nouvel évaluateur ni de nouveau contrat.

Aucun diff dans le catalogue, routes, correcteur DM, fixtures historiques ou règles normatives. Les défauts préexistants du correcteur DM ne sont pas recherchés à nouveau ni présentés comme corrigés par cette mission.

## Générateur et garde-fous du profil

Le nouveau comportement est une branche explicite de `render_context`, distincte du guidage TD générique. `validate_session` exige le profil spécifique dès que l'ID ou le nom de fichier désigne l'édition. Un profil manquant échoue, sans repli silencieux vers le TD générique. Un profil renseigné est réservé à l'ID et au nom de fichier de l'édition, au semestre 1 et à l'activité TD ; profil inconnu, identité du contrôle original, semestre ou mode différent sont refusés.

La branche contrôle demeure prioritaire et son texte inchangé. Le DM original conserve son profil `DM_INTERMEDIAIRE_S1`, activité `controle`, et le refus complet d'assistance. Lui attacher le profil de révision échoue à la validation. Les modes du tuteur et de la notation sont explicitement séparés : le mode LLM de la nouvelle copie est TD, mais sa notation reste un contrôle à reçu privé.

Le profil exige exactement les IDs Q1 à Q18, interdit les doublons, exige des fiches non vides et conserve les validations de types de listes et d'inclusion des notions introduites. Les bibliothèques autorisées et fournies sont vides à l'échelle de la séance ; une bibliothèque autorisée par une question est nécessairement incluse dans la liste vide de séance, donc refusée.

Le prompt spécifique final mesure **4 256 caractères**, inférieur au budget applicatif de 4 400. La mesure ancienne de 4 230 ne correspond pas au dernier libellé : « Vérifiez la compréhension conceptuelle, sans valider une réponse du devoir ni une note. » Les 18 fiches et leurs notions sont présentes sans troncature ; les notions regroupées doivent être abordées individuellement. Le contexte contient des instructions et noms de notions, aucun corrigé, résultat du devoir, code de solution ou commande d'outil. Les règles demandent identification de la question, périmètre fermé, révision de toutes les notions, une question puis attente, exemples conceptuels distincts, suivi des acquis, autonomie et refus de fournir une solution ou de modifier/exécuter des cellules.

Les défenses communes contre délimiteurs HTML/LLM dans les données et dépassement de budget continuent à s'appliquer. Les deux emplacements du contexte de la nouvelle copie sont strictement synchronisés et sa migration est idempotente.

## Modes web, catalogue et distribution

Le catalogue est inchangé : 35 supports de notation, dont 34 actifs. Le manifeste contient désormais 36 séances de tutorat, car cette édition réemploie le contrat d'un devoir existant. Ni `EVALUATORS`, ni les modes de notation, ni le résolveur ne déduisent le mode de correction de `metadata.tal_tutor`.

Sondage web indépendant, avec identité fictive et base de soumissions temporaire isolée : POST de la nouvelle édition vers `/submit` résout `dm-intermediaire-s1` en mode `controle`, HTTP 200, reçu de dépôt sans score ni détail de correction. Une copie, un rapport et un CSV sont persistés ; la copie conserve exactement les octets soumis. Aucun évaluateur `devoir_S1_tuteur` n'est présent dans le registre. Aucun code étudiant exécuté ; répertoire temporaire supprimé après le contrôle.

La nouvelle édition est une source directement ouvrable dans Colab, pas une entrée supplémentaire du catalogue et pas une nouvelle distribution automatique par défaut. Les mécanismes de préparation restent fondés sur les 34 sujets actifs existants. La présence dans le dossier des contrôles ne requalifie pas son profil LLM ; inversement, son nouveau profil LLM ne rend pas publique la correction du DM.

## Adaptation bornée du test d'inventaire

L'ancien `test_baseline_catalog_tutors_and_registry_cover_the_same_subjects` imposait l'égalité entre chemins du catalogue de notation et chemins de toutes les séances du tuteur. La nouvelle édition séparée, autorisée sans nouvel évaluateur, ajoute légitimement un chemin au second ensemble.

Le test devient `test_baseline_catalog_tutors_and_registry_cover_the_same_assessments`. La comparaison est conservée en ajoutant **uniquement** le chemin exact `Notebooks contrôles finaux/S1/devoir_S1_tuteur.ipynb` à l'ensemble attendu. Deux assertions lient ce chemin à l'ID et au `tutor_profile` spécifiques. Les assertions historiques sur sujets actifs/inactifs, catalogue, exclusions, semestre, mode et correspondance registre de chaque ancien évaluateur sont inchangées. Aucune fixture historique ni liste de tolérance générique modifiée. L'inventaire du générateur continue à refuser les fichiers non classés, doublons et chemins absents.

Cette adaptation vérifie la distinction désormais voulue entre édition de tutorat et évaluateur ; elle ne masque pas l'absence d'une route de notation nouvellement annoncée, puisque aucune nouvelle route n'est demandée.

## Tests et attribution des preuves

L'auditeur a exécuté après synchronisation du dernier prompt les modules existants/ajoutés suivants :

```python
modules = [
    'test_devoir_s1_tuteur',
    'test_tutor_metadata',
    'test_notebook_migration_integrity',
]
```

**36 tests ciblés PASS**, dont les six nouveaux tests de l'édition. Ils couvrent le SHA du DM, invariants de copie, 18 fiches et prérequis introduits, double contexte/idempotence, contrôle original sans aide et notation privée, refus de profil absent/inconnu/mal attaché, fiches partielles/vides et bibliothèques interdites. La nouvelle logique applicative justifie ces contrôles de séparation et d'échec, au-delà d'un simple test miroir de texte.

Preuves indépendantes supplémentaires : comparaison des 36 objets gelés contre Git et snapshot ; égalité des 35 anciennes sessions, des 35 contextes générés et migrations ; copie JSON ; lecture intégrale du prompt final ; POST réel avec persistance et confidentialité ; `git diff --check` sans erreur.

Le journal final de l'intégration `/tmp/devoir-s1-tuteur-tests-verified.log`, lu par l'auditeur, confirme **308 tests PASS en 6,622 s après la dernière clarification du prompt et la régénération**. Ce passage porte sur le contexte final de 4 256 caractères et la copie d'empreinte `e67df7e49ea623346cc50964002ef0473359649b3fa3b13af7353ae9a80ac25b`, identiques à la version relue. Les 36 tests ciblés indépendants portent également sur ce prompt final ; ils sont inclus dans les 308 cas de la suite, pas 36 nouveaux tests supplémentaires. Tuteur 36, vérification des 34 sujets actifs et nbformat de la nouvelle édition rapportés PASS par l'intégration ; aucun test relancé par l'auditeur pour cette clôture.

## Empreintes de la version relue

| Fichier | SHA-256 |
|---|---|
| app/tutor_metadata.py | 2a0230d00ebf2bb5d96a9c5334e10f9ca65ae62c0ee035a97392c151ff1b138e |
| docs/pedagogy/tutor_sessions.json | 85a44caff0a98f8e7fe6bb23d6a4a328e869e3dd84f8e1c4464c67d4e5ac7c28 |
| Notebooks contrôles finaux/S1/devoir_S1_tuteur.ipynb | e67df7e49ea623346cc50964002ef0473359649b3fa3b13af7353ae9a80ac25b |
| tests/test_devoir_s1_tuteur.py | 5314fe79de81f0a15903434f60f711741627d3cae5637915e08a5fdfcf3890a5 |
| tests/test_notebook_migration_integrity.py | 8eb38b2f7f411cd7407916cebc585f7ba406783c6e9e16616cdac7411286e8fa |

## Limites et relais

La fidélité des notions au besoin pédagogique et la lisibilité font l'objet de verdicts spécialisés séparés. Cette revue statique ne teste pas Gemini dans Colab : respect réel de l'attente, résistance à l'insistance, suivi d'acquis sur plusieurs tours et absence de réponse divulguée restent non démontrés en conditions réelles. Aucun verrou technique de sécurité ne doit être déduit du seul prompt. Docker, production, CI distante et exécution humaine des réponses ne sont pas attestés.

Critères techniques remplis : original et 35 contextes existants préservés, copie non dégradante hors seuls passages autorisés, profil explicitement réservé et complet, budget et double synchronisation, aucune fuite de mode contrôle, pas de nouveau grader ou changement de distribution, test d'inventaire adapté au seul chemin autorisé, preuves ciblées PASS. Relais demandé à la gouvernance et à l'intégration avec les avis pédagogique/éditorial indépendants. L'intégration ayant produit le test d'inventaire et sa synthèse relève de MAINTAINER_REVIEW ; aucune fusion ni publication autorisée par cet avis.
