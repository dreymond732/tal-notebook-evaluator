# Gouvernance indépendante — rapports simplifiés

Date : 17 octobre 2026. Branche auditée : `integration/rapports-simplifies`, reprise de la PR #33. Référence intégrée : `main` à `992108a` ; résolution de conflit à `38596070bba39a8535ea8c3cf0c73886d60af27f`, puis fichiers de travail stabilisés et revus.

## Verdict

**CONFORME pour présentation au mainteneur.** Aucun blocage de gouvernance ouvert. Le producteur assure aussi l’intégration : statut **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. Ce verdict n’autorise ni fusion dans `main`, ni déploiement.

## Mandat, périmètre et séparation

L’enseignant demande de réconcilier les changements de deux sessions, de montrer une solution dans « Résultat attendu » et de limiter le bilan d’une réponse juste à un ✓ vert. La reprise conserve les corrections de restitution de la PR #33 et intègre les douze TD S1 des PR #31 et #32 déjà fusionnées par le mainteneur.

Le lot couvre 31 correcteurs formatifs S1/S3, soit 188 questions : 45 historiques S1, 72 nouvelles S1 et 71 S3. Les exemples historiques restent présents ; les 72 nouvelles solutions sont un catalogue applicatif autonome. Le template commun conserve le repli historique S2 sans revendiquer de nouveaux exemples complets pour ce semestre.

| Rôle | Production ou preuve indépendante |
| --- | --- |
| Parent, Code-Architect / Prof / Integration-Master | Template, raccordement, tests de présentation et de routes, matrice de restitution, documentation et préparation de l’intégration. Producteur, donc pas de validation indépendante de ses changements. |
| `solutions_s1`, Code-Architect | Catalogue des 72 solutions et tests associés, uniquement dans `app/` et `tests/`. |
| `review_feedback_code`, Code-Auditor | **ACCEPT** ; 29 tests et 94 sous-tests, comparaison des scores/statuts des douze copies avec et sans enrichissement. Aucun fichier produit audité modifié. |
| `review_feedback_pedagogy`, Pedagogy-Reviewer | **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** ; 72 énoncés et solutions comparés, exécution indépendante, matrice de restitution vérifiée. Aucun produit modifié. |
| `review_feedback_editorial`, Editorial-Reviewer | **ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE** ; template, 72 solutions et deux rendus textuels relus. Écriture limitée au [rapport éditorial](../editorial/rapports-simplifies.md). Les précisions demandées ont été écrites par le producteur. |
| `review_feedback_governance`, Governance-Auditor | Présent audit après réception des trois verdicts ; écriture limitée à ce fichier. Aucun autre rôle de production dans cette mission. |

Les permissions correspondent à `docs/AGENT_PERMISSION_MATRIX.md`. La branche est dédiée. Aucun producteur ne signe sa propre revue spécialisée et aucune règle normative n’est modifiée pour lever un constat.

## Couverture et sécurité

Sources normatives relues : `AGENTS.md`, matrice de permissions, fiche Governance-Auditor et `docs/agents/WORKFLOW.md`. La [matrice source → cible](../../docs/pedagogy/restitution_simplifiee.md) explicite la conservation des réponses retrouvées, solutions, distinctions d’état, points et limites du score.

La comparaison indépendante à `992108a` confirme un diff vide pour les sujets TD/contrôles, corrigés modèles, règles des agents, contrat normatif, routes, rubriques de l’expansion et CI. La mission ne réduit ni activité, ni objectif, ni autonomie ; aucune adaptation de notebook ni essai Étudiant-Modèle nouveau n’est revendiqué.

La résolution de `s1_revision.py` conserve ensemble l’enrichissement des réponses et `optional_review = evaluator in STRICT_S1`. Le catalogue nouveau est lu après notation : aucun changement de validateur ou de barème. Le bilan réussi masque seulement la répétition des diagnostics. Un état non vérifiable, une preuve absente ou un champ rédigé obligatoire manquant reste distinct d’une réussite. Les interprétations non notées restent à autoévaluer, avec productions complémentaires et portée du score accessibles dans des blocs repliables.

Le chemin serveur conserve une lecture AST/JSON inerte ; ni copie soumise ni solution affichée n’est exécutée. Les exécutions d’exemples concernent exclusivement les sources applicatives de confiance et les préparations du cours, localement dans les tests. Le catalogue n’exige aucune lecture des corrigés modèles au déploiement. Le code, les sorties et les solutions sont échappés par Jinja ; les sorties HTML/SVG soumises ne deviennent pas du HTML actif.

Les contrôles utilisent toujours les rapports enseignants et le reçu public distincts : le retour public ne reçoit ni résultats ni solutions, y compris cachés. Aucun contenu nouveau n’est raccordé au moteur partagé de notation des contrôles.

## Preuves et clôture des constats

- Exécution indépendante par Governance-Auditor : `python -m unittest discover -s tests` dans l’environnement du projet, **352 tests réussis, sans saut**, 15,147 s. Les tests d’affichage exécutés séparément donnent également **10/10**.
- `git diff --check` : **PASS** après correction par le producteur des espaces terminaux des aperçus HTML. Le générateur retire désormais ces espaces, puis les exemples ont été régénérés.
- Les tests de routes couvrent **62 dépôts HTTP** : 31 correcteurs via leurs deux entrées, avec préfixe proxy, extrait effectivement retrouvé, solution visible, échappement et persistance. Les tests de confidentialité des contrôles restent dans la suite complète.
- Les tests nouveaux vérifient **72 solutions**, douze copies synthétiques à **6/6**, les cas limites et l’évaluation avec `exec` interdit. Les audits spécialisés confirment l’absence de changement des scores.
- Intégration rapporte en complément : compilation, contrôle des tuteurs et des 46 sources, génération puis vérification de la distribution de 46 notebooks réussis. Ces contrôles ne constituent pas une validation de déploiement.
- Le handoff historique a été actualisé : il ne déclare plus les PR #31/#32 ouvertes ni les 72 solutions manquantes. Les rapports du 16 octobre restent des preuves historiques datées, bornées à leurs 116 exemples.

Les trois revues spécialisées sont favorables ; le rapport éditorial conserve ses preuves par question et empreintes. Aucun constat bloquant restant.

## Limites du verdict

Les 116 exemples antérieurs ne sont pas intégralement relus à nouveau dans cette reprise ; leurs revues antérieures restent identifiées. Les 27 exemples S3 nécessitant les modèles spaCy ne sont pas réexécutés ici. Le navigateur interactif, Colab, Docker local, la classe et la production ne sont pas validés par cet audit. La construction et le démarrage du conteneur relèvent de la CI de PR.

Les sorties enregistrées peuvent rester périmées et leur auteur n’est pas certifié. Aucun ancien rapport archivé n’est régénéré sans sa copie source. **CONFORME ; intégration : MAINTAINER_REVIEW.**
