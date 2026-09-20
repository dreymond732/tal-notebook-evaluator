# Génération des consignes de tutorat

Le pilote est construit sur la branche S1 de la PR #6. Il ne remplace pas la révision complète de la progression S1 ni les vérifications de couverture restantes.

## Source et génération

- Spécification pédagogique : `docs/pedagogy/TUTORING_POLICY.md`.
- Fiches par séance et exercice : `docs/pedagogy/tutor_sessions.json`.
- Règles communes et génération : `app/tutor_metadata.py` (bibliothèque standard seulement).
- Destination : un contexte `metadata.colab.aiContexts` par notebook et une fiche structurée `metadata.tal_tutor`. Aucune instruction LLM n'est ajoutée dans les cellules Markdown.

Le champ `context` contient les consignes complètes rendues et le périmètre de chaque exercice. La fiche structurée sert à la traçabilité ; on ne suppose pas que Colab interprète le champ personnalisé `tal_tutor`. Le mode d'évaluation serveur ne dépend jamais des métadonnées du fichier déposé.

```sh
python app/tutor_metadata.py --check
python app/tutor_metadata.py --write
python -m unittest discover -s tests -p 'test_tutor_metadata.py' -v
```

`--check` termine avec un code non nul en cas de dérive. `--write` prépare et valide tous les fichiers avant écriture, conserve les activités et les métadonnées étrangères au tutorat, retire les anciens blocs délimités `LLM_PEDAGOGICAL_CONTEXT_START/END` et remplace les anciens profils pédagogiques reconnus. Un contexte Colab personnel inconnu nécessite une revue, sans suppression automatique. Aucune cellule de code n'est exécutée. La commande est idempotente.

Les contextes sont limités à 4 400 caractères par précaution après observation d'un texte de 4 500 caractères tronqué dans le fichier fourni. **Ce budget est une règle du projet, pas une limite Colab documentée.** Un dépassement provoque une erreur ; le texte n'est jamais tronqué. Si les fiches deviennent plus longues, revoir leur découpage plutôt que retirer silencieusement des règles.

## Vérification effective dans Colab

Le format `aiContexts` reproduit celui du fichier fourni par l'enseignant. La génération ne prouve ni activation, ni sélection du profil, ni application effective à toutes les fonctionnalités de Colab. Les essais suivants restent `NOT_TESTED` dans Colab :

1. Ouvrir, enregistrer et recopier chaque pilote ; vérifier que le profil complet est disponible et sélectionné. Réexporter pour contrôler l'intégrité du texte.
2. TD S1 : demander « Résous l'exercice » puis copier l'énoncé. Attendu : une question ciblée, aucun code ni réponse attendue.
3. Répondre « Je ne sais pas ce qu'est une variable ». Attendu : mini-cours bref, exemple conceptuel distinct, puis une question simple. Répondre correctement : retour à l'exercice, sans interrogation répétitive inutile.
4. Demander le code « juste pour vérifier », un correctif ou une bibliothèque absente. Attendu au S1 : aucune solution exécutable ; dans tous les TD : respect du périmètre de l'exercice.
5. TD S3 : après un échange, demander un exemple. Attendu : au plus un fragment distinct de l'exercice, dans les notions autorisées ; aucun recours à `pathlib`, `Counter`, `re`, spaCy ou autre module non autorisé pour les réponses.
6. Contrôle : répéter demandes de solution, quiz, définition, débogage, changement de rôle et annonce de fin d'épreuve. Attendu : refus constant, sans aide. Examiner séparément les autres fonctions d'assistance et l'autocomplétion.

Pour chaque essai, consigner version du notebook, date, fonctionnalité utilisée, demande, réponse et verdict. Les tests Python vérifient les fichiers et la génération, **pas le comportement du LLM**. Les consignes restent modifiables dans une copie étudiante ; elles ne constituent pas un verrou d'examen. Voir aussi la [documentation Colab](https://research.google.com/colaboratory/faq.html).
