"""Relecture humaine du DM S1 : une seule copie active par étudiant.

Les anciennes archives et les scores techniques restent inchangés.
Les transactions DB sont protégées par progression_lock pendant les dépôts.
Aucune réponse étudiante n'est exécutée : JSON, AST et sorties inertes.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

import outils
from app_correction_DM_intermediaire_S1 import (
    AUTO_WEIGHTS, HUMAN_WEIGHTS, GRADING_VERSION, MAX_HUMAN_TOTAL,
    MAX_SCORE_TOTAL, EVAL_ID, check_notebook, student_feedback,
)
from progression import _date, _academic_start
from storage_layout import storage_id

RECEIPT_RE = re.compile(r"[0-9a-f]{32}\Z")
NUMBER_RE = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
POINT_RE = re.compile(r"(?:0|[0-9]{1,2})(?:[.,][0-9]{1,3})?\Z")
SUBMIT_CUTOFF = 10 * MAX_SCORE_TOTAL / 20  # strictement inférieur : 8,875

# Textes basés sur les consignes de Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb.
HUMAN_QUESTIONS = {
    2: "Expliquez l'ordre des opérations dans chaque expression et justifiez celle qui partage équitablement le stock restant.",
    6: "Expliquez les limites du découpage sur les espaces pour compter des mots linguistiques, en considérant la virgule, l'apostrophe et le point d'exclamation.",
    12: "Expliquez la progression et l'arrêt de la boucle while et pourquoi le septième effectif n'appartient pas aux six tours demandés.",
    14: "Examinez les trois essais complémentaires : liste courte, limite de deux essais et liste vide ; expliquez les trois motifs d'arrêt.",
    17: "Donnez deux limites concrètes du traitement proposé pour traduire des phrases et reliez-les au programme ou à un autre exemple.",
}


class SubmissionClosed(ValueError):
    """Dépôt supplémentaire interdit selon le seuil ou la validation."""


class StaleReview(ValueError):
    """Version de fiche ancienne, sans écrasement des corrections récentes."""


def _root():
    return Path(outils.BASE_DIR)


def _db():
    directory = _root() / "suivi"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = directory / "dm_s1_corrections.sqlite3"
    conn = sqlite3.connect(path, timeout=12, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=12000")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS submissions(
            submission_id TEXT PRIMARY KEY,
            student_number TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            received_at TEXT NOT NULL,
            auto_score REAL NOT NULL,
            auto_version INTEGER NOT NULL,
            notebook_sha256 TEXT NOT NULL,
            state TEXT NOT NULL CHECK(state IN ('pending','draft','published','superseded')),
            review_json TEXT NOT NULL DEFAULT '{}',
            revision INTEGER NOT NULL DEFAULT 0,
            final_score REAL,
            published_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_dm_student_year
            ON submissions(student_number,academic_year,received_at);
        CREATE INDEX IF NOT EXISTS idx_dm_state ON submissions(state,academic_year);
    """)
    os.chmod(path, 0o600)
    return conn


def _year():
    value = os.environ.get("TAL_ACADEMIC_YEAR", "").strip()
    start = _academic_start(value)
    if start is None:
        raise ValueError("TAL_ACADEMIC_YEAR absent")
    return value


def _latest(conn, number):
    return conn.execute(
        """SELECT * FROM submissions
           WHERE academic_year=? AND student_number=? AND state!='superseded'
           ORDER BY received_at DESC, rowid DESC LIMIT 1""",
        (_year(), number),
    ).fetchone()


def _legacy_score(number):
    """Dernière note historique, non comparable sans son maximum original."""
    path = _root() / storage_id(EVAL_ID) / ("notes_" + storage_id(EVAL_ID) + ".csv")
    if not path.is_file():
        return None
    start = _academic_start(_year())
    latest = None
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        for index, row in enumerate(reader):
            if row.get("Numéro étudiant") != number:
                continue
            date = _date(row.get("Date", ""))
            if date is None or not datetime(start, 9, 1) <= date < datetime(start + 1, 9, 1):
                continue
            try:
                raw = float(str(row["Score"]).replace(",", "."))
                maximum = float(row.get("Maximum technique") or 20)
            except (ValueError, TypeError, KeyError):
                continue
            if not math.isfinite(raw) or not math.isfinite(maximum) or maximum <= 0:
                continue
            if latest is None or (date,index) > latest[0]:
                latest = ((date,index), (raw,maximum))
    return latest[1] if latest else None


