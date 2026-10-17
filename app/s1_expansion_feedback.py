"""Trusted resolution examples for the twelve S1 expansion notebooks.

Application-owned text, independent of model copies and submitted notebooks.
The evaluator only displays these examples; it never executes them. Examples
follow question order and reuse the preparation and functions indicated by
each explanation. They illustrate the requested result, not every practice case.
"""
from textwrap import dedent


def _example(source, explanation):
    return {'solution_code': dedent(source).strip(),
            'solution_explanation': explanation}


SOLUTIONS = {
    'td3-bis-s1': [
        _example(r'''
            langues_romanes = ("français", "italien", "espagnol")
            choix_tuple = "Les positions du tuple ne peuvent pas être réaffectées ; je conserve ainsi cette référence. Cela ne garantit pas l’exactitude de sa composition."
            print("Type de la référence :", type(langues_romanes))
            print("Mon choix :", choix_tuple)
            print("Résultat Q1 :", langues_romanes)
        ''', 'Les positions d’un tuple ne peuvent pas être remplacées. Cette stabilité ne garantit pas l’exactitude des valeurs choisies.'),
        _example(r'''
            codes = ("fr", "it", "es", "pt")
            code_unique = (codes[0],)
            codes_centraux = codes[1:3]
            print(type(code_unique), type(codes_centraux))
            print("Résultat Q2 :", code_unique, codes_centraux)
        ''', 'La virgule de (codes[0],) crée un tuple contenant une seule chaîne ; [1:3] conserve les indices 1 et 2.'),
        _example(r'''
            noms = ("Jean", "Sonia", "Maximilien")
            fiches_noms = []
            for nom_courant in noms:
                fiches_noms.append(f"{nom_courant} : {len(nom_courant)}")
            print("Résultat Q3 :", fiches_noms, noms)
        ''', 'Le parcours lit le tuple sans le modifier et enrichit une liste. Les longueurs sont 4, 5 et 10.'),
        _example(r'''
            fiche_personne = ("Alice", 22, 1.72)
            prenom_fiche, age_fiche, taille_fiche = fiche_personne
            print("Résultat Q4 :", prenom_fiche, age_fiche, taille_fiche)
        ''', 'Le déballage respecte l’ordre convenu : prénom, âge en années, taille en mètres.'),
        _example(r'''
            references = (("fr", "français"), ("it", "italien"), ("es", "espagnol"))
            fiches_langues = []
            for code, langue in references:
                fiches_langues.append(f"{code} -> {langue}")
            print("Résultat Q5 :", fiches_langues)
        ''', 'Le déballage dans la boucle conserve chaque association et l’ordre des paires.'),
        _example(r'''
            reference = ("français", "italien", "espagnol")
            reference_etendue = reference + ("portugais",)
            reference_revisee = ("roumain",) + reference[1:]
            print("Résultat Q6 :", reference, reference_etendue, reference_revisee)
        ''', 'La concaténation et les tranches construisent deux nouveaux tuples ; reference reste inchangé.'),
    ],
    'td3-one-s1': [
        _example(r'''
            mots = ["texte", "langue", "texte", "corpus", "analyse"]
            premier = mots[0]
            dernier = mots[-1]
            milieu = mots[1:4]
            print("Résultat Q1 :", premier, dernier, milieu)
        ''', 'Les indices commencent à 0 ; la borne finale de [1:4] est exclue. La liste source reste inchangée.'),
        _example(r'''
            outils = ["corpus", "lexique", "concordancier"]
            outils.append("tokeniseur")
            print("Résultat Q2a :", outils)
            outil_retire = outils.pop()
            print("Résultat Q2 :", outils, outil_retire)
        ''', 'Affichez les quatre outils après append, puis les trois outils restants et la valeur renvoyée par pop.'),
        _example(r'''
            noms = ["Anne", "Marc", "Louise", "Jean-Michel"]
            fiches_noms = []
            for nom_courant in noms:
                fiches_noms.append(f"{nom_courant} : {len(nom_courant)}")
            print("Résultat Q3 :", fiches_noms)
        ''', 'Initialisez la liste avant le parcours. Les longueurs sont 4, 4, 6 et 11, trait d’union compris.'),
        _example(r'''
            mois = ["Janvier", "Février", "Mars"]
            ligne_mois = ""
            for mois_courant in mois:
                print(mois_courant)
                ligne_mois = ligne_mois + mois_courant + " "
            ligne_mois = ligne_mois.strip()
            print("Résultat Q4 :", ligne_mois)
        ''', 'Le parcours affiche les mois et construit la ligne ; strip retire l’espace final de cette nouvelle chaîne.'),
        _example(r'''
            mois = ["Janvier", "Février", "Mars"]
            jours = [31, 28, 31]
            calendrier = []
            i = 0
            for mois_courant in mois:
                calendrier.append(mois_courant)
                calendrier.append(jours[i])
                i = i + 1
            print("Résultat Q5 :", calendrier)
        ''', 'Un même indice associe chaque mois à son nombre de jours. Les deux listes sources restent inchangées.'),
        _example(r'''
            reference = ["texte", "corpus", "langue"]
            revision = reference[:]
            revision[0] = "document"
            revision.append("analyse")
            print("Résultat Q6 :", reference, revision)
        ''', 'La tranche crée une autre liste. Une simple affectation donnerait deux noms à la même liste.'),
    ],
    'td3-ter-s1': [
        _example(r'''
            lexique = {"book": "livre", "language": "langage", "data": "données"}
            lexique["corpus"] = "corpus"
            print("Résultat Q1a :", lexique["language"])
            print("Résultat Q1b :", lexique)
            entrees_lexique = []
            for anglais, francais in lexique.items():
                entrees_lexique.append(f"{anglais} -> {francais}")
            print("Résultat Q1 :", entrees_lexique)
        ''', 'items fournit chaque paire clé-valeur. Les quatre entrées sont conservées ; langue est aussi accepté si ce choix reste cohérent dans les trois affichages.'),
        _example(r'''
            personnes = {"Alice": (22, 1.72), "Malo": (25, 1.80)}
            personnes["Zoé"] = (21, 1.65)
            fiche_malo = personnes["Malo"]
            taille_zoe = personnes["Zoé"][1]
            print("Résultat Q2 :", personnes, fiche_malo, taille_zoe)
        ''', 'Consultez d’abord la fiche de la personne, puis sa position : âge à l’indice 0, taille à l’indice 1.'),
        _example(r'''
            codes_langues = {"fr": "français", "it": "italien", "es": "espagnol"}
            codes_inverses = {}
            for code, langue in codes_langues.items():
                codes_inverses[langue] = code
            print("Résultat Q3 :", codes_inverses, len(codes_inverses))
        ''', 'Les trois valeurs distinctes deviennent trois clés. Avec deux valeurs identiques, une affectation remplacerait la précédente.'),
        _example(r'''
            formes = ["texte", "corpus", "texte", "donnée", "corpus", "analyse"]
            vocabulaire = set(formes)
            print("Résultat Q4 :", len(formes), len(vocabulaire))
            print("Résultat Q4b :", vocabulaire)
        ''', 'La liste contient six occurrences et l’ensemble quatre formes distinctes. L’ordre d’affichage de l’ensemble est libre.'),
        _example(r'''
            observations = ["français", "italien", "français", "espagnol", "italien"]
            langues_observees = set()
            for langue in observations:
                langues_observees.add(langue)
            print("Résultat Q5 :", langues_observees, len(langues_observees), "français" in langues_observees, "allemand" in langues_observees)
        ''', 'add conserve trois langues distinctes malgré les cinq observations. Les tests donnent True, puis False.'),
        _example(r'''
            corpus_a = ["texte", "analyse", "langue", "corpus"]
            corpus_b = ["langue", "corpus", "modèle"]
            vocabulaire_a = set(corpus_a)
            vocabulaire_b = set(corpus_b)
            communs = vocabulaire_a & vocabulaire_b
            seulement_a = vocabulaire_a - vocabulaire_b
            seulement_b = vocabulaire_b - vocabulaire_a
            print("Résultat Q6 :", communs, seulement_a, seulement_b)
        ''', 'L’intersection contient langue et corpus ; A-B contient texte et analyse, B-A contient modèle. Les ensembles ne conservent ni fréquences ni positions.'),
    ],
    'td4-bis-s1': [
        _example(r'''
            positions_paires = list(range(0, 11, 2))
            print("Résultat Q1 :", positions_paires)
        ''', 'La borne 11 est exclue : avec un pas de 2, la liste va de 0 à 10 inclus.'),
        _example(r'''
            positions_inversees = list(range(10, -1, -2))
            positions_vides = list(range(10, -1, 2))
            print("Résultat Q2 :", positions_inversees, positions_vides)
        ''', 'La descente exclut -1 et inclut 0 ; un pas positif ne permet pas de descendre de 10 vers -1.'),
        _example(r'''
            multiple = 7
            multiples = []
            while multiple <= 70:
                multiples.append(multiple)
                multiple = multiple + 7
            print("Résultat Q3 :", multiples)
            print("Résultat Q3b :", multiple)
        ''', 'La boucle conserve les multiples de 7 jusqu’à 70 ; à 77, la condition devient fausse.'),
        _example(r'''
            table_sept = []
            terme = 7
            compteur = 0
            while compteur < 20:
                table_sept.append(terme)
                terme = terme + 7
                compteur = compteur + 1
            nombre_termes = compteur
            print("Résultat Q4 :", table_sept, nombre_termes)
        ''', 'Un compteur distinct garantit vingt termes : le premier est 7 et le dernier 140.'),
        _example(r'''
            multiples_retenus = []
            for rang in range(1, 51):
                candidat = rang * 13
                if candidat % 7 == 0:
                    multiples_retenus.append(candidat)
            print("Résultat Q5 :", multiples_retenus)
        ''', 'range(1, 51) parcourt les cinquante rangs positifs. Le filtre retient 91, 182, 273, 364, 455, 546 et 637.'),
        _example(r'''
            a = 1
            b = 30
            somme_et = 0
            somme_ou = 0
            for entier in range(a, b + 1):
                if entier % 3 == 0 and entier % 5 == 0:
                    somme_et = somme_et + entier
                if entier % 3 == 0 or entier % 5 == 0:
                    somme_ou = somme_ou + entier
            print("Résultat Q6 :", somme_et, somme_ou)
        ''', 'Les bornes 1 et 30 sont incluses. and donne 45 ; or donne 225, sans compter deux fois les multiples communs.'),
    ],
    'td4-one-s1': [
        _example(r'''
            mots = ["TAL", "corpus", "analyse", "IA"]
            majuscules = []
            for mot in mots:
                majuscules.append(mot.upper())
            print("Résultat Q1 :", majuscules)
        ''', 'La boucle conserve les quatre positions et laisse mots inchangée.'),
        _example(r'''
            mots_longs = []
            for mot in mots:
                if len(mot) > 5:
                    mots_longs.append(mot)
            print("Résultat Q2 :", mots_longs)
        ''', 'Reprenez mots de Q1. Le seuil strict > 5 conserve corpus et analyse.'),
        _example(r'''
            mots_avec_a = []
            for mot in mots:
                if "a" in mot.lower():
                    mots_avec_a.append(mot)
            print("Résultat Q3 :", mots_avec_a)
        ''', 'Reprenez mots de Q1. Testez la version en minuscules et ajoutez le mot original : TAL, analyse, IA.'),
        _example(r'''
            chaine_revue = "Revue"
            chaine_ete = "ÉTÉ"
            chaine_vide = ""
            presence_revue = "e" in chaine_revue.lower()
            presence_ete = "e" in chaine_ete.lower()
            presence_vide = "e" in chaine_vide.lower()
            print("Résultat Q4 :", presence_revue, presence_ete, presence_vide)
        ''', 'Les résultats sont True, False, False : lower conserve les accents et la chaîne vide ne contient pas e.'),
        _example(r'''
            prenoms = ["Jean", "Maximilien", "Brigitte", "Sonia", "Jean-Pierre", "Sandra"]
            prenoms_courts = []
            prenoms_longs = []
            for prenom_lu in prenoms:
                if len(prenom_lu) < 6:
                    prenoms_courts.append(prenom_lu)
                else:
                    prenoms_longs.append(prenom_lu)
            print("Résultat Q5 :", prenoms_courts, prenoms_longs)
        ''', 'Le test < 6 classe Sonia parmi les courts et Sandra parmi les longs. Chaque occurrence emprunte une seule branche.'),
        _example(r'''
            nombres = [32, 5, 12, 8, 3, 75, 2, 15]
            pairs = []
            impairs = []
            for nombre in nombres:
                if nombre % 2 == 0:
                    pairs.append(nombre)
                else:
                    impairs.append(nombre)
            print("Résultat Q6 :", pairs, impairs)
        ''', 'Le reste modulo 2 distingue pairs et impairs. Les deux listes gardent l’ordre relatif de la source.'),
    ],
    'td4-ter-s1': [
        _example(r'''
            texte = "Le texte est une donnée"
            nombre_e = 0
            for caractere in texte.lower():
                if caractere == "e":
                    nombre_e = nombre_e + 1
            print("Résultat Q1 :", nombre_e)
        ''', 'Le comptage donne 6 ; lower ne transforme pas é en e.'),
        _example(r'''
            nombres = [32, 5, 12, 8, 3, 75, 2, 15]
            negatifs = [-8, -3, -12]
            maximum_nombres = nombres[0]
            for nombre in nombres:
                if nombre > maximum_nombres:
                    maximum_nombres = nombre
            maximum_negatifs = negatifs[0]
            for nombre in negatifs:
                if nombre > maximum_negatifs:
                    maximum_negatifs = nombre
            print("Résultat Q2 :", maximum_nombres, maximum_negatifs)
        ''', 'Initialisez chaque candidat avec un élément de sa liste. Les maxima sont 75 et -3, sans max ni tri.'),
        _example(r'''
            animaux = ["chat", "chien", "chat", "oiseau", "chien", "chat"]
            frequences_animaux = {}
            for animal in animaux:
                if animal in frequences_animaux:
                    frequences_animaux[animal] = frequences_animaux[animal] + 1
                else:
                    frequences_animaux[animal] = 1
            print("Résultat Q3 :", frequences_animaux)
        ''', 'La première occurrence crée la clé ; les suivantes augmentent son effectif : chat 3, chien 2, oiseau 1.'),
        _example(r'''
            mots_a_compter = "le TAL traite le langage et le texte".lower().split()
            frequences = {}
            for mot in mots_a_compter:
                frequences[mot] = frequences.get(mot, 0) + 1
            frequences_autrement = {}
            for mot in mots_a_compter:
                if mot in frequences_autrement:
                    frequences_autrement[mot] = frequences_autrement[mot] + 1
                else:
                    frequences_autrement[mot] = 1
            total_effectifs = 0
            for forme, effectif in frequences.items():
                total_effectifs = total_effectifs + effectif
            print("Résultat Q4 :", frequences, frequences_autrement, total_effectifs, len(mots_a_compter))
        ''', 'Les écritures avec get et avec if/else donnent les mêmes fréquences. Leur total vaut 8, comme la longueur de la liste.'),
        _example(r'''
            mots = ["TAL", "corpus", "analyse", "IA"]
            longueurs_tous = [len(mot) for mot in mots]
            print("Résultat Q5 :", longueurs_tous)
        ''', 'La compréhension transforme chaque mot en longueur : 3, 6, 7 et 2, sans filtrer.'),
        _example(r'''
            longueurs_mots_longs = [len(mot) for mot in mots if len(mot) > 5]
            print("Résultat Q6 :", longueurs_mots_longs)
        ''', 'Reprenez mots de Q5. Le filtre conserve les mots de plus de 5 caractères ; la transformation conserve leurs longueurs, 6 et 7.'),
    ],
    'td5-bis-s1': [
        _example(r'''
            def etiquette(categorie, contenu):
                return categorie + " : " + contenu
            print("Résultat Q1 :", etiquette("source", "archive"), etiquette("archive", "source"))
        ''', 'Les arguments sont associés aux paramètres dans l’ordre : les inverser échange la catégorie et le contenu.'),
        _example(r'''
            texte = "Archives"
            def preparer_local(texte):
                texte = texte.lower()
                return texte
            print("Résultat Q2 :", preparer_local("MUSÉE"), texte)
        ''', 'La réaffectation du paramètre texte reste locale : l’appel retourne musée et la variable extérieure reste Archives.'),
        _example(r'''
            def volume_defaut(longueur=10, largeur=10, hauteur=10):
                return longueur * largeur * hauteur
            print("Résultat Q3 :", volume_defaut(), volume_defaut(5), volume_defaut(5, 3), volume_defaut(5, 3, 2))
        ''', 'Les arguments omis gardent la valeur 10. Les quatre volumes sont 1000, 500, 150 et 30.'),
        _example(r'''
            def saluer(personne, formule="Bonjour"):
                return formule + " " + personne
            print("Résultat Q4 :", saluer("Ada"), saluer("Zoé", "Bonsoir"))
        ''', 'Le premier appel conserve Bonjour ; le second remplace cette valeur par Bonsoir.'),
        _example(r'''
            lexique = {"language": "langage", "data": "données", "book": "livre"}
            def traduire_mot(mot, lexique):
                mot_normalise = mot.strip().lower()
                if mot_normalise in lexique:
                    return lexique[mot_normalise]
                return mot_normalise
            print("Résultat Q5 :", traduire_mot("language", lexique), traduire_mot("Unknown", lexique))
        ''', 'Normalisez le mot puis consultez le dictionnaire reçu. Un mot inconnu est retourné sous sa forme normalisée.'),
        _example(r'''
            autre_lexique = {"book": "livret", "data": "données"}
            def traduire_ou_signaler(mot, lexique, absence="?"):
                mot_normalise = mot.strip().lower()
                if mot_normalise in lexique:
                    return lexique[mot_normalise]
                return absence
            print("Résultat Q6 :", traduire_ou_signaler(" BOOK ", autre_lexique), traduire_ou_signaler("Mystery", autre_lexique), traduire_ou_signaler("Mystery", autre_lexique, "absent"))
        ''', 'Le dictionnaire reçu donne livret ; un mot absent donne ? par défaut ou la valeur "absent" donnée au troisième argument.'),
    ],
    'td5-one-s1': [
        _example(r'''
            def longueur_texte(texte):
                return len(texte)
            print("Résultat Q1 :", longueur_texte("TAL"), longueur_texte("corpus"))
        ''', 'len retourne un entier ; les deux appels donnent 3 et 6.'),
        _example(r'''
            def ligne_caracteres(nombre, caractere):
                return caractere * nombre

            ligne_encadree = "[" + ligne_caracteres(5, "-") + "]"
            print(ligne_encadree)
            print("Résultat Q2 :", ligne_caracteres(4, "*"), ligne_caracteres(3, "é"))
        ''', 'La multiplication répète le caractère. La valeur retournée peut être réutilisée pour ajouter les crochets.'),
        _example(r'''
            def volume_boite(longueur, largeur, hauteur):
                return longueur * largeur * hauteur
            print("Résultat Q3 :", volume_boite(2, 3, 4), volume_boite(0, 3, 4))
        ''', 'Le produit des dimensions donne 24 et 0 ; la même définition accepte des dimensions décimales.'),
        _example(r'''
            def maximum3(a, b, c):
                if a >= b and a >= c:
                    return a
                if b >= c:
                    return b
                return c
            print("Résultat Q4 :", maximum3(2, 7, 4), maximum3(-2, -7, -4))
        ''', 'Les comparaisons choisissent une valeur maximale, y compris en cas d’égalité et avec des nombres négatifs.'),
        _example(r'''
            def normaliser(texte):
                return texte.strip().lower()
            print("Résultat Q5 :", normaliser("  Bonjour TAL  "))
        ''', 'strip retire les espaces de bord et lower met en minuscules. Les espaces intérieurs sont conservés.'),
        _example(r'''
            def annoncer_atelier(theme):
                return "Au programme : " + normaliser(theme)
            print("Résultat Q6 :", annoncer_atelier("  CORPUS  "))
        ''', 'Réutilisez normaliser de Q5. Le préfixe exact est concaténé au thème normalisé et reste présent si le thème est vide.'),
    ],
    'td5-ter-s1': [
        _example(r'''
            def compte_caractere(caractere, texte):
                total = 0
                for courant in texte:
                    if courant == caractere:
                        total = total + 1
                return total
            print("Résultat Q1 :", compte_caractere("e", "texte"), compte_caractere("é", "été"))
        ''', 'La boucle compte les caractères exacts, sans normalisation : deux e dans texte, deux é dans été.'),
        _example(r'''
            def nombre_mots(texte):
                texte_normalise = normaliser(texte)
                return len(texte_normalise.split())
            print("Résultat Q2 :", nombre_mots("  Le TAL traite les textes  "))
        ''', 'Réutilisez normaliser fourni dans le TD, puis split et len. Le résultat demandé est 5 ; une chaîne vide donne 0.'),
        _example(r'''
            def traduire_phrase(phrase, lexique):
                traductions = []
                for fragment in phrase.split():
                    traductions.append(traduire_mot(fragment, lexique))
                return " ".join(traductions)
            print("Résultat Q3 :", traduire_phrase("Language data", lexique))
        ''', 'Réutilisez traduire_mot et lexique fournis dans le TD. Chaque fragment est traduit puis join les réunit avec un espace.'),
        _example(r'''
            def resume_texte(texte):
                texte_normalise = normaliser(texte)
                return {"texte_normalise": texte_normalise,
                        "nb_caracteres": len(texte_normalise),
                        "nb_mots": nombre_mots(texte_normalise)}
            print("Résultat Q4 :", resume_texte("  Le TAL avance  "))
        ''', 'Réutilisez normaliser fourni et nombre_mots de Q2. Le texte normalisé contient 13 caractères et 3 fragments.'),
        _example(r'''
            lexique_expressions = {"data": "jeu de données", "book": "livre"}
            def mesurer_traduction(phrase, lexique):
                traduction = traduire_phrase(phrase, lexique)
                return {"traduction": traduction,
                        "mots_source": nombre_mots(phrase),
                        "mots_cible": nombre_mots(traduction)}
            print("Résultat Q5 :", mesurer_traduction("data book", lexique_expressions))
        ''', 'Réutilisez traduire_phrase de Q3 et nombre_mots de Q2 : la source a 2 fragments, la traduction jeu de données livre en a 4.'),
        _example(r'''
            def resumer_corpus(textes):
                resumes = []
                for texte in textes:
                    resumes.append(resume_texte(texte))
                return resumes
            print("Résultat Q6 :", resumer_corpus(["  TAL  ", ""]))
        ''', 'Réutilisez resume_texte de Q4 pour chaque élément, sans modifier la liste. L’ordre et les doublons sont conservés ; une liste vide reste vide.'),
    ],
    'td6-bis-s1': [
        _example(r'''
            with open("affiliations_s1.txt", "r", encoding="utf-8") as fichier:
                texte_affiliations = fichier.read()
            enregistrements = []
            for ligne in texte_affiliations.splitlines():
                if ligne.strip() != "":
                    identite, affiliation = ligne.split(";", 1)
                    enregistrements.append((identite, affiliation))
            print("Résultat Q1 :", enregistrements[0])
            print("Résultat Q1b :", enregistrements)
        ''', 'Exécutez la préparation. Le découpage au premier point-virgule conserve les graphies brutes et les cinq couples dans leur ordre.'),
        _example(r'''
            fiches = [("Bernard", "Élodie", "83000"), ("Lamy", "Zoé", "06000"), ("Petit", "Chloé", "83000")]
            with open("personnes_s1.txt", "w", encoding="utf-8") as fichier:
                for fiche in fiches:
                    fichier.write(";".join(fiche) + "\n")
            with open("personnes_s1.txt", "r", encoding="utf-8") as fichier:
                fiches_relues = fichier.read()
            print("Résultat Q2 :", repr(fiches_relues))
        ''', 'Une ligne contient nom, prénom et code postal, séparés par des points-virgules. Le code 06000 reste une chaîne.'),
        _example(r'''
            with open("personnes_s1.txt", "r", encoding="utf-8") as fichier:
                lignes_personnes = fichier.read().splitlines()
            personnes_83000 = []
            for ligne in lignes_personnes:
                nom_fiche, prenom_fiche, code_postal = ligne.split(";")
                if code_postal == "83000":
                    personnes_83000.append((nom_fiche, prenom_fiche))
            print("Résultat Q3 :", personnes_83000)
        ''', 'Reprenez le fichier produit en Q2. Le filtre conserve Bernard Élodie et Petit Chloé dans l’ordre, sans le code postal.'),
        _example(r'''
            def normaliser_personne(identite):
                return " ".join(identite.strip().split()).title()
            print("Résultat Q4 :", normaliser_personne("DURAND ALICE"), normaliser_personne("durand alice"), normaliser_personne("Durand Alice"), normaliser_personne("  Durand   Alice  "))
        ''', 'split puis join réduisent les espaces et title harmonise ici la casse. Les quatre variantes donnent Durand Alice ; cette égalité ne prouve pas l’identité réelle.'),
        _example(r'''
            affiliations_par_personne = {}
            for identite, affiliation in enregistrements:
                personne = normaliser_personne(identite)
                if personne not in affiliations_par_personne:
                    affiliations_par_personne[personne] = set()
                affiliations_par_personne[personne].add(affiliation)
            print("Résultat Q5 :", affiliations_par_personne["Durand Alice"])
            print("Résultat Q5b :", affiliations_par_personne)
        ''', 'Reprenez enregistrements de Q1 et normaliser_personne de Q4. Les ensembles gardent deux affiliations distinctes pour Durand Alice et une pour Martin Bob.'),
        _example(r'''
            Path("affiliations_atelier.txt").write_text("lamy zoé;Studio;annexe\n\n LAMY   ZOÉ ;Musée\nlamy zoé;Studio;annexe\n   \nPetit chloé;Musée\n", encoding="utf-8")
            with open("affiliations_atelier.txt", "r", encoding="utf-8") as fichier:
                texte_atelier = fichier.read()
            groupes_atelier = {}
            for ligne in texte_atelier.splitlines():
                if ligne.strip() != "":
                    identite, affiliation = ligne.split(";", 1)
                    personne = normaliser_personne(identite)
                    if personne not in groupes_atelier:
                        groupes_atelier[personne] = set()
                    groupes_atelier[personne].add(affiliation)
            print("Résultat Q6 :", groupes_atelier)
        ''', 'Réutilisez normaliser_personne de Q4. split(";", 1) garde Studio;annexe dans une seule affiliation ; les lignes blanches sont ignorées et les doublons éliminés.'),
    ],
    'td6-one-s1': [
        _example(r'''
            with open("affiliations_s1.txt", "r", encoding="utf-8") as fichier:
                texte_affiliations = fichier.read()
            print("Résultat Q1 :", len(texte_affiliations))
        ''', 'Exécutez d’abord la préparation fournie. read conserve les 156 caractères, fins de ligne comprises ; with ferme le fichier après le bloc.'),
        _example(r'''
            lignes = []
            for ligne in texte_affiliations.splitlines():
                if ligne.strip() != "":
                    lignes.append(ligne)
            print("Résultat Q2 :", len(lignes), lignes)
        ''', 'Reprenez texte_affiliations de Q1. Le test strip écarte les lignes blanches ; l’ajout conserve le texte initial des cinq lignes utiles.'),
        _example(r'''
            with open("note_lecture.txt", "w", encoding="utf-8") as fichier:
                fichier.write("Corpus ouvert\n")
                fichier.write("Analyse à vérifier\n")
            with open("note_lecture.txt", "r", encoding="utf-8") as fichier:
                note_relue = fichier.read()
            print("Résultat Q3 :", repr(note_relue))
        ''', 'Écrivez puis relisez les deux lignes en UTF-8. repr rend visibles les deux fins de ligne.'),
        _example(r'''
            with open("lignes_blanches.txt", "r", encoding="utf-8") as fichier:
                texte_lignes = fichier.read()
            lignes_utiles = []
            for ligne in texte_lignes.splitlines():
                if ligne.strip() != "":
                    lignes_utiles.append(ligne)
            with open("lignes_utiles.txt", "w", encoding="utf-8") as fichier:
                for ligne in lignes_utiles:
                    fichier.write(ligne + "\n")
            with open("lignes_utiles.txt", "r", encoding="utf-8") as fichier:
                texte_utile_relu = fichier.read()
            print("Résultat Q4 :", lignes_utiles, repr(texte_utile_relu))
        ''', 'Exécutez la préparation. strip sert uniquement au test : les espaces de bord de Salle A sont conservés dans le fichier de sortie.'),
        _example(r'''
            with open("phrases_s1.txt", "r", encoding="utf-8") as fichier:
                phrases = fichier.read().splitlines()
            ligne_plus_longue = ""
            for ligne in phrases:
                if len(ligne) > len(ligne_plus_longue):
                    ligne_plus_longue = ligne
            print("Résultat Q5 :", ligne_plus_longue, len(ligne_plus_longue))
        ''', 'Exécutez la préparation. splitlines exclut les fins de ligne du calcul ; l’initialisation à une chaîne vide traite aussi un fichier vide.'),
        _example(r'''
            with open("texte_espaces.txt", "r", encoding="utf-8") as fichier:
                texte_source = fichier.read()
            texte_triple = texte_source.replace(" ", "   ")
            with open("texte_espaces_triples.txt", "w", encoding="utf-8") as fichier:
                fichier.write(texte_triple)
            with open("texte_espaces_triples.txt", "r", encoding="utf-8") as fichier:
                texte_triple_relu = fichier.read()
            print("Résultat Q6 :", repr(texte_triple_relu))
        ''', 'Exécutez la préparation. replace transforme chaque espace en trois espaces ; la relecture conserve les accents, la ponctuation et les fins de ligne.'),
    ],
    'td6-ter-s1': [
        _example(r'''
            with open("documents_s1.csv", "w", encoding="utf-8", newline="") as fichier:
                ecrivain = csv.writer(fichier)
                ecrivain.writerow(["document", "pages"])
                ecrivain.writerow(["rapport", 12])
                ecrivain.writerow(["note", 3])
            with open("documents_s1.csv", "r", encoding="utf-8", newline="") as fichier:
                documents_relus = list(csv.reader(fichier))
            print("Résultat Q1 :", documents_relus)
        ''', 'Après la préparation et l’import de csv fourni dans le cours, writer écrit l’en-tête et les deux documents ; reader relit les pages comme des chaînes.'),
        _example(r'''
            with open("lieux_s1.csv", "r", encoding="utf-8", newline="") as fichier:
                lieux_relus = list(csv.reader(fichier))
            print("Résultat Q2 :", lieux_relus)
        ''', 'Après la préparation et l’import de csv, reader conserve Musée, aile nord dans une seule cellule ; chaque ligne contient deux colonnes.'),
        _example(r'''
            with open("personnes_s1.csv", "r", encoding="utf-8", newline="") as fichier:
                personnes_relues = list(csv.reader(fichier))
            noms_83000 = []
            for fiche in personnes_relues[1:]:
                if fiche[2] == "83000":
                    noms_83000.append(fiche[0] + " " + fiche[1])
            print("Résultat Q3 :", noms_83000)
        ''', 'Après la préparation et l’import de csv, la tranche exclut l’en-tête. Le test compare les codes comme des chaînes et conserve les accents.'),
        _example(r'''
            with open("affiliations_s1.txt", "r", encoding="utf-8") as fichier:
                texte_affiliations = fichier.read()
            affiliations_par_personne = {}
            for ligne in texte_affiliations.splitlines():
                if ligne.strip() != "":
                    identite, affiliation = ligne.split(";", 1)
                    personne = normaliser_personne(identite)
                    if personne not in affiliations_par_personne:
                        affiliations_par_personne[personne] = set()
                    affiliations_par_personne[personne].add(affiliation)
            print("Résultat Q4 :", affiliations_par_personne)
        ''', 'Après la préparation, réutilisez normaliser_personne fourni. Le dictionnaire associe chaque personne à ses affiliations distinctes, sans doublons.'),
        _example(r'''
            with open("affiliations_uniques.csv", "w", encoding="utf-8", newline="") as fichier:
                ecrivain = csv.writer(fichier)
                ecrivain.writerow(["personne", "nb_affiliations", "affiliations"])
                for personne in sorted(affiliations_par_personne):
                    affiliations = affiliations_par_personne[personne]
                    ecrivain.writerow([personne, len(affiliations), " | ".join(sorted(affiliations))])
            with open("affiliations_uniques.csv", "r", encoding="utf-8", newline="") as fichier:
                affiliations_relues = list(csv.reader(fichier))
            print("Résultat Q5 :", affiliations_relues)

            with open("affiliations_uniques.csv", "r", encoding="utf-8", newline="") as verification_texte:
                print("Texte CSV relu :", repr(verification_texte.read()))
        ''', 'Reprenez les groupes de Q4 et l’import de csv. Chaque ligne contient la personne, le nombre de valeurs distinctes et leur assemblage par | ; reader relit les trois colonnes.'),
        _example(r'''
            groupes_nouveaux = {"Lamy Zoé": {"Musée", "Centre, langues"}, "Petit Chloé": {"Équipe TAL"}}
            with open("affiliations_nouvelles.csv", "w", encoding="utf-8", newline="") as fichier:
                ecrivain = csv.writer(fichier)
                ecrivain.writerow(["personne", "nb_affiliations", "affiliations"])
                for personne in sorted(groupes_nouveaux):
                    affiliations = groupes_nouveaux[personne]
                    ecrivain.writerow([personne, len(affiliations), " | ".join(sorted(affiliations))])
            with open("affiliations_nouvelles.csv", "r", encoding="utf-8", newline="") as fichier:
                nouveaux_relus = list(csv.reader(fichier))
            print("Résultat Q6 :", nouveaux_relus)
        ''', 'Après l’import de csv, le tri fixe l’ordre des personnes et des affiliations. writer protège la virgule de Centre, langues ; reader restitue trois colonnes par ligne.'),
    ],
}
