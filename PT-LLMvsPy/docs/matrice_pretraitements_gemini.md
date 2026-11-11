# Matrice critique des prétraitements — rapport Studio et tableau Gemini

**Source examinée :** tableau de données Gemini transmis par l'enseignant le 10 novembre 2026, identifiants `OP01` à `OP12`. Les douze lignes portent le statut **PROPOSÉ** ; aucune ne contient de preuve d'exécution. Le rapport Studio antérieur et le tableau ne permettent pas de certifier le prétraitement effectivement réalisé par Gemini. Les exemples avant/après sont parfois génériques, et la mention « Source 1 » constitue un renvoi documentaire, non une trace d'exécution.

**Objet :** convertir ces propositions en **questions de validation**, puis en contrats testables lorsque les règles auront été explicitement approuvées. Ne pas utiliser les nombres du rapport Gemini comme résultats attendus des tests.

## Revue de chacune des 12 opérations

| ID | Niveau correct | Proposition de Gemini | Correction / vigilance | Statut bibliothèque et décision |
|---|---|---|---|---|
| **OP01** | Transformation du texte / définition du corpus | Supprimer péritexte, en-têtes, séparateurs | Distinguer titre de chapitre, marque éditoriale et contenu analytique ; le fichier Faguet des TD est déjà une version nettoyée dont l'historique complet n'est pas documenté | **Partiellement disponible** : `masquer_lignes_exactes` pour des titres explicitement sélectionnés et `masquer_separateurs` pour les lignes d'astérisques ; aucun nettoyage automatique du péritexte |
| **OP02** | Transformation du texte ou exclusion d'une couche documentaire | Supprimer les notes et marqueurs entre crochets | Ne pas confondre appel de note, contenu de note et référence bibliographique ; examiner les **quatre appels et trois blocs** détectés dans cette version du fichier | **Disponible en option** : `masquer_appels_notes` et `masquer_blocs_notes`, séparément, avec les positions d'origine conservées |
| **OP03** | Transformation du texte | Recoller les césures de fin de ligne | Distinguer césure éditoriale et trait d'union lexical ; aucune césure mot-CRLF-fragment détectée dans cette version figée | **Disponible uniquement sur liste validée** : `raccorder_cesures_validees` masque trait d'union et retour dans la vue de contrôle et raccorde dans le rendu épuré, avec table d'alignement |
| **OP04** | Transformation du texte | Recomposer les sauts de ligne internes aux paragraphes | Une suppression compacte décale les offsets ; notre remplacement par espaces de même longueur **les préserve**. La composition des paragraphes ou des vers reste à vérifier sur 8 456 retours CRLF | **Implémenté en option** : `recomposer_lignes` ; jamais actif par défaut |
| **OP05** | Transformation du texte | Harmoniser les apostrophes courbes | Préserve la longueur en caractères dans notre version, mais change les graphies, la recherche exacte et les empreintes | **Implémenté en option** : `apostrophes_droites` ; original conservé |
| **OP06** | Configuration de la tokenisation ; transformation seulement si les caractères sont réellement réécrits | Scinder ou conserver des composés, normaliser des tirets | Si spaCy segmente « lui-même », il ne réécrit pas nécessairement le texte : il modifie des **frontières de tokens**, pas les offsets caractères. Normaliser des tirets Unicode serait une autre opération | **Non implémenté dans le module texte** ; tester d'abord `nlp.tokenizer.explain()` |
| **OP07** | Représentation lexicale | Mettre en minuscules | `token.lower_` permet un calcul insensible à la casse sans modifier `doc.text`. La minuscule appliquée au texte avant les entités peut dégrader leur identification | **Déjà paramétrable** dans `ProtocoleGlobal.formes` |
| **OP08** | Annotation linguistique (tokenisation) | Séparer le texte en tokens | spaCy produit un `Doc` non destructif : `doc.text == texte_analysé`. `token.i` peut changer, `token.idx` donne un offset de caractères dans le texte analysé | **Déjà disponible via spaCy** ; à tester sur élisions, césures, composés |
| **OP09** | Filtrage **par mesure** | Exclure ponctuation, chiffres et mots vides | `is_alpha` exclut typiquement ponctuation et nombres purs mais **ne retire pas les stopwords**. Un filtre `is_stop` serait un choix supplémentaire, différent selon l'indicateur | **Filtres alphabétiques disponibles**, exclusion des stopwords **non activée** |
| **OP10** | Annotation linguistique (lemmatisation) | Calculer les lemmes | La qualité dépend du pipeline, du modèle, de ses versions et des néologismes ; `spacy.blank("fr")` sans lemmatiseur ne produit pas les annotations nécessaires | **Mode lemmes conditionné** aux annotations présentes, à valider |
| **OP11** | Annotation linguistique (segmentation en phrases) | Délimiter les phrases à partir de la ponctuation | Le parser, le senter et le sentencizer ne sont pas interchangeables ; une coupure fautive change tous les comptes par phrase | **Segmentation spaCy disponible**, mais protocole et validation humaine nécessaires |
| **OP12** | Configuration de la segmentation / du tokenizer | Protéger les abréviations | Les abréviations ne sont pas toutes prises en charge par une simple liste ; vérifier les frontières de phrases, pas seulement la liste des tokens | **Non implémenté spécifiquement** ; inventaire des abréviations à construire |

