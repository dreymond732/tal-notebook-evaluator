# Revue éditoriale — présentation et ordre du parcours, 7 octobre 2026

**Verdict : ACCEPT. LISIBILITÉ_ÉTUDIANTE_VALIDÉE sur le périmètre déclaré.**

Réviseur indépendant : TAL-Editorial-Reviewer (`s1_editorial`). Base technique : `1ee4581`. Ce rapport est ma seule écriture ; aucune modification des produits ni des prescriptions normatives. Les corrections proposées ont été réalisées par leurs producteurs puis relues. Le verdict ne vaut ni fusion ni validation comportementale de Colab.

## Sources, mandat et méthode

Lecture d’AGENTS, de la fiche du rôle, du workflow, des permissions et du contrat d’évaluation ; lecture de la matrice `docs/pedagogy/presentation_order_2026.md`. La matrice a été produite par TAL-Prof puis validée indépendamment par le Pedagogy-Reviewer avant la conception. Lecture des six notebooks de l’archive utilisateur `drive-download-20261007T062707Z-1-001.zip` et comparaison avec les sources actuelles. Les anciennes versions v1 de l’archive Devoirs ne sont pas des sources techniques à réimporter. Les retouches utilisateur ne justifient pas la reprise de leur description inexacte des fonctions dans TD1.b, ni d’une URL déployée dans la source.

Lecture intégrale des douze supports S3, prose, commentaires du code, données, exemples, réponses, restitutions et contextes cachés compris ; 71 questions. Les indices ci-dessous sont à base zéro. Lecture du README S3 et audit des prescriptions modifiées dans AGENTS, TAL-Editorial-Reviewer, TAL-Pedagogy-Designer et TUTORING_POLICY. Contrôle distinct de la première cellule et des deux copies du tuteur sur les 35 profils. Les 23 autres supports ne font pas l’objet d’une nouvelle revue disciplinaire : comparaison de leur corps avec la base après extraction du seul H1 déplacé, sans différence pédagogique relevée.

## Constats clos après reprise

| Constat | Localisation | Difficulté et correction relue |
|---|---|---|
| TAL-EDIT-P01 | TD0 c1/c6 | Énumération des champs d’identité et référence au temps prévu retirées ; les étapes et prédictions restent demandées. |
| TAL-EDIT-P02 | R0 c1/c14 | R0 explicitement selon les besoins après TD0 ; explication critique non autocorrigée, sans promesse de lecture systématique par un enseignant. |
| TAL-EDIT-P03 | TD1.a c36 | Sous-titre devenu sans objet remplacé par « Versions et documentation ». |
| TAL-EDIT-P04 | TD1.c c1/c32 | Description des quatre champs et procédure générale répétée supprimées ; critères des quatre activités, essais infructueux et sauvegarde conservés. |
| TAL-EDIT-P05 | TD2 c35 ; TD3 c36 | Notices de mauvaise version et d’identification technique retirées ; fonctions, sorties, figures, tests et interprétations maintenus. |
| TAL-EDIT-P06 | TD0 c10 | Référence à `mots.` absente du texte remplacée par `rôle.` présent ; l’essai autonome de Q7 reste distinct. |
| TAL-EDIT-P07 | Politique de tutorat | Antécédent « contexte » explicité pour sa présence dans le Markdown ; correspondance des sept exercices TD0 avec les sept marqueurs vérifiée séparément. |

Le signalement d’un prétendu mauvais compte de `Été : lire.` n’est pas retenu : la chaîne comporte bien onze caractères. Aucun exemple de réponse complète n’a été ajouté sous couvert d’autoévaluation.

## Lecture par question

Chaque ligne désigne un énoncé relu intégralement : ses données et contraintes, la production demandée et les vérifications locales. La colonne « Réponse » repère la cellule de code associée ; les observations personnelles peuvent aussi être demandées dans le commentaire/Markdown immédiatement adjacent, notamment TD1.c et TD4–TD7. Les exemples cités sont fournis, sur d’autres données ; la construction des réponses reste étudiante. Les renvois Q désignent les dépendances du même support, sauf indication contraire. Les petits cas ne remplacent jamais les calculs sur Faguet, les essais personnels ni les interprétations demandées.

