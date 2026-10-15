# S1 — Gouvernance du nettoyage de présentation

**CONFORME**, le 15 octobre 2026, pour les quatre changements de présentation autorisés dans les sept TD S1 et pour l'adaptation ciblée du test historique. Ce verdict permet de préparer la PR de ce lot sous **MAINTAINER_REVIEW**. Il ne lève pas le verdict global `NON_CONFORME` de l'audit S1 antérieur ni les constats concernant le DM, le contrôle final et les corrigés hors périmètre.

## Mission, autorisation et référence

Branche dédiée : `pedagogy/s1-nettoyage-presentation`. Référence source : `590b9a6c78fc6b27f8985e060c6ea2325367f652`. La cible auditée est la version de travail aux sept empreintes consignées ci-dessous et au test d'empreinte `4ccdb25263712e689d9bf7fab8dfdec5205f1718bb919ed99a6be118d2bd1f50`.

L'autorisation enseignante « ok. opère ce nettoyage et fait une PR » couvre les quatre points déjà explicités : retirer les minutages et les notices d'identification ; réunir la procédure générale d'autoévaluation au TD1 ; présenter Gemini une seule fois, au TD1. Elle suffit pour ces retraits de présentation, sans demander une nouvelle confirmation. Aucune suppression d'activité, de donnée, d'interprétation ou d'autonomie n'a été autorisée ni constatée.