## Invariants proposés avant toute mesure

1. **L'acquisition conserve les octets d'origine.** `io_corpus.charger_corpus` calcule leur SHA-256 avant toute transformation ; le fichier et son empreinte restent les références.
2. **Un plan de traitement est explicite et ordonné.** Par défaut, aucun nettoyage n'est appliqué. Chaque opération activée doit avoir une justification et un journal des modifications exécutées.
3. **Un texte transformé n'est jamais assimilé à la source.** Conserver au minimum le SHA-256 original et celui de la représentation analysée. Ne pas afficher une phrase normalisée comme une citation originale exacte.
4. **Préservation des offsets** : toutes les transformations de la vue de contrôle conservent les positions d'origine ; la version épurée est accompagnée d'une **table de correspondance**, notamment pour les zones masquées et les césures approuvées.
5. **Annotation ≠ réécriture.** Tokenisation, lemmatisation et délimitation des phrases sont des sorties de spaCy sur le texte analysé ; elles peuvent avoir leurs propres configurations et versions.
6. **Filtrage ≠ nettoyage.** Les règles d'exclusion des tokens doivent être fixées **pour chaque mesure**, avec dénominateurs cohérents, sans éliminer silencieusement les stopwords.
7. **PROPOSÉ ≠ EXÉCUTÉ ≠ VÉRIFIÉ.** Une description dans Gemini ne constitue pas une preuve d'application ; le statut vérifié exige un test indépendant.
8. **L'échantillon précède le corpus entier.** Étudier les cas positifs et négatifs avant toute activation collective d'une transformation.

## Priorités pour la revue pédagogique

- **Décision A — statut des titres, notes et apparats (OP01–OP02)** : les conserver, les exclure de certaines mesures ou les décrire comme sous-corpus ? D'abord relever des exemples exacts du fichier.
- **Décision B — retours de ligne et césures (OP03–OP04)** : valider sur des micro-extraits les retours typographiques, paragraphes, dialogue et vers ; garder `recomposer_lignes` optionnel.
- **Décision C — représentations linguistiques (OP06–OP12)** : inventorier les abréviations et les termes composés, comparer les frontières de tokens et de phrases sur un échantillon annoté manuellement.
- **Décision D — filtrages (OP09)** : fixer pour chaque indicateur l'inclusion ou non de la ponctuation, des chiffres et des stopwords ; ne pas modifier le texte d'origine pour cela.

Le notebook 01 importe la bibliothèque depuis Git, teste des phrases types puis des contre-exemples choisis par les étudiants et prévisualise les effets sur Faguet entier. **L'export du texte épuré, de son manifeste et de ses offsets est subordonné à l'approbation de chaque opération et à une validation globale motivée.** Le notebook 02 exige ce résultat approuvé pour lancer les métriques.

## Références techniques

- Explosion. (s. d.). *Token — API documentation*. https://spacy.io/api/token (notamment `i`, `idx`, `is_alpha`, `is_stop`).
- Explosion. (s. d.). *Linguistic features*. https://spacy.io/usage/linguistic-features (tokenisation non destructive, configuration du tokenizer et segmentation en phrases).

Ce document constitue la revue de **propositions Gemini**, et non une certification de l'exécution du pipeline Gemini.
