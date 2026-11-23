"""Le support diffusé contient des cellules exécutables et des sorties à produire en séance."""
import ast
import json
from pathlib import Path


def test_cahier_fourni_avec_cellules_executables_et_sorties_vides():
    path = Path(__file__).resolve().parents[1] / "notebooks/02_mesures_lexicales.ipynb"
    nb = json.loads(path.read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4
    for cell in nb["cells"]:
        source = "".join(cell["source"])
        assert source.strip()
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is None and cell["outputs"] == []
            ast.parse(source, filename=f"notebook02:{cell['id']}")
