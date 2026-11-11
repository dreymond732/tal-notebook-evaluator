"""Le notebook de projet est syntaxiquement valide et ses étapes bien ordonnées."""
import ast
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]


def analyser_notebook(nom):
    nb = json.loads((RACINE / "notebooks" / nom).read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4 and len(nb["cells"]) >= 20
    scripts, textes = [], []
    for i, cell in enumerate(nb["cells"]):
        source = "".join(cell.get("source", []))
        assert source.strip(), f"Cellule vide {i}"
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is None and cell["outputs"] == []
            ast.parse(source, filename=f"{nom}:{i}")
            scripts.append(source)
        else:
            textes.append(source)
    return scripts, textes


def test_notebook_01_processus_de_revision_et_inspection():
    codes, textes = analyser_notebook("01_corpus_protocole.ipynb")
    code = "\n".join(codes)
    presentation = "\n".join(textes)
    for element in (
        "VERSION_NOTEBOOK", "REVISION_GIT", "MODE_REVISION",
        "exécuter_pretraitements" if False else "executer_pretraitements",
        "preparer_faguet_standard_td01", "files.download(str(FICHIER_APERCU))",
        "localiser_dans_original", "fonctions_ayant_modifie_zone",
        "compter_motif", "ANOMALIES_A_EXAMINER", "DECISION_SUITE",
        "journal_inspection", "valider_inspection",
        "preparer_archive_td01", "inspection=journal_inspection",
        "version_notebook=VERSION_NOTEBOOK",
        "deposer_archive_drive_api", "bouton_depot.on_click(_deposer_td01)",
    ):
        assert element in code, element
    for expression in (
        "dépendance des traitements lexicaux",
        "Bloc-notes", "estime la portée du motif",
        "## 1", "## 2", "## 3", "## 4",
        "une copie", "révision",
    ):
        assert expression.lower() in presentation.lower(), expression
    assert presentation.index("## 2") < presentation.index("## 3")
    assert "imaginez d'abord" not in presentation.lower()
    assert "sélectionnez **deux passages authentiques**" not in presentation.lower()
    assert "### Examiner et valider le résultat" not in presentation
    assert "notebook de TD" not in presentation
    assert "DOSSIER_DEPOTS" not in code
    assert "GITHUB_TAL_TOKEN" not in code
    assert "REVUE_ECHANTILLONS_VALIDE" not in code
    assert "MES_CAS" not in code
    assert 'DOSSIER_DRIVE_ID = "18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO"' in code


def test_notebook_02_audit_conserve():
    codes, textes = analyser_notebook("02_mesures_lexicales.ipynb")
    code = "\n".join(codes)
    assert "calculer_metriques_globales" in code
    assert "comparer_annonces" in code
