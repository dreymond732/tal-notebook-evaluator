# TD4 — Handoffs des revues indépendantes

Mission `pedagogy/s1-td4-swinnen`, base `126cf63cbae085cf095a4488d547296a7ce7df02`, dépendante de la PR #31. Ce document consigne les verdicts transmis par les agents indépendants ; l'orchestrateur qui les archive est producteur de l'intégration, pas auteur des verdicts.

## TAL-Pedagogy-Reviewer : ACCEPT

Sous-agent `/root/pedagogy_td4`, en lecture seule. Verdict : **COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, après lecture exhaustive des trois sujets, 18 questions, cours, exemples, essais, vérifications, bilans et profils du tuteur.

La comparaison physique des sept activités historiques de `c81c386`, inchangées dans `126cf63`, confirme leur maintien : Q1→oneQ1, Q2→oneQ2, Q3→oneQ3, Q4→bisQ1+Q2, Q5→bisQ3, Q6→terQ4, Q7→terQ6. La matrice complète `docs/pedagogy/s1-td4-swinnen.md` distingue les activités historiques renforcées, les exercices authentiques de Swinnen et les ajouts du cours.

| Cahier | Preuves par question |
|---|---|
| one | Q1 for/append/upper, source/vide/initialisation ; Q2 seuil strict5/6 et ordre ; Q3 comparaison normalisée, graphie conservée, casse/accents/vide ; Q4 présence distincte des occurrences et cas vide ; Q5 partition exhaustive <6/≥6 et répétitions ; Q6 modulo/parité, nombres négatifs/zéro/vide/exhaustivité. |
| bis | Q1 range1/2/3arguments et pas ou condition ; Q2 parcours inverse, sens vide et négatifs ; Q3 état/condition/mise à jour, première rejetée, absence de mise à jour étudiée sans exécution ; Q4 compteur de tours distinct du terme ; Q5 rang/candidat/filtre sur cinquante multiples ; Q6 and/or, valeurs communes ajoutées une fois, bornes et aucun résultat retenu. |
| ter | Q1 compteur de caractère exact, casse et accents ; Q2 candidat initial et listes négatives, vide discuté ; Q3 fréquences conditionnelles, doublons/casse/vide ; Q4 les deux écritures get et if/else effectivement manipulées et comparées, somme égale à huit ; Q5 transformation par compréhension et boucle équivalente ; Q6 compréhension avec filtre strict puis transformation, reconstruction effective des mots_longs, seuil5/6/vide/doublons. |

Repères finaux communs : Q1 cellules4–9 ; Q2 10–15 ; Q3 16–21 ; Q4 22–27 ; Q5 28–33 ; Q6 34–39 ; bilan40 ; annexe41 ; restitution42. Les renvois erronés bisQ3/terQ6 ont été corrigés. Les scopes terQ4 (`len`) et bisQ6 (liste/append) ont été complétés et revérifiés dans les doubles contextes du tuteur.

Les prérequis ont été retrouvés dans TD1/TD2 et TD3-one/bis/ter ; les notions nouvelles sont expliquées avant usage. Aucun def, input ou import dans les exercices. Les huit références de Swinnen ont été authentifiées dans l'exemplaire fourni, pages imprimées31/35/44/47/58. Les annexes décodées reproduisent exactement la notice existante.

Limites du verdict : ne certifie ni la rédaction française, ni le comportement réel du tuteur dans Colab, ni la faisabilité en huit séances de deux heures. La validation technique est distincte.

## TAL-Editorial-Reviewer

Rapport indépendant avec preuves par question et empreintes : `reports/editorial/td4-swinnen.md`.

## TAL-Code-Auditor : ACCEPT

Sous-agent `/root/code_td4`, resté en lecture seule. Contrôles : trois sujets/wrappers, rubriques, chargeur `s1_expansion.py`, catalogue, contrat, routes, distribution et tests.

Deux anomalies de construction ont été signalées, corrigées par le producteur puis revérifiées :

- **TAL-AUD-001** : terQ4 exige désormais une condition reliée aux résultats en plus de `get` et `For`. `get/get` est refusé ; `get/if-else` et `if-else/get` restent acceptés.
- **TAL-AUD-002** : terQ2 refuse les appels `max`, `sorted` et `sort` liés aux résultats. Les parcours comparatifs initialisés au premier élément restent acceptés, y compris avec des listes négatives.

Les interdits sont une extension optionnelle des seules rubriques applicatives concernées ; les neuf rubriques précédentes sont inchangées et le comportement des rubriques sans interdits reste identique. Le chargeur n'exécute aucun code ni import de la copie. Les éléments sans lien avec la production demandée ne donnent pas crédit à une construction.

Preuves de l'auditeur : 32 tests du dépôt, 19 sondes synthétiques initiales et 7 sondes de correction ; tests des trois GET avec proxy `/universite/tal`, POST automatique avec fichier renommé, persistance copie/HTML/CSV sous chaque identifiant versionné et échec simulé de sauvegarde affiché sans faux succès. Les 12 empreintes ont été reconstituées depuis Git ; les neuf rubriques précédentes sont conservées. Trois nouveaux contrats à 6 questions / 6 points, ancien TD4 à 7 questions / 7 points maintenu. Vérification des sources distribuables : 46.

Limite explicitement maintenue : les traces et dépendances syntaxiques ne prouvent ni fraîcheur, ni auteur, ni toutes les propriétés sémantiques du programme. Colab et production ne sont pas vérifiés par ces contrôles.

## Étudiant-Modèle et QA locale

Sous-agent `/root/student_td4`, lecture des sujets et seuls acquis autorisés, sans correcteur, test, spécification d'évaluation ou infrastructure. Livraisons : `Corrigés modèles/TD/td4-swinnen/lecture.md` et trois copies non exécutées. La note contient 18 preuves avant résolution et 36 cellules d'essais complétées. L'auteur a repris les dernières métadonnées et cellules fournies depuis les sujets gelés, sans exécution ni soumission.

L'orchestrateur a ensuite exécuté des **copies temporaires** de ces références synthétiques, chaque cahier dans un dossier vide et un processus distinct, avec délai limite de 20 secondes pour éviter un blocage accidentel de `while`. Exemples, réponses et essais terminent sans erreur ; les sorties réellement capturées donnent 6/6 pour chacun des trois correcteurs. Les fichiers suivis restent sans sorties et compteurs d'exécution nuls ; l'orchestrateur n'a pas réécrit les références de l'auteur.

## Vérifications finales

Commande globale : `python -m pytest -q --disable-warnings --maxfail=2` dans l'environnement de QA. Résultat : **314 tests réussis, 7 ignorés, 2 283 sous-tests réussis**. Les sept tests optionnels ignorés concernent l'outil de nettoyage historique `git_filter_repo`, indisponible dans cet environnement ; aucun nouveau test n'est désactivé.

Autres preuves : schéma nbformat des six nouveaux fichiers sujets/références ; toutes sorties sources vides ; cellule finale canonique préservée ; inventaire des tuteurs complet ; `python app/tutor_metadata.py --check` réussi ; génération temporaire puis vérification exacte des 46 sujets actifs avec une URL factice sous `/universite/tal`, sans corrigé dans la distribution ; `git diff --check` propre. Les empreintes des neuf sujets précédents et du TD4 historique restent inchangées.

Ces preuves locales ne revendiquent aucun test de comportement réel du tuteur dans Colab, ni déploiement ou essai sur le serveur de production. Le rapport de gouvernance est distinct et l'intégration auto-produite reste **MAINTAINER_REVIEW**.
