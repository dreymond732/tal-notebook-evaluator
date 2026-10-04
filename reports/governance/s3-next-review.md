# Gouvernance — Révision des TD suivants du S3

## Verdict

**CONFORME**, le 3 octobre 2026, pour le lot TD1B et TD2–TD7 sur la branche `pedagogy/s3-next-review`, base `cdc52d08cc02c8880003d962d0631658f04392c1`.

Audit indépendant par TAL-Governance-Auditor (`next_governance`). Seul ce rapport a été écrit par cet auditeur ; aucun support, correcteur, test, manifeste ou règle n'a été modifié. Le verdict intervient après les trois avis spécialisés définitifs et la mise à jour finale de la matrice et de l'inventaire. L'intégration a participé à la production : son statut doit être **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. Le mainteneur décide de la fusion et du déploiement.

## Autorisation, périmètre et séparation des rôles

La demande enseignante est de revoir tous les TD suivants du S3 et de créer les correcteurs nécessaires, après fusion de la révision R1/TD1. Le lot couvre sept notebooks, **311 cellules et 46 questions**, leurs correcteurs et le README S3. Il applique aussi la demande de limiter la relecture individuelle sans réduire les activités linguistiques.

| Fonction | Production ou examen | Séparation vérifiée |
|---|---|---|
| TAL-Prof, `next_prof` | Matrice préalable, périmètres du tuteur, inventaire et bilan | Écrit dans `docs/pedagogy/`, recueille les verdicts indépendants avant le statut REVU |
| Trois Pedagogy-Designers | Deux notebooks TD2–TD7 par Designer | Production distincte des deux réviseurs de contenu |
| Intégration agissant aussi comme Designer | TD1B et README ; intégration des copies du tuteur | Participation à la production déclarée ; aucune auto-approbation finale |
| TAL-Code-Architect, `next_architect` | Application, correcteur TD1B, tests et documentation technique | Audité par `next_code_audit`, distinct de l'auteur |
| TAL-Pedagogy-Reviewer, `next_ped_review` | Cadrage avant conception puis couverture finale | Aucune modification de produit ; verdict autonome |
| TAL-Editorial-Reviewer, `next_editorial_review` | Lecture exhaustive et rapport éditorial | Écriture limitée à `reports/editorial/` |
| TAL-Étudiant-Modèle, `next_student_reader` | Lecture par question dans `Corrigés modèles/TD/s3-next-review/` | Aucun accès aux correcteurs, tests ou infrastructure ; aucune résolution, exécution ou soumission |
| TAL-Governance-Auditor | Permissions, contrats, preuves et relais | Écriture limitée à `reports/governance/` |

La branche dédiée et sa base ont été vérifiées directement. Aucun fichier normatif (`AGENTS.md`, matrice de permissions, contrat des évaluateurs, `docs/agents/`) n'est modifié. Aucun travail direct sur `main`, fusion ou déploiement n'est inclus.

**Incident de périmètre corrigé :** l'Architecte avait initialement changé le compteur de correcteurs dans `.github/workflows/ci.yml`, zone qui lui est en lecture seule. L'intégration déclare avoir restauré la version du parent puis appliqué elle-même, sous son rôle autorisé, l'unique changement nécessaire de 33 à 34. L'interdiction d'écriture a été rappelée à l'Architecte. Le diff final a été examiné : seul ce compteur change. Cette correction n'est pas une extension des permissions de l'Architecte ; aucune règle n'a été réécrite pour la permettre.

## Couverture pédagogique et destinataire

La matrice `docs/pedagogy/s3_next_review_coverage.md` identifie l'historique, le parent technique, les acquis, activités, productions et degrés d'autonomie des 46 questions. Le réviseur pédagogique confirme deux validations **avant conception** : les 42 questions TD2–TD7, puis les quatre activités TD1B avec le contrat v3 exact. Il a comparé la référence historique `2a367529963f66a186dff1658b5951d0dbc27642`, le parent technique et les activités spaCy historiques disponibles.

Il n'y a ni suppression substantielle ni déplacement vers une cible future. Les essais, transferts à Faguet, interprétations, figures, échanges entre pairs et exports restent demandés. Les options PMI et difflib restent optionnelles ; les autres tâches ne deviennent pas facultatives pour réduire artificiellement la durée. Aucune décision enseignante supplémentaire de réduction n'est donc requise.

Les avis finaux reçus et les preuves écrites concordent :

- `next_ped_review` : **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, lecture intégrale des 311 cellules, 46 questions et du README ; toutes les remarques levées.
- `next_editorial_review` : **ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, rapport `reports/editorial/s3-next-review.md`, lecture sans échantillonnage des cours, exemples, consignes, commentaires et bilans. Chaque passage visible s'adresse à l'étudiant. Le commentaire canonique de restitution reste le format explicitement demandé par l'enseignant.
- Lecture Étudiant-Modèle : les données, tâches et productions des 46 questions sont identifiables ; l'ambiguïté TD6 Q5 a été corrigée, puis relue. Les conditions de durée et de travail en binôme sont conservées comme réserves explicites.

L'inventaire final distingue les dix supports déjà revus selon cette méthode des 35 autres fichiers encore à reprendre. Les contrôles S3, TD0 et R0 ne reçoivent aucun verdict de contenu par ce lot. Les anciens bilans restent des états historiques, notamment le dépôt sans note de TD1B avant sa version 3.

## Contrats et sécurité

