# Gouvernance — présentation et ordre du parcours, 7 octobre 2026

## Verdict

**CONFORME**, pour le lot de présentation défini ci-dessous. Branche dédiée vérifiée : `pedagogy/notebook-presentation-order`, parent exact `1ee45813283cec79463a8acc4b6204f50cbafe74`. Le présent auditeur indépendant écrit uniquement ce rapport et n'a modifié aucun produit ni règle audités.

Le lot réorganise et harmonise les douze TD/révisions S3 (71 questions), renomme trois chemins en TD1.a/b/c et applique le placement titre + instructions cachées dans la même première cellule aux 35 sujets à profil tuteur. Hors S3, cette opération ne constitue pas une révision intégrale de présentation ou de contenu. Les règles pérennes sont propagées dans les consignes des agents ; leur application complète aux autres contenus reste distincte.

L'intégration ayant contribué aux produits, notamment à des corrections éditoriales ciblées et à l'assemblage, le statut de livraison est **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. Publication autorisée dans la continuité de la mission ; aucune fusion ni mise en production autorisée par le présent verdict.

## Autorisation des normes et séparation des rôles

La demande enseignante transmise dans le handoff est explicite : « Fais les ajustements pour remettre les TD dans l’ordre. reprendre et propager les règles de présentation. Les instructions cachées passent sous le titre pour ne pas se trouver dans une cellule seule que les étudiants pourraient malencontreusement supprimer. » Elle complète la demande de retirer minutages et descriptions de l'identification, d'éviter les répétitions de présentation Gemini et d'alléger la procédure générale d'autoévaluation.

Cette autorisation couvre le volet normatif de la mission, malgré le préfixe pédagogique de la branche. Les modifications de `AGENTS.md`, des fiches Designer/Editorial-Reviewer et de `TUTORING_POLICY.md` concrétisent ces préférences ; elles ne changent ni permissions d'écriture, ni indépendance des revues, ni critères de conservation pour contourner une non-conformité. Les données, contraintes de production, critères locaux, introductions et activités restent expressément protégés. Le double tuteur et le refus d'aide en contrôle restent requis.

TAL-Prof a établi la matrice `docs/pedagogy/presentation_order_2026.md`, validée indépendamment avant conception selon son historique de mission et le handoff. La comparaison prend les six copies retouchées par l'enseignant comme références de présentation et le parent exact comme référence technique. Les anciens R0/R1/R2 v1 ne sont pas réimportés. Designer et Architecte produisent ; réviseurs pédagogique, éditorial et technique restent distincts. Les retouches de l'intégration ont été relues avant clôture.

## Avis indépendants et constats clos

