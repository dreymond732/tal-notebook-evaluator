# Les rapports Gemini sur *Le Féminisme*

Les cahiers confrontent les affirmations des rapports aux mesures obtenues en Python et aux passages du livre. Pour reprendre une affirmation, retrouvez d’abord les mots et les nombres dans le document source. Les liens vers les JSON indiquent ensuite quelle partie de ce document le cours a transcrite.

## Rapport 1 · Gemini, 18 septembre 2026

Le premier échange a lieu dans Gemini pour Google Workspace le matin du **18 septembre 2026**, selon la mention figurant en tête de la transcription. La première demande est « Fais une analyse lexicométrique du texte. » Deux relances suivent dans la même conversation. Elles précisent les relations lexicales à examiner.

- [Lire la transcription, avec les trois prompts et leurs réponses](../../Notebooks%20TD/S3/ressources/gemini_transcription.txt).
- [Retrouver les six affirmations G1 à G6 du troisième prompt](../../Notebooks%20TD/S3/ressources/affirmations_gemini.json). Le JSON conserve les intervalles annoncés et laisse les conventions non précisées à `null`.
- [Retrouver les trois citations C1 à C3 tirées des deux premiers prompts](../../Notebooks%20TD/S3/ressources/citations_gemini.json). Pour les vérifier, recherchez leurs mots dans le [texte de Faguet utilisé en cours](../../Notebooks%20TD/S3/ressources/faguet_source.txt).

## Rapport 2 · Gemini Notebook, rapport chiffré transmis le 10 novembre 2026

Le rapport *Analyse lexicométrique, quantitative et relationnelle de « Le Féminisme » d’Émile Faguet* a été **transmis le 10 novembre 2026**. Le § 1 annonce 79 540 tokens. Le § 4 annonce 208 phrases associant *femme(s)* et *homme(s)*. L’original conservé ne donne pas sa date de génération.

- [Lire le fichier original](../../app/static/PT_LLMvsPy_Analyse_Gemini_source_originale.md) ou [la version avec les tableaux remis en forme](../../app/static/PT_LLMvsPy_Analyse_Gemini_integrale.md).
- [Consulter les huit annonces du § 1 transcrites en JSON](../data/annonces_globales_gemini.json). Le chiffre de 208 phrases se retrouve directement au § 4 de l’original.
- [Consulter la notice de provenance et les empreintes des deux versions](../../app/static/PT_LLMvsPy_Analyse_Gemini_provenance.json).

## Rapport 3 · Gemini Notebook, rapport méthodologique transmis le 10 novembre 2026

Le *Rapport d’analyse lexicométrique, quantitative et relationnelle de l’ouvrage Le Féminisme d’Émile Faguet* s’ouvre sur le « Protocole méthodologique et exigences préalables de reproductibilité ». La date de génération ne figure pas dans l’original. Son § 2 présente six indicateurs, identifiés de M-01 à M-06. Le § 6.1 reprend pour chacun le statut et la justification donnés par le rapport. Ainsi, le nombre de tokens (M-01) est qualifié de « NON VÉRIFIABLE » et le TTR (M-04) d’« ESTIMÉ ».

- [Lire le rapport méthodologique original, avec ses six parties](../../app/static/PT_LLMvsPy_Rapport_03_Gemini_Notebook_source_originale.md).
- [Consulter la transcription en JSON des six statuts déclarés au § 6.1 et de leurs justifications](../data/statuts_mesures_rapport_03.json).

## Repères A, B et C du cahier 04

Dans le cahier 04, **la pièce A** renvoie au rapport 2 (§ 1 et § 4), **la pièce B** à la conversation partagée ci-dessous et **la pièce C** au rapport 1 (citations de septembre).

Au 03, le cours reprend de la première réponse de cette conversation un protocole portant sur les lemmes *femme* et *droit*. L’effectif est à calculer sur le texte préparé au 01. Le JSON produit par le 03 conserve votre propre mesure.

[Ouvrir la conversation Gemini et retrouver la ligne M4_COOC_SENT](https://share.gemini.google/43HURKzcfoet)

Dans Gemini Notebook, **Studio** est le nom du panneau qui permet notamment de générer un rapport. [Aide officielle de Google sur la génération de rapports](https://support.google.com/gemininotebook/answer/18323649?hl=fr)
