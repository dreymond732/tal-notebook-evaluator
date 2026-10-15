# devoir_S1_tuteur — Gouvernance indépendante

**CONFORME**, le 15 octobre 2026, pour la création de l'édition de révision séparée `devoir_S1_tuteur`, son profil fermé par question et les adaptations techniques nécessaires. Ce verdict porte sur le support et les instructions livrés, leur conservation et le workflow. Il ne certifie pas le comportement réel de Gemini dans Colab et ne lève aucun constat antérieur concernant le DM original ou les autres supports S1. Statut d'intégration : **MAINTAINER_REVIEW**.

## Mission, autorisation et référence

Branche dédiée : `pedagogy/devoir-s1-tuteur`. Référence source : `590b9a6c78fc6b27f8985e060c6ea2325367f652`. La demande enseignante autorise expressément une **nouvelle version** du DM, destinée à réviser toutes les notions de la question choisie avec un tuteur propre. Elle autorise l'introduction conceptuelle des prérequis nécessaires dans cette révision ; elle ne transforme pas le devoir évalué original en devoir assisté et ne fixe pas de nouvelles modalités de note.

La [matrice préalable](../../docs/pedagogy/devoir_s1_tuteur_spec.md) identifie le DM source, les références TD1–TD5 et les 18 questions source→cible, avec notions déjà présentées, compléments à introduire et invariants de copie. Les références privées historiques non disponibles ne sont pas annoncées relues. La politique de tutorat prévoit une version de remédiation distincte pour aider sur le contenu d'un contrôle ; la copie autorisée applique cette séparation, sans modifier les règles communes.

