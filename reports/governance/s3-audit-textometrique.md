# Audit de gouvernance — progression S3 d’audit textométrique

## Verdict et périmètre

**CONFORME pour présentation au mainteneur.** Ce verdict ne vaut ni autorisation de fusion ou de déploiement, ni `READY_TO_MERGE`. L’intégration impliquée dans la préparation du lot rend `MAINTAINER_REVIEW` ; la PR doit rester en brouillon pour la revue enseignante.

Branche : `pedagogy/s3-audit-textometrique`. Base : `7990234`, après fusion de la PR9. Les ressources ont été figées dans le commit `7b34850800a5310b42a00590fefac2c54d2a1395` ; les huit préparations visent ce commit et contrôlent les empreintes. Le lot comprend huit sujets TD0–TD7, leurs évaluateurs formatifs, les ressources Faguet/Gemini, la documentation, les profils du tuteur, les tests et l’ajout des ressources nécessaires au Dockerfile.

L’enseignant a demandé : « Passe à la mise en place de cette progression. Construit des TD étayés de plusieurs exemples. Ils ont 2h par TD. » La progression préalablement discutée remplace le projet bilingue terminal par un instrument d’audit quantitatif des analyses LLM. Le déplacement hors tronc commun des représentations vectorielles et activités bilingues était explicite dans cette proposition approuvée. Les prolongements correspondants sont annoncés comme non livrés, sans prétendre à une équivalence avec les nouvelles activités.