| Support / question | Énoncé relu | Repères enseignés ou réemployés avant la question | Réponse |
|---|---|---|---|
| R0 Q1 | c6 — Compter les mots | c3–5 ; acquis TD0/S1 fonctions | c7 |
| R0 Q2 | c8 — Normaliser | TD0 c9 et Q1 | c9 |
| R0 Q3 | c12 — Fréquences | c10–11 ; Q1–Q2 | c13 |
| R0 Q4 | c14 — Regard critique | Q3 ; TD0 distinction unités | c15 |
| R2 Q1 | c9 — Fonction | TD1.a c9–24 ; c5–8 | c10 |
| R2 Q2 | c13 — Noms et lemmes | c11–12 ; Q1 | c14 |
| R2 Q3 | c19 — Filtrer | c15–18 ; Q1–Q2 | c20 |
| R2 Q4 | c23 — Comparer | c21–22 ; Q3 | c24 |
| TD0 Q1 | c7 — Lire et préserver le texte | c5–6 ; acquis S1 lecture/chaînes | c8 |
| TD0 Q2 | c10 — Voir les unités réellement comptées | c9 ; Q1 | c11 |
| TD0 Q3 | c12 — Occurrences et vérification | Q2 ; acquis S1 boucles | c13 |
| TD0 Q4 | c15 — Construire le vocabulaire observé | c14 ; Q2–Q3 | c16 |
| TD0 Q5 | c20 — Fréquences brutes et fonction réutilisable | c17–19 ; Q3–Q4 | c21 |
| TD0 Q6 | c22 — Normaliser sans tout confondre | c9/c17 ; Q5 | c23 |
| TD0 Q7 | c24 — Passer du comptage à l’audit | Q1–Q6 ; diagnostic des limites | c25 |
| TD1.a Q1 | c16 — Lire puis contrôler les annotations | c3–15 | c17 |
| TD1.a Q2 | c20 — Segmenter et vérifier | c18–19 ; Q1 | c21 |
| TD1.a Q3 | c24 — Comparer trois filtres | c22–23 ; Q1 | c25 |
| TD1.a Q4 | c28 — Visualiser puis expliquer | c26–27 ; Q1 | c29 |
| TD1.a Q5 | c32 — Comparer deux découpages sur une même donnée | c30–31 ; TD0 | c33 |
| TD1.a Q6 | c34 — Réinvestissement autonome et export de preuves | Q1–Q5 ; transfert autonome | c35 |
| TD1.b Q1 | c9 — Construire et compter les tokens | TD1.a ; c7–8 | c10 |
| TD1.b Q2 | c15 — Décrire les tokens dans leur ordre | c11–14 ; Q1 | c16 |
| TD1.b Q3 | c19 — Sélectionner les noms | c17–18 ; Q2 | c20 |
| TD1.b Q4 | c21 — Réutiliser la sélection pour les verbes | c17–18 ; Q3 | c22 |
| TD1.c Q1 | c11 — Confronter le repérage humain aux entités détectées | TD1.a ; c7–10 | c13 |
| TD1.c Q2 | c16 — Extraire les personnes et les organisations | c14–15 ; Q1 | c17 |
| TD1.c Q3 | c21 — Des mots aux phrases : que mesure le score ? | c19–20 ; TD1.a Doc/Token | c23 |
| TD1.c Q4 | c29 — Reconnaître « Université de Toulon », puis éprouver vos règles | c24–28 ; Q1–Q3 | c30 |
| TD2 Q1 | c9 — Lire le corpus et rendre l’annotation inspectable | TD1.a ; c7–8 | c10 |
| TD2 Q2 | c14 — Deux fonctions de fréquences | R2 ; c11–13 | c15 |
| TD2 Q3 | c20 — Mesurer l’effet des exclusions | c16–19 ; Q2 | c21 |
| TD2 Q4 | c23 — Fréquences grammaticales | c22 ; Q1 | c24 |
| TD2 Q5 | c27 — Contrôle qualité et objets recherchés | c25–26 ; Q1–Q4 | c28 |
| TD2 Q6 | c31 — Visualiser sans surinterpréter | c29–30 ; Q2–Q5 | c32 |
| TD2 Q7 | c33 — Généraliser et transférer | Q1–Q6 ; transfert | c34 |
| TD3 Q1 | c10 — Fixer le périmètre de la preuve | TD2 ; c7–9 | c11 |
| TD3 Q2 | c17 — Construire une concordance exacte | c12–16 ; Q1 | c18 |
| TD3 Q3 | c23 — Comparer des recherches explicites | c19–22 ; Q2 | c24 |
| TD3 Q4 | c25 — Auditer une citation exacte | Q1–Q3 ; données citations | c26 |
| TD3 Q5 | c30 — Qualifier une altération | c27–29 ; Q4 | c31 |
| TD3 Q6 | c32 — Un rapprochement n’est pas une preuve automatique | c27–29 ; Q4–Q5 | c33 |
| TD3 Q7 | c34 — Assembler un dossier de preuves | Q1–Q6 ; dossier | c35 |
| TD4 Q1 | c10 — Présence et marges | TD3 ; c6–9 | c11 |
| TD4 Q2 | c16 — Compter une paire par phrase | c13–15 ; Q1 | c17 |
| TD4 Q3 | c21 — Réunion et somme des paires | c19–20 ; Q2 | c22 |
| TD4 Q4 | c27 — Mesurer une distance entre positions | c24–26 ; Q2 | c28 |
| TD4 Q5 | c31 — Choisir les frontières | c30 ; Q4 | c32 |
| TD4 Q6 | c36 — Contrôler la normalisation | c34–35 ; TD1.a/TD3 | c37 |
| TD4 Q7 | c41 — Exporter une mesure contrôlable | c39–40 ; Q1–Q6 | c42 |
| TD5 Q1 | c11 — Donner un dénominateur | TD4 ; c6–10 | c12 |
| TD5 Q2 | c15 — Fréquent ou associé ? | c14 ; Q1 | c16 |
| TD5 Q3 | c20 — Comparer des tailles de texte | c18–19 ; Q1–Q2 | c21 |
| TD5 Q4 | c24 — Inverser la condition | c23 ; Q1 | c25 |
| TD5 Q5 | c30 — Traiter les absences et les petits nombres | c27–29 ; Q1–Q4 | c31 |
| TD5 Q6 | c36 — Tester la sensibilité du résultat | c33–35 ; TD4 Q4 | c37 |
| TD5 Q7 | c40 — Rédiger une conclusion mesurée | c39 ; Q1–Q6 | c41 |
| TD6 Q1 | c13 — Situer les occurrences | TD3–TD5 ; c6–12 | c14 |
| TD6 Q2 | c18 — Découper en segments | c16–17 ; Q1 | c19 |
| TD6 Q3 | c24 — Comparer une carte de chaleur | c21–23 ; Q2 | c25 |
| TD6 Q4 | c29 — Visualiser la sensibilité | c27–28 ; TD4 Q4/TD5 Q6 | c30 |
| TD6 Q5 | c35 — Revenir aux passages | c32–34 ; TD3 Q2/Q4 | c36 |
| TD6 Q6 | c40 — Rendre un graphique vérifiable | c38–39 ; Q3/TD4 | c41 |
| TD6 Q7 | c47 — Interpréter et exporter | c43–46 ; Q1–Q6 | c48 |
| TD7 Q1 | c13 — Formaliser une affirmation | TD3–TD6 ; c8–12 | c14 |
| TD7 Q2 | c19 — Construire le moteur commun | c16–18 ; TD3/TD4 | c20 |
| TD7 Q3 | c24 — Vérifier les citations | c22–23 ; TD3 | c25 |
| TD7 Q4 | c30 — Comparer un nombre défini | c27–28 ; Q1–Q3 | c31 |
| TD7 Q5 | c34 — Traiter groupes et expressions | c33 ; Q2/TD4 | c35 |
| TD7 Q6 | c39 — Éprouver sur un cas nouveau | c37–38 ; Q1–Q5 | c40 |
| TD7 Q7 | c44 — Livrer un audit argumenté | c42–43 ; Q1–Q6 | c45 |

