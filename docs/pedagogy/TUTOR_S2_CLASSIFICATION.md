# Classement des supports S2 pour le tuteur

La révision complète S2 est spécifiée dans [la matrice de couverture](s2_complete_review_coverage.md) et [le contrat des productions](s2_v2_answer_contract.md). Les numéros historiques sont conservés ; TD2 et TD4 désignent des contrôles, non des séances formatives. Les identifiants de routage ne changent pas.

| Support révisé | Mode | Couverture conservée | Position |
|---|---|---|---|
| `Notebooks TD/S2/TD3_S2_algorithmique_structures.ipynb` | TD | Q1–Q30 | Deux séances de 2 h après S1 |
| `Notebooks TD/S2/TD5_S2_algorithmes_texte.ipynb` | TD | Q1–Q25 | Deux séances de 2 h après TD3 |
| `Notebooks TD/S2/TD6_S2_fichiers_ressources.ipynb` | TD | Q1–Q10 et génération du corpus | Une séance de 2 h après TD5 |
| `Notebooks contrôles finaux/S2/Controle_TD2_S2_algorithmique.ipynb` | Contrôle | Q1–Q13 | Après TD3 complet et ateliers préparatoires |
| `Notebooks contrôles finaux/S2/Controle_TD4_S2_ensembles.ipynb` | Contrôle | Q1–Q14 | Après TD5 et travail sur les ensembles |
| `Notebooks contrôles finaux/S2/Devoir_maison_S2_approfondissement.ipynb` | Contrôle | Q1–Q30 | Après TD5, y compris la transposition |
| `Notebooks contrôles finaux/S2/Controle_final_S2_algorithmique_fichiers.ipynb` | Contrôle inactif | Q1–Q18 et données | Après TD6, sous réserve d’un correcteur et barème détaillé conformes |

Les trois TD possèdent 65 profils d’exercice couvrant les notions et essais associés. Le tuteur guide par le dialogue ; en S2 un petit exemple distinct peut suivre l’échange, sans donner directement la solution. Les quatre contrôles, devoir compris, ne reçoivent aucun guidage, quiz, cours, exemple, correction ou validation de réponse par le tuteur. Le contexte est identique dans la première cellule Markdown et les métadonnées.

Pour TD3, l’import historique de `collections.Counter` est conservé comme préparation fournie, sans autoriser son utilisation dans les exercices. `math` n’est autorisé que pour Q22. TD5 et TD6 restent en Python natif ; TD6 sans regex et sans Counter. La restitution HTML fournie appartient à l’infrastructure et n’étend pas les bibliothèques autorisées pour résoudre les questions.

Les cellules d’essais et d’exemples ne comptent pas comme preuves notées. Les trois TD conservent toutes leurs activités obligatoires ; leur découpage explicite en cinq séances ne transfère pas de travail obligatoire hors classe. Les supports contiennent le numéro étudiant, les métadonnées v2 et une cellule finale de restitution dont l’URL est injectée au déploiement. Six supports S2 sont distribués, le final inactif reste exclu.

## Archives et limites

Les fichiers portant « corrigé » restent exclus et inchangés. `Notebooks contrôles finaux/DevoirS2.ipynb` est une solution enseignant mal nommée (identité CORRECTION) dont le JSON est tronqué ; elle reste exclue. Aucun TD1 absent n’est inventé. Le correcteur historique du final porte 11 réponses d’un autre sujet et ne permet pas de corriger ses 18 questions ; son existence ne justifie pas une activation.

Une instruction de tuteur embarquée n’est pas un contrôle d’accès au service Colab. La conformité vérifiable concerne sa présence, sa synchronisation et son périmètre ; le comportement du service reste à observer en situation. La validation indépendante relève des réviseurs pédagogique et technique.
