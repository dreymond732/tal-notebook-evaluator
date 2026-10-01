# S3 — contrat de consolidation des 15 évaluateurs v2

## Mission, autorisation et limites

Mission TAL-Prof du 1er octobre 2026, branche `code/s3-evaluation-complete-v2`, source `02f435dc770834b21e242592804d231e0836a4b7`. L’enseignant a validé les quatre lots : identité et contrats, validateurs, diagnostics et relecture, conformité quantitative TD1–TD2. **CHANGEMENT_DE_CONTRAT** soumis aux deux revues spécialisées. La matrice préalable est `s3_complete_v2_coverage.md` : 15 supports et 104 questions, sans suppression ni réduction. Les 2 h, corpus, exemples, interprétations, transferts, figures et barèmes sont conservés.

Ce document remplace, pour les 15 évaluateurs concernés, les anciennes descriptions qui limitaient TD1–TD2 à la simple cohérence structurelle. Il ne modifie pas les programmes des S1/S2, les contrats R0/R1/R2 déjà v2, ni les poids des contrôles. Il n’introduit aucune bibliothèque étudiante : Python, spaCy 3.8.7 et `fr_core_news_sm` 3.8.0 sont déjà prescrits. Les sorties sont comparées à des références produites par du code enseignant indépendant sur les textes exacts. Le serveur ne charge ni n’exécute le code soumis.

## Contrat transversal et distribution

1. Les IDs `td0-s3` à `td7-s3` et `controle-td1-s3` à `controle-td7-s3` sont inchangés ; leur `metadata.tal.version` passe à l’entier **2** dans le notebook et le catalogue. Chaque sujet contient exactement une identité et chaque réponse Q1…Qn attendue. TD1 possède six réponses ; les quatorze autres, sept.
2. L’identité est une cellule de code `metadata.tal = {"question": "identity", "role": "identification"}` ; elle comporte `nom`, `prenom`, `classe`, `numero_etudiant`, initialisés à des chaînes vides. Les valeurs doivent être des chaînes littérales non vides. Le numéro comporte 1 à 64 lettres ASCII, chiffres, tirets ou soulignements, conformément aux révisions v2. Il distingue les copies des homonymes ; aucun identifiant réel n’est fourni dans Git. Les commentaires, l’ordre des affectations et `prenom` ne peuvent devenir le nom par recherche de sous-chaîne.
3. Une réponse identifiée est une cellule de code `metadata.tal = {"question": "Qn", "role": "answer"}`. Elle reste reconnue après déplacement. Les exemples, préparations et cellules ajoutées ne fournissent pas de preuve pour une réponse. Une réponse présente mais vide est une absence de preuve, pas une mauvaise version. Une cellule requise absente, désidentifiée, dupliquée ou de rôle incompatible invalide le contrat.
4. Ancienne version, version absente/incohérente, contrat requis incomplet : message exact **« mauvaise version du notebook »**, avant correction et persistance, sur parcours automatique et route directe. Aucun rattrapage par titre, ancien marqueur ou analyse de toutes les cellules. Une identité vide dans un contrat valide reçoit une erreur d’identification explicite, sans dépôt accepté.
5. Les nouveaux résultats sont stockés par contrat v2 et numéro étudiant ; ne pas écraser les anciennes copies/notes, ni mélanger leurs anciens en-têtes CSV. Les contrôles restent privés et ne divulguent pas le détail de correction à l’étudiant.
6. Le tuteur reste dans les métadonnées et la première cellule Markdown : guidance contextualisée en TD, aucune assistance en contrôle. Aucun nouveau concept n’est nécessaire au tuteur pour les précisions présentes : indices et tranches, types, `is_space`/`is_stop` et parcours des tokens figurent déjà dans les périmètres concernés.
7. Les sources ne contiennent ni URL serveur privée ni cellule de dépôt. Le rendu depuis la configuration d’environnement ajoute la cellule HTML finale à chaque copie de `dist/`. Après fusion, régénérer et vérifier la distribution avant de redistribuer les **15 nouveaux supports v2**. Ne pas rebaptiser les anciennes copies en modifiant uniquement leur numéro de version.

## TD1 — conformité technique sur données fixes, critique conservée

