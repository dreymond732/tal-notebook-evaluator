# S1 — Matrice de renforcement de la progression, contrat v2

## Autorisation, périmètre et moment de validation

L’enseignant demande le 1er octobre 2026 une PR traitant les limites constatées par la revue `s1_td_review_distribution.md`. Il précise que l’étayage existant ne doit subir aucune réduction : les TD ultérieurs doivent être enrichis. Cette matrice a été établie avant conception puis validée par l’orchestrateur le 1er octobre 2026 ; la revue indépendante de la réalisation demeure obligatoire.

Référence : branche PR19 au commit `322abf53`. Sept TD, 45 questions principales, sept traces complémentaires du TD2. Le contenu pédagogique du TD2 est conservé mot pour mot : seules l’identification, la notice du contrat, les métadonnées et la synchronisation du tuteur peuvent évoluer. Aucun objectif, jeu de données, exercice obligatoire, explication ou niveau d’autonomie n’est supprimé ni déplacé vers une activité optionnelle.

**CHANGEMENT_DE_CONTRAT** : version 2 pour les sept TD, identité avec numéro étudiant, preuves par cellule et valeurs vérifiées, traces complémentaires explicites. Les scores maximaux restent respectivement 6, 7, 6, 7, 6, 6 et 7, soit un point technique par question principale. Les essais ajoutés ne créent pas de points supplémentaires.

## Matrice source → cible

| Source obligatoire, données et production | Objectif/autonomie conservés | Renfort cible obligatoire | Charge cible | Statut |
|---|---|---|---|---|
| TD1 Q1, prix 0.12 et 125 mots, coût ; Q2 type de 14.5 | Affecter, calculer, distinguer valeur et type | Exemples distincts achat de cahiers et effectif ; prédiction puis variation d’une donnée | Q1 15 min, Q2 12 min | RENFORCÉ |
| TD1 Q3, comparaison et conjonction ; Q4 français/anglais et f-string | Construire soi-même les expressions et la phrase | Exemple de seuil de places ; exemple d’annonce avec interpolation ; courte vérification vrai/faux | Q3 18 min, Q4 17 min | RENFORCÉ |
| TD1 Q5, chaîne "80" puis +20 ; Q6 phrase personnelle, longueur et TAL | Conversion et réinvestissement autonome | Exemple de quantité saisie distincte ; contraste TAL/tal ; phrase enregistrée pour vérifier son résultat sans imposer son contenu | Q5 18 min, Q6 22 min | RENFORCÉ |
| TD2 Q1–Q7, toutes données et sorties Q/Qb, prédictions et interprétations | Nettoyer, transformer, indexer, découper, reconstruire, normaliser trois chaînes sans boucle, interpréter split | Aucun retrait ni réécriture des activités ; contrat d’identité et version cohérents | 8 + 106 + 6 = 120 min existantes | CONSERVÉ |
| TD3 Q1, liste outils, ajout puis retrait ; Q2 tuple français/italien/espagnol et justification | Choisir et manipuler liste/tuple | Exemple distinct append/pop et états intermédiaires ; exemple de tuple et type ; conserver justification | Q1 16 min, Q2 15 min | RENFORCÉ |
| TD3 Q3 lexique book/language/data puis corpus ; Q4 liste clé→valeur | Construire dictionnaire puis premier parcours | Dictionnaire sur couleurs distinctes ; introduction explicite `for`, déballage clé–valeur, indentation et `items()` avant Q4 ; exercice d’essai | Q3 18 min, Q4 25 min | RENFORCÉ |
| TD3 Q5 six formes dont répétitions ; Q6 deux vocabulaires fournis | Distinguer occurrences/types, intersection/différence | Exemple distinct d’ensembles, absence d’ordre ; comparaison des deux opérateurs ou méthodes ; transfert commenté | Q5 14 min, Q6 14 min | RENFORCÉ |
| TD4 Q1 majuscules ; Q2 longueur >5 ; Q3 a insensible à la casse | Construire par boucle, filtrer avec deux critères distincts | Exemples sur mots différents ; trace de variable d’accumulation ; prédictions de conservation/rejet | Q1 13 min, Q2 14 min, Q3 12 min | RENFORCÉ |
| TD4 Q4 pairs 0..10 ; Q5 multiples de7 <=70 | Bornes de range et progression/arrêt while | Présenter pas positif/négatif puis essai de parcours inverse ; prévoir première/dernière valeur, premier échec de condition ; exemple distinct de boucle bornée | Q4 15 min, Q5 20 min | RENFORCÉ |
| TD4 Q6 fréquence du texte fourni ; Q7 compréhension des longueurs >5 | Accumulation dictionnaire et réécriture concise | Montrer sur d’autres données les deux alternatives `.get` et `if/else` ; comparer boucle/compréhension sans retirer la boucle demandée | Q6 17 min, Q7 11 min | RENFORCÉ |
| TD5 Q1 longueur, Q2 normaliser, Q3 compter | Définition, paramètres, retour, composition | Exemple distinct de fonction ; cas vide ; distinguer affichage/retour ; introduire un paramètre à valeur par défaut dans un entraînement séparé (préparation du contrôle final) | Q1 16 min, Q2 14 min, Q3 16 min | RENFORCÉ |
| TD5 Q4 traduction mot connu/inconnu ; Q5 Language data ; Q6 résumé | Normalisation avant recherche, composition, structure de sortie | Clarifier normalisation du mot avant recherche ; tests connus majuscules/inconnus/vides ; contrat explicite des clés du résumé ; réemploi des paramètres plutôt que globales | Q4 18 min, Q5 20 min, Q6 18 min | RENFORCÉ |
| TD6 Q1 fichier fourni inchangé ; Q2 lignes ; Q3 split avec maxsplit | Lecture UTF-8 avec fermeture, découpage structuré | Exemples distincts `with`, `splitlines`, `split(';',1)` ; essai avec seconde occurrence de séparateur ; aucune modification du fichier pédagogique | Q1 15 min, Q2 13 min, Q3 17 min | RENFORCÉ |
| TD6 Q4 normaliser ; Q5 affiliations distinctes | Identités normalisées et dédoublonnage | Clarifier espaces de bord et intérieurs ; tests des trois graphies et d’espaces multiples ; exemple distinct dictionnaire d’ensembles, ordre non évalué | Q4 17 min, Q5 18 min | RENFORCÉ |
| TD6 Q6 CSV UTF-8, colonnes existantes et relecture | Écrire, relire, contrôler une transformation complète | Exemple distinct `csv.writer`, `writerow`, `newline`, en-tête ; définir séparateur interne des affiliations sans imposer tri ; contrôles nombre lignes/contenu | Q6 22 min | RENFORCÉ |
| TD7 Q1 search sans casse ; Q2 findall chiffres ; Q3 lettres accentuées et commentaire | Recherche/extraction puis interprétation | Exemples distincts, chaînes brutes, classes, `+`, accents ; cas non trouvé ; conserver comparaison split et limite | Q1 12 min, Q2 13 min, Q3 18 min | RENFORCÉ |
| TD7 Q4 date→[DATE] ; Q5 nettoyage | Échappements, répétitions exactes, ordre des transformations | Exemple distinct de dates ; `[DATE]` reste majuscule car lowercase précède remplacement ; dates formelles sans validation calendaire ; prédiction d’ordre | Q4 14 min, Q5 20 min | RENFORCÉ |
| TD7 Q6 pipeline ; Q7 limite linguistique | Composition autonome et recul méthodologique | Exemple distinct de compte ; cas vide et donnée de transfert ; conserver les deux demandes « situation » et « information linguistique manquante » | Q6 16 min, Q7 9 min | RENFORCÉ |