Sources normatives relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md`, rôles `TAL-Pedagogy-Reviewer` et `TAL-Governance-Auditor`.

## Rôles, séparation et relais

| Rôle / agent | Périmètre constaté et relais |
|---|---|
| TAL-Prof — `s3_prof` | Matrice préalable, spécification, manifeste du tuteur et README dans `docs/pedagogy/`. Aucun sujet ni correcteur produit. |
| TAL-Pedagogy-Designer — `s3_designer_a` | TD0–TD3, ressources pédagogiques, README S3 ; corrections demandées par la revue et régénération des profils. |
| TAL-Pedagogy-Designer — `s3_designer_b` | TD4–TD7 ; exemples, transfert, visualisations, reprise des fonctions et régénération des profils. |
| TAL-Code-Architect — `s3_architect` | Évaluateurs, moteur de traces, routes, tests, note technique, ressource Docker ; aucune auto-validation. |
| TAL-Code-Auditor — `s3_review_code` | Revue indépendante en lecture seule ; verdict final **ACCEPT**, 77 tests réussis et vérifications détaillées transmises en session. |
| TAL-Pedagogy-Reviewer — `s3_review_pedagogy` | Matrice validée avant conception, puis lecture indépendante des huit sujets et contrats ; verdict **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**. |
| TAL-Governance-Auditor — même agent `s3_review_pedagogy`, second mandat | Le parent a confié ce rôle après la revue, le plafond de fils empêchant un nouvel agent. Aucune production pédagogique ou technique n’a été effectuée par cet agent ; son écriture est limitée au présent rapport. La séparation producteur/réviseur demeure assurée. |
| Orchestrateur / intégration — parent | Branche, répartition, publication des données figées, collecte des preuves, vérifications d’environnement et préparation de la PR. Intégration impliquée : `MAINTAINER_REVIEW`. |

Les verdicts et preuves spécialisés sont des relais explicites de session, pas des revues GitHub présentées comme déjà publiées. Aucun Étudiant modèle n’a été mobilisé et aucune copie résolue ou exécutée n’est annoncée.

## Preuves examinées

| Exigence | Résultat et provenance |
|---|---|
| Branche dédiée | Observation propre : branche distincte de `main`, base et commit de ressources identifiés. Aucun merge ni déploiement réalisé par la Gouvernance. |
| Matrice préalable et décision | `S3_COVERAGE_MATRIX.md` lue et validée par le Reviewer avant autorisation de conception. La partie active conserve l’historique et distingue conservation, renforcement et déplacement approuvé hors tronc commun. |
| Couverture TD0–TD2 | Lecture propre : fichier UTF-8, chaînes, liste/ensemble, fréquences, fonctions, normalisation ; Doc, tokens, lemmes/POS/tag, phrases, displaCy, extrait personnel ; Counter, fonctions spécialisées/générale, exclusions, POS/top3, contrôle manuel de cinq annotations, WordCloud et barres conservés. |
| Nouvelle progression TD3–TD7 | Concordances/citations ; cooccurrences par phrase, fenêtres, union/somme ; marges, proportions et cas indéfinis ; dispersion, cartes de chaleur, matrice de cooccurrences et retour au texte ; audit des six lignes Gemini et trois citations avec cas nouveaux indépendants. |
| Charge et exemples | Huit budgets totalisant chacun 120 minutes. Sept exercices par TD, sauf six au TD1 ; 55 traces. Au moins quatre exemples commentés distincts dans chaque sujet. Synthèse finale TD7 ramenée à 200–300 mots et assemblage préparé progressivement. Durées prévisionnelles, non mesurées en classe. |
| Réemploi entre séances | Les exports JSON sauvegardent les données ; la copie/reprise du code des fonctions est explicitement demandée dans les nouvelles sessions. Le corpus et les objets préparatoires sont disponibles indépendamment d’un export précédent. Aucun JSON n’est présenté comme sauvegarde de fonctions. |
| Contrat scientifique | La conversation Gemini est séquentielle, pas trois expériences indépendantes. Les paramètres absents restent absents. Forme, lemme, expression et famille sont distingués ; les fenêtres conservent leurs indices ; union et somme ne sont pas assimilées. Dénominateur nul distinct de zéro. Une citation approchée n’est pas déclarée conforme. |
| Changement de contrat | Déclaré dans les spécifications et `docs/S3_AUDIT_EVALUATION.md` : huit évaluateurs `td0-s3` à `td7-s3`, traces JSON, un point par contrôle, maximum 6 au TD1 et 7 ailleurs, signature et tuple conservés. Les anciens marqueurs TD0 ne sont plus le contrat actif. Flux mixte avec deux verdicts spécialisés favorables. |
| Portée de l’autoévaluation | Lecture propre du moteur et des supports : JSON, AST et sorties déjà enregistrées ; aucune exécution du code soumis, aucun chargement spaCy serveur. Les contrôles linguistiques sont des invariants de structure/cohérence. Interprétations, figures et qualité scientifique demandent une lecture humaine. Une sortie plausible fabriquée ou périmée peut passer ; cette limite est documentée et testée. |
| Tuteur | Observation propre : `python app/tutor_metadata.py --check` réussit sur les 26 profils. Cellule Markdown dédiée en première position et métadonnées synchronisées. S3 : guidage immédiat, fragment distinct seulement après échange, pas de solution complète ni modification/exécution des cellules. Scopes finaux corrigés pour graphiques TD7, PhraseMatcher TD4 et tests/exceptions. |
| Non-régression hors lot | Comparaison propre à la base : sujets S1, contrôles, règles de gouvernance et workflows inchangés ; remédiations R0–R2 identiques octet pour octet. Parmi les anciens profils, seuls TD0–TD2 S3 ont changé ; les cinq autres TD S3 sont ajoutés. |
| Sources et positions | Code-Auditor : octets de Faguet et empreintes des ressources vérifiés. Préparations `read_bytes().decode("utf-8")` : CRLF conservés, positions Unicode dans la source, début inclus/fin exclue. Root : téléchargement du commit fixé et SHA réussis. Aucun nouveau nettoyage de la source ni provenance du modèle Gemini inventée. |
| Validation indépendante | Code-Auditor : dernière campagne complète **77/77 PASS**, après synchronisation finale, correction des types/alternatives et pins des préparations. Huit POST à partir des vrais sujets, identité fictive, proxy, copie exacte, HTML et CSV persistés ; sujets vierges à zéro. Tests marqueurs/types/erreurs/non-exécution/échappement et non-régression des contrôles réussis. Root confirme un second passage final de 77 tests. |
| Préparation technique | Root a testé un environnement Python 3.12 isolé : spaCy 3.8.7, modèle français 3.8.0, Matplotlib 3.9.2 et WordCloud 1.9.4. Un conflit initial de dépendances Typer a été corrigé par `typer==0.16.1` et `typer-slim==0.16.1` dans les sept préparations concernées. Imports et `pip check` réussis ; Faguet entièrement annoté et positions contrôlées. Il s’agit d’un essai d’environnement enseignant, pas d’une exécution de solution étudiante ni de Colab. |
| État des sujets | Observation propre : les huit sujets ont sorties vides et compteurs nuls ; aucune réponse résolue dans leurs cellules d’exercice. Code-Auditor et root : nbformat/AST conformes. `git diff --check` propre lors de la vérification finale. |

Les premiers échecs intermédiaires de synchronisation ne sont pas dissimulés : ils sont clos par la régénération des profils puis la campagne complète finale de 77 tests. Le défaut CRLF et le conflit Typer ont également donné lieu à des corrections vérifiées. La Gouvernance n’a ni réexécuté la suite complète ni soumis un notebook ; les résultats spécialisés restent attribués à leurs auteurs.

## Empreintes des sujets audités

| Sujet | SHA-256 |
|---|---|
| TD0_S3_diagnostic_texte.ipynb | `efd5f32918058f59a20047968665718bbb3e7f467eb79393fc7e0cc805e390cf` |
| TD1_S3_fondations_spacy.ipynb | `7c6b4148aa3456e92af4efe1818167092f420ac6e570a3084150f68bee2332cf` |
| TD2_S3_analyse_corpus.ipynb | `ac9a5ac9ea29a23b0ab2902896947c001b6f32151b62124c77be5aa7506854f8` |
| TD3_S3_concordances_citations.ipynb | `87db85e67827f78dfab0388bab8e570cc48152bc011c0cdc0c56acbe7dff41ab` |
| TD4_S3_cooccurrences.ipynb | `5259a44a78c02c8d7590a8098b315a396fad337099608ada1d000464dce6f9a7` |
| TD5_S3_associations.ipynb | `c130d926fe1a02dce7a3b714b8b532deec31801c88d9ef9727e914ce3ba63de4` |
| TD6_S3_visualisations.ipynb | `f0b2bd3df1d322da39dc4f4bddf44816843649b8ca3293fc6b07bcfa4ae3da24` |
| TD7_S3_audit_llm.ipynb | `66f179815dc81a4a748c1569b89a6bfcbca59b61b5bf00776136c34db613d6e1` |

## Limites et relais

- **Colab : `NOT_TESTED`** pour l’exécution intégrale des exercices et le comportement effectif des huit tuteurs. Les consignes ne constituent pas un verrou technique.
- **Classe : `NOT_TESTED`.** Deux heures sont un budget de conception ; le temps réel dépend des acquis et de la reprise des fonctions antérieures.
- **Docker : `NOT_TESTED`.** La copie des ressources est ajoutée, mais aucun build/démarrage du conteneur n’a été réalisé dans cette session. L’annotation spaCy locale ne constitue pas une preuve de déploiement.
- **Qualité scientifique : relecture humaine.** Les 55 traces ne valident pas automatiquement toutes les productions sur Faguet, les interprétations ou les figures. La réussite ne se mesure pas au nombre d’erreurs attribuées à Gemini.
- **Programme déplacé : non livré.** Les prolongements NER, représentations et bilingue ne sont pas annoncés comme nouveaux ateliers disponibles ; la matrice garde leur historique et la décision de périmètre.

Relais : conserver ce rapport, les deux verdicts spécialisés et les limites dans la PR vers `main`, puis présenter le lot en brouillon au mainteneur. Aucun veto de gouvernance restant ; **CONFORME**, avec intégration **MAINTAINER_REVIEW**.
