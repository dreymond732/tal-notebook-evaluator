# TAL — Matrice de permissions

Par défaut, tout droit absent vaut `FORBIDDEN`. `*` signifie « indispensable à la mission et déclaré dans le handoff ».

| Zone | Architecte | Auditeur code | Designer | Réviseur pédago. | Gouvernance | Intégration | Prof | Étudiant modèle |
|---|---|---|---|---|---|---|---|---|
| `app/` | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY* | READ_ONLY | FORBIDDEN |
| `Notebooks TD/` | READ_ONLY* | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY limité |
| `Notebooks contrôles finaux/` | READ_ONLY* | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY limité |
| `Corrigés modèles/` | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE |
| `tests/` | WRITE | READ_ONLY | READ_ONLY* | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | FORBIDDEN |
| `.github/workflows/` | READ_ONLY* | READ_ONLY | FORBIDDEN | FORBIDDEN | FORBIDDEN | WRITE | FORBIDDEN | FORBIDDEN |
| Dockerfile / Compose | WRITE | READ_ONLY | FORBIDDEN | FORBIDDEN | READ_ONLY | WRITE* | FORBIDDEN | FORBIDDEN |
| Documentation technique | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | FORBIDDEN |
| `docs/pedagogy/` | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE | FORBIDDEN |
| Documentation pédagogique | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | FORBIDDEN |
| `reports/governance/` | READ_ONLY | READ_ONLY | READ_ONLY | READ_ONLY | WRITE | READ_ONLY | READ_ONLY | FORBIDDEN |

L'Étudiant modèle lit uniquement le sujet et les ressources autorisées : jamais correcteurs, tests, corrigés existants, infrastructure ou identités réelles. Il écrit seulement dans `Corrigés modèles/`.

Les actifs de gouvernance (`AGENTS.md`, cette matrice, `docs/agents/` et les règles structurantes du contrat) évoluent seulement dans une mission `agents/` soumise à décision du mainteneur.
