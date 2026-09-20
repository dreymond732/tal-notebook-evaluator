# Ressources du parcours S3 : audit textométrique

## Provenance

`faguet_source.txt` reproduit **octet pour octet** le fichier texte fourni par l'enseignant dans l'archive du 20 septembre 2026. Empreinte SHA-256 : `c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`. Il s'agit de sa version nettoyée de *Le féminisme* d'Émile Faguet, publiée sur [Project Gutenberg](https://www.gutenberg.org/files/59719/59719-h/59719-h.htm). Aucun nettoyage supplémentaire n'est appliqué ici. L'historique détaillé du nettoyage antérieur n'est pas fourni : ce fichier constitue le corpus figé de l'exercice, et non une certification de conformité à l'édition imprimée.

`gemini_transcription.txt` reproduit l'extraction textuelle du DOCX fourni. Les paragraphes et les cellules des tableaux ont été extraits dans leur ordre ; la mise en page et les images ne sont pas conservées. Les trois prompts appartiennent à **une même conversation progressive**, déclarée dans le document comme réalisée avec Gemini dans Google Workspace le 18 septembre 2026. Le modèle exact, ses paramètres et ses opérations internes ne sont pas connus.

`affirmations_gemini.json` transcrit manuellement les six lignes du tableau du troisième prompt. Les champs manquants sont `null` : ils ne sont pas déduits. Les intervalles annoncés sont des affirmations à auditer, pas des références de correction. Le pivot « Raison / Bon sens » et ses analogues restent volontairement non normalisés. Aucune fenêtre n'étant définie dans la réponse, un calcul ne peut pas réfuter directement l'intervalle sans préciser une convention de comparaison.

`citations_gemini.json` repère trois citations présentes dans la transcription ; leur fidélité au corpus est à vérifier. Ne pas corriger silencieusement une citation avant l'audit.

## Ressources pédagogiques

`exemples.json` fournit de petits textes distincts de Faguet. `annotation_manuelle` est une référence didactique visible sur un exemple résolu : elle sert à apprendre à contrôler une annotation, jamais à présumer qu'un modèle est infaillible. Les autres entrées ne donnent pas les solutions des exercices. Les exemples sont originaux et réutilisables dans le cours.

Les nombres automatiques spaCy dépendent du modèle et de ses versions. L'audit doit garder le texte, ses positions et les paramètres. Les exports d'un TD peuvent être repris au suivant ; sans export, les cellules de préparation fournissent le même corpus et permettent de reconstruire les objets nécessaires, sans reprendre les réponses du TD précédent.

`empreintes.json` associe à chaque donnée son empreinte SHA-256. Dans les notebooks, le téléchargement vise un commit Git figé et vérifie ces empreintes. Conserver les fichiers localement permet de travailler après le téléchargement initial. Les fichiers de données n'exécutent aucun code.
