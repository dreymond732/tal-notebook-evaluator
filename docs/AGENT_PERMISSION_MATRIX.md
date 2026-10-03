# TAL — Matrice de permissions

Par défaut, tout droit absent vaut `FORBIDDEN`. `*` signifie « indispensable à la mission et déclaré dans le handoff ».

| Zone | Architecte | Auditeur code | Designer | Réviseur pédago. | Gouvernance | Intégration | Prof | Étudiant modèle | Réviseur éditorial |
|---|---|---|---|---|---|---|---|---| --- |
| `app/` | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY* | READ_ONLY | FORBIDDEN | READ_ONLY |
| `Notebooks TD/` | READ_ONLY* | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY limité | READ_ONLY |
| `Notebooks contrôles finaux/` | READ_ONLY* | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY limité | READ_ONLY |
| `Corrigés modèles/` | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE | READ_ONLY |
| `tests/` | WRITE | READ_ONLY | READ_ONLY* | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | FORBIDDEN | READ_ONLY |
| `.github/workflows/` | READ_ONLY* | READ_ONLY | FORBIDDEN | FORBIDDEN | FORBIDDEN | WRITE | FORBIDDEN | FORBIDDEN | FORBIDDEN |
| Dockerfile / Compose | WRITE | READ_ONLY | FORBIDDEN | FORBIDDEN | READ_ONLY | WRITE* | FORBIDDEN | FORBIDDEN | FORBIDDEN |
| Documentation technique | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | FORBIDDEN | READ_ONLY |
| `docs/pedagogy/` | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE | FORBIDDEN | READ_ONLY |
| Documentation pédagogique | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | FORBIDDEN | READ_ONLY |
| `reports/governance/` | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | FORBIDDEN | READ_ONLY |
| `reports/editorial/` | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | FORBIDDEN | WRITE |

L'Étudiant modèle lit uniquement le sujet et les ressources autorisées : jamais correcteurs, tests, corrigés existants, infrastructure ou identités réelles. Il écrit seulement dans `Corrigés modèles/`.

Les actifs de gouvernance (`AGENTS.md`, cette matrice, `docs/agents/` et les règles structurantes du contrat) évoluent seulement dans une mission `agents/` soumise à décision du mainteneur.

Le Réviseur éditorial (`TAL-Editorial-Reviewer`) ne modifie aucun support, contrat, profil du tuteur ou correcteur. Son droit WRITE se limite à ses rapports dans `reports/editorial/` ; il peut aussi rendre son verdict de PR. Les autres revues conservent leurs canaux de handoff ou de statut de PR.

Les missions explicitement autorisées de type `agents/` permettent de proposer les changements normatifs demandés, sous revue indépendante et décision de fusion du mainteneur. Cette exception de mission ne permet pas de réécrire les règles auditées dans une mission de contenu.
