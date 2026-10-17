# TD4 S1 — Intégration du renforcement Swinnen

La mission `pedagogy/s1-td4-swinnen` poursuit le travail de la PR #31, sur sa révision `126cf63cbae085cf095a4488d547296a7ce7df02`. La PR du TD4 cible sa branche `pedagogy/s1-swinnen-renforcement` tant que cette dernière n'est pas fusionnée ; elle permet de relire uniquement l'extension TD4. Aucune fusion ou mise en production n'est comprise dans la mission.

## Contrat et couverture

| Cahier | Objet | Contrat |
|---|---|---|
| `TD4-one_S1_conditions_filtres.ipynb` | Conditions et filtres | `td4-one-s1`, v2, six questions, six points |
| `TD4-bis_S1_bornes_repetitions.ipynb` | Bornes de parcours, range et while | `td4-bis-s1`, v2, six questions, six points |
| `TD4-ter_S1_comptages_comprehensions.ipynb` | Compteurs, fréquences et compréhensions | `td4-ter-s1`, v2, six questions, six points |

La matrice préalable `docs/pedagogy/s1-td4-swinnen.md` couvre les sept exercices historiques, leurs cours, exemples, essais, interprétations et cas limites. Le sujet historique et le correcteur `td4-s1` restent disponibles, avec leurs sept questions et leur barème inchangés. Les neuf cahiers de la PR #31 et leurs rubriques ne sont pas remaniés. Une preuve indépendante, calculée depuis Git `126cf63`, fige leurs empreintes et celles du TD4 historique dans `tests/fixtures/td4_swinnen_source_baseline.json`.

Les trois ajouts réutilisent le moteur inerte `s1_expansion` et `check_saved_notebook`. Le code soumis et ses imports ne sont jamais exécutés par le serveur ; seules les sources et sorties enregistrées sont analysées. Les contraintes de construction correspondent aux méthodes effectivement demandées ; les alternatives autorisées dans l'énoncé demeurent valides. Le score reste un diagnostic technique provisoire, sans preuve de fraîcheur ou d'auteur ni validation automatique des explications.

Les bibliothèques autorisées restent vides. Les fonctions définies et la saisie interactive ne sont pas requises avant TD5. Les nouvelles opérations sont expliquées avant leur réemploi. Le tuteur S1 reste verbal, sans code, avec contexte complet synchronisé sous le titre et dans les métadonnées, et permissions distinctes par question.

## Sources et distribution

Les adaptations citent Gérard Swinnen, *Apprendre à programmer avec Python*, copyright 2000–2012, exemplaire fourni. Les numéros d'exercices et pages imprimées ont été vérifiés dans ce document. Chaque cahier comprend la notice, la préface et la licence intégrale, identiques au fichier déjà livré `docs/swinnen/NOTICE_PREFACE_LICENCE.txt`, dans une annexe repliable. Les adaptations restent CC BY-NC-SA 2.0 France ; la licence du serveur n'est pas modifiée.

Le catalogue, les routes et les manifestes sont complétés ; les modules de correction portent le suffixe `_S1`. La cellule canonique de restitution conserve `__TAL_PUBLIC_URL__` dans les sources. La distribution injecte l'URL uniquement dans les copies générées, et exclut les trois corrigés de référence. Le parcours et son diaporama présentent désormais quinze cahiers de TD hors DM et contrôle ; les quatre synthèses historiques sont distinguées.

## Limites et décision

La charge n'a pas été mesurée en classe ; quinze cahiers ne signifient pas quinze séances. L'enseignant conserve l'arbitrage sur leur répartition dans les huit séances initiales et le travail personnel. Les évaluations finales ne sont pas remaniées. Le comportement réel de Colab et le serveur de production ne sont pas vérifiés par des tests locaux.

L'orchestrateur assure les fonctions productrices d'intégration ; sa propre conclusion est donc `MAINTAINER_REVIEW`, après les revues indépendantes, et non `READY_TO_MERGE`.

## État de validation

Les revues indépendantes pédagogique, rédactionnelle et technique ont rendu leur accord. Handoffs, corrections et limites : `docs/td4_swinnen_reviews.md` et `reports/editorial/td4-swinnen.md`. Les trois références synthétiques ont été exécutées localement et obtiennent chacune 6/6 ; elles restent non exécutées dans Git. Suite globale : 314 tests et 2 283 sous-tests réussis, sept tests optionnels de nettoyage historique ignorés. Distribution générée et vérifiée pour 46 sujets actifs, sans corrigé. L'accord de gouvernance est consigné séparément dans `reports/governance/td4-swinnen.md`.
