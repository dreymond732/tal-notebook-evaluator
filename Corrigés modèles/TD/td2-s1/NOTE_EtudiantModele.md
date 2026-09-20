# TD2 S1 — Note de résolution indépendante

Identité fictive : **Claire Exemple**, groupe **MODELE**. Date : 2026-09-19.

Branche de travail communiquée : `pedagogy/s1-td2-progressive`. Sujet utilisé : `Notebooks TD/S1/TD2_S1_python_texte.ipynb`, SHA256 après synchronisation des métadonnées et du repère d’identité : `df8be0b6b1da0b8427368bb23b1279fff50cba6e74ad737ca335cb9cf1d445df`. Ressource antérieure autorisée : `Notebooks TD/S1/TD1_S1_python_texte.ipynb`. Consignes de rôle lues : `AGENTS.md` et `docs/agents/TAL-Étudiant-Modèle.md`.

Livrable : `TD2_S1_EtudiantModele_non_execute.ipynb`. Seules les sources des cellules de code ont été remplies, identité comprise. Les cellules de cours et les métadonnées du sujet ont été conservées dans la copie. Le sujet original n'a pas été modifié.

## Cloisonnement et état d'exécution

Aucun correcteur, test, autre corrigé, document de pédagogie ni fichier d'infrastructure n'a été consulté. Les réponses ont été construites à partir des deux sujets autorisés. Aucun import, aucune boucle, aucune compréhension ni définition de fonction ne figurent dans le code de réponse.

Le notebook n'a **jamais été exécuté ni soumis au serveur**. Toutes les sorties sont vides et tous les compteurs d'exécution sont nuls. Les commentaires expriment des prédictions et des explications raisonnées, pas des observations d'une exécution effective. Le sujet demande une confrontation aux sorties : cette partie devra être réalisée humainement. La vérification livrée est une vérification indépendante de faisabilité pédagogique, sans jugement sur un correcteur.

## Couverture des questions et sous-questions

| Partie | Réponse construite et couverture | Notions et provenance |
| --- | --- | --- |
| Avant de commencer | Identité fictive ; exemple `prix = 12` distinguant nom, valeur et type ; distinction affectation/comparaison ; ce que compte `len()` pour une chaîne. | Variables, entier, `=`, `==`, `len()` : TD1. |
| Exemple 1 | Prédiction : espace intérieur conservé ; `etiquette` garde la source. | `strip()` et immuabilité explicités en exercice 1. |
| 1.1 | Création de `texte_propre`, affichage Q1. | Affectation et `strip()`. |
| 1.2 | Affichage des deux longueurs avec Q1b. | `len()` et `print()` : TD1. |
| 1.3 | Écart attendu de six caractères, espaces intérieurs conservés, source conservée grâce à un nom distinct. | Chaînes immuables et réaffectation : exercice 1. |
| Exemple 2 | Pourquoi `livre` ne remplace pas directement `LIVRE`. | Sensibilité à la casse : exercice 2. |
| 2.1 | Deux étapes nommées : minuscules, puis remplacement. | `lower()` et `replace()` introduits en exercice 2. |
| 2.2 | Q2 et Q2b, présence de corpus et absence de textes. | `in` déjà utilisé au TD1. |
| 2.3 | Interprétation des deux booléens ; ordre non indispensable pour ces données, contrairement à l'exemple du livre. | Raisonnement sur données et casse. |
| 2.4 | Affichage supplémentaire de `texte_propre`, explication de la conservation. | Réinvestissement de l'exercice 1. |
| Exemple 3 | Correspondance caractères/indices d'archive, longueur attendue de la tranche. | Indices et borne exclue introduits en exercice 3. |
| 3.1 | Premier et dernier caractères, tranche `[0:4]`, Q3. | Indices `0` et `-1`, tranche. |
| 3.2 | Tranche `[1:5]`, longueur de la source, Q3b. | Tranche et `len()`. |
| 3.3 | Deux groupes de quatre indices, contenus décalés ; affichage de la source inchangée. | Borne exclue et immuabilité. |
| Exemple 4 | `len()` compte des caractères ou des éléments selon la donnée ; espaces successifs sans élément vide. | Liste de chaînes et `split()` introduits en exercice 4. |
| 4.1 | Construction de `tokens`, liste et troisième élément affichés avec Q4. | `split()` et indice de liste. |
| 4.2 | Nombre d'éléments et dernier élément affichés avec Q4b. | `len()` de liste et indice négatif. |
| 4.3 | Types de la chaîne, de la liste et du troisième élément ; comparaison des deux longueurs. | `type()` : TD1, liste : exercice 4. |
| 4.4 | Troisième caractère (espace) comparé au troisième élément (chaîne entière), avec affichage supplémentaire. | Unité d'une séquence et indexation. |
| Exemple 5 | Deux séparateurs entre trois couleurs, sans séparateur aux extrémités. | `join()` introduit en exercice 5. |
| 5.1 | Reconstruction avec le séparateur exact demandé, Q5. | `join()`. |
| 5.2 | Création de `tokens_reconstruits`. | `split(separateur)` introduit en exercice 5. |
| 5.3 | Liste reconstruite et égalité affichées avec Q5b. | `==` sur listes explicitement défini dans le sujet. |
| 5.4 | Espaces inclus dans le séparateur ; explication des barres qui deviendraient des éléments avec `split()` seul. | Comparaison des deux formes de `split()`. |
| 6.1 | Traitement séparé des indices 0, 1 et 2 ; pour chacun, variable après `strip()` puis variable après `lower()`. | Indexation, méthodes déjà introduites ; aucune boucle et aucun chaînage de méthodes nécessaire. |
| 6.2 | Liste littérale des trois variables, ordre conservé, Q6. | Construction de liste introduite par l'exemple des langues en exercice 6. |
| 6.3 | Q6b affiche la source ; comparaison supplémentaire des listes ; espaces de bord retirés, espace intérieur et cédille conservés. | `==`, transformation et lecture des chaînes. |
| 6.4 | Explication : nouvelles chaînes et nouvelle liste ; aucune modification d'un élément source. | Immuabilité des chaînes, distinction source/résultat explicitée dans le sujet. |
| 7.1 | Chaîne exacte et prédiction détaillée : quatre éléments, virgule accolée, apostrophes internes et exclamation isolée. | Chaîne, espaces et ponctuation. |
| 7.2 | Construction de `tokens_limite` et Q7b. | Réinvestissement de `split()`. |
| 7.3 | Affichage des premier, deuxième et dernier éléments ; explication de la ponctuation accolée, isolée, et des apostrophes. | Indexation et interprétation linguistique. |
| 7.4 | Deux phrases dans `commentaire`, appuyées sur L’analyse, c’est et ! ; affichage Q7. | Chaîne personnelle reliant résultats attendus et limite du découpage. |
| Vérifier et déposer | Tous les affichages demandés sont écrits ; question personnelle à l'enseignant ajoutée en commentaire final. Exécution, conservation de sorties et dépôt non réalisés conformément à la consigne de rôle. | Relecture statique ; validation humaine restante. |