def assert_redrop_allowed(conn, number):
    """À appeler sous progression_lock, avant toute écriture de dépôt."""
    if not NUMBER_RE.fullmatch(number):
        raise ValueError("Numéro étudiant invalide")
    latest = _latest(conn, number)
    if latest is not None:
        if latest["state"] == "published":
            raise SubmissionClosed("Correction humaine déjà validée : aucun nouveau dépôt accepté.")
        if latest["auto_score"] >= SUBMIT_CUTOFF - 1e-9:
            raise SubmissionClosed("Le score technique atteint le seuil autorisant la relecture ; aucun redépôt nécessaire.")
    else:
        history = _legacy_score(number)
        if history is not None and history[0] / history[1] >= 0.5:
            raise SubmissionClosed("Dernier devoir historique au moins égal à 10/20 : aucun redépôt automatique autorisé.")
    return latest


def register(conn, number, receipt, score, notebook_bytes):
    """Insertion dans la transaction ouverte par le stockage des dépôts."""
    if not RECEIPT_RE.fullmatch(receipt):
        raise ValueError("Identifiant de dépôt invalide")
    latest = assert_redrop_allowed(conn, number)
    if not isinstance(score, (float,int)) or not math.isfinite(score) or not 0 <= score <= MAX_SCORE_TOTAL:
        raise ValueError("Score technique DM invalide")
    if latest:
        conn.execute("UPDATE submissions SET state='superseded' WHERE submission_id=?",
                     (latest["submission_id"],))
    conn.execute(
        """INSERT INTO submissions
           (submission_id,student_number,academic_year,received_at,auto_score,
            auto_version,notebook_sha256,state)
           VALUES(?,?,?,datetime('now'),?,?,?,'pending')""",
        (receipt,number,_year(),score,GRADING_VERSION,
         hashlib.sha256(notebook_bytes).hexdigest()),
    )


def active_for(number):
    if not isinstance(number,str) or not NUMBER_RE.fullmatch(number):
        return None
    conn = _db()
    try:
        row = _latest(conn, number)
        return dict(row) if row else None
    finally:
        conn.close()