| Revue | Preuve et verdict | Portée exacte |
|---|---|---|
| Pédagogie | `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, retranscrit du handoff indépendant dans la matrice finale | 71 questions, données, exemples, essais, interprétations et productions conservés ; TD1.b facultatif ; activités sur Gemini maintenues |
| Éditorial | `ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE`, `reports/editorial/presentation-order-2026.md` | Lecture intégrale de 449 cellules S3 et contrôle de structure des 35 premières cellules ; normes examinées séparément |
| Étudiant-Modèle | `Corrigés modèles/TD/presentation-order-2026/lecture.md`, lecture des 71 questions sans blocage de présentation restant | Sujets et ressources autorisées seulement ; aucune réponse résolue ou exécutée, aucun correcteur consulté |
| Technique | `ACCEPT` de TAL-Code-Auditor, statut d'agent consulté directement et bilan technique | 43 tests ciblés, 35 snapshots exacts du parent, conservation et migration idempotente, distribution de 34 supports |

Les derniers signalements de lecture ont été traités : référence TD0 `mots.` remplacée par `rôle.` réellement présent, usage conditionnel de R0 explicité, derniers renvois de minutage et notices d'identification retirés. Le signalement d'une longueur incorrecte de « Été : lire. » a été retiré après contre-lecture, sans modification injustifiée du sujet.

**TAL-AUD-P01 est clos** : les comparaisons historiques des contrôles restent adossées aux anciennes empreintes, sans régénération ; la conservation courante est vérifiée séparément. Les modifications de tests ne valent pas preuve d'équivalence pédagogique : celle-ci est apportée par les avis de contenu.

## Contrôles propres de la gouvernance

Ont été directement vérifiés :

- Sources normatives, diff des règles, branche et parent Git ; cohérence avec l'autorisation de propager les règles.
- Matrice, rapport technique, rapport éditorial, note étudiante et états des agents disponibles. Le verdict pédagogique est une preuve de handoff retranscrite, pas une nouvelle lecture pédagogique exhaustive par cet auditeur.
- Lecture JSON des 35 sujets : première cellule commençant par H1, puis contexte complet caché dans la même cellule ; une seule occurrence du bloc géré ; copie complète présente dans les métadonnées Colab. Douze sources S3 effectivement disponibles.
- Recalcul des douze SHA-256 finaux, tous concordants avec la matrice et le rapport éditorial. Le verdict porte sur ces versions finales, et non les empreintes intermédiaires.
- Diff catalogue/routes/générateur : trois nouveaux chemins, intitulés et ordre du menu ajustés ; identifiants techniques et modules conservés ; aucune exécution de code étudiant introduite.
- Lecture du journal final `/tmp/tal-presentation-tests-final.log` : **302 tests, OK**. La gouvernance n'a pas elle-même réexécuté cette suite.
- `git diff --check` sans erreur. Aucun fichier original de l'archive enseignante ajouté au lot. Les adresses présentes dans les diffs examinés sont celles des ressources/documentations ou valeurs locales déjà transportées par les cellules ; aucune adresse électronique ajoutée. La source garde le mécanisme d'URL injectée, sans copie de l'URL de déploiement de l'enseignant. Ceci ne constitue pas un audit de secrets de tout l'historique.

## Preuves techniques rapportées

Le Code-Auditor a vérifié les 35 snapshots bruts octet pour octet contre le parent Git et exécuté 43 tests ciblés. Ses contrôles couvrent IDs, métadonnées, AST, sources volontairement erronées des exercices de débogage, sorties et compteurs ; les permissions de notions et bibliothèques restent inchangées. Hors douze TD S3, l'inversion indépendante du seul déplacement H1 restitue le parent, avec une exception bornée : le libellé de prérequis TD1.a dans la configuration du contrôle concerné. Le helper de preuve n'appelle pas le générateur qu'il contrôle.

L'Architecte rapporte 72 tests ciblés initiaux. L'intégration rapporte la suite finale de 302 tests, la synchronisation de 35 profils et `check`, `render`, `verify` pour 34 distribuables avec une URL neutre. Ces nombres correspondent à des périmètres distincts et ne sont pas additionnés. Pas de nouvelle exécution des exercices spaCy : leurs AST sont conservés. Versions, barèmes, marqueurs et routes de correction demeurent stables. Les noms distribués doivent être régénérés au déploiement ; les copies antérieures restent identifiables par leurs métadonnées.

## Réserves explicites et limites

La lecture étudiante conserve deux réserves d'acquis antérieurs : lemme en TD0 Q7 et `is_alpha` en TD4 Q1. Elles ne sont pas démontrées comme des régressions de ce lot ; aucun avis ne certifie leur apprentissage effectif. Le commentaire canonique de restitution décrivant l'injection d'URL et le bloc fonctionnel de dépôt restent conservés : le rapport éditorial les distingue des notices Markdown répétitives retirées. Cette limite doit rester visible, sans prétendre que toute mention technique a disparu.

R0 demeure conditionnel et TD1.b facultatif ; aucune activité n'est annoncée déplacée vers un support non livré. Les critères d'autoévaluation et les échanges entre pairs restent présents, sans nouvelle promesse de relecture individuelle systématique. Le lot ne restaure pas exhaustivement les sources 2025 et ne revalide pas intégralement les contenus S1/S2 ou les contrôles. Comportement réel de Gemini/Colab, apprentissage, durée en classe et disponibilité réseau des ressources ne sont pas démontrés. Les résultats locaux ne valent pas CI distante ou validation Docker après publication ; celles-ci restent à observer séparément.
