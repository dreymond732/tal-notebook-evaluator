"""Outils d'analyse statique pour les activités formatives S3.

Le module ne lance jamais le code remis : il lit seulement les cellules et
les sorties déjà présentes dans le notebook JSON.
"""
import json
import io
import tokenize
from typing import Dict, List

import outils


def _sources(cells: List[Dict]) -> str:
    """Retourne le code sans commentaires, sans jamais l'exécuter."""
    cleaned = []
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        try:
            tokens = tokenize.generate_tokens(io.StringIO(source).readline)
            cleaned.append("".join(
                token.string for token in tokens if token.type != tokenize.COMMENT
            ))
        except tokenize.TokenError:
            cleaned.append(source)
    return "\n".join(cleaned)


def _outputs(cells: List[Dict]) -> str:
    texts = []
    for cell in cells:
        for output in cell.get("outputs", []):
            if output.get("output_type") == "stream":
                value = output.get("text", [])
                texts.append("".join(value) if isinstance(value, list) else str(value))
            elif output.get("output_type") == "execute_result":
                value = output.get("data", {}).get("text/plain", [])
                texts.append("".join(value) if isinstance(value, list) else str(value))
    return "\n".join(texts)


def check_formative_notebook(content_str, checks, max_score):
    try:
        notebook = json.loads(content_str)
    except json.JSONDecodeError as exc:
        return 0.0, [], max_score, {"nom": "Erreur", "prenom": "JSON"}, f"Erreur JSON: {exc}"

    cells = notebook.get("cells", [])
    source, output = _sources(cells), _outputs(cells)
    details, score = [], 0.0

    for check in checks:
        code_ok = all(fragment in source for fragment in check.get("source", []))
        alternatives = check.get("source_any", [])
        if alternatives:
            code_ok = code_ok and any(fragment in source for fragment in alternatives)
        output_marker = check.get("output")
        output_ok = not output_marker or output_marker in output
        success = code_ok and output_ok
        points = check["points"] if success else 0.0
        score += points
        missing = []
        if not code_ok:
            missing.append("élément de code attendu")
        if not output_ok:
            missing.append(f"sortie « {output_marker} » absente : exécutez la cellule d'essai")
        details.append({
            "check": check["label"],
            "student_answer": "validé" if success else "; ".join(missing),
            "correct_answer": check["feedback"],
            "status": "✅" if success else "❌",
            "points": points,
            "max_points": check["points"],
        })

    info = outils.extract_identification_info(cells)
    info["score_brut"] = round(score, 2)
    return score, details, max_score, info, None