def queue():
    conn = _db()
    try:
        rows = conn.execute(
            """SELECT * FROM submissions
               WHERE academic_year=? AND state IN ('pending','draft','published')
               ORDER BY state DESC, received_at DESC""", (_year(),)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def by_receipt(receipt):
    if not isinstance(receipt,str) or not RECEIPT_RE.fullmatch(receipt):
        return None
    conn = _db()
    try:
        row = conn.execute("SELECT * FROM submissions WHERE submission_id=? AND academic_year=?",
                           (receipt,_year())).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def _notebook_path(receipt):
    if not RECEIPT_RE.fullmatch(receipt):
        raise ValueError("Identifiant invalide")
    folder = _root() / storage_id(EVAL_ID) / "nb"
    if folder.is_symlink():
        raise ValueError("Dossier d'archives non régulier")
    files = list(folder.glob("*_" + receipt + "_*.ipynb")) if folder.is_dir() else []
    if len(files) != 1 or not files[0].is_file() or files[0].is_symlink():
        raise ValueError("Copie introuvable ou ambiguë")
    if files[0].stat().st_size > 12_000_000:
        raise ValueError("Copie trop volumineuse")
    return files[0]


def review_evidence(record):
    """Vue inerte de la copie effectivement associée à la note et au numéro."""
    from notebook_contract import validate_cell_metadata
    blob = _notebook_path(record["submission_id"]).read_bytes()
    if hashlib.sha256(blob).hexdigest() != record["notebook_sha256"]:
        raise ValueError("Empreinte de copie incorrecte")
    notebook = json.loads(blob)
    index = validate_cell_metadata(notebook)
    identity = index.get(("identity","identification"))
    if not identity:
        raise ValueError("Identité du devoir absente")
    # Ne jamais réinterpréter l'identité à partir d'un contenu non vérifié.
    from app_correction_DM_intermediaire_S1 import _identification, _text
    info = _identification(index)
    if info["numero_etudiant"] != record["student_number"]:
        raise ValueError("Numéro étudiant incohérent")
    score, details, maximum, _, error = check_notebook(blob.decode("utf-8-sig"), "copie.ipynb")
    if error or abs(score - record["auto_score"]) > 0.001 or maximum != MAX_SCORE_TOTAL:
        raise ValueError("Calcul du devoir non reproductible")
    observed = {}
    for q in HUMAN_WEIGHTS:
        cell = index.get((f"Q{q}","answer"))
        source = _text(cell.get("source","")) if cell else ""
        outputs = cell.get("outputs",[]) if cell else []
        traces = []
        for output in outputs if isinstance(outputs,list) else []:
            if isinstance(output,dict) and output.get("output_type")=="stream":
                value = output.get("text","")
                try:
                    traces.append(_text(value))
                except ValueError:
                    pass
            elif isinstance(output,dict) and output.get("output_type")=="error":
                traces.append("Erreur Python enregistrée : " + str(output.get("ename","")))
        observed[q] = {
            "number": q, "prompt": HUMAN_QUESTIONS[q],
            "code": source[:18000], "output": "\n".join(traces)[:18000],
            "auto_points": next(d["points"] for d in details if d["check"].startswith(f"Q{q} —")
                                and d["max_points"] > 0),
            "auto_max": AUTO_WEIGHTS[q],
            "human_max": HUMAN_WEIGHTS[q],
        }
    return info, observed, student_feedback(details)


def parse_grade(value, maximum):
    raw = str(value or "").strip()
    if not POINT_RE.fullmatch(raw):
        raise ValueError("Note de relecture invalide")
    number = float(raw.replace(",", "."))
    if not math.isfinite(number) or not 0 <= number <= maximum + 1e-9:
        raise ValueError("Note hors barème")
    return round(number,3)


def save_review(receipt, revision, notes, validate=False):
    """Opération atomique : protège contre une fiche obsolète/redépôt concurrent."""
    if not RECEIPT_RE.fullmatch(receipt):
        raise ValueError("Dépôt inconnu")
    conn = _db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM submissions WHERE submission_id=? AND academic_year=?",
                           (receipt,_year())).fetchone()
        if not row or row["state"] not in ("pending","draft"):
            raise StaleReview("Cette copie n'est plus active à corriger")
        if row["revision"] != revision:
            raise StaleReview("La fiche a changé depuis son ouverture")
        clean = {}
        for q, maximum in HUMAN_WEIGHTS.items():
            user_note = notes.get(q,{})
            appreciation = str(user_note.get("appreciation","")).strip()
            if len(appreciation) > 2500:
                raise ValueError("Appréciation trop longue")
            raw = str(user_note.get("points","")).strip()
            if validate and (not raw or not appreciation):
                raise ValueError("Notes et appréciations requises pour les cinq questions")
            value = parse_grade(raw,maximum) if raw else None
            clean[str(q)] = {"points":value,"appreciation":appreciation}
        total = round(sum(clean[str(q)]["points"] for q in HUMAN_WEIGHTS),3) if validate else None
        if validate and abs(total - MAX_HUMAN_TOTAL) > 1e-6 and total > MAX_HUMAN_TOTAL:
            raise ValueError("Note humaine hors barème")
        final = round(row["auto_score"] + total,3) if validate else None
        conn.execute(
            """UPDATE submissions
               SET state=?, review_json=?, revision=revision+1,
                   final_score=?, published_at=CASE WHEN ? THEN datetime('now') ELSE NULL END
               WHERE submission_id=?""",
            ("published" if validate else "draft", json.dumps(clean,ensure_ascii=False),
             final,1 if validate else 0,receipt),
        )
        conn.commit()
        return final
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