Sources normatives relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/agents/WORKFLOW.md`, fiche Governance-Auditor. Les exigences de couverture, de rédaction, de double contexte tuteur et d'indépendance s'appliquent. Les règles structurantes et les correcteurs restent inchangés.

Le présent rôle, **TAL-Governance-Auditor**, est indépendant du Prof, du Designer, des réviseurs spécialisés et du producteur du test et de la synthèse. Il écrit uniquement ce rapport sous `reports/governance/`. Aucun changement de branche, commit, support, test, code ou règle n'est produit par ce rôle.

## Cadrage préalable et permissions

La [matrice du Prof](../../docs/pedagogy/s1_presentation_cleanup_coverage.md) désigne les 45 questions et les emplacements précis de présentation, classe les éléments conservés et les retraits autorisés et livre immédiatement leur cible : TD1 cellule 5 en base 1. Aucune activité n'est reportée vers un support futur.

La prévalidation ne repose pas sur une déclaration du seul producteur. Le [handoff pédagogique indépendant](../../docs/s1_presentation_cleanup_pedagogical_review.md) atteste sa lecture et son `ACCEPT DU CADRAGE` avant toute modification de notebook, puis son relais au Prof et à l'orchestrateur. Il identifie l'empreinte initiale `fbfcc1238b461d6cabe141f8404def7c32e23177e991d43cb87a9ae004ba72ab`, la correction de provenance sans changement de périmètre `fa9483e94fdd06992d745033e29110ae326e709dad9794b02692bb352c82dca4` et une relecture de l'attribution. La matrice finale attribue ces étapes. Sa consignation par le Prof ne vaut pas auto-validation.

Le réviseur a conservé une baseline indépendante avant conception ; la gouvernance a comparé les sept objets notebook et leurs empreintes aux blobs Git de `590b9a6` : identité confirmée. Les attestations de séquence, les références et cette baseline concordent. Les anciennes sources privées 2025 restent indisponibles pour une nouvelle lecture ; aucune restauration historique exhaustive n'est affirmée.

| Production ou revue | Rôle et permission | Preuve livrée |
|---|---|---|
| Cadrage source→cible | TAL-Prof, écriture `docs/pedagogy/` | Matrice préalable liée ci-dessus, avec attribution de prévalidation indépendante |
| Sept TD | TAL-Pedagogy-Designer, écriture `Notebooks TD/` | Diff limité aux cellules désignées par la matrice |
| Test et synthèse | TAL-Integration-Master, écriture `tests/` et documentation technique | Test adapté et [synthèse du lot](../../docs/s1_presentation_cleanup.md) |
| Couverture | TAL-Pedagogy-Reviewer, lecture seule des supports | [Revue pédagogique](../../docs/s1_presentation_cleanup_pedagogical_review.md), `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE — ACCEPT` sur chacun des sept TD |
| Français et destinataire | TAL-Editorial-Reviewer, écriture de son seul rapport | [Revue éditoriale](../editorial/s1-presentation-cleanup.md), `ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE`, 293 cellules et 45 questions |
| Lecture à blanc | TAL-Étudiant-Modèle, sujets seuls, écriture `Corrigés modèles/` | [Lecture étudiante](../../Corrigés%20modèles/TD/s1-presentation-cleanup/lecture_etudiante.md), 293 cellules et 45 questions, intégrée à la revue éditoriale finale |
| Invariants et test | TAL-Code-Auditor, lecture seule | [Revue technique](../../docs/s1_presentation_cleanup_technical_review.md), `ACCEPT`, 38 tests ciblés indépendants |
| Gouvernance | TAL-Governance-Auditor, écriture `reports/governance/` | Présent verdict indépendant |

L'intégration archive les handoffs pédagogique et technique avec leur attribution ; ces deux archives sont strictement identiques aux rapports temporaires de leurs auteurs lors de la vérification de gouvernance. Les rapports nécessaires sont livrés avec ce lot. Aucune preuve requise ne dépend d'un lien vers un fichier non livré de l'ancien audit S1.

## Vérifications indépendantes et résultat

La gouvernance a comparé les sept notebooks JSON actuels aux blobs de `590b9a6`, calculé leurs empreintes, lu le diff du test, vérifié son périmètre et confronté les rapports finaux. Aucun code de cellule étudiante, d'exemple ou de corrigé n'a été exécuté pour ce contrôle.

| Contrôle | Résultat corroboré |
|---|---|
| Périmètre suivi | Exactement sept notebooks sous `Notebooks TD/S1/` et `tests/test_presentation_order.py` modifiés ; aucun diff applicatif, correcteur, fixture historique ou actif normatif |
| Structure | 293 cellules conservées, mêmes IDs, ordre, types et tous champs hors source ; objets racines, métadonnées, sorties et compteurs d'exécution identiques |
| Activités | Sources exactes des 45 réponses, 44 exemples, 52 cellules de pratique/vérification/synthèse, deux préparations fournies et sept restitutions ; les revues vérifient aussi les activités mêlées aux énoncés et les synthèses modifiées |
| Code | 157 AST identiques ; 156 sources de code strictement identiques, seul le commentaire administratif prévu en TD2 cellule 4 base 1 est retiré. Les quatre affectations d'identification et le commentaire de rappel restent identiques |
| Sources modifiées | 45 cellules aux seuls indices de la matrice : 44 Markdown et le commentaire TD2. Aucun autre changement source détecté |
| Tuteur | Premières cellules et métadonnées intégralement identiques au parent ; contexte HTML complet concordant avec Colab. Une présentation visible de Gemini au TD1, aucune dans TD2–7 ; aucune permission cachée modifiée |
| Présentation et couverture | Plus de minutage ni notice détaillée d'identification ; procédure générale regroupée au TD1. Revues pédagogique et éditoriale positives et distinctes, avec preuves des 45 questions et critères locaux préservés |
| Restitution | Sept cellules finales exactement conservées, dont `__TAL_PUBLIC_URL__`, HTML et commentaire d'injection. La conservation de ce commentaire canonique est explicitement cadrée ; elle n'est pas une levée générale de la règle du destinataire étudiant |
| Test historique | Exception ajoutée par appartenance aux sept chemins exacts de `S1_RENAMED_SUBJECTS`, sans exclusion globale S1. Snapshot : 35 sujets − 12 TD S3 déjà exclus − 7 TD S1 revus = **16** sujets toujours soumis à l'égalité stricte. Assertions restantes et fixtures intactes |
| Protection complémentaire | Test global des 35 titres/contextes/structures/AST maintenu ; tests de conservation des 45 réponses S1 maintenus. L'adaptation de prose ne modifie pas le contrat d'évaluation |

Empreintes SHA-256 des cibles, concordantes dans les quatre lectures spécialisées :

| TD | SHA-256 |
|---|---|
| TD1 | `94abfa27d9b6a21395f60c91f0b8ca149cfcf20b5248799df0feec6f0aa338c3` |
| TD2 | `5d5e0ecc6650e07acf4a4b1695963802cbad3298df41053976d2d30d0636eed3` |
| TD3 | `822aeab68461784d9fa0e410ae18a37bb295486aecb46657e1bce0981c7944e8` |
| TD4 | `fc82a243ba0c09d1a7d1a89203885c78381ccf323a2a3a8c0d93d991b18a0e51` |
| TD5 | `2e2dbc49943a2070b8ad7c155c377a2e30fe8db0fa58e5fd09f70d9c8668b3cf` |
| TD6 | `01e00fff36a012f091097794d1d62b0f9255976fc61a8299366238b131b165d8` |
| TD7 | `b7ff9f64672c0886543a27a5079638f79f8eab4127553d2c1b2b7aaab4489f79` |

Le journal de la suite complète se termine par **302 tests, OK**, sans échec ni erreur. L'auditeur a réexécuté indépendamment 38 cas inclus dans ces 302, tous PASS ; il ne s'agit pas de 340 tests distincts. Le journal du tuteur comporte 35 profils OK. La synthèse et le handoff technique rapportent aussi compilation, nbformat des sept sujets et check/render/verify des 34 supports actifs réussis. Ces vérifications n'ont pas été relancées par la gouvernance ; les sorties générées restent ignorées sous `dist/`. Les lectures et verdicts spécialisés ne sont pas déduits de ces tests.

## Handoff, limites et décision

**Mission :** clôturer la gouvernance du nettoyage autorisé et remettre le lot à l'intégration pour PR. **Branche :** `pedagogy/s1-nettoyage-presentation`. **Fichier écrit par ce rôle :** uniquement `reports/governance/s1-presentation-cleanup.md`. **Contrat affecté :** présentation ; aucun `CHANGEMENT_DE_CONTRAT` notebook-correcteur constaté. Le changement du test est une adaptation ciblée à la prose autorisée, produite par un rôle habilité et auditée indépendamment.

Les critères d'acceptation du lot sont remplis : matrice réellement préalable, autorisation suffisante, activités et autonomie préservées, tuteur et restitution intacts, avis indépendants positifs, protections historiques restantes maintenues et tests pertinents réussis. Aucun constat de gouvernance bloquant nouveau sur ces quatre points.

Les risques restants concernent les éléments exclus : notation et contradictions du contrôle, faux positif du DM, modèles absents ou historiques non alignés. Le verdict global S1 antérieur reste ouvert sur ces points. Compréhension de vrais étudiants, durée en classe, comportement réel Colab/Gemini, Docker, CI distante et production ne sont pas certifiés par ce lot. Les rapports locaux de l'ancien audit sont préservés, sans être incorporés implicitement à cette PR.

L'intégration ayant produit le test et la synthèse, son statut doit rester **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE` auto-attribué. La fusion et la production restent sous décision du mainteneur. La demande de PR autorise sa préparation, son push et sa création ; aucune confirmation supplémentaire n'est nécessaire pour ces opérations dans ce périmètre.

La création externe de la PR est distincte de la conformité du nettoyage. Lors du contrôle runtime, les observations étaient actuelles et la politique réseau appliquée n'autorisait pas `api.github.com`. L'ajout de ce domaine dans un brouillon ne prouve pas son activation runtime. Cette restriction peut empêcher l'appel GitHub nécessaire à la création de PR ; elle ne constitue pas un défaut pédagogique ni une raison de transformer le présent verdict en `NON_CONFORME`. Ne déclarer la PR créée qu'après confirmation effective du service.

**Verdict remis : `CONFORME`, limité au nettoyage de présentation des sept TD S1 et au test adapté.** Poursuite vers intégration et PR sous `MAINTAINER_REVIEW`, sans clôturer les non-conformités S1 hors de ce lot.
