# Nettoyage de présentation des sept TD S1

## Résultat et périmètre

Demande du 15 octobre 2026 : appliquer aux sept TD S1 le nettoyage discuté avec l'enseignant et proposer une PR. Branche : `pedagogy/s1-nettoyage-presentation`, référence avant modification : `590b9a6c78fc6b27f8985e060c6ea2325367f652`.

Les TD ne présentent plus de minutages ni de notices décrivant l'identification. Le premier TD explique la procédure générale d'autoévaluation et présente Gemini, son rôle et ses limites S1. Les TD suivants gardent les indications locales utiles à leurs exercices. Le travail demandé, les données et les critères d'interprétation sont conservés.

Cette livraison concerne la présentation des sept sujets TD. Les constats de l'audit S1 du 14 octobre sur les DM, contrôle final, moteurs de correction et modèles restent ouverts. Les rapports locaux de cet audit, préexistants à la présente mission, sont préservés dans le workspace et ne font pas partie de cette PR.

## Conservation vérifiée

Comparaison JSON intégrale avec les sept fichiers de la référence avant modification :

- 293 cellules, même ordre, mêmes IDs, types, métadonnées, sorties et compteurs d'exécution.
- 45 réponses, 44 exemples, 52 cellules d'essai/vérification/synthèse, deux préparations et sept restitutions conservés.
- 157 AST de cellules Python identiques. Les sources de code sont identiques, sauf retrait du seul commentaire de notice d'identification au TD2 ; ses affectations restent identiques.
- Les seules 45 cellules sources modifiées correspondent aux emplacements autorisés par la matrice : 44 cellules Markdown et le commentaire TD2.
- Première cellule complète, double contexte du tuteur, profils et métadonnées Colab inchangés dans chacun des sept TD.
- Restitutions finales canoniques intactes, y compris le commentaire d'injection d'adresse et `__TAL_PUBLIC_URL__`. Ce commentaire fourni est conservé conformément au cadrage ; le présent nettoyage ne modifie pas le mécanisme de distribution.
- Limites locales du retour automatique conservées : phrase personnelle TD1 Q6, commentaire TD2 Q7, analyse linguistique TD7 Q7. Les onze essais après fonction restent placés après la réponse correspondante.

Aucun code étudiant, exemple de notebook ou corrigé n'a été exécuté pour établir ces preuves. Les comparaisons portent sur JSON, code source et AST ; les tests utilisent les fixtures inertes existantes.

## Tests et adaptation du contrôle historique

Le test historique `test_outside_s3_td_only_title_moves_no_field_or_prose_changes` imposait une prose S1 identique au parent du lot S3. Après le nettoyage demandé, il échoue sur les sept TD S1 uniquement. Son périmètre strict est donc adapté aux sujets non révisés et son nom devient `test_unrevised_subjects_only_move_title_without_other_changes`.

L'exception comprend exactement les sept chemins déjà recensés dans `S1_RENAMED_SUBJECTS`, en plus des douze TD S3 précédemment révisés. L'égalité complète reste exigée sur les seize autres sujets. Le contrôle global des 35 titres/contextes/cellules/AST reste actif, ainsi que les tests de conservation des 45 réponses S1. Les fixtures historiques, le code applicatif et les règles normatives ne changent pas. L'adaptation a été examinée indépendamment par le Code-Auditor.

Commandes exécutées depuis la racine du dépôt, avec Python 3.12 et les dépendances de `.venv` :

```bash
export PATH="$PWD/.venv/bin:$PATH"
TMPDIR=/var/tmp/tal-cloud-tests python -m unittest discover -s tests -v
python -m compileall -q app tests
python app/tutor_metadata.py --check
python app/prepare_student_notebooks.py check
export TAL_PUBLIC_URL=https://example.test/universite/tal
python app/prepare_student_notebooks.py render --output-dir dist/s1-cleanup
python app/prepare_student_notebooks.py verify --output-dir dist/s1-cleanup
```

Résultats : **302 tests réussis**, sans échec ni test ignoré ; compilation réussie ; **35 profils** du tuteur synchronisés ; **34 sujets** vérifiés, générés et vérifiés après génération ; validation nbformat des sept TD réussie. Le dossier temporaire externe sert aux tests d'archivage, qui refusent les marqueurs Git du cloud présents sous `/tmp` et `/workspace`.

Le Code-Auditor a également réexécuté indépendamment **38 tests ciblés réussis** inclus dans ces 302 cas. Les fichiers générés sous `dist/` restent ignorés et ne sont pas ajoutés à la PR. Le build Docker et la CI distante ne sont pas déclarés réussis sur la seule base des vérifications locales.

## Workflow et preuves indépendantes

La [matrice du Prof](pedagogy/s1_presentation_cleanup_coverage.md) a reçu un ACCEPT indépendant **avant** toute édition des notebooks. Elle attribue les deux étapes de validation et leurs empreintes. Le Designer a ensuite effectué les seuls changements de présentation autorisés.

- [Revue pédagogique](s1_presentation_cleanup_pedagogical_review.md) : preuve par question et comparaison de couverture.
- [Revue éditoriale](../reports/editorial/s1-presentation-cleanup.md) : lecture de toutes les cellules et du français visible, distincte du verdict pédagogique.
- [Lecture à blanc Étudiant-Modèle](../Corrigés%20modèles/TD/s1-presentation-cleanup/lecture_etudiante.md) : sujets seuls, sans correcteurs ni corrigés.
- [Audit technique](s1_presentation_cleanup_technical_review.md) : invariants et adaptation du test historique.
- [Gouvernance](../reports/governance/s1-presentation-cleanup.md) : contrôle du workflow et du périmètre.

L'intégration archive les handoffs spécialisés avec leur attribution ; elle ne se substitue pas aux réviseurs indépendants. Les verdicts finaux sont :

| Revue | Verdict au périmètre du nettoyage |
|---|---|
| Pédagogique | ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE |
| Éditoriale | ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE |
| Technique | ACCEPT, y compris l'adaptation ciblée du test |
| Gouvernance | CONFORME |
| Intégration | MAINTAINER_REVIEW |

La lecture étudiante a été intégrée aux deux avis spécialisés. Le Code-Auditor a également relu la fidélité de cette synthèse et des archives avec un ACCEPT documentaire distinct de son avis sur les fichiers. L'intégration ayant produit le test et la synthèse, elle ne s'attribue pas READY_TO_MERGE. La fusion et la production restent sous décision du mainteneur.