## Appréciation de la lecture étudiante

Les repères, exemples, manipulations guidées et transferts autonomes restent distingués. TD1.a introduit spaCy par son usage linguistique, l’installation, les objets et attributs, puis les exemples avant les questions. TD1.b reprend Doc et la sélection ; il ne prétend plus enseigner les fonctions de R2. TD1.c conserve les essais de proximité, leurs limites et les règles à éprouver. R2 distingue les deux versions successives de la fonction et le filtre spaCy des exclusions personnelles, sans faire du bonus TD1.b un préalable.

Dans TD2–TD3, les filtres définissent l’objet observé ; positions originales et texte normalisé restent distincts, de même que citation exacte et rapprochement. TD4 conserve les deux agrégations, les frontières et les unités. TD5 distingue proportion, taux, couverture et absence de dénominateur. TD6 conserve effectifs et dénominateurs, carte comparable, passages sources, légendes et confrontation des lectures. TD7 conserve les six annonces originales, trois citations, protocole exploratoire distinct, tests manuels et par un voisin, export et synthèse de 200 à 300 mots. La réduction des notices ne transforme pas les traces techniques en preuve d’interprétation ou en réponses à recopier.

TD0 reste un diagnostic de réactivation : Q7 fait expliciter les limites du comptage et annonce les notions linguistiques approfondies dans TD1.a ; ce lot ne prétend pas transformer ce diagnostic en un cours complet initial de linguistique. Les noms de champs requis dans les traces restent des consignes de production utiles, distinctes des descriptions des champs d’identité supprimées. Les versions de bibliothèques et paramètres de reproductibilité nécessaires aux exercices restent légitimes ; le commentaire canonique de restitution demandé par l’enseignant est conservé.