Sources normatives relues ou confrontées : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/agents/WORKFLOW.md`, fiche Governance-Auditor, `docs/EVALUATOR_CONTRACT.md` et clauses pertinentes de `docs/pedagogy/TUTORING_POLICY.md`. Ce rapport est produit par **TAL-Governance-Auditor**, distinct des producteurs et des réviseurs spécialisés. Ce rôle écrit uniquement `reports/governance/devoir-s1-tuteur.md` ; aucun produit, test, règle ou autre rapport n'est modifié par lui, sans commit, changement de branche, push ou publication.

## Prévalidation, permissions et indépendance

Le [handoff pédagogique](../../docs/devoir_S1_tuteur_pedagogy.md) atteste une lecture indépendante du cadrage avant conception : source toujours inchangée, cible encore absente, vérification physique des références TD et des 18 fiches, compléments Q12/Q14/Q15/Q18 relus. Son `ACCEPT DU CADRAGE PRÉALABLE` est attribué à la version d'empreinte `b322b5916ade77cb835c8a7df9d9a99ff43369d4bc011196a2d8d4a33e2cbdf8`, avant ajout de l'attribution par le Prof. Le producteur du cadrage n'a donc pas validé seul son travail. Aucune activité n'est supprimée ni reportée vers une cible non livrée ; aucune nouvelle confirmation enseignante n'est nécessaire dans ce périmètre déjà autorisé.

| Production ou contrôle | Rôle et périmètre permis | Preuve |
|---|---|---|
| Cadrage et séance du manifeste | TAL-Prof, agent distinct, écriture `docs/pedagogy/` | Matrice préalable et nouvelle entrée `devoir_S1_tuteur` |
| Copie du notebook et régénération finale | TAL-Pedagogy-Designer, écriture `Notebooks contrôles finaux/` | [Édition livrée](../../Notebooks%20contr%C3%B4les%20finaux/S1/devoir_S1_tuteur.ipynb) |
| Générateur et deux fichiers de tests | TAL-Code-Architect, assumé par root à cette étape | `app/tutor_metadata.py`, `tests/test_devoir_s1_tuteur.py`, adaptation de `tests/test_notebook_migration_integrity.py` |
| Couverture et protocole | TAL-Pedagogy-Reviewer indépendant du Prof et du Designer | [Revue pédagogique](../../docs/devoir_S1_tuteur_pedagogy.md), `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` |
| Rédaction et destinataire | TAL-Editorial-Reviewer indépendant, écriture de son seul rapport | [Revue éditoriale](../editorial/devoir-s1-tuteur.md), `ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE` |
| Lecture étudiante | TAL-Étudiant-Modèle, seuls sujet et TD autorisés | [Lecture à blanc](../../Corrig%C3%A9s%20mod%C3%A8les/TD/devoir-s1-tuteur/lecture_etudiante.md), 45 cellules et 18 questions, sans résolution ni exécution |
| Code, modes et tests | TAL-Code-Auditor distinct des producteurs | [Audit technique](../../docs/devoir_S1_tuteur_code_review.md), `ACCEPT`, 36 tests ciblés indépendants et sondage POST privé |
| Synthèse et archivage | TAL-Integration-Master, root après production technique | [Dossier de livraison](../../docs/devoir_S1_tuteur.md), sans auto-validation indépendante |
| Gouvernance | TAL-Governance-Auditor distinct des rôles précédents | Présent rapport |

L'attribution des rôles successifs Code-Architect puis Integration-Master a été explicitée par l'orchestrateur et consignée dans la documentation. Le Code-Auditor n'a modifié aucun produit ni test. Les archives pédagogique et technique livrées sont strictement identiques aux handoffs finaux de leurs auteurs au moment du contrôle. La lecture étudiante a été intégrée aux deux avis spécialisés avant leur clôture. Aucun ancien rapport S1 local non livré n'est nécessaire pour suivre les liens de preuve de ce dossier.

## Preuves indépendantes de conservation et de portée

La gouvernance a lu le diff applicatif et l'adaptation du test d'inventaire, confronté les rapports finaux et exécuté uniquement des lectures JSON/Git, calculs d'empreintes et appels en mémoire au générateur. Aucun code de cellule étudiante, d'exemple de solution ou de corrigé n'a été exécuté.

| Contrôle | Résultat constaté |
|---|---|
| Source et autres supports | Les **35 notebooks originaux** correspondent octet pour octet aux blobs Git de `590b9a6`. Le catalogue `app/notebook_catalog.json` est lui aussi identique. Le DM original garde le SHA `6fd62ebefdb8e8cd1a7673edf1dbfca2b26a02745dd2ab98a6183f9ea46122f1` |
| Manifestes et contextes historiques | Ajout d'une seule séance, soit **36** au total. Chacune des 35 anciennes séances et les autres champs du manifeste sont identiques ; leurs contextes régénérés restent exactement égaux aux contextes Colab enregistrés, avec migration idempotente |
| Copie physique | **45 cellules**, mêmes types, IDs, ordre et champs hors source. Les **43 cellules après titre/introduction** sont strictement identiques au DM, comprenant tous les énoncés, réponses, code, essais, explications et données |
| Différences permises | Seulement le titre/contexte initial, le paragraphe des conditions d'accompagnement et les métadonnées propres au tutorat/Colab. Métadonnées racines hors tutorat et `colab.aiContexts`, dont `tal` et le contrat de correction, identiques |
| Fiches par question | Exactement **Q1 à Q18**, chacune non vide, aucune bibliothèque autorisée ou fournie. Les 18 listes `available_concepts` sont exactement égales au JSON de la matrice acceptée, sans union des permissions |
| Double contexte | Contexte complet de **4 256 caractères**, inférieur au budget interne de 4 400, identique dans Colab et le commentaire HTML de première cellule sous le titre visible ; régénération idempotente |
| Contrôle original | Séance `DM_INTERMEDIAIRE_S1` inchangée, mode `controle`, refus d'assistance conservé. Le nouveau profil n'est pas attachable à cet original par le validateur |
| Séparation des modes | La nouvelle séance d'aide est `td`, semestre 1, profil explicite `devoir_S1_tuteur`. La copie conserve le contrat de notation `dm-intermediaire-s1`, avec reçu privé ; elle ne crée pas un évaluateur ni un retour public |
| Test d'inventaire | L'égalité historique entre catalogue et séances de tutorat est adaptée au **seul chemin exact** de cette édition supplémentaire, avec assertions sur son ID/profil. Les autres assertions et fixtures historiques restent intactes |
| Limites de livraison | Catalogue, routes, correcteurs, schéma de persistance et distribution automatique des **34 sujets actifs** inchangés. La copie est une source ouvrable directement dans Colab, sans nouvelle distribution automatique par défaut |

Le code réserve explicitement le profil à l'ID, au nom de fichier, au semestre 1 et au mode TD attendus ; l'absence de profil sur cette édition échoue au lieu de revenir au comportement TD générique. Les doublons, listes partielles, fiches vides et bibliothèques sont refusés. La branche contrôle demeure distincte. Ces garde-fous techniques ne constituent pas un contrôle du comportement interne de Gemini.

Le contexte demande identification de la question, diagnostic et révision de **toutes** ses notions et sous-notions, prérequis et dépendances compris, une question par tour puis attente, explication conceptuelle sur d'autres données en cas d'hésitation, suivi des notions vérifiées/restantes et retour à un essai autonome. Il interdit code, pseudocode, résultat, correctif ou solution à recopier, agrégation des fiches et modification/exécution des cellules. Les deux avis spécialisés confirment séparément ces propriétés à partir des 18 questions.

Le constat pédagogique `TAL-PED-DST-001` concernant une formulation conditionnelle de validation a été corrigé puis revu : « Vérifiez la compréhension conceptuelle, sans valider une réponse du devoir ni une note. » La gouvernance confirme cette phrase dans le contexte final synchronisé. Le constat est clos sur cette version ; aucune validation de réponse du devoir n'est autorisée par une prétendue preuve.

## Version auditée et tests

Empreintes recalculées et concordantes avec les avis finaux :

| Objet | SHA-256 |
|---|---|
| Notebook `devoir_S1_tuteur.ipynb` | `e67df7e49ea623346cc50964002ef0473359649b3fa3b13af7353ae9a80ac25b` |
| Contexte canonique final | `1ce982aa091861a5550f50721f30e68d0eb0ae5b6f4c85cb7ff29b9752d3306b` |
| `app/tutor_metadata.py` | `2a0230d00ebf2bb5d96a9c5334e10f9ca65ae62c0ee035a97392c151ff1b138e` |
| `docs/pedagogy/tutor_sessions.json` | `85a44caff0a98f8e7fe6bb23d6a4a328e869e3dd84f8e1c4464c67d4e5ac7c28` |
| `tests/test_devoir_s1_tuteur.py` | `5314fe79de81f0a15903434f60f711741627d3cae5637915e08a5fdfcf3890a5` |
| `tests/test_notebook_migration_integrity.py` | `8eb38b2f7f411cd7407916cebc585f7ba406783c6e9e16616cdac7411286e8fa` |

Le journal final `/tmp/devoir-s1-tuteur-tests-verified.log`, postérieur à la dernière clarification du contexte, se termine par **308 tests, OK**. L'auditeur a exécuté **36 tests ciblés** sur ce même contexte final, dont les six nouveaux cas de séparation et de validation ; ils sont inclus dans les 308, sans total artificiel de 344 tests distincts. Le journal des contextes confirme 36 profils OK, dont la nouvelle édition à 4 256 caractères. La synthèse rapporte aussi validation nbformat, compilation et vérification des 34 sujets actifs réussies ; ces commandes n'ont pas été relancées par la gouvernance.

Le POST indépendant du Code-Auditor a résolu la copie vers le correcteur DM en mode contrôle : HTTP 200, reçu sans score ni détails publics, copie exacte, rapport et CSV dans un répertoire synthétique temporaire supprimé ensuite. Il n'implique aucune nouvelle modalité académique de remise. Les tests et cette intégration ne remplacent ni les lectures pédagogique et éditoriale ni un essai réel de Gemini.

## Réserves et handoff

La **note héritée** est une réserve d'organisation non bloquante, explicitement conservée par les deux revues. Les conditions annoncent une révision distincte alors que le paragraphe Évaluation repris du DM mentionne toujours la confirmation enseignante de la note. Cette livraison conserve le barème et les métadonnées à la demande ; elle ne permet d'inventer ni une nouvelle remise notée ni une interdiction de soumettre la copie. Aucune clarification supplémentaire n'est une condition de conformité de l'adaptation technique et pédagogique examinée.

La division et les priorités Q1–Q2, l'ordre d'insertion Q9/Q13 et la sûreté de l'indice/conditions multiples Q14 sont expressément à introduire ou reprendre dans cette révision. Leur présence dans un prompt ne prouve pas qu'ils ont été enseignés antérieurement ni effectivement acquis. Les réserves de préparation du DM original demeurent donc ouvertes ; les défauts préexistants du moteur DM et les autres constats S1 ne sont pas corrigés par cette copie.

**Non testé :** comportement réel de Gemini dans Colab, résistance à l'insistance sur plusieurs tours, attente effective, suivi des acquis, absence de divulgation en pratique, durée de révision et maîtrise de vrais étudiants. Les scénarios documentaires et tests du générateur ne sont pas des conversations observées. Aucun verrou technique garantissant le LLM, déploiement, CI distante ou production n'est certifié.

**Handoff :** mission et branche indiquées en tête ; seul fichier écrit par la gouvernance : `reports/governance/devoir-s1-tuteur.md`. Évolution examinée : nouveau support et protocole LLM plus validation/génération et tests associés, sans changement du contrat de notation. Risques contrôlés : activation involontaire d'aide en contrôle, perte de questions, permission agrégée, fiche incomplète, confusion entre concept et solution, confusion entre aide LLM et note. Les critères du cadrage sont remplis pour les éléments livrés, avec limites observables explicitement déclarées.

**Verdict transmis : `CONFORME` dans ce périmètre.** L'intégration étant assurée par un producteur du changement, elle relève de **MAINTAINER_REVIEW**, sans `READY_TO_MERGE` auto-attribué. Préserver les empreintes et les preuves dans la livraison ; ne pas y ajouter implicitement les anciens rapports S1 locaux. Toute modification ultérieure de portée, des permissions ou du contrat appelle les revues correspondantes. Fusion et production restent sous décision du mainteneur.