Conserver toutes les traces JSON et leurs clés, les six exercices et leurs exemples. Ajouter au cadrage : les références fixes contrôlent la conformité au pipeline prescrit, **pas une vérité linguistique** ; les désaccords se commentent sans réécrire les prédictions du modèle. Une version différente de pipeline doit être signalée à l’enseignant, pas dissimulée par une modification des résultats.

| Question | Contrôle v2 et invariants | Travail humain conservé |
|---|---|---|
| Q1 | `annotations` égale, dans l’ordre, à tous les tokens non ponctuation du texte fourni : forme, lemme, POS, tag et offsets exacts. `tag` est une chaîne, éventuellement vide ; jamais `null`. Positions entières non booléennes, `0 <= debut < fin <= len(texte)`, tranche exacte et longueur cohérente. | Prédictions, deux écarts forme/lemme, utilité du tag, comparaison des cinq entrées à la référence manuelle distincte. |
| Q2 | Phrases et nombre de tokens de chaque phrase exacts pour le texte fourni et le pipeline fixé, dans l’ordre. Tous les tokens de chaque phrase sont comptés selon le Doc. | Comptage manuel, abréviation, citation interrogative et cas à contrôler dans Faguet. |
| Q3 | Listes complètes ordonnées, répétitions conservées : NOUN, VERB, puis NOUN/VERB/ADJ avec `not token.is_stop`. Comparaison aux annotations de référence indépendantes, sans accepter un sous-ensemble arbitraire. | Prédiction des retraits, choix thématique et perte d’information. |
| Q4 | Deux formes de tokens distincts, localisées dans la première phrase ; bornes strictes ; relation non vide. Le point reste celui des **repères**, pas une certification de la relation syntaxique. | Figure displaCy, verbe principal selon lecture, vérification des annotations `dep_` et `head.text`, interprétation et attribution de parole. Le modèle prescrit peut diverger de la lecture grammaticale : ne pas imposer que le mot choisi comme verbe principal soit à la fois ROOT et VERB. Ajouter une consigne demandant de distinguer lecture et annotation, sans dévoiler une réponse. |
| Q5 | `split`, `tokens`, `non_ponctuation` exacts sur `texte_td0`. **Convention à expliciter :** `tokens` compte tous les tokens, espaces compris ; `non_ponctuation` écarte à la fois `is_punct` et `is_space`. | Deux écarts commentés et comparaison à l’export TD0 disponible. |
| Q6 | Extrait libre de 2–4 phrases déclaré ; cinq annotations de tokens, ponctuation comprise, ordonnées et bornées. Le préfixe avant le premier token et les interstices ne doivent pas omettre de caractère non blanc : interdit de sauter au milieu du texte ou de sauter une ponctuation. Listes et question gardent leurs types. | Segmentation réelle, lemme/POS, exhaustivité des noms/verbes, cinq contrôles manuels, question et limite : relecture humaine. Sans pipeline exécuté sur cet extrait libre, les invariants ne certifient pas que chaque segment est effectivement un token spaCy. Cette limite demeure explicite. |

Le texte fixe de Q1 contient des prédictions grammaticales contre-intuitives avec le modèle prescrit. C’est précisément une occasion de contrôle linguistique ; les références ne sont pas corrigées à la main pour satisfaire une intuition. Q4 ne doit pas devenir impossible par une contrainte technique incohérente avec ces prédictions.

## TD2 — fréquences vérifiées et choix argumentés

Conserver les sept schémas JSON, corpus, exemples et transferts. Les références portent sur le microcorpus de `corpus_td2.txt`, identique à `exemples["microcorpus_td2"]`. Elles sont calculées indépendamment de la copie ; les fonctions restent à construire et à expliquer par l’étudiant.