Le parcours affiché est TD0 → R0 si besoin → TD1.a → TD1.b facultatif → TD1.c → R2 → TD2–TD7. Aucun support déplacé n’est simplement promis pour plus tard. Gemini apparaît comme tuteur dans le TD0 ; ses autres mentions en S3 concernent le matériau d’audit. Les durées et budgets visibles du lot S3 sont retirés sans supprimer les activités correspondantes.

## Audit de structure et des normes

Les 35 premières cellules commencent par le H1 visible suivi du commentaire HTML complet dans la même cellule ; comparaison exacte du contexte entre les balises et `metadata.colab.aiContexts`. Le profil structuré reste présent. S1 conserve son interdiction de code ; les contrôles conservent le refus d’aide. Aucun succès de ce contrôle structurel n’est présenté comme un essai effectif de Gemini.

Les nouvelles prescriptions normatives maintiennent le destinataire étudiant, la distinction entre activités sur Gemini et présentation de son rôle, l’intégrité des introductions après déplacement du titre, la conservation des critères locaux et la facultativité des remédiations concernées. Elles ne permettent pas au rédacteur de s’autoévaluer ni d’effacer du contenu pédagogique sous couvert d’allègement. Leur portée pérenne doit être distinguée de la migration présente : seule la prose S3 est reprise intégralement ici ; les autres semestres ne sont pas déclarés conformes à toutes les nouvelles règles de présentation du seul fait de la migration des titres.

## État effectivement relu

Les empreintes ci-dessous décrivent les fichiers après les corrections finales. Elles remplacent, pour cette lecture éditoriale, les empreintes intermédiaires du gel initial.

