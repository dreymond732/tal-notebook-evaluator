"""Exécuter les six micro-exemples réellement décrits dans le notebook 01."""
import json
from pathlib import Path

from tal_toolkit import (
    OperationPretraitement, PlanPretraitement, executer_pretraitements,
    composer_texte_epure,
)


def test_toutes_les_phrases_types_du_notebook_01():
    fichier = Path(__file__).resolve().parents[1] / "notebooks" / "01_corpus_protocole.ipynb"
    cellules = json.loads(fichier.read_text(encoding="utf-8"))["cells"]
    code = next(
        "".join(c["source"]) for c in cellules
        if c["cell_type"] == "code"
        and "EXEMPLES_FOURNIS = [" in "".join(c["source"])
    )
    def operation(nom, justification, cibles=()):
        return OperationPretraitement(nom, justification, tuple(cibles))

    contexte = {
        "operation": operation,
        "PlanPretraitement": PlanPretraitement,
        "executer_pretraitements": executer_pretraitements,
        "composer_texte_epure": composer_texte_epure,
    }
    exec(compile(code, "notebook01:phrases-types", "exec"), contexte)
    assert len(contexte["EXEMPLES_FOURNIS"]) == 6
    assert {x["nom"] for x in contexte["EXEMPLES_FOURNIS"]} == {
        "retours typographiques",
        "apostrophes courbes",
        "appel et contenu de note",
        "séparateur d'astérisques",
        "titre conservé",
        "césure approuvée",
    }