## Autonomie, ambiguïtés et prérequis

Aucun prérequis technique bloquant non introduit n'a été identifié pour résoudre les exercices actuels. Les méthodes sont présentées avant leur emploi ; les activités finales combinent des notions déjà introduites. Le traitement de trois chaînes peut être écrit avec des variables intermédiaires, sans supposer le chaînage des méthodes ni une boucle. Les appels aux fonctions usuelles `print`, `len` et `type` relèvent du TD1 ; aucune fonction nouvelle n'est définie.

Deux précisions de lecture ne bloquent pas la résolution : en 6.3, « comparez-la » peut désigner une comparaison visuelle ou un test d'égalité ; la copie propose les deux. Dans « Les accents ont-ils disparu ? », le signe présent dans les données est une cédille : la copie parle donc plus précisément de signes diacritiques conservés. Le mot « espaces blancs » est présenté par le sujet ; aucune exploration de tabulations ou sauts de ligne n'est nécessaire aux données proposées.

Le TD1 utilisé rappelle ou met en exercice plusieurs notions sans les détailler toutes longuement. La faisabilité constatée présuppose que l'étudiant a effectivement travaillé ce TD1, comme annoncé dans l'objectif du TD2 ; elle ne mesure pas la maîtrise individuelle de ces acquis.

## Réponses construites et exemples repris

Les chaînes de départ, les noms de variables imposés et les libellés d'affichage proviennent du sujet. Les exemples distincts de cours restent dans les cellules Markdown copiées ; leur code n'est pas recopié comme réponse aux exercices. Leurs prédictions demandées sont traitées dans les commentaires. Les réponses, variables intermédiaires, affichages supplémentaires et explications ont été construits pour les données des exercices. Q1 à Q5 sont des réemplois guidés ; Q6 combine les opérations antérieures sur trois entrées ; Q7 construit une interprétation personnelle et n'introduit aucune nouvelle méthode de découpage.

## Charge indicative, non mesurée

Le découpage annoncé totalise 120 minutes : démarrage 8, exercices 14 + 16 + 17 + 15 + 12 + 18 + 14, vérification/dépôt 6. Cette charge paraît compatible avec une séance de débutants si les prédictions, essais et commentaires sont réellement réalisés. Elle n'a pas été chronométrée ni testée auprès d'étudiants. Les raisonnements sur l'ordre des opérations (Q2), caractère versus élément (Q4) et limites linguistiques (Q7) peuvent demander un accompagnement variable. Une résolution statique par un modèle ne démontre pas à elle seule que chaque étudiant tiendra ce rythme.

## Vérifications et limites

La relecture statique contrôle la couverture de toutes les questions et les notions nécessaires. Le JSON de la copie est lisible, les cellules de cours et métadonnées concordent avec la source, et les cellules de code ne comportent ni sorties ni compteurs d'exécution renseignés. Une analyse syntaxique sans exécution vérifie la validité du code et l'absence des constructions exclues. Aucun test du correcteur et aucune soumission n'ont été effectués.

Verdict demandé au relecteur indépendant : valider la couverture pédagogique et les commentaires ; faire ensuite exécuter humainement la copie si une validation des résultats affichés est souhaitée. **Faisabilité statique constatée ; exécution non réalisée.**
