# Navigation des correcteurs par semestre

## Parcours étudiant

L'accueil `/` présente trois choix : S1, S2 et S3. Chaque lien ouvre
`/semestre/S1`, `/semestre/S2` ou `/semestre/S3`, avec uniquement les correcteurs
actifs de ce semestre. Chaque formulaire, résultat de TD et reçu de contrôle
permet de revenir au semestre ou d'en changer.

Les URL historiques `/eval/<identifiant>` restent inchangées : les notebooks
et favoris continuent de mener directement au bon formulaire. Tous les liens
sont générés avec `url_for`, y compris derrière `/universite/tal/`.

## Inventaire vérifié

État de référence : `origin/main` au commit `8ee3954`, le 24 septembre 2026.
Les modules, les noms des supports et les semestres de
`docs/pedagogy/tutor_sessions.json` concordent pour les 32 correcteurs actifs.

| Semestre | Identifiants actifs | Total |
|---|---|---:|
| S1 | `td1-s1` à `td7-s1`, `Controletilt-s1` | 8 |
| S2 | `td2-S2` à `td6-S2`, `ControleDevoirMaisonS2` | 6 |
| S3 | `td0-s3` à `td7-s3`, `td-r0-s3` à `td-r2-s3`, `controle-td1-s3` à `controle-td7-s3` | 18 |

Deux modules historiques supplémentaires sont également identifiables comme S2,
mais ne sont pas actifs dans `EVALUATORS` : `app_correction_controle_S2` et
`app_correction_controle_Final_S2`. Ce changement de navigation ne les active pas.

Le semestre est déclaré explicitement dans `EVALUATOR_SEMESTERS`. Il ne dépend
ni de la casse des URL ni du mode pédagogique. L'application refuse de démarrer
si le classement est incomplet, contient une entrée inconnue ou un semestre
autre que S1, S2 et S3 : aucun nouveau correcteur ne peut être omis silencieusement.

Les badges utilisent `EVALUATOR_MODES`. Ainsi, les URL historiques `td2-S2`
et `td4-S2`, déjà classées comme contrôles, affichent « Contrôle — dépôt ».
Leurs règles de correction et de confidentialité restent identiques.

## Périmètre et acceptation

Évolution technique de navigation, sans changement de notebook, de barème,
de marqueur, de contrat `check_notebook` ni de persistance. Aucun code étudiant
n'est exécuté. Aucune dépendance ajoutée.

Critères : chaque correcteur apparaît une seule fois, dans son semestre ; les
32 accès directs fonctionnent ; les retours après GET/POST restent dans le bon
semestre ; le préfixe proxy est conservé ; les contrôles restent sans résultats
publics. Les tests existants S3 consultent désormais la liste `/semestre/S3`.

```bash
python -m unittest discover -s tests -v
```

Risques ciblés : oubli d'un classement futur, mélange des listes, lien cassé
depuis Colab, retour incorrect après dépôt et perte du préfixe du reverse proxy.
La validation au démarrage et les tests de navigation couvrent ces risques.
La vérification locale ne vaut pas déploiement sur le serveur de l'enseignant.
