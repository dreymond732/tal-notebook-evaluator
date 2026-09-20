# TD2 S1 — Chaînes et séquences

## État, autorisation et périmètre

Source comparée : `Notebooks TD/S1/TD2_S1_python_texte.ipynb`, base `ad28d093cd807729aaefa30aa8261f8e0d6947ca`. Cette fiche et sa matrice précèdent l'adaptation du support.

**Constat.** Les sept exercices couvrent nettoyage, transformation, indexation, découpage, reconstruction, traitement de trois chaînes et interprétation. Ils offrent peu d'entraînement et pas de budget de séance. Le correcteur demande `for` en Q6, alors que les boucles sont introduites au TD4. Q7 est accepté par simple présence du marqueur, sans preuve d'observation ni analyse de l'argumentation.

**Décision enseignante.** Dans l'échange de cadrage puis « passe au TD2 du S1 », l'enseignant autorise la progression des TD, le renforcement des exercices et le tutorat dans les seules métadonnées. Au S1, le tuteur ne produit jamais de code ; demande de solution et énoncé recopié déclenchent un questionnement adaptatif. Une difficulté persistante appelle un bref cours avec exemple en langage naturel, puis une nouvelle question.

**Hypothèse de conception.** La séance est prévue pour deux heures et suit TD1 ; les durées ci-dessous sont des estimations à éprouver par le parcours de l’Étudiant modèle, puis en classe. Aucun élément existant n'est supprimé, déplacé ou rendu optionnel. Les trois chaînes de Q6 restent obligatoires. Les exemples de code préparés par l'enseignant sont autorisés, distincts des tâches et courts ; leur présence ne lève pas l'interdiction de code pour le tuteur.

Périmètre : chaînes Python, listes issues du découpage et liste littérale minimale. Aucun import, boucle, compréhension, définition de fonction, branchement conditionnel, dictionnaire ou ensemble. La manipulation générale des collections appartient au TD3 ; les boucles au TD4. Aucune bibliothèque nouvelle n'est nécessaire.

## Matrice source → cible, avant conception

Tous les groupes ci-dessous sont **obligatoires**. Le niveau d'autonomie progresse de l'observation d'un exemple distinct à la formulation personnelle d'une limite. Les sorties de référence restent dans cette fiche destinée aux concepteurs ; elles ne doivent pas devenir les solutions des cellules étudiantes ni le contexte du tuteur.

| Source et objectif conservé | Cible et activité étudiante | Production et autonomie | Statut | Durée |
|---|---|---|---|---:|
| Prise en main et rappel de chaîne | Réactiver variable, type, valeur, `len`, affectation et affichage depuis TD1 ; exécuter dans l'ordre | Diagnostic bref et identification ; pas de notion supposée maîtrisée sans observation | RENFORCÉ | 8 min |
| Q1 : retirer les espaces périphériques de `texte_brut` | Prédire une transformation sur un exemple distinct ; appliquer `strip` ; comparer deux longueurs ; expliquer les espaces internes conservés et la valeur source inchangée | `texte_propre`, puis deux longueurs ; explication en mots avant vérification | RENFORCÉ | 14 min |
| Q2 : minuscules et remplacement de « textes » par « corpus » | Observer deux méthodes ; réaliser deux étapes ; vérifier la présence/absence des sous-chaînes ; expliquer l'ordre retenu | `texte_transforme` ; deux booléens ; justification personnelle | RENFORCÉ | 16 min |
| Q3 : premier, dernier, tranche 0:4 de « tokenisation » | Prédire indices et borne exclue sur un autre mot ; conserver trois extractions ; effectuer une seconde tranche et vérifier la longueur source | `premier`, `dernier`, `debut`, `milieu` ; expliquer la borne exclue | RENFORCÉ | 17 min |
| Q4 : découper la phrase, afficher liste et troisième élément | Introduire la liste produite par `split` ; réactiver `type()` pour distinguer chaîne, liste et élément ; récupérer des éléments par index ; distinguer longueur de chaîne et nombre d’éléments | `tokens`, troisième et dernier éléments, nombre d'éléments | RENFORCÉ | 15 min |
| Q5 : recomposer avec le séparateur ` \| ` | Reconstituer la chaîne puis la découper selon ce séparateur ; tester l'égalité avec la liste initiale | `phrase_avec_barres`, `tokens_reconstruits` et comparaison | RENFORCÉ | 12 min |
| Q6 : nettoyer **les trois chaînes** de `exemples` dans une nouvelle liste | Accéder explicitement aux trois indices ; nettoyer chaque chaîne ; construire la liste résultat avec une liste littérale ; observer la liste source | `exemple_0`, `exemple_1`, `exemple_2`, `exemples_nettoyes` ; aucune boucle attendue | RENFORCÉ | 18 min |
| Q7 : tester `split` sur « L’analyse, c’est utile ! » et interpréter | Enregistrer le découpage observé ; repérer les éléments visuellement ou par les indices déjà étudiés ; distinguer séparation par espaces, ponctuation et unités linguistiques ; argumenter avec un fragment effectivement observé | `phrase_limite`, `tokens_limite`, `commentaire` ; synthèse autonome courte | RENFORCÉ | 14 min |
| Exécution et dépôt du notebook | Réexécuter dans l'ordre, conserver toutes les sorties et déposer dans le correcteur formatif | Auto-évaluation et questions encore ouvertes | RENFORCÉ | 6 min |
| **Total** | | | | **120 min** |

