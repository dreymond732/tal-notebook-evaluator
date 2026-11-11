"""Vue épurée destinée aux analyses ; indexation vers le texte source intact.

La vue de contrôle est de longueur identique à l'original. L'export lisible
supprime les zones MASQUÉES et compacte les seuls espaces de mise en page ;
une correspondance caractère par caractère permet de revenir à la source.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Mapping
import gzip
import json

from .pretraitements import ResultatPretraitement


@dataclass(frozen=True)
class TexteEpure:
    texte: str
    indices_source: tuple[int, ...]
    sha256_texte_utf8: str
    sha256_source: str
    total_exclus: int
    total_espaces_regroupes: int

    def position_originale(self, position: int) -> int:
        """Indice source du caractère épuré demandé."""
        return self.indices_source[position]

    def manifeste(self) -> dict:
        return {
            "sha256_texte_utf8": self.sha256_texte_utf8,
            "sha256_source": self.sha256_source,
            "longueur_texte": len(self.texte),
            "longueur_index": len(self.indices_source),
            "total_caracteres_masques": self.total_exclus,
            "total_espaces_regroupes": self.total_espaces_regroupes,
            "index_correspondance": "indices_source[i] = indice d'origine du caractère i",
            "operation_export": {
                "nom": "compacter_espaces_et_retours",
                "statut": "EXECUTEE",
                "regle": (
                    "Compacte les suites de blancs ; un retour isolé devient un "
                    "espace et plusieurs retours deviennent deux sauts de paragraphe."
                ),
                "caracteres_contractes": self.total_espaces_regroupes,
                "indices_source_conserves": True,
            },
        }


def composer_texte_epure(resultat: ResultatPretraitement) -> TexteEpure:
    """N'enlève que les zones explicitement masquées, puis compacte les espaces.

    Un saut de ligne unique devient un espace, plusieurs sauts de ligne
    deviennent deux \\n de paragraphe. Conserve les lettres et la ponctuation.
    Les indices retournés pointent vers le texte ORIGINAL, y compris pour
    les caractères typographiques transformés (apostrophes).
    """
    analyse = resultat.analyse
    original = resultat.original
    if len(analyse) != len(original) or not resultat.indices_conserves:
        raise ValueError("Vue de contrôle sans offsets source invariants")

    masque = bytearray(len(analyse))
    for debut, fin in resultat.zones_masquees:
        if not (0 <= debut < fin <= len(analyse)):
            raise ValueError("Bornes de masquage incorrectes")
        masque[debut:fin] = b"\x01" * (fin - debut)

    visibles = [(c, i) for i, c in enumerate(analyse) if not masque[i]]
    texte_sortie: list[str] = []
    indices: list[int] = []
    position = 0
    total_compactions = 0
    while position < len(visibles):
        char, offset = visibles[position]
        if not char.isspace():
            texte_sortie.append(char)
            indices.append(offset)
            position += 1
            continue
        depart = position
        newlines: list[int] = []
        while position < len(visibles) and visibles[position][0].isspace():
            if visibles[position][0] == "\n":
                newlines.append(visibles[position][1])
            position += 1
        if not texte_sortie or position == len(visibles):
            total_compactions += position - depart
            continue
        if len(newlines) >= 2:
            texte_sortie.extend(("\n", "\n"))
            indices.extend((newlines[0], newlines[-1]))
            total_compactions += position - depart - 2
        else:
            texte_sortie.append(" ")
            indices.append(offset)
            total_compactions += position - depart - 1

    propre = "".join(texte_sortie)
    if len(propre) != len(indices):
        raise AssertionError("La table d'alignement est incomplète")
    if any(a > b for a, b in zip(indices, indices[1:])):
        raise AssertionError("Les positions source doivent rester ordonnées")
    return TexteEpure(
        texte=propre,
        indices_source=tuple(indices),
        sha256_texte_utf8=sha256(propre.encode("utf-8")).hexdigest(),
        sha256_source=resultat.sha256_original,
        total_exclus=sum(masque),
        total_espaces_regroupes=total_compactions,
    )


def exporter_texte_approuve(
    resultat: ResultatPretraitement,
    dossier: str | Path,
    *,
    decisions: Mapping[str, str],
    confirmation_sha256: str,
    justification_globale: str,
    approbation_compaction: bool,
) -> dict:
    """Écrit les fichiers UNIQUEMENT après acceptation humaine de chaque effet.

    decisions : opération -> 'approuve'. Pour un plan vide, une justification
    globale et la confirmation de l'empreinte originale restent nécessaires.
    On évite de déclarer approuvé un plan distinct de celui qui a été prévisualisé.
    """
    noms = [op["nom"] for op in resultat.plan["operations"]]
    if set(decisions) != set(noms) or any(decisions[n] != "approuve" for n in noms):
        raise ValueError("Chaque opération du plan doit être approuvée explicitement")
    if confirmation_sha256 != resultat.sha256_original:
        raise ValueError("Empreinte de l'original non confirmée")
    if len(justification_globale.strip()) < 20:
        raise ValueError("Justification globale motivée requise (20 caractères minimum)")
    if approbation_compaction is not True:
        raise ValueError("La compaction finale des blancs doit être approuvée")
    if not resultat.indices_conserves:
        raise ValueError("Décalages non pris en charge")

    rendu = composer_texte_epure(resultat)
    destination = Path(dossier)
    destination.mkdir(parents=True, exist_ok=True)
    chemin_texte = destination / "faguet_epure.txt"
    chemin_manifest = destination / "faguet_epure.manifest.json"
    chemin_index = destination / "faguet_epure.offsets.json.gz"

    # Tous les fichiers sont propres à cette session. Il ne faut pas utiliser
    # un répertoire public partagé avec des utilisateurs non autorisés.
    with chemin_texte.open("w", encoding="utf-8", newline="") as f:
        f.write(rendu.texte)
    with gzip.open(chemin_index, "wt", encoding="utf-8") as f:
        json.dump(rendu.indices_source, f, separators=(",", ":"))

    manifeste = {
        "schema": "faguet-epuration-v1",
        "source": resultat.manifeste(),
        "export": rendu.manifeste(),
        "validation": {
            "decisions": dict(decisions),
            "confirmation_sha256": confirmation_sha256,
            "justification_globale": justification_globale.strip(),
            "compaction_blancs_approuvee": approbation_compaction,
            "portee": "effets du plan examiné sur corpus entier",
        },
        "fichiers": {
            "texte": chemin_texte.name,
            "correspondance": chemin_index.name,
        },
    }
    chemin_manifest.write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {
        "texte": str(chemin_texte),
        "manifeste": str(chemin_manifest),
        "correspondance": str(chemin_index),
        "sha256_epure": rendu.sha256_texte_utf8,
    }