Pour TD1, TD3–TD7 : démarrage 8 min + activités 102 min + synthèse et restitution 10 min = 120 min. Les durées sont une hypothèse de préparation, non un temps empiriquement mesuré. Les exemples commentés sont courts ; leur lecture, prédiction et un essai font partie du temps de chaque question. Les transferts ajoutés restent modestes et obligatoires ; ils ne remplacent aucune production historique. Si la séance réelle déborde, l’enseignant adapte le rythme sans suppression implicite du parcours.

## Éléments transversaux

| Source | Cible | Statut |
|---|---|---|
| Les 45 cellules `answer` et leurs identifiants Q1..Qn | Identifiants et barèmes maintenus ; nouvelles traces dans la cellule de la question concernée | RENFORCÉ |
| Sept cellules identité nom/prénom/classe | Ajouter `numero_etudiant` ; littéraux non vides ; aucune identité extraite d’un exemple ou commentaire | RENFORCÉ |
| Racines TAL v1 | Même évaluateur/id, version2 ; v1 refusée sans correction ni persistance | RENFORCÉ |
| Tuteur metadata + première cellule | Règles S1 inchangées, nouveaux entraînements rattachés au périmètre de notions effectivement introduites ; pas de code produit par le tuteur | CONSERVÉ |
| Dernière cellule restitution HTML | Même substitut source `__TAL_PUBLIC_URL__`, injection seulement dans dist au déploiement ; jamais une preuve notée | CONSERVÉ |
| Bibliothèques | Aucune TD1–5 ; pathlib fourni puis csv TD6 ; re TD7 ; display reste infrastructure fournie | CONSERVÉ |
| Exemples/essais ajoutés | Exemples sur autres données, balises distinctes ; essais étudiants non notés, jamais utilisés comme preuves pour une réponse Q | RENFORCÉ |
| Explications libres | Recueillies pour relecture, présence distinguée de qualité ; aucun score sémantique à partir de longueur ou mots-clés | RENFORCÉ |

## Acceptation

Chaque ligne doit être vérifiable par diff et lecture du notebook livré. Le contrat détaillé accompagne cette matrice ; le Designer n’invente pas de critères supplémentaires. Le correcteur vérifie des valeurs enregistrées et des indices syntaxiques locaux adaptés, sans exécuter de code. Il ne certifie ni l’auteur des traces ni la généralité d’une fonction. Les alternatives équivalentes, ordres non significatifs et commentaires libres sont traités explicitement. Revues code, pédagogie, gouvernance et intégration requises ; cette spécification ne constitue pas sa propre validation.