Aucune réduction de couverture n'appelle un arbitrage supplémentaire. Le retrait de l'exigence `for` du correcteur rétablit l'alignement avec le TD ; il ne retire pas une activité obligatoire du sujet source, qui n'imposait aucune boucle.

## Contrat des productions

**CHANGEMENT_DE_CONTRAT.** Les sept groupes principaux, leurs variables existantes, l'identifiant `td2-s1` et le total de **7 points** sont conservés. Les sous-marqueurs étendent le contrôle formatif à plusieurs manipulations par groupe. Les groupes valent chacun 1 point : Q1–Q6 attribuent 0,5 point à la production principale et 0,5 à la production complémentaire ; Q7 attribue 1 point à la trace de découpage exacte accompagnée d’une tentative de commentaire renseignée. L’absence d’une production supplémentaire est signalée dans le groupe concerné. Ne pas ajouter un point par sous-marqueur.

| Groupe | Marqueur principal et valeur de référence | Sous-marqueur obligatoire et valeur de référence |
|---|---|---|
| Q1 | `Résultat Q1 :` — `texte_propre` = `Le TAL transforme des textes.` | `Résultat Q1b :` — `len(texte_brut)`, `len(texte_propre)` = `35 29` |
| Q2 | `Résultat Q2 :` — `texte_transforme` = `le tal transforme des corpus.` | `Résultat Q2b :` — `"corpus" in texte_transforme`, `"textes" in texte_transforme` = `True False` |
| Q3 | `Résultat Q3 :` — `premier`, `dernier`, `debut` = `t n toke` | `Résultat Q3b :` — `milieu = mot[1:5]`, `len(mot)` = `oken 12` |
| Q4 | `Résultat Q4 :` — `tokens`, `tokens[2]` = `['La', 'traduction', 'automatique', 'aide', 'parfois'] automatique` | `Résultat Q4b :` — `len(tokens)`, `tokens[-1]` = `5 parfois` |
| Q5 | `Résultat Q5 :` — `phrase_avec_barres` = `La \| traduction \| automatique \| aide \| parfois` | `Résultat Q5b :` — `tokens_reconstruits`, `tokens_reconstruits == tokens` = liste Q4 puis `True` |
| Q6 | `Résultat Q6 :` — `exemples_nettoyes` = `['bonjour', 'tal', 'corpus français']` | `Résultat Q6b :` — `exemples` = `['  Bonjour  ', 'TAL', '  Corpus Français']` |
| Q7 | `Résultat Q7 :` — `commentaire`, phrase personnelle argumentée, sans texte de référence imposé | `Résultat Q7b :` — `tokens_limite` = `['L’analyse,', 'c’est', 'utile', '!']` |

La cellule d’identification restaure le commentaire attendu par le parseur existant ; cette remise en cohérence conserve les champs d’identité demandés et n’introduit aucune donnée étudiante réelle.

Données Q1, Q3, Q4 et Q6 conservées exactement. Q7 utilise la chaîne exacte du sujet historique ; l'apostrophe typographique fait partie de ces données. Les commentaires de prédiction et d'explication peuvent être saisis dans la cellule de réponse puis confrontés aux sorties : leur pertinence n'est pas certifiée automatiquement.

Le correcteur analyse le JSON, les sorties enregistrées et le code par examen statique ; il n'exécute jamais le code soumis. Il distingue production enregistrée, présence d'une opération attendue et validité pédagogique : une sortie peut être copiée ou ancienne. Il ignore les commentaires et les exemples enseignant pour établir qu'une opération étudiante a été écrite. Les variantes équivalentes d’indexation ou les transformations en plusieurs affectations restent acceptables. Une notion hors programme appelle un signalement pédagogique ; aucune pénalité générale supplémentaire ni extension du barème n’est introduite pour cela.

Q6 doit pouvoir réussir sans `for` : accès aux indices 0, 1 et 2, nettoyage de chaque valeur puis liste littérale. La seule présence d'une occurrence de `strip` ou `lower` dans une autre question ne démontre pas le traitement des trois chaînes.

Q7 exige le découpage enregistré et un commentaire non vide, différent d'un emplacement à compléter. Ni longueur minimale arbitraire ni mot-clé ne prouve une interprétation correcte. Le retour doit annoncer explicitement que l'interprétation nécessite une relecture humaine, même si les traces du groupe sont complètes. Le score est un repère formatif de productions observables, pas une certification sémantique.

## Tutoriel embarqué et critères d'acceptation

La fiche `TD2_S1` dans `tutor_sessions.json` reprend les sept groupes. Chaque ligne inclut les notions antérieures nécessaires et les notions introduites ici, sans anticiper les suivantes. Les sous-questions Q1b à Q7b appartiennent au groupe de même numéro. Les consignes sont générées par `app/tutor_metadata.py` uniquement dans `metadata.colab.aiContexts` et `metadata.tal_tutor`, sans instruction au LLM dans le Markdown.

La livraison exige : sept groupes et tous leurs renforcements, durée totale 120 minutes, notions explicitement introduites avant usage, aucune anticipation obligatoire de TD3/TD4, tutorat S1 sans code et sans bibliothèque, métadonnées non tronquées sous le budget du projet, notebook étudiant sans solution et sans sortie résiduelle, correcteur plafonné à 7, preuve de réussite par une solution modèle limitée au sujet et preuve de rejet de réponses absentes/erronées. Double revue spécialisée requise avant gouvernance ; la fusion reste au mainteneur.
