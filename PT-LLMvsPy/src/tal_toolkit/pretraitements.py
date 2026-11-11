"""Prétraitements traçables : conserver la source et examiner les effets.

Chaque opération produit une vue de contrôle avec les MÊMES indices caractères que
l'original. Les passages exclus sont MASQUÉS, puis omis uniquement lors de
l'export du texte épuré (module epuration). Le texte source n'est jamais modifié.

Une proposition de Gemini ne constitue pas une preuve d'exécution.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import re
from typing import Literal

from .io_corpus import Corpus

NomOperation = Literal[
    "recomposer_lignes",
    "apostrophes_droites",
    "masquer_appels_notes",
    "masquer_blocs_notes",
    "masquer_separateurs",
    "masquer_lignes_exactes",
    "raccorder_cesures_validees",
]

_NOMS = {
    "recomposer_lignes", "apostrophes_droites", "masquer_appels_notes",
    "masquer_blocs_notes", "masquer_separateurs", "masquer_lignes_exactes",
    "raccorder_cesures_validees",
}
_CIBLES_OBLIGATOIRES = {"masquer_lignes_exactes", "raccorder_cesures_validees"}


@dataclass(frozen=True)
class OperationPretraitement:
    """Opération autorisée et son intention ; les cibles sont des textes EXACTS."""

    nom: NomOperation
    justification: str
    cibles: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.nom not in _NOMS:
            raise ValueError(f"Transformation non prise en charge : {self.nom}")
        if not self.justification.strip():
            raise ValueError("Chaque transformation exige une justification")
        if self.nom in _CIBLES_OBLIGATOIRES and not self.cibles:
            raise ValueError(f"{self.nom} nécessite des cibles explicites")
        if self.nom not in _CIBLES_OBLIGATOIRES and self.cibles:
            raise ValueError(f"{self.nom} n'accepte pas de cibles")
        if any(not c.strip() for c in self.cibles):
            raise ValueError("Les cibles doivent être non vides")
        if self.nom == "raccorder_cesures_validees":
            regex = re.compile(r"(?u)^[^\W\d_]{2,}-(?:\r\n|\n|\r)[^\W\d_]{2,}$")
            if any(not regex.fullmatch(c) for c in self.cibles):
                raise ValueError("Une césure validée doit être exactement mot-\\nfragment")


@dataclass(frozen=True)
class PlanPretraitement:
    """Ordre explicite ; par défaut aucune transformation."""

    operations: tuple[OperationPretraitement, ...] = ()
    identifiant: str = "texte-original-v1"

    def __post_init__(self) -> None:
        if not self.identifiant.strip():
            raise ValueError("Identifiant de plan manquant")
        noms = [op.nom for op in self.operations]
        if len(noms) != len(set(noms)):
            raise ValueError("Une opération ne doit pas être appliquée deux fois")
        if "raccorder_cesures_validees" in noms and "recomposer_lignes" in noms:
            if noms.index("raccorder_cesures_validees") > noms.index("recomposer_lignes"):
                raise ValueError("Valider les césures avant de recomposer les lignes")


@dataclass(frozen=True)
class ResultatPretraitement:
    original: str
    analyse: str
    sha256_original: str
    sha256_analyse_utf8: str
    plan: dict
    execution: tuple[dict, ...]
    indices_conserves: bool
    origine: str
    zones_masquees: tuple[tuple[int, int], ...] = ()

    def manifeste(self) -> dict:
        """Méta sans recopier le texte ; zones masquées et bilan exact inclus."""
        return {
            "origine": self.origine,
            "sha256_original": self.sha256_original,
            "sha256_analyse_utf8": self.sha256_analyse_utf8,
            "plan": self.plan,
            "execution": list(self.execution),
            "indices_conserves": self.indices_conserves,
            "longueur_original": len(self.original),
            "longueur_analyse": len(self.analyse),
            "zones_masquees": [list(x) for x in self.zones_masquees],
        }


_RETOURS = re.compile(r"(?<=[^\r\n])(?:\r\n|\n|\r)(?=[^\r\n])")
_APOSTROPHES = re.compile("[\u2018\u2019]")
_APPELS = re.compile(r"\[\d{1,4}\]")
_DEBUT_NOTE = re.compile(r"\[Note\s+\d+:", flags=re.I)


def _reperer_blocs_notes(texte: str) -> list[tuple[int, int]]:
    """Repère une note complète, même si son texte contient des [crochets].

    Lève une erreur pour une note non fermée : aucun bloc n'est alors masqué
    partiellement. Les notes sont détectées par l'ouverture « [Note n: ».
    """
    resultat: list[tuple[int, int]] = []
    fin_precedent = 0
    for debut_note in _DEBUT_NOTE.finditer(texte):
        depart = debut_note.start()
        if depart < fin_precedent:
            continue
        profondeur = 0
        fin = None
        for indice in range(depart, len(texte)):
            caractere = texte[indice]
            if caractere == "[":
                profondeur += 1
            elif caractere == "]":
                profondeur -= 1
                if profondeur == 0:
                    fin = indice + 1
                    break
        if fin is None:
            raise ValueError(f"Bloc de note non fermé à l'indice {depart}")
        resultat.append((depart, fin))
        fin_precedent = fin
    return resultat
_SEPARATEURS = re.compile(r"(?m)^[ \t]*(?:\*[ \t]*){4,}(?=\r?$)")
_CESURES = re.compile(r"(?u)[^\W\d_]{2,}-(?:\r\n|\n|\r)[^\W\d_]{2,}")
_TITRES_POSSIBLES = re.compile(r"(?m)^[A-ZÉÈÊÀÂÎÏÔÙÛÜÇ0-9 \-'’]{7,}(?=\r?$)")


def recenser_elements(source: str | Corpus, *, max_exemples: int = 10) -> dict:
    """Repérage descriptif, SANS transformation ni suppression."""
    texte = source.texte if isinstance(source, Corpus) else source
    if not isinstance(texte, str) or max_exemples < 0:
        raise ValueError("Source texte et max_exemples >= 0 attendus")
    motifs = {
        "appels_notes": _APPELS, "blocs_notes": _DEBUT_NOTE,
        "separateurs": _SEPARATEURS, "cesures_candidates": _CESURES,
        "titres_potentiels": _TITRES_POSSIBLES,
        "apostrophes_courbes": _APOSTROPHES,
    }
    retour: dict = {"retours_crlf": texte.count("\r\n"), "categories": {}}
    for nom, motif in motifs.items():
        exemples: list[dict] = []
        n = 0
        if nom == "blocs_notes":
            intervalles = _reperer_blocs_notes(texte)
        else:
            intervalles = [(m.start(), m.end()) for m in motif.finditer(texte)]
        n = len(intervalles)
        for debut, fin in intervalles[:max_exemples]:
            exemples.append({
                "debut": debut, "fin": fin,
                "texte": texte[debut:fin][:160],
            })
        retour["categories"][nom] = {"nombre": n, "exemples": exemples}
    return retour


def _masque(texte: str) -> str:
    return "".join(c if c in "\r\n" else " " for c in texte)


def _modifier(
    texte: str, operation: OperationPretraitement
) -> tuple[str, list[tuple[int, int, str, str]], list[tuple[int, int]]]:
    """Tous les changements sont de longueur strictement identique."""
    changements: list[tuple[int, int, str, str]] = []
    masques: list[tuple[int, int]] = []

    def enregistrer(debut: int, fin: int, apres: str, masquer: bool = False) -> str:
        avant = texte[debut:fin]
        if len(avant) != len(apres):
            raise AssertionError("Les transformations doivent conserver les offsets")
        if avant != apres:
            changements.append((debut, fin, avant, apres))
        if masquer:
            masques.append((debut, fin))
        return apres

    nom = operation.nom
    if nom == "masquer_blocs_notes":
        morceaux: list[str] = []
        position = 0
        for debut, fin in _reperer_blocs_notes(texte):
            morceaux.append(texte[position:debut])
            morceaux.append(enregistrer(debut, fin, _masque(texte[debut:fin]), True))
            position = fin
        morceaux.append(texte[position:])
        return "".join(morceaux), changements, masques

    if nom in {"recomposer_lignes", "apostrophes_droites",
               "masquer_appels_notes", "masquer_separateurs"}:
        motifs = {
            "recomposer_lignes": _RETOURS,
            "apostrophes_droites": _APOSTROPHES,
            "masquer_appels_notes": _APPELS,
            "masquer_separateurs": _SEPARATEURS,
        }
        def remplaçant(m: re.Match[str]) -> str:
            t = m.group()
            if nom == "recomposer_lignes":
                apres = " " * len(t)
            elif nom == "apostrophes_droites":
                apres = "'"
            else:
                apres = _masque(t)
            return enregistrer(m.start(), m.end(), apres, nom.startswith("masquer_"))
        return motifs[nom].sub(remplaçant, texte), changements, masques

    if nom == "masquer_lignes_exactes":
        cibles = set(operation.cibles)
        def remplaçant_ligne(m: re.Match[str]) -> str:
            ligne = m.group()
            if ligne.strip() not in cibles:
                return ligne
            return enregistrer(m.start(), m.end(), _masque(ligne), True)
        resultat = re.sub(r"(?m)^[^\r\n]+", remplaçant_ligne, texte)
        return resultat, changements, masques

    if nom == "raccorder_cesures_validees":
        # Masquer seulement le trait d'union et le saut de ligne, pas les lettres.
        # Dans le rendu épuré ces positions seront retirées, recollant le mot.
        cibles = set(operation.cibles)
        def remplaçant_cesure(m: re.Match[str]) -> str:
            chaine = m.group()
            if chaine not in cibles:
                return chaine
            coupe = re.search(r"-(?:\r\n|\n|\r)", chaine)
            assert coupe is not None
            debut = m.start() + coupe.start()
            fin = m.start() + coupe.end()
            remplacement = enregistrer(debut, fin, " " * (fin - debut), True)
            return chaine[:coupe.start()] + remplacement + chaine[coupe.end():]
        return _CESURES.sub(remplaçant_cesure, texte), changements, masques

    raise ValueError(f"Opération non reconnue : {nom}")


def _fusionner_zones(zones: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    triees = sorted(zones)
    result: list[list[int]] = []
    for debut, fin in triees:
        if not result or debut > result[-1][1]:
            result.append([debut, fin])
        else:
            result[-1][1] = max(fin, result[-1][1])
    return tuple((a, b) for a, b in result)


def executer_pretraitements(
    source: str | Corpus, *,
    plan: PlanPretraitement | None = None,
    max_exemples: int = 12,
) -> ResultatPretraitement:
    """Exécute les opérations explicites ; les masques sont réversibles via l'original."""
    plan = plan if plan is not None else PlanPretraitement()
    if max_exemples < 0:
        raise ValueError("max_exemples doit être positif ou nul")
    if isinstance(source, Corpus):
        original, sha_orig, origine = source.texte, source.sha256, source.origine
    elif isinstance(source, str):
        original = source
        sha_orig = sha256(original.encode("utf-8")).hexdigest()
        origine = "chaine Python : hachage UTF-8 réencodé"
    else:
        raise TypeError("La source doit être une chaîne ou un Corpus")

    courant = original
    execution: list[dict] = []
    zones: list[tuple[int, int]] = []
    for op in plan.operations:
        nouveau, changements, masques = _modifier(courant, op)
        # Aperçu réparti sur tout le document : première, dernières et étapes
        # intermédiaires. Éviter un biais limité aux premières pages de Faguet.
        if not max_exemples:
            echantillon = []
        elif len(changements) <= max_exemples:
            echantillon = changements
        elif max_exemples == 1:
            echantillon = [changements[0]]
        else:
            indices = [
                round(i * (len(changements) - 1) / (max_exemples - 1))
                for i in range(max_exemples)
            ]
            echantillon = [changements[i] for i in indices]
        execution.append({
            "operation": op.nom,
            "statut": "EXECUTEE",
            "justification": op.justification,
            "modifications": len(changements),
            "zones_masquees": len(masques),
            "exemples": [{
                "debut": debut, "fin": fin,
                "avant": avant[:120], "apres": apres[:120],
                "longueur": len(avant),
            } for debut, fin, avant, apres in echantillon],
        })
        zones.extend(masques)
        courant = nouveau
    if len(courant) != len(original):
        raise AssertionError("Indices originaux décalés")
    return ResultatPretraitement(
        original=original,
        analyse=courant,
        sha256_original=sha_orig,
        sha256_analyse_utf8=sha256(courant.encode("utf-8")).hexdigest(),
        plan={"identifiant": plan.identifiant,
              "operations": [asdict(op) for op in plan.operations]},
        execution=tuple(execution),
        indices_conserves=True,
        origine=origine,
        zones_masquees=_fusionner_zones(zones),
    )