| Question | Contrôle v2 et variantes acceptées | Relecture humaine |
|---|---|---|
| Q1 | Nombres exacts de caractères, phrases et tokens ; `annotations` contient les **dix premiers tokens non ponctuation**, forme/lemme/POS exacts et ordonnés, pas dix tokens quelconques. | Lecture effective du fichier et commentaire forme/lemme. |
| Q2 | Deux dictionnaires complets des lemmes NOUN et VERB hors ponctuation et stopwords, sans exclusion personnelle. Effectifs entiers stricts positifs ; `true` n’est jamais 1. L’ordre des clés ne compte pas. | Construction des fonctions, paramètre exclusions, essais, choix VERB/AUX et contrôle des sommes. |
| Q3 | Exclusions non vides en minuscules comprenant au moins un nom présent ; `avant` correspond aux noms de référence, `apres` retire exactement les exclusions sans modifier les autres effectifs. Résultat vide autorisé ici. Les choix d’exclusion restent libres. | Justification, question étudiée, conséquence des exclusions femme/homme dans Faguet. |
| Q4 | Distribution exacte des POS hors ponctuation et espaces ; trois catégories les plus fréquentes, effectifs décroissants ; ordre libre entre ex æquo. | Observation grammaticale et conclusion thématique impossible. |
| Q5 | `lemmes` : liste complète dans l’ordre de NOUN/VERB/ADJ hors stopwords et ponctuation. `controle` : cinq occurrences réellement présentes avec leur triplet forme/lemme/POS de référence ; choix et ordre libres. Vérifier les multiplicités pour ne pas accepter cinq copies d’une occurrence unique ; aucune nouvelle clé d’offset nécessaire. | Cinq jugements et justifications, désaccords avec le modèle sans réécriture de ses sorties, autre exclusion, distinctions forme/lemme/expression. La provenance par triplets ne distingue pas deux occurrences au triplet identique ; ne pas promettre davantage. |
| Q6 | `frequences` reprend exactement les noms filtrés de Q3, non vides, avec types stricts. Le validateur distingue absence de la trace Q3, schéma inutilisable et données incompatibles. | Deux figures, seed, axes, lisibilité, hypothèse et vérification par concordance. Présence de sorties image ne signifie pas que ces exigences sont satisfaites. |
| Q7 | Dictionnaires généraux/spécialisés conformes aux noms/verbes de référence sur le microcorpus sans exclusions ; `combine` somme exactement ces fréquences. Une incohérence Q2 ne doit pas invalider un calcul Q7 vérifiable indépendamment. | Fonction paramétrée, texte vide et exclusions vides, transfert aux 5 000 premiers caractères de Faguet, comparaison de généralité. |

Une dépendance déclarée n’est retenue que si elle est réellement nécessaire au validateur : les références fixes permettent souvent une vérification indépendante. Ne pas utiliser un dictionnaire mal typé comme base d’un calcul ultérieur sous prétexte qu’il est analysable en JSON.

## Autres corrections locales

- TD0 Q7 : conserver la liste attendue et la synthèse ; signaler `limites` vide comme production interprétative absente. Ne pas déduire sa qualité d’un nombre de mots ou d’un vocabulaire attendu ; les points techniques restent attachés aux critères techniques annoncés.
- TD3 Q3 : toutes les positions sont des entiers non booléens, dans les bornes exactes, et restituent le passage ; le slicing Python ne doit pas masquer une fin hors texte.
- TD3 Q7 : les preuves apportent au moins trois **occurrences absolues distinctes** du pivot retenu, indépendamment du choix des fenêtres. G1 correspond au mot entier intelligence ; G2 à aptitude/aptitudes, sans distinction de casse. Plusieurs fenêtres autour d’une occurrence ne créent pas plusieurs preuves. Conserver les fenêtres de contexte libres et les passages exacts, sans normaliser les CRLF.
- Contrôle TD1 Q1 : expliciter que le split porte sur le texte original et les fréquences sur les formes mises en minuscules ; ne pas confondre les deux conventions dans le feedback privé.
- TD4–TD7 et contrôles TD3–TD7 : ne pas réécrire les bons calculs attestés par l’audit ; conserver les références, tolérances, ordres significatifs et alternatives déjà admises. Les renforcements transversaux suffisent hors défaut démontré.

## Diagnostics, dépendances et barèmes

Les poids demeurent inchangés : TD1 6 points techniques, autres TD 7 ; contrôles `2,3,3,3,3,3,3`, total 20. Ne pas inventer des demi-points ni une nouvelle pondération sans décision supplémentaire de l’enseignant. Tous sont présentés comme **scores techniques provisoires**, avec portée et relecture requise ; jamais comme note globale/finale des compétences.

