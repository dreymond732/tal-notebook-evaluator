"""Le notebook de projet reste syntaxiquement valide et sans formulaire bloquant."""
import ast
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]


def analyser_notebook(nom):
    nb = json.loads((RACINE / "notebooks" / nom).read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4 and len(nb["cells"]) >= 20
    codes, textes = [], []
    for i, cell in enumerate(nb["cells"]):
        texte = "".join(cell.get("source", []))
        assert texte.strip(), f"Cellule vide {i}"
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is None and cell["outputs"] == []
            ast.parse(texte, filename=f"{nom}:{i}")
            codes.append(texte)
        else:
            textes.append(texte)
    return "\n".join(codes), "\n".join(textes)


def test_notebook_01_resultats_libres_et_drive_monte():
    code, presentation = analyser_notebook("01_corpus_protocole.ipynb")
    for element in (
        "VERSION_NOTEBOOK", "REVISION_GIT", "REVISION_GIT_RESOLUE",
        'DOSSIER_TRAVAIL = Path("/content")',
        'NUMERO_SESSION = f"{secrets.randbelow',
        "DATE_SESSION = datetime.now(timezone.utc)",
        "executer_pretraitements", "composer_texte_epure",
        "files.download(str(FICHIER_APERCU))",
        "localiser_dans_original", "fonctions_ayant_modifie_zone",
        "compter_motif", "NOTES_INSPECTION",
        "FICHIER_COMPARAISON", "FICHIER_COMPARAISON_JSON",
        "METADONNEES_ANALYSE", "FICHIER_ARCHIVE",
        "COMMENTAIRES_ANALYSE", 'drive.mount("/content/drive")',
        'DOSSIER_DEPOT_DRIVE = ""', "sha_drive != sha_local",
        'DOSSIER_DRIVE_ID = "18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO"',
    ):
        assert element in code, element
    for element in (
        "dépendance des traitements lexicaux",
        "Bloc-notes", "## 1", "## 2", "## 3", "## 4",
        "une copie",
    ):
        assert element.lower() in presentation.lower()
    assert presentation.index("## 2") < presentation.index("## 3")
    for ancien in (
        "MON_IDENTIFIANT", "DECISION_SUITE", "STATUT_ANALYSE",
        "ANOMALIES_A_EXAMINER", "valider_inspection(",
        "VALIDATION_ANALYSE", "MODE_REVISION",
        "exporter_texte_approuve(", "deposer_archive_drive_api(",
        "preparer_archive_td01(", "MES_CAS", "REVUE_ECHANTILLONS_VALIDE",
    ):
        assert ancien not in code, ancien


def test_notebook_02_audit_conserve():
    code, presentation = analyser_notebook("02_mesures_lexicales.ipynb")
    assert "calculer_metriques_globales" in code
    assert "comparer_annonces" in code
