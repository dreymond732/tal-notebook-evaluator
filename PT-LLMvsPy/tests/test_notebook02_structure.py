"""Entrée des trois séances de reprise et intégrité des cahiers à distribuer."""
import ast
import json
from pathlib import Path
import re


def test_cahiers_diffuses_avec_reprise_locale_et_sorties_vides():
    notebooks = Path(__file__).resolve().parents[1] / "notebooks"
    for nom in ("02_mesures_lexicales", "03_relations_lexicales", "04_audit_llm"):
        path = notebooks / f"{nom}.ipynb"
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
        paquet = "tal-toolkit[nlp] @ git+https://github.com/dreymond732/tal-notebook-evaluator.git@main#subdirectory=PT-LLMvsPy"
        assert paquet in initialisation
        if nom == "04_audit_llm":
            ouvrir = next(c for c in cahier["cells"] if c["id"] == "ouvrir-04")
            assert paquet in "".join(ouvrir["source"])
        assert not any("drive.mount(" in code or "/content/drive" in code for code in codes.values())


def test_le_02_ouvre_le_corpus_du_01_puis_travaille_sur_les_unites():
    chemin = Path(__file__).resolve().parents[1] / "notebooks/02_mesures_lexicales.ipynb"
    cellules = json.loads(chemin.read_text(encoding="utf-8"))["cells"]
    sections = []
    for cellule in cellules:
        source = "".join(cellule["source"])
        if cellule["cell_type"] == "markdown":
            sections.extend(re.findall(r"^## (\d+)\b", source, re.MULTILINE))
        else:
            assert "auditer_reapplication" not in source, cellule["id"]
            assert "sha256_attendu" not in source, cellule["id"]
    assert sections == ["0", "1", "2", "3", "4"]
