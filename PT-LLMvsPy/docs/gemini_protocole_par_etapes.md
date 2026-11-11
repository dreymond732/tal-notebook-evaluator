# Expérience Gemini Notebook — prompts courts et reproductibilité

**Matériau** : le texte Faguet du dépôt TAL S3, conservé dans une source propre du notebook Google ; empreinte contrôlée séparément. Le rapport Studio fourni par l'enseignant est une **production à auditer**, pas une preuve que les traitements mentionnés ont été exécutés.

## Organisation recommandée

1. Créer **un seul notebook Gemini** avec le fichier texte Faguet comme source sélectionnée. Conserver le lien vers le fichier du dépôt et son commit.
2. Dans **Discussion**, utiliser un prompt court par étape, sauvegarder les réponses comme Notes si leur statut est explicite.
3. Après validation manuelle, créer une **Note « Protocole confirmé »** (seules les opérations effectivement observées ou décidées y figurent).
4. Dans **Studio → Rapports → Document → Personnaliser**, produire **un rapport par partie** en sélectionnant seulement le corpus et la Note confirmée. Utiliser « Afficher le prompt personnalisé » pour vérifier la consigne enregistrée.
5. Exporter les rapports vers Docs et, si pertinent, les tableaux vers Sheets. Conserver ces exports, la date et les versions accessibles. Ne pas attribuer automatiquement des capacités d'exécution de code à toutes les sessions.

### Règle commune à conserver dans les paramètres de Discussion ou dans une Note sélectionnée

> N'annonce « CALCULÉ » que si tu as réellement exécuté un programme sur le corpus entier et conservé son résultat. Sinon indique « NON CALCULÉ ». Sépare la définition proposée, l'opération effectivement exécutée et l'observation. N'invente ni empreinte, ni version de modèle, ni protocole. Ne conclus pas sur l'intention de l'auteur à partir d'un compte lexical isolé.

## P0 — Vérifier l'accès réel (Discussion)

> Sur la source `faguet_source.txt`, indique si tu peux ouvrir **les octets intégraux** dans Python ou seulement consulter des passages indexés. Si Python a accès au fichier, exécute le calcul SHA-256 **sur ses octets** et restitue le code, le résultat et la taille. Sinon écris « accès informatique insuffisant » et n'invente aucune valeur. Indique les outils, versions et ressources effectivement observés.

**Critère de passage** : soit la preuve d'accès et de hachage, soit un refus explicite de l'analyse exhaustive ; ne pas attribuer à Gemini une procédure qu'il n'a pas démontrée.

## P1 — Inventorier les prétraitements (Discussion)

> **Sans compter les mots**, fournis la liste ordonnée des prétraitements du texte Faguet : exclusions de paratexte, notes, césures, retours typographiques, apostrophes, casse, tokenisation, stopwords et lemmatisation. Pour chacun : opération exacte, exemple avant/après, modification éventuelle des positions, statut **exécuté / seulement proposé / inconnu**, preuve disponible. Distingue les transformations du texte des filtres de tokens. Si aucune transformation n'a été exécutée, dis-le.

**Critère de passage** : une table de spécifications et de statuts, non un récit invérifiable de traitements déjà faits.

## P2 — Formaliser un prétraitement testable (Discussion)

> Propose un code Python limité à **un** traitement prioritaire : identifier les retours à la ligne typographiques sans détruire les paragraphes. Préserve l'original et ses indices de caractères. Donne un micro-exemple avec résultat attendu avant d'exécuter quoi que ce soit. Si l'exécution est possible, fournis l'entrée, la sortie et les tests ; sinon indique « code proposé non exécuté ». Ne supprime pas les notes ou césures à cette étape.

**Critère de passage** : code et tests pour une seule transformation, vérifiés indépendamment avant intégration.

## P3 — Reproduire les métriques globales (§ 1)

> Applique **uniquement le protocole préalablement validé** au corpus Faguet complet. Produis tokens, types, hapax, TTR, phrases et longueur moyenne, avec définitions, numérateurs, dénominateurs, versions et état d'exécution. Si aucun comptage intégral n'a été exécuté, inscris « NON CALCULÉ » partout ; ne donne pas de nombres estimés. Conserve les résultats bruts avant arrondi et un exemple permettant de contrôler les frontières de phrase.

## P4 — Fréquences et énonciation (§ 2–3)

> Examine séparément les regroupements lexicaux, les pronoms et les marqueurs d'obligation du rapport Faguet. Fournis les **listes exactes** de formes/lemmes retenues et les cas ambigus. Pour chaque chiffre, indique le calcul exécuté ou « NON CALCULÉ ». Distingue comptage de forme, regroupement interprétatif et exemples textuels. Ne déduis pas automatiquement une intention de l'auteur.

## P5 — Relations lexicales (§ 4)

> Compare pour trois paires de termes les cooccurrences par phrase, en fenêtre ±5 et ±10 tokens, sans franchir la frontière des phrases. Définis le token, la présence d'un pivot et les comptes de paires ; ces mesures doivent rester séparées. Ne donne des effectifs que si du code a été effectivement exécuté sur le texte ; sinon propose le protocole et un micro-test manuel, sans estimation.

## P6 — Mentions et interprétations (§ 5–6)

> Identifie les variantes écrites de Turgeon, Joran et Ellen Key. Distingue forme observée, mention de personne et interprétation intertextuelle. Pour chaque affirmation de synthèse, classe-la comme **mesure reproductible, observation textuelle, hypothèse interprétative ou non démontrée**. Cite des passages localisables ; ne fournis aucun total non calculé.

## Traçabilité des résultats

Pour chaque étape : identifiant du prompt, date, sources sélectionnées, modèle si visible, copie du prompt personnalisé, rapport intégral, code proposé/exécuté, sortie vérifiée, protocole retenu ou refusé. Les Notes constituent des **documents de méthode**, pas des preuves automatiques d'exécution.

Le passage de P1–P2 aux fonctions de comptage doit être validé lors d'une revue : aucune opération de nettoyage destructrice ne doit être ajoutée implicitement à la bibliothèque commune.
