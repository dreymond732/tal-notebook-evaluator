"""Student-facing S1 examples, separate from scoring and submitted evidence.

Examples follow the active subject cells. They are trusted application text,
never generated from a submission and never executed by the evaluator.
"""
import re
from textwrap import dedent

from report_evidence import answer_evidence


def example(source, explanation):
    return {'solution_code': dedent(source).strip(), 'solution_explanation': explanation}


SOLUTIONS = {
    1: [
        example('''
            prix_par_mot = 0.12
            nb_mots = 125
            cout_total = prix_par_mot * nb_mots
            print("Résultat Q1 :", cout_total)
        ''', 'Multipliez le prix unitaire par le nombre de mots : le coût est 15 euros.'),
        example('''
            # Prédiction : un nombre décimal a ici le type float.
            note = 14.5
            print("Résultat Q2 :", type(note))
        ''', 'type(note) affiche le type de la valeur, ici float.'),
        example('''
            meme_nombre = nb_mots == 125
            commande_importante = nb_mots >= 100 and prix_par_mot > 0
            print("Résultat Q3 :", meme_nombre, commande_importante)
        ''', 'Réutilisez les données de Q1. == compare deux valeurs ; and exige que les deux conditions soient vraies. Les deux réponses valent ici True.'),
        example('''
            langue_source = "français"
            langue_cible = "anglais"
            phrase_presentation = f"Traduction du {langue_source} vers l’{langue_cible}."
            print("Résultat Q4 :", phrase_presentation)
        ''', 'Les accolades insèrent les deux variables. Conservez les espaces, l’apostrophe et le point final de la phrase demandée.'),
        example('''
            volume_saisi = "80"
            volume_corrige = int(volume_saisi) + 20
            print("Résultat Q5 :", volume_corrige, type(volume_corrige))
        ''', 'Convertissez la chaîne en entier avant l’addition : le résultat est 100, de type int.'),
        example('''
            phrase = "Le TAL aide."
            print("Résultat Q6 :", len(phrase), "TAL" in phrase)
            print("Résultat Q6b :", repr(phrase))
            # Les espaces et le point comptent ; TAL est présent avec cette casse.
        ''', 'Cet exemple utilise une phrase possible ; gardez votre propre choix. len compte tous les caractères, et in distingue les majuscules des minuscules. repr rend la donnée choisie visible.'),
    ],
    2: [
        example('''
            texte_brut = "   Le TAL transforme des textes.   "
            texte_propre = texte_brut.strip()
            print("Résultat Q1 :", texte_propre)
            print("Résultat Q1b :", len(texte_brut), len(texte_propre))
            # Les six espaces de bord disparaissent ; les espaces intérieurs restent.
        ''', 'Les longueurs sont 35 puis 29. strip produit une nouvelle chaîne : texte_brut reste disponible.'),
        example('''
            texte_minuscule = texte_propre.lower()
            texte_transforme = texte_minuscule.replace("textes", "corpus")
            print("Résultat Q2 :", texte_transforme)
            print("Résultat Q2b :", "corpus" in texte_transforme, "textes" in texte_transforme)
            print(texte_propre)
        ''', 'Après Q1, mettez en minuscules puis remplacez textes par corpus. Les recherches donnent True puis False. Ici, textes est déjà en minuscules : inverser ces deux opérations donnerait le même résultat.'),
        example('''
            mot = "tokenisation"
            premier = mot[0]
            dernier = mot[-1]
            debut = mot[0:4]
            milieu = mot[1:5]
            print("Résultat Q3 :", premier, dernier, debut)
            print("Résultat Q3b :", milieu, len(mot))
            print(mot)
        ''', 'La borne de fin est exclue : [0:4] donne toke et [1:5] donne oken. Ces tranches ne changent pas les 12 caractères de mot.'),
        example('''
            phrase = "La traduction automatique aide parfois"
            tokens = phrase.split()
            print("Résultat Q4 :", tokens, tokens[2])
            print("Résultat Q4b :", len(tokens), tokens[-1])
            print(type(phrase), type(tokens), type(tokens[2]))
            print(len(phrase), len(tokens))
        ''', 'La liste compte cinq éléments. tokens[2] est le troisième élément, automatique ; phrase[2] serait un caractère de la chaîne.'),
        example('''
            phrase_avec_barres = " | ".join(tokens)
            tokens_reconstruits = phrase_avec_barres.split(" | ")
            print("Résultat Q5 :", phrase_avec_barres)
            print("Résultat Q5b :", tokens_reconstruits, tokens_reconstruits == tokens)
        ''', 'Réutilisez tokens de Q4. Le séparateur exact, espaces compris, permet de retrouver la même liste ; la comparaison vaut True.'),
        example('''
            exemples = ["  Bonjour  ", "TAL", "  Corpus Français"]
            exemple_0 = exemples[0].strip().lower()
            exemple_1 = exemples[1].strip().lower()
            exemple_2 = exemples[2].strip().lower()
            exemples_nettoyes = [exemple_0, exemple_1, exemple_2]
            print("Résultat Q6 :", exemples_nettoyes)
            print("Résultat Q6b :", exemples)
        ''', 'Traitez les trois chaînes séparément avec les notions de ce TD. Les accents et les espaces intérieurs sont conservés ; la liste exemples n’est pas modifiée.'),
        example('''
            phrase_limite = "L’analyse, c’est utile !"
            tokens_limite = phrase_limite.split()
            commentaire = "L’analyse, conserve sa virgule et son apostrophe ; ! devient un élément séparé car un espace le précède."
            print("Résultat Q7b :", tokens_limite)
            print("Résultat Q7 :", commentaire)
        ''', 'Voici une interprétation possible. Reliez votre propre commentaire aux fragments observés : split sépare selon les espaces, pas selon une analyse linguistique. La présence d’un commentaire ne valide pas son contenu.'),
    ],
    3: [
        example('''
            outils = ["corpus", "lexique", "concordancier"]
            outils.append("tokeniseur")
            print("Résultat Q1a :", outils)
            outils.pop()
            print("Résultat Q1 :", outils)
        ''', 'Placez le premier affichage après append et avant pop : il montre quatre éléments. Après le retrait du dernier, la liste retrouve ses trois éléments initiaux.'),
        example('''
            langues_romanes = ("français", "italien", "espagnol")
            choix_tuple = "Un tuple convient à cette collection ordonnée dont les éléments ne doivent pas être remplacés."
            print("Résultat Q2 :", type(langues_romanes), choix_tuple)
            print("Résultat Q2b :", langues_romanes)
        ''', 'Le tuple conserve l’ordre et ne permet pas de remplacer ses éléments. Adaptez la justification à votre compréhension ; sa présence ne suffit pas à valider son sens.'),
        example('''
            lexique = {"book": "livre", "language": "langage", "data": "données"}
            lexique["corpus"] = "corpus"
            print("Résultat Q3 :", lexique["language"])
            print("Résultat Q3b :", lexique)
        ''', 'Ajoutez corpus par sa clé puis consultez language. La traduction langue est également admise ; réutilisez votre choix en Q4.'),
        example('''
            entrees_lexique = []
            for anglais, francais in lexique.items():
                entrees_lexique.append(f"{anglais} -> {francais}")
            print("Résultat Q4 :", entrees_lexique)
        ''', 'Après Q3, items fournit chaque paire clé-valeur. La liste doit conserver les quatre correspondances ; l’ordre des entrées est libre.'),
        example('''
            formes = ["texte", "corpus", "texte", "donnée", "corpus", "analyse"]
            vocabulaire = set(formes)
            print("Résultat Q5 :", len(formes), len(vocabulaire))
            print("Résultat Q5b :", vocabulaire)
        ''', 'La liste compte six occurrences et l’ensemble quatre formes distinctes. L’ordre d’affichage d’un ensemble n’est pas un critère de réussite.'),
        example('''
            corpus_a = ["texte", "analyse", "langue", "corpus"]
            corpus_b = ["langue", "corpus", "modèle"]
            a = set(corpus_a)
            b = set(corpus_b)
            communs = a.intersection(b)
            seulement_a = a.difference(b)
            print("Résultat Q6 :", communs, seulement_a)
        ''', 'L’intersection contient langue et corpus ; la différence de a avec b contient texte et analyse. La différence dépend du sens de la comparaison.'),
    ],
    4: [
        example('''
            mots = ["TAL", "corpus", "analyse", "IA"]
            majuscules = []
            for mot in mots:
                majuscules.append(mot.upper())
            print("Résultat Q1 :", majuscules)
        ''', 'Parcourez les mots et ajoutez chaque transformation à la nouvelle liste, dans le même ordre.'),
        example('''
            mots_longs = []
            for mot in mots:
                if len(mot) > 5:
                    mots_longs.append(mot)
            print("Résultat Q2 :", mots_longs)
        ''', 'Réutilisez mots de Q1. Le test strictement supérieur à 5 conserve corpus et analyse.'),
        example('''
            mots_avec_a = []
            for mot in mots:
                if "a" in mot.lower():
                    mots_avec_a.append(mot)
            print("Résultat Q3 :", mots_avec_a)
        ''', 'Réutilisez mots de Q1. Testez une version en minuscules, puis conservez la forme initiale : TAL, analyse et IA.'),
        example('''
            positions_paires = list(range(0, 11, 2))
            print("Résultat Q4 :", positions_paires)
        ''', 'range exclut sa borne de fin. Avec 11 et un pas de 2, les positions vont de 0 à 10 inclus.'),
        example('''
            multiples = []
            multiple = 7
            while multiple <= 70:
                multiples.append(multiple)
                multiple += 7
            print("Résultat Q5 :", multiples)
        ''', 'Ajoutez le multiple avant de l’augmenter. L’incrément garantit que la boucle finit ; <= inclut 70.'),
        example('''
            mots_a_compter = "le TAL traite le langage et le texte".lower().split()
            frequences = {}
            for mot in mots_a_compter:
                if mot in frequences:
                    frequences[mot] += 1
                else:
                    frequences[mot] = 1
            print("Résultat Q6 :", frequences)
        ''', 'Une première occurrence crée une entrée ; les suivantes augmentent son compteur. le apparaît trois fois ; chaque autre forme apparaît une fois.'),
        example('''
            longueurs_mots_longs = [len(mot) for mot in mots if len(mot) > 5]
            print("Résultat Q7 :", longueurs_mots_longs)
        ''', 'Réutilisez mots de Q1. La compréhension filtre les mots puis conserve leur longueur : 6 et 7.'),
    ],
    5: [
        example('''
            def longueur_texte(texte):
                return len(texte)

            print("Résultat Q1 :", longueur_texte("TAL"), longueur_texte("corpus"))
        ''', 'return fournit le résultat à l’appelant. La même fonction donne 3 puis 6 selon l’argument reçu.'),
        example('''
            def normaliser(texte):
                return texte.strip().lower()

            print("Résultat Q2 :", normaliser("  Bonjour TAL  "))
        ''', 'strip retire les espaces de bord ; lower convertit les lettres en minuscules. Retournez la chaîne obtenue.'),
        example('''
            def nombre_mots(texte):
                return len(normaliser(texte).split())

            print("Résultat Q3 :", nombre_mots("  Le TAL traite les textes  "))
        ''', 'Après Q2, composez les traitements : normalisation, découpage, puis comptage des cinq éléments.'),
        example('''
            lexique = {"language": "langage", "data": "données", "book": "livre"}

            def traduire_mot(mot, lexique):
                mot = normaliser(mot)
                return lexique.get(mot, mot)

            print("Résultat Q4 :", traduire_mot("language", lexique), traduire_mot("Unknown", lexique))
        ''', 'Après Q2, normalisez la clé avant la recherche. get conserve le mot normalisé lorsqu’il est absent : Unknown devient unknown.'),
        example('''
            def traduire_phrase(phrase, lexique):
                mots_traduits = []
                for mot in phrase.split():
                    mots_traduits.append(traduire_mot(mot, lexique))
                return " ".join(mots_traduits)

            print("Résultat Q5 :", traduire_phrase("Language data", lexique))
        ''', 'Réutilisez traduire_mot et lexique de Q4 pour chaque mot, puis assemblez les traductions avec un espace.'),
        example('''
            def resume_texte(texte):
                texte_normalise = normaliser(texte)
                return {
                    "texte_normalise": texte_normalise,
                    "nb_caracteres": len(texte_normalise),
                    "nb_mots": nombre_mots(texte),
                }

            print("Résultat Q6 :", resume_texte("  Le TAL avance  "))
        ''', 'Réutilisez les fonctions de Q2 et Q3. Le résumé contient le texte normalisé, ses 13 caractères et ses 3 mots.'),
    ],
    6: [
        example('''
            with open("affiliations_s1.txt", encoding="utf-8") as fichier:
                texte_affiliations = fichier.read()
            print("Résultat Q1 :", len(texte_affiliations))
        ''', 'Exécutez d’abord la préparation du fichier fournie dans le TD. with ferme le fichier après lecture ; le texte fourni contient 156 caractères.'),
        example('''
            lignes = []
            for ligne in texte_affiliations.splitlines():
                if ligne.strip():
                    lignes.append(ligne)
            print("Résultat Q2 :", len(lignes))
        ''', 'Après Q1, splitlines sépare les lignes. Le test ligne.strip() écarte les lignes vides ou composées seulement d’espaces. Les cinq lignes de données sont conservées.'),
        example('''
            enregistrements = []
            for ligne in lignes:
                enregistrements.append(ligne.split(";", maxsplit=1))
            print("Résultat Q3 :", enregistrements[0])
            print("Résultat Q3b :", enregistrements)
        ''', 'Après Q2, séparez chaque ligne une seule fois au point-virgule. Gardez les cinq couples personne-affiliation dans l’ordre du fichier.'),
        example('''
            def normaliser_personne(identite):
                return " ".join(identite.split()).title()

            print("Résultat Q4 :", normaliser_personne("DURAND ALICE"))
            print("Résultat Q4b :", normaliser_personne("durand alice"), normaliser_personne("Durand Alice"), normaliser_personne("  Durand   Alice  "))
        ''', 'split puis join ramènent les espaces à un seul ; title harmonise ici la casse. Les quatre essais donnent Durand Alice. Cette règle simple n’est pas une règle générale pour tous les noms.'),
        example('''
            affiliations_par_personne = {}
            for personne, affiliation in enregistrements:
                personne = normaliser_personne(personne)
                if personne not in affiliations_par_personne:
                    affiliations_par_personne[personne] = set()
                affiliations_par_personne[personne].add(affiliation)
            print("Résultat Q5 :", affiliations_par_personne["Durand Alice"])
            print("Résultat Q5b :", affiliations_par_personne)
        ''', 'Après Q3 et Q4, normalisez avant de regrouper. Chaque ensemble élimine les affiliations répétées : Durand Alice en a deux et Martin Bob une.'),
        example('''
            import csv
            from pathlib import Path

            with open("affiliations_uniques.csv", "w", encoding="utf-8", newline="") as fichier:
                writer = csv.writer(fichier)
                writer.writerow(["personne", "nb_affiliations", "affiliations"])
                for personne, affiliations in affiliations_par_personne.items():
                    writer.writerow([personne, len(affiliations), " | ".join(affiliations)])
            print("Résultat Q6 :", repr(Path("affiliations_uniques.csv").read_text(encoding="utf-8")))
        ''', 'Après Q5, écrivez l’en-tête et une ligne par personne. La virgule sépare les colonnes ; | sépare les affiliations à l’intérieur d’une colonne. L’ordre des personnes et des affiliations est libre.'),
    ],
    7: [
        example('''
            import re
            texte = "Le tal traite parfois 12 documents en 2026."
            tal_present = bool(re.search("TAL", texte, re.IGNORECASE))
            print("Résultat Q1 :", tal_present)
        ''', 'search cherche dans tout le texte. IGNORECASE permet de trouver tal malgré la différence de casse ; bool donne True.'),
        example('''
            texte_nombres = "Version 2 : 14 corpus, 3 langues et 250 phrases."
            nombres = re.findall(r"[0-9]+", texte_nombres)
            print("Résultat Q2 :", nombres)
        ''', 'Après l’import de re, + regroupe les chiffres consécutifs. findall conserve l’ordre et renvoie des chaînes : 2, 14, 3 et 250.'),
        example('''
            texte_mots = "L’analyse, c’est déjà 2 étapes !"
            mots_regex = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", texte_mots)
            commentaire_mots = "La regex sépare L et analyse à l’apostrophe, tandis que split conserve L’analyse, dans un même élément."
            print("Résultat Q3 :", mots_regex, commentaire_mots)
        ''', 'Après l’import de re, la classe étendue conserve les lettres accentuées. Apostrophes, chiffres et ponctuation séparent les fragments. Comparez une différence observée dans votre propre commentaire.'),
        example('''
            journal = "Le 03/09/2026, Alice a relu 12 segments."
            journal_sans_date = re.sub(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", "[DATE]", journal)
            print("Résultat Q4 :", journal_sans_date)
        ''', 'Après l’import de re, les quantités exactes reconnaissent la forme JJ/MM/AAAA. Le nombre 12 reste présent. Reconnaître cette forme ne vérifie pas la validité d’une date dans le calendrier.'),
        example(r'''
            def nettoyer_texte(texte):
                texte = texte.lower()
                texte = re.sub(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", "[DATE]", texte)
                texte = re.sub(r"[0-9]+", "", texte)
                return " ".join(texte.split())

            print("Résultat Q5 :", nettoyer_texte("  Le 03/09/2026 comporte 12 exemples. "))
        ''', 'Après l’import de re, respectez l’ordre : minuscules, dates, chiffres, espaces. Le marqueur ajouté après lower reste en majuscules ; le point final reste présent.'),
        example('''
            def analyser_texte(texte):
                texte_nettoye = nettoyer_texte(texte)
                mots = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", texte_nettoye)
                frequences = {}
                for mot in mots:
                    frequences[mot] = frequences.get(mot, 0) + 1
                return {"texte_nettoye": texte_nettoye, "mots": mots, "frequences": frequences}

            print("Résultat Q6 :", analyser_texte("Le TAL, le TAL : 2 exemples."))
        ''', 'Réutilisez nettoyer_texte de Q5 et l’import de re. Comptez les fragments extraits : le et tal apparaissent deux fois. Sur un autre texte contenant une date, le motif extrairait aussi DATE du marqueur.'),
        example('''
            limite_regex = "Dans il est avocat et un avocat mûr, la même forme désigne un métier ou un fruit ; le contexte et une analyse sémantique aideraient à choisir le sens."
            print("Résultat Q7 :", limite_regex)
        ''', 'Voici un exemple possible : un cas concret, une ambiguïté que la seule forme ne résout pas et une information linguistique utile. Le correcteur constate seulement la présence d’une réponse ; relisez vous-même son argumentation.'),
    ],
}