Le **CHANGEMENT_DE_CONTRAT TD1B v3** est déclaré dans la matrice et `docs/s3_next_correctors.md` : quatre vérifications techniques, traces JSON fournies à partir des résultats construits par l'étudiant, identifiants de réponse conservés, catalogue et routes cohérents, persistance dans `td1b-s3-v3`. Les anciennes copies v2 sont refusées avec « mauvaise version du notebook », sans correction ni enregistrement. Les anciens dépôts manuels restent intacts. Le nouveau serveur doit être déployé avant de distribuer TD1B v3.

Les 42 vérifications et barèmes TD2–TD7 restent inchangés ; les modifications de leurs modules portent sur la portée des retours. Le passage à une relecture facultative des TD ne change pas les contrôles sommatifs. Le score ne prétend noter ni la qualité linguistique, ni le rendu des figures, ni la validité générale du code ; les productions ouvertes disposent de critères d'autoévaluation.

L'auditeur code indépendant confirme **ACCEPT** : 136 tests ciblés réussis, 228 mutations de structures/types sans exception, tuple de cinq éléments et score borné. Il a recalculé indépendamment les références fixes spaCy 3.8.7 / modèle md 3.8.0, confirmé les similarités et Tesla/PER comme prédiction réelle, puis éprouvé les règles DATE. Les essais personnels restent soumis à des contrôles limités de structure, provenance et cohérence, explicitement annoncés.

Le défaut `TAL-AUD-001` de message de sauvegarde invisible à la première réponse a été levé : le rendu intermédiaire ne consomme plus les messages Flask. Le contre-test indépendant couvre deux routes et trois étapes de panne (CSV, notebook, rapport) ; la première réponse indique l'échec sans score ni faux succès. La persistance multi-fichiers demeure non transactionnelle, limite documentée préexistante.

Le nouveau correcteur, les fonctions communes, le contrat et les routes analysent uniquement le source et les sorties enregistrées. L'examen direct des appels n'y relève aucun `exec`/`eval` de code soumis ; les tests de l'auditeur vérifient la non-exécution et l'échappement HTML. Aucun code de réponse étudiante n'a été exécuté : les exécutions locales annoncées concernent les exemples fournis et les références enseignantes.

Les différences et nouveaux fichiers ont été examinés pour les URL et signatures de secrets courantes : seuls des hôtes publics de documentation et de ressources pédagogiques sont présents. Aucun secret ni adresse réelle de dépôt n'a été constaté. Les sept cellules finales conservent `__TAL_PUBLIC_URL__` ; les sources n'ont aucune sortie enregistrée. Ce contrôle ciblé n'est pas une garantie générale d'absence de toute vulnérabilité du dépôt.

## Preuves techniques et état exact relu

Vérifications effectuées directement par la gouvernance :

- Les sept textes de `tests/fixtures/s3_next_editorial_source_baseline.json` sont identiques, octet pour octet, aux blobs du parent. La référence n'a pas été reconstruite depuis les supports modifiés.
- Les sept empreintes ci-dessous correspondent à celles du rapport éditorial et de la matrice finale ; le total est bien de 311 cellules et 46 réponses.
- Chaque notebook possède un seul contexte Colab, copié intégralement dans le commentaire HTML initial ; son empreinte `tal_tutor.context_sha256` est exacte, et le profil est en mode TD. Les réviseurs ont aussi validé les permissions par exercice après correction des anticipations de notions.
- Les sorties des sept notebooks sont vides ; les placeholders de restitution sont présents ; `git diff --check` réussit.
- Le journal de la suite complète annonce **293 tests réussis**. Le résultat des exemples fourni par l'intégration contient **39 entrées PASS**. Ces exécutions ne sont pas attribuées à la gouvernance.

L'intégration rapporte séparément la validation nbformat/AST des sept supports, 35 profils de tutorat et la génération puis vérification de 34 notebooks distribués avec une URL neutre. La CI distante n'a pas encore été exécutée à l'écriture de ce rapport : son résultat doit être vérifié après publication, sans le confondre avec les preuves locales.

| Support | SHA-256 |
|---|---|
| TD1B | `7f740064aecb0d877d1e407429c4e26ded1ac6a7b89637049a8fd4a9594c6daa` |
| TD2 | `ff5fd1d037eb8c4e7c5b5495e0903d4ba2a8844678ececad28462e7c1c17f6f9` |
| TD3 | `1ec40c816a269a79c925eaab48b2d4db16c5b6a64c48640f44367a2d6ca77e95` |
| TD4 | `dc8d1b7240f1be8ec6a57f314bdf5cb50742487849e622d3e14f8d2f8e9aa2f7` |
| TD5 | `b9beee85f8e11b4c676c7507d649644f0d61a17b8ed1b7d33978e11f1412e74c` |
| TD6 | `828aabddf5410bda7dfea9c0bc7f7e0ee8e365e47c1a9bb17687a96a494d0f73` |
| TD7 | `bf1a04b5193d52bd1dcf9ecad40d512b816d31b1259906eddd8c13443ada384f` |

## Limites et relais

Les deux heures restent prévisionnelles ; TD7 est dense et suppose le réemploi des fonctions antérieures et la constitution progressive du dossier. La réalisation isolée des activités entre pairs n'est pas décrite. Le comportement réel du tuteur dans Colab n'a pas été éprouvé ; ses deux copies ne constituent pas une contrainte système garantie. Les traces ne prouvent ni leur authenticité, ni leur fraîcheur, ni la qualité d'une interprétation. Aucun appel à une API LLM de correction n'est introduit.

Les critères de conformité de ce lot sont satisfaits. Relais demandé : intégration sous **MAINTAINER_REVIEW**, publication d'une PR avec résultats de CI vérifiés, puis décision du mainteneur. Après fusion et déploiement du correcteur, régénérer les notebooks distribués depuis les sources ; ne pas diffuser l'ancien TD1B v2 au nouveau correcteur.