| État | Signification | Conséquence et retour |
|---|---|---|
| Conforme | Trace présente, typée et conforme au critère vérifié | Points techniques prévus, portée du contrôle rappelée |
| Preuve absente | Cellule attendue présente mais trace manquante/non exploitable | Aucun point attesté ; localiser la trace à produire/réenregistrer |
| Incorrect | Preuve vérifiable mais critère technique non satisfait | Aucun point pour ce critère ; indiquer la dimension concernée |
| Non vérifiable : dépendance Qn | Preuve aval existe mais une annotation amont indispensable manque ou son schéma est inutilisable | Points non attestés provisoirement, **à réexaminer** par l’enseignant ; ne pas présenter plusieurs erreurs de calcul indépendantes |

Dépendances techniques effectives à expliciter : contrôle TD1 Q3/Q4/Q5 utilisent l’annotation Q2 ; contrôle TD2 Q2/Q3/Q4/Q6 utilisent l’annotation Q1. Une annotation structurellement utilisable peut permettre un calcul aval cohérent même si un autre critère de sa question amont est erroné. Ne pas bloquer automatiquement tout aval parce que la note amont vaut zéro. À l’inverse, une valeur booléenne dans un effectif rend ce schéma impropre à son utilisation comme compte.

Le rapport indique le total de points attestés et les points non vérifiables à réexaminer, sans les additionner automatiquement ni les retirer deux fois. Les productions absentes non techniques sont signalées séparément ; aucune qualité argumentative n’est inférée de la longueur, du nombre de mots ou d’un mot-clé.

## Rapport enseignant et présence des productions

Regrouper par Q les traces, le code enregistré, les commentaires, les analyses Markdown associées et les indices de présence des sorties visuelles. Les cellules existantes « Votre analyse » des contrôles reçoivent seulement `metadata.tal_review = {"question": "Qn"}` : cette annotation de relecture ne les transforme ni en cellule `answer` ni en preuve quantitative. Elle permet de garder l’association après déplacement des cellules. Les analyses TD restent dans leurs cellules de réponse conformément aux consignes actuelles ; les cellules personnelles non identifiées ne doivent pas être attribuées arbitrairement à une question.

Les extraits peuvent être bornés pour garder le rapport lisible, à condition d’indiquer toute troncature et de renvoyer à la copie conservée pour la lecture complète. Mentionner les formats de figures présents et les sorties manquantes ; n’exécuter ni code ni HTML étudiant. Les contrôles ne montrent ces productions et diagnostics que dans le rapport privé enseignant. Présence, qualité, autonomie et authenticité sont quatre questions distinctes.

## Acceptation, preuves et relais

- Matrice de conservation validée avant réalisation ; revue pédagogique indépendante attestant les 104 activités, tuteurs et barèmes conservés.
- Références spaCy générées par code enseignant séparé, versions/provenance archivées ; positifs exacts et contre-exemples cohérents mais faux testés. Pas d’exécution de copie étudiante.
- Rejets v1/métadonnées manquantes/contrats incomplets testés en parcours automatique et direct, sans persistance ; identité littérale et homonymes de numéros différents testés.
- Bornes, booléens, ordre, doublons d’occurrence, cellules déplacées, extra-cellules et ex æquo testés selon le contrat.
- Absence de dépendance distinguée d’erreur de calcul ; note provisoire et relecture explicites dans HTML/CSV ; sécurité des rendus maintenue.
- Sources sans dépôt, distributions générées avec HTML final et versions v2 ; CI et double revue avant gouvernance/intégration. Le mainteneur décide de la fusion et du déploiement.

Fichiers autorisés au TAL-Prof : cette spécification et la matrice associée, uniquement dans `docs/pedagogy/`. Hypothèse : les références du modèle décrit ci-dessus sont reproductibles dans l’environnement enseignant épinglé ; aucune revendication de justesse linguistique universelle n’en découle. Risque résiduel : les sorties enregistrées peuvent être fabriquées ; le correcteur ne certifie ni exécution réelle, ni généralité des fonctions, ni interprétation. Verdict demandé après réalisation : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` et conformité technique du nouveau contrat, puis décision du mainteneur.