# The principal call illustrates a method, not the full set of practice cases.
for _solution in SOLUTIONS[5]:
    _solution['solution_explanation'] += (' L’exemple illustre l’appel principal. Réalisez aussi les cas d’essai prévus dans le TD, '
                                         'notamment les entrées vides, les espaces ou les mots inconnus lorsque l’exercice les demande.')
for _solution in SOLUTIONS[7][3:6]:
    _solution['solution_explanation'] += ' Cet appel ne remplace pas les autres essais et les commentaires demandés dans le TD.'


def enrich_s1_details(notebook, evaluator, details):
    """Add evidence and examples without changing validation, points or contract."""
    match = re.fullmatch(r'td([1-7])(?:-(one|bis|ter))?-s1', evaluator)
    if not match:
        return details
    td = int(match[1])
    solutions = SOLUTIONS[td] if match[2] is None else []
    for number, detail in enumerate(details, 1):
        detail.update(answer_evidence(notebook, f'Q{number}'))
        if number <= len(solutions):
            solution = solutions[number - 1]
            detail.update(solution)
        state = detail.get('evaluation_status')
        detail['technical_diagnostic'] = detail.get('diagnostic', '')
        references = ', '.join(dict.fromkeys(re.findall(r'Q[0-9]+[a-z]?', detail.get('diagnostic', ''))))
        diagnostic = {
            'preuve_absente': 'Un affichage demandé est absent, répété ou inutilisable. Vérifiez les sorties et les lignes print ci-contre, puis réexécutez et enregistrez votre notebook.',
            'incorrect': 'Le résultat enregistré ne correspond pas à la valeur ou au type demandé. Comparez vos données et votre traitement aux consignes et à l’exemple de résolution.',
            'non_verifiable': 'Un affichage d’une étape précédente manque. Reprenez ces étapes, puis réexécutez cette question pour pouvoir vérifier le traitement demandé.',
            'construction_absente': 'La valeur affichée correspond au résultat attendu, mais le correcteur ne retrouve pas le traitement demandé pour la calculer. Comparez votre méthode aux consignes ; si vous avez utilisé une autre solution, signalez-la à l’enseignant.',
            'conforme': 'Les résultats enregistrés et le traitement repéré correspondent aux critères vérifiés. Relisez aussi les explications et les essais demandés dans le TD.',
        }.get(state)
        if diagnostic:
            if references and state in {'preuve_absente', 'non_verifiable'}:
                diagnostic = 'Affichage(s) à reprendre : ' + references + '. ' + diagnostic
            detail['diagnostic'] = diagnostic
        if not detail.get('diagnostic'):
            detail['diagnostic'] = ('Les affichages demandés sont retrouvés et conformes.'
                                    if detail['points'] == detail['max_points'] else
                                    'Reprenez les affichages demandés et comparez-les à l’exemple de résolution.')
        if state == 'conforme' or detail['points'] == detail['max_points']:
            detail['action'] = 'Vérifiez aussi les essais et les explications demandés dans l’énoncé : la note automatique ne valide pas leur contenu.'
        elif state == 'preuve_absente':
            detail['action'] = ('Retrouvez les lignes print ' + (references or 'demandées')
                                + ', activez-les après le calcul des variables, réexécutez les cellules dans l’ordre et enregistrez les sorties avant un nouvel envoi.')
        elif state == 'non_verifiable':
            detail['action'] = ('Rétablissez les affichages des étapes ' + (references or 'précédentes')
                                + ', puis relancez les cellules qui réutilisent leurs variables et enregistrez le notebook.')
        elif state == 'construction_absente':
            detail['action'] = 'Vérifiez que le résultat vient bien de la manipulation demandée, et non d’une valeur saisie directement. Présentez votre méthode à l’enseignant si le retour vous semble injustifié.'
        elif td == 2 and detail['points'] > 0:
            detail['action'] = 'Une partie des affichages est conforme. Repérez l’affichage encore à reprendre dans le diagnostic, comparez son opération et sa valeur à l’exemple, puis réexécutez et enregistrez.'
        else:
            detail['action'] = 'Comparez les données, l’opération, la valeur, le type et l’ordre des éléments aux consignes. Vérifiez les lignes print demandées, réexécutez puis enregistrez avant un nouvel envoi.'
    return details
