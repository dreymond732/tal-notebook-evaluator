"""Mesures contrôlables sur mots, passages et phrases tokenisées."""
from __future__ import annotations

from collections import Counter
import math
import re
from typing import Literal, Sequence, TypedDict


class Concordance(TypedDict):
    debut: int
    fin: int
    pivot: str
    gauche: str
    droite: str


class Mesure(TypedDict):
    N: int
    cooc: int
    marge_pivot: int
    marge_associe: int
    indices_cooc: list[int]
    agregation: Literal["union", "somme_paires"]


class Contingence(TypedDict):
    n11: int
    n10: int
    n01: int
    n00: int


def frequences(tokens: Sequence[str], *, minimum: int = 1) -> list[dict]:
    """Occurrences des tokens fournis, classement déterministe ; aucun filtrage implicite."""
    if minimum < 1:
        raise ValueError("minimum doit être >= 1")
    comptes = Counter(tokens)
    total = sum(comptes.values())
    return [
        {"terme": t, "effectif": n, "total": total, "pour_mille": 1000 * n / total}
        for t, n in sorted(comptes.items(), key=lambda pair: (-pair[1], pair[0]))
        if n >= minimum
    ]


def _concordance(source: str, debut: int, fin: int, largeur: int) -> Concordance:
    return {
        "debut": debut, "fin": fin, "pivot": source[debut:fin],
        "gauche": source[max(0, debut - largeur):debut], "droite": source[fin:fin + largeur],
    }


def concordances_exactes(source: str, motif: str, largeur: int = 20) -> list[Concordance]:
    """Cherche sans chevauchement ; bornes en caractères du texte original."""
    if not motif:
        raise ValueError("Le motif doit être non vide")
    if largeur < 0:
        raise ValueError("La largeur doit être positive ou nulle")
    trouvailles: list[Concordance] = []
    position = 0
    while (debut := source.find(motif, position)) != -1:
        fin = debut + len(motif)
        trouvailles.append(_concordance(source, debut, fin, largeur))
        position = fin
    return trouvailles


def concordances_mot(source: str, mot: str, largeur: int = 45) -> list[Concordance]:
    r"""Cherche une graphie entière sans distinguer la casse, avec les frontières Unicode \b.

    Le mot est littéral, sans espace et avec un caractère de mot à chaque extrémité.
    Les bornes [debut:fin] et les contextes, en caractères, se rapportent au texte reçu.
    """
    if not re.fullmatch(r"\w(?:\S*\w)?", mot):
        raise ValueError("Saisissez un mot dont les extrémités sont des caractères de mot.")
    if largeur < 0:
        raise ValueError("La largeur doit être positive ou nulle")
    motif = r"\b" + re.escape(mot) + r"\b"
    return [_concordance(source, m.start(), m.end(), largeur)
            for m in re.finditer(motif, source, flags=re.IGNORECASE)]


def contient_expression(tokens: Sequence[str], expression: Sequence[str]) -> bool:
    """Une expression est une suite CONTIGUË et ordonnée de tokens."""
    if not expression:
        raise ValueError("Une expression vide est ambiguë")
    taille = len(expression)
    return any(list(tokens[i:i + taille]) == list(expression)
               for i in range(len(tokens) - taille + 1))


def mesurer(
    contextes: Sequence[Sequence[str]],
    pivots: Sequence[Sequence[str]],
    associes: Sequence[Sequence[str]],
    agregation: Literal["union", "somme_paires"] = "union",
) -> Mesure:
    """Un contexte = une phrase.

    union : chaque phrase contenant au moins un pivot ET un associé compte une fois.
    somme_paires : somme des présences de chaque couple d'expressions, potentiellement
    supérieure au nombre de phrases. indices_cooc est dans les deux cas l'union
    des indices des phrases communes, PAS la somme des contributions des paires.
    """
    if agregation not in {"union", "somme_paires"}:
        raise ValueError("Agrégation inconnue")
    if not pivots or not associes:
        raise ValueError("Préciser au moins un pivot et un associé")
    if any(not expr for expr in [*pivots, *associes]):
        raise ValueError("Expression vide non permise")

    indices: list[int] = []
    marg_p = marg_a = cooc = 0
    for i, tokens in enumerate(contextes):
        presence_p = [contient_expression(tokens, p) for p in pivots]
        presence_a = [contient_expression(tokens, a) for a in associes]
        est_p = any(presence_p)
        est_a = any(presence_a)
        marg_p += int(est_p)
        marg_a += int(est_a)
        if est_p and est_a:
            indices.append(i)
            cooc += 1 if agregation == "union" else sum(presence_p) * sum(presence_a)
    return {
        "N": len(contextes), "cooc": cooc,
        "marge_pivot": marg_p, "marge_associe": marg_a,
        "indices_cooc": indices, "agregation": agregation,
    }