| Fichier | Plage intégrale relue | Questions | SHA-256 |
|---|---|---:|---|
| `Notebooks TD/S3/R0_S3_python_texte.ipynb` | c0–c16 (17 cellules) | 4 | `ac4081b73115dcdabeb245c75490bf8d1a47645a3e777c7862682cad56281301` |
| `Notebooks TD/S3/R2_S3_frequences_reutilisables.ipynb` | c0–c25 (26 cellules) | 4 | `c73877a7cda40928f7dcae07b82dd4ee8700c39898a17a5d355234c06f92c079` |
| `Notebooks TD/S3/TD0_S3_diagnostic_texte.ipynb` | c0–c28 (29 cellules) | 7 | `9b61a6e1d1f5ccd7e37535219425b0c4166b984416b0ee90560271e4a1b27c7e` |
| `Notebooks TD/S3/TD1.a_S3_fondations_spacy.ipynb` | c0–c39 (40 cellules) | 6 | `538e1e2df525066a2d96d341691316a3f860d6ca8201b70aecd4b9ae7b827ccd` |
| `Notebooks TD/S3/TD1.b_S3_doc_spacy.ipynb` | c0–c25 (26 cellules) | 4 | `ed74ea3148b20467e359045f94d46ad94faf641d5a0d19fd375a3e753ec3a981` |
| `Notebooks TD/S3/TD1.c_S3_entites_similarite_regles.ipynb` | c0–c35 (36 cellules) | 4 | `e213bd45b1c153256f10f74f294a2d0a3f96b5db34481941cf2148041199b5e5` |
| `Notebooks TD/S3/TD2_S3_analyse_corpus.ipynb` | c0–c38 (39 cellules) | 7 | `c75dd20ea2bf45243cd1298c9960c8688e283bf9508ae295ae82794d948c1107` |
| `Notebooks TD/S3/TD3_S3_concordances_citations.ipynb` | c0–c39 (40 cellules) | 7 | `1d1ce7f366e4614df55817ca8a0314991951caec514edb3485311da417d165ed` |
| `Notebooks TD/S3/TD4_S3_cooccurrences.ipynb` | c0–c46 (47 cellules) | 7 | `3102cfb711cc8c20498b8fc25dd2a1d603e591b9a95e5af860fd435195286e3d` |
| `Notebooks TD/S3/TD5_S3_associations.ipynb` | c0–c45 (46 cellules) | 7 | `948aa55de73748ab686f111d668e859db02896b8676f4824134f68177e0d1615` |
| `Notebooks TD/S3/TD6_S3_visualisations.ipynb` | c0–c52 (53 cellules) | 7 | `107b1812439b39401ae1389a365490ecde1912bce76625dd52e7ac453386efcf` |
| `Notebooks TD/S3/TD7_S3_audit_llm.ipynb` | c0–c49 (50 cellules) | 7 | `25cb948f91f2832e6adc60bdf5a743013b27ad2dcf2b2e996cbc991efdf89bca` |

Limites : ni restauration exhaustive des sources historiques 2025, ni validation nouvelle des contenus S1/S2/contrôles, ni exécution des modèles spaCy ou observation d’un comportement Colab. La note indépendante `Corrigés modèles/TD/presentation-order-2026/lecture.md` complète ce verdict avec les données et productions comprises pour chacune des 71 questions ; sa conclusion a été relue. Ses réserves sur les acquis antérieurs de TD0 Q7 et sur `is_alpha` à TD4 Q1 ne sont pas démontrées comme des régressions de ce lot et ne valent pas certification de ces acquis. Sa remarque sur le commentaire canonique de déploiement et le bloc fonctionnel de restitution reste une limite explicitement conservée, distincte des notices Markdown répétitives supprimées. Le README reste succinct sur R0 ; le bilan TD0 et l’ouverture R0 rendent son usage conditionnel explicite. Cette lecture simulée n’est pas un essai réel en classe. La conservation pédagogique et la conformité technique relèvent également des avis indépendants correspondants.
