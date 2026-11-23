"""Entrée des trois séances de reprise et intégrité des cahiers à distribuer."""
import ast
import json
from pathlib import Path
import re


def test_cahiers_diffuses_avec_reprise_locale_et_sorties_vides():
    notebooks = Path(__file__).resolve().parents[1] / "notebooks"
    revisions = []
    for path in sorted(notebooks.glob("0[234]_*.ipynb")):
        cahier = json.loads(path.read_text(encoding="utf-8"))
        assert cahier["nbformat"] == 4
        codes = {}
        for cell in cahier["cells"]:
            source = "".join(cell["source"])
            assert source.strip()
            if cell["cell_type"] == "code":
                assert cell["execution_count"] is None and cell["outputs"] == []
                ast.parse(source, filename=f"{path.name}:{cell['id']}")
                codes[cell["id"]] = source

        initialisation = codes["initialisation-pt"]
        assert 'NUMERO_ETUDIANT = ""' in initialisation
        assert 'preparer_atelier(numero_etudiant=NUMERO_ETUDIANT)' in initialisation
        revision = re.search(r"\.git@([0-9a-f]{40})#subdirectory=PT-LLMvsPy", initialisation)
        assert revision, f"{path.name} doit installer une révision Git immuable"
        revisions.append(revision.group(1))
        assert not any("drive.mount(" in code or "/content/drive" in code for code in codes.values())
    assert len(revisions) == 3 and len(set(revisions)) == 1