def table_contingence(mesure: Mesure) -> Contingence:
    """Table 2x2 de PRÉSENCES par phrase ; impossible pour somme_paires."""
    if mesure["agregation"] != "union":
        raise ValueError("Table 2x2 impossible avec une somme de paires")
    n = mesure["N"]
    p = mesure["marge_pivot"]
    a = mesure["marge_associe"]
    c = mesure["cooc"]
    cellules = (c, p - c, a - c, n - p - a + c)
    if any(x < 0 for x in cellules) or sum(cellules) != n:
        raise ValueError("Marges ou cooccurrence incohérentes")
    return dict(zip(("n11", "n10", "n01", "n00"), cellules))  # type: ignore[return-value]


def proportion(numerateur: int, denominateur: int) -> float | None:
    """Pas de fausse proportion zéro si le dénominateur est nul."""
    if numerateur < 0 or denominateur < 0:
        raise ValueError("Effectifs négatifs")
    if denominateur == 0:
        return None
    if numerateur > denominateur:
        raise ValueError("Numérateur supérieur au dénominateur")
    return numerateur / denominateur


def pour_mille(effectif: int, taille: int) -> float | None:
    p = proportion(effectif, taille)
    return None if p is None else 1000 * p


def pmi_phrase(mesure: Mesure) -> float | None:
    """PMI en base 2, uniquement pour une union de présences par phrase.

    None signifie que la valeur n'est pas définie, notamment pour cooc=0.
    """
    table_contingence(mesure)
    n, c, p, a = (mesure[k] for k in ("N", "cooc", "marge_pivot", "marge_associe"))
    if not all((n, c, p, a)):
        return None
    return math.log2(c * n / (p * a))


def couverture_pivots(tokens: Sequence[str], pivot: str, associe: str, k: int) -> dict:
    """Compte les POSITIONS du pivot ayant un associé à distance <= k tokens."""
    if k < 0:
        raise ValueError("k doit être positif ou nul")
    piv = [i for i, t in enumerate(tokens) if t == pivot]
    ass = [i for i, t in enumerate(tokens) if t == associe]
    couverts = [i for i in piv if any(abs(i - j) <= k for j in ass)]
    return {"positions_pivot": piv, "positions_couvertes": couverts,
            "effectif": len(couverts), "total": len(piv)}


def bilan_fenetres(
    phrases: Sequence[Sequence[str]], pivot: str, associe: str, k: int,
) -> dict[str, int]:
    """Compter positions de pivot, positions couvertes et paires dans ±k tokens.

    Une fenêtre reste dans sa phrase. La répétition de l'associé ajoute une
    paire par position voisine, tandis que le pivot reste couvert une fois.
    Les termes de cette comparaison doivent être distincts.
    """
    if not pivot or not associe or pivot == associe:
        raise ValueError("Choisir deux termes non vides et distincts.")
    if k < 0:
        raise ValueError("k doit être positif ou nul.")
    total = couverts = paires = 0
    for phrase in phrases:
        for i, terme in enumerate(phrase):
            if terme == pivot:
                voisins = phrase[max(0, i - k):i + k + 1]
                nombre = voisins.count(associe)
                total += 1
                couverts += int(nombre > 0)
                paires += nombre
    return {"pivots": total, "pivots_couverts": couverts, "paires": paires}


def compter_paires_fenetre(tokens: Sequence[str], pivot: str, associe: str, k: int) -> int:
    """Nombre de couples de positions (pivot, associé) à distance de 1 à k.

    Les deux termes sont distincts. Chaque occurrence de l'associé à gauche
    ou à droite du pivot compte, bornes incluses. Tous les tokens fournis
    occupent une position. Passer une phrase limite la recherche à celle-ci.
    """
    return bilan_fenetres([tokens], pivot, associe, k)["paires"]


def extraire_ngrammes(phrases: Sequence[Sequence[str]], n: int) -> list[str]:
    """Suites de n tokens contigus dans chaque phrase, dans l'ordre de lecture.

    Chaque occurrence est conservée, y compris les répétitions. Les tokens
    d'une suite sont joints par une espace pour un décompte avec frequences().
    """
    if n < 1:
        raise ValueError("La longueur d'une séquence doit être positive.")
    return [
        " ".join(phrase[i:i + n])
        for phrase in phrases
        for i in range(len(phrase) - n + 1)
    ]


def frequences_ngrammes(phrases: Sequence[Sequence[str]], n: int) -> list[dict]:
    """Fréquences des suites de n tokens contigus, limitées à une phrase."""
    return frequences(extraire_ngrammes(phrases, n))
