"""Notebook 02 : prétraitement inspecté, métriques calculées et preuves exportées."""
import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_notebook_02_ne_repart_pas_du_texte_brut():
    path = ROOT / "notebooks" / "02_mesures_lexicales.ipynb"
    nb = json.loads(path.read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4
    assert len(nb["cells"]) >= 20
    codes, texts = [], []
    for index, cell in enumerate(nb["cells"]):
        text = "".join(cell["source"])
        assert text.strip()
        if cell["cell_type"] == "code":
            assert cell.get("outputs") == [] and cell.get("execution_count") is None
            ast.parse(text, filename=f"notebook02:{index}")
            codes.append(text)
        else:
            texts.append(text)
    code, prose = "\n".join(codes), "\n".join(texts)

    for expected in (
        'DOSSIER_N1 = Path("/content/analyse_faguet_v2_0_0")',
        '"faguet_nettoye.txt"', '"metadonnees_analyse.json"',
        'sha256_attendu=META_N1["sha256_nettoye"]',
        "auditer_reapplication", "plan_rejoue",
        "recenser_elements", "analyser_lexique_pt02",
        "MODELE_SPACY", "calculer_metriques_globales", "comparer_annonces",
        "TAILLE_STTR = 1000",
        "resultats_et_preuves.json", "DOSSIER_DEPOT_DRIVE",
    ):
        assert expected in code, expected
    for op in (f"OP{i:02d}" for i in range(1, 13)):
        assert op in prose, op
    for old in (
        'MON_IDENTIFIANT', 'ANOMALIES_A_EXAMINER',
        'DEBUT_EXTRAIT = None', 'FIN_EXTRAIT = None',
        'ATTENDU_MANUEL', 'JUSTIFICATION_EXTRAIT',
        'VALIDE', 'create_pull_request', 'drive.mount(',
    ):
        # Drive mount is acceptable in code, but not a mandatory
        # prerequisite in the student prose.
        assert old not in prose, old
    assert "cooccurrences" in prose.lower()
    assert "notebook 03" in prose
    assert "F(F(x)) = F(x)" in prose
