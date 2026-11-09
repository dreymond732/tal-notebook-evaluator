"""Bilan hybride DM S1 : dernière copie active, annotations privées par dépôt.

La base est dans soumissions/suivi, jamais dans l'arbre public. Un nouveau
dépôt ne supprime aucune archive, mais invalide sa fiche de relecture.
Aucun code étudiant n'est exécuté.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

import outils
from app_correction_DM_intermediaire_S1 import (
    HUMAN_WEIGHTS, FINAL_MAX_SCORE, MAX_SCORE_TOTAL,
    REDEPOSIT_THRESHOLD, HYBRID_RUBRIC_VERSION, LABELS,
)

QUESTIONS = (2, 6, 12, 14, 17)
# Consignes vérifiées côté serveur, jamais déduites d'une cellule non fiable.
REVIEW_PROMPTS = {
    2: "Expliquer les priorités des opérations et identifier le calcul correspondant au partage égal du stock restant.",
    6: "Expliquer pourquoi le nombre de fragments de split() ne représente pas nécessairement les mots linguistiques, avec les exemples de ponctuation et d’apostrophes du texte.",
    12: "Expliquer la progression de while, sa condition d'arrêt et l'exclusion de l'effectif après le sixième tour.",
    14: "Examiner les trois essais supplémentaires (liste courte, limite atteinte, liste vide), puis expliquer les trois motifs d'arrêt.",
    17: "Présenter deux limites concrètes empêchant de considérer le traitement comme une traduction linguistique générale.",
}


def _db():
    root = Path(outils.BASE_DIR) / "suivi"
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    path = root / "dm_hybride.sqlite3"
    conn = sqlite3.connect(path, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 10000")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS attempts (
            receipt TEXT PRIMARY KEY,
            number TEXT NOT NULL,
            name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            created_at TEXT NOT NULL,
            score REAL NOT NULL CHECK (score >= 0 AND score <= 17.75),
            rubric INTEGER NOT NULL CHECK (rubric = 2),
            feedback TEXT NOT NULL,
            evidence TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS current_attempt (
            number TEXT PRIMARY KEY,
            receipt TEXT NOT NULL REFERENCES attempts(receipt)
        );
        CREATE TABLE IF NOT EXISTS reviews (
            receipt TEXT NOT NULL REFERENCES attempts(receipt),
            question INTEGER NOT NULL,
            points TEXT,
            comment TEXT NOT NULL DEFAULT '',
            PRIMARY KEY (receipt, question)
        );
        CREATE TABLE IF NOT EXISTS validation (
            receipt TEXT PRIMARY KEY REFERENCES attempts(receipt),
            validated_at TEXT NOT NULL
        );
    """)
    os.chmod(path, 0o600)
    return conn


def can_redeposit(number):
    """Premier dépôt autorisé ; suivants sous seuil seulement, avant validation."""
    conn = _db()
    try:
        row = conn.execute("""
            SELECT a.receipt, a.score, v.validated_at
            FROM current_attempt c JOIN attempts a ON a.receipt=c.receipt
            LEFT JOIN validation v ON v.receipt=a.receipt
            WHERE c.number=?
        """, (number,)).fetchone()
        if row is None:
            return True
        return row["validated_at"] is None and row["score"] < REDEPOSIT_THRESHOLD
    finally:
        conn.close()


def _extract_evidence(notebook):
    evidence = {}
    cells = notebook.get("cells", []) if isinstance(notebook, dict) else []
    for q in QUESTIONS:
        matches = [
            cell for cell in cells
            if isinstance(cell, dict)
            and cell.get("metadata", {}).get("tal") == {
                "question": "Q" + str(q), "role": "answer"
            }
        ]
        # Des clés TAL supplémentaires ne doivent pas faire disparaître
        # une cellule : les identifiants sont lus explicitement.
        if not matches:
            matches = [
                cell for cell in cells if isinstance(cell, dict)
                and cell.get("metadata", {}).get("tal", {}).get("question") == "Q" + str(q)
                and cell.get("metadata", {}).get("tal", {}).get("role") == "answer"
            ]
        if len(matches) != 1:
            raise ValueError("Cellule de réponse absente ou ambiguë pour Q" + str(q))
        cell = matches[0]
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        if not isinstance(source, str):
            raise ValueError("Code étudiant non textuel")
        outputs = []
        for out in cell.get("outputs", []):
            if not isinstance(out, dict):
                continue
            if out.get("output_type") == "stream":
                value = out.get("text", "")
                if isinstance(value, list):
                    value = "".join(value)
                if isinstance(value, str):
                    outputs.append(value)
            elif out.get("output_type") == "error":
                outputs.append("Erreur d'exécution : " + str(out.get("ename", "")))
        evidence[str(q)] = {
            "code": source[:16000],
            "outputs": "\n".join(outputs)[:8000],
        }
    return evidence


def record_submission(receipt, info, filename, score, feedback, notebook):
    """Appelée sous progression_lock après persistance du journal de notes."""
    if not isinstance(receipt, str) or len(receipt) != 32 or not all(
        x in "0123456789abcdef" for x in receipt
    ):
        raise ValueError("Identifiant de dépôt invalide")
    number = str(info.get("numero_etudiant") or "").strip()
    if not number:
        raise ValueError("Numéro étudiant absent")
    if int(info.get("dm_rubric_version", 0)) != HYBRID_RUBRIC_VERSION:
        raise ValueError("Barème hybride DM non reconnu")
    score = float(score)
    if not (0 <= score <= MAX_SCORE_TOTAL):
        raise ValueError("Score automatique DM hors barème")
    if len(feedback) != 18 or [f["number"] for f in feedback] != list(range(1, 19)):
        raise ValueError("Bilan automatique DM incomplet")
    evidence = _extract_evidence(notebook)
    conn = _db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        current = conn.execute("""
            SELECT a.score, v.validated_at
            FROM current_attempt c JOIN attempts a ON c.receipt=a.receipt
            LEFT JOIN validation v ON a.receipt=v.receipt
            WHERE c.number=?
        """, (number,)).fetchone()
        if current is not None and (
            current["validated_at"] is not None or current["score"] >= REDEPOSIT_THRESHOLD
        ):
            raise ValueError("Redépôt DM fermé pour cet étudiant")
        conn.execute("""
            INSERT INTO attempts(receipt,number,name,first_name,filename,created_at,
                                 score,rubric,feedback,evidence)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (receipt, number, str(info["nom"])[:128], str(info["prenom"])[:128],
              str(filename)[:255], datetime.now(timezone.utc).isoformat(),
              score, HYBRID_RUBRIC_VERSION,
              json.dumps(feedback, ensure_ascii=False),
              json.dumps(evidence, ensure_ascii=False)))
        conn.execute("""
            INSERT INTO current_attempt(number,receipt) VALUES (?,?)
            ON CONFLICT(number) DO UPDATE SET receipt=excluded.receipt
        """, (number, receipt))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _load(conn, receipt, *, current_only=True):
    row = conn.execute("""
        SELECT a.*, v.validated_at FROM attempts a
        LEFT JOIN validation v ON v.receipt=a.receipt
        WHERE a.receipt=?
    """, (receipt,)).fetchone()
    if row is None:
        return None
    if current_only and conn.execute(
        "SELECT 1 FROM current_attempt WHERE number=? AND receipt=?",
        (row["number"], receipt),
    ).fetchone() is None:
        return None
    review = {r["question"]: dict(r) for r in conn.execute(
        "SELECT question, points, comment FROM reviews WHERE receipt=?", (receipt,)
    )}
    result = dict(row)
    result["feedback"] = json.loads(row["feedback"])
    result["evidence"] = json.loads(row["evidence"])
    result["questions"] = [{
        "number": q, "label": LABELS[q - 1],
        "prompt": REVIEW_PROMPTS[q],
        "maximum": HUMAN_WEIGHTS[q],
        "code": result["evidence"].get(str(q), {}).get("code", ""),
        "outputs": result["evidence"].get(str(q), {}).get("outputs", ""),
        "score_auto": result["feedback"][q-1]["points"],
        "points": review.get(q, {}).get("points"),
        "comment": review.get(q, {}).get("comment", ""),
    } for q in QUESTIONS]
    result["human_score"] = sum(float(q["points"]) for q in result["questions"]
                                if q["points"] is not None)
    result["final_score"] = round(result["score"] + result["human_score"], 3) if row["validated_at"] else None
    result["redraw_allowed"] = (row["validated_at"] is None and row["score"] < REDEPOSIT_THRESHOLD)
    return result


def current_for_student(number):
    conn = _db()
    try:
        row = conn.execute("SELECT receipt FROM current_attempt WHERE number=?", (number,)).fetchone()
        return _load(conn, row["receipt"]) if row else None
    finally:
        conn.close()


def current_by_receipt(receipt):
    conn = _db()
    try:
        return _load(conn, receipt)
    finally:
        conn.close()


def queue():
    conn = _db()
    try:
        rows = conn.execute("""
            SELECT a.receipt,a.number,a.name,a.first_name,a.created_at,a.score,
                   CASE WHEN v.receipt IS NULL THEN 'À corriger' ELSE 'Validée' END AS status
            FROM current_attempt c JOIN attempts a ON c.receipt=a.receipt
            LEFT JOIN validation v ON a.receipt=v.receipt
            ORDER BY a.name COLLATE NOCASE, a.first_name COLLATE NOCASE, a.number
        """).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def save_review(receipt, values, validate=False):
    """Sauvegarde une fiche complète/partielle, refuse une copie périmée."""
    conn = _db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        current = _load(conn, receipt)
        if current is None or current["validated_at"]:
            raise ValueError("Copie remplacée ou correction déjà validée")
        cleaned = {}
        for q in QUESTIONS:
            raw = (values.get(f"points_{q}") or "").strip().replace(",", ".")
            comment = (values.get(f"comment_{q}") or "").strip()
            if len(comment) > 4000:
                raise ValueError("Appréciation trop longue pour Q" + str(q))
            points = None
            if raw:
                try:
                    points = Decimal(raw)
                except InvalidOperation as exc:
                    raise ValueError("Points non numériques pour Q" + str(q)) from exc
                if not points.is_finite() or not 0 <= points <= Decimal(str(HUMAN_WEIGHTS[q])):
                    raise ValueError("Points hors barème pour Q" + str(q))
                if points.as_tuple().exponent < -2:
                    raise ValueError("Deux décimales maximum pour Q" + str(q))
            if validate and (points is None or not comment):
                raise ValueError("Note et appréciation requises pour Q" + str(q))
            cleaned[q] = (str(points) if points is not None else None, comment)
        for q, (points, comment) in cleaned.items():
            conn.execute("""
                INSERT INTO reviews(receipt,question,points,comment) VALUES (?,?,?,?)
                ON CONFLICT(receipt,question)
                DO UPDATE SET points=excluded.points,comment=excluded.comment
            """, (receipt, q, points, comment))
        if validate:
            conn.execute("INSERT INTO validation(receipt,validated_at) VALUES (?,?)",
                         (receipt, datetime.now(timezone.utc).isoformat()))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
