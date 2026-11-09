"""Espace de consultation enseignant, fermé aux sessions étudiantes."""
from __future__ import annotations

import hmac
import io
import os
import secrets
import time

from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, send_file, session, url_for)

import teacher_access
from teacher_progress import cohort, csv_export, student_sheet
from progression import SEMESTERS
from tal_urls import tal_url_for

teacher_bp = Blueprint("teacher", __name__, url_prefix="/enseignant/progression")


def _enabled():
    return (
        teacher_access.configured()
        and (request.is_secure or current_app.config.get("TESTING", False))
    )


def _authenticated():
    return teacher_access.session_valid(
        session.get("teacher_authenticated_at"),
        session.get("teacher_identity"),
    )


def _csrf():
    if "teacher_csrf" not in session:
        session["teacher_csrf"] = secrets.token_urlsafe(24)
    return session["teacher_csrf"]


def _require_csrf():
    value = request.form.get("csrf", "")
    saved = session.get("teacher_csrf", "")
    if not saved or not hmac.compare_digest(value, saved):
        # N'enregistrer NI le jeton CSRF NI la valeur du cookie : seuls les
        # booléens aideront à repérer un cookie absent ou obsolète sous SWAG.
        cookie_name = current_app.config.get("SESSION_COOKIE_NAME", "")
        current_app.logger.warning(
            "Formulaire enseignant TAL : session CSRF non reconnue "
            "(cookie_recu=%s, cookies_homonymes=%s, session_presente=%s, jeton_formulaire_present=%s)",
            bool(cookie_name and request.cookies.get(cookie_name)),
            len(request.cookies.getlist(cookie_name)) if cookie_name else 0,
            bool(saved), bool(value),
        )
        abort(400)


def _require_teacher():
    if not _enabled() or not _authenticated():
        abort(403)


def _redirect_home():
    """Canonical public redirect; preserve the cookie and proxy prefix."""
    return redirect(tal_url_for("teacher.index"), code=303)

def _render(**kwargs):
    return render_template(
        "teacher_progress_template.html",
        ready=True,
        year=os.environ["TAL_ACADEMIC_YEAR"],
        semesters=SEMESTERS,
        csrf=_csrf(),
        **kwargs,
    )


@teacher_bp.errorhandler(400)
def invalid_teacher_form(error):
    """Renvoyer un diagnostic utile sans accepter un formulaire non signé.

    Aucun code OTP ni relevé privé n'est lu lorsque le CSRF est invalide.
    """
    name = current_app.config.get("SESSION_COOKIE_NAME", "")
    cookie_present = bool(name and request.cookies.get(name))
    return render_template(
        "teacher_session_error_template.html",
        return_url=tal_url_for("teacher.index"),
        cookie_present=cookie_present,
    ), 400


@teacher_bp.after_request
def protect_private_data(response):
    response.headers["Cache-Control"] = "private, no-store, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; "
        "script-src 'self'; style-src 'self'; "
        "base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
    )
    return response


@teacher_bp.route("", methods=["GET"])
@teacher_bp.route("/", methods=["GET"])
def index():
    if not _enabled():
        return render_template(
            "teacher_progress_template.html", ready=False,
            authenticated=False,
        ), 503
    if not _authenticated():
        return _render(authenticated=False, listing=None, selected=None)
    semester = request.args.get("semestre", "S1")
    if semester not in SEMESTERS:
        abort(404)
    try:
        listing = cohort(semester)
    except (OSError, UnicodeError, ValueError):
        current_app.logger.exception("Lecture du suivi enseignant indisponible")
        return "Suivi momentanément indisponible. Contactez l'administrateur.", 503
    return _render(authenticated=True, listing=listing, selected=None)


@teacher_bp.route("/connexion", methods=["POST"])
def login():
    if not _enabled():
        abort(503)
    # Le code aléatoire, envoyé UNIQUEMENT par la CLI, est le secret
    # d'authentification : ne pas exiger le CSRF d'une session anonyme
    # qui peut avoir changé derrière SWAG. Les routes privées gardent
    # l'authentification et le CSRF sur les opérations POST.
    try:
        accepted = teacher_access.consume_code(
            request.form.get("code", ""), request.remote_addr or "unknown",
            request.form.get("email", ""),
        )
    except Exception:
        current_app.logger.exception("Vérification du code enseignant indisponible")
        accepted = False
    if accepted:
        session.clear()  # Privilèges ne coexistent pas avec la session étudiant.
        session.permanent = True
        session["teacher_authenticated_at"] = int(time.time())
        session["teacher_identity"] = teacher_access.session_identity()
        flash("Accès enseignant confirmé.", "info")
    else:
        flash("Code invalide, expiré ou déjà utilisé.", "error")
    return _redirect_home()


@teacher_bp.route("/fiche", methods=["POST"])
def detail():
    _require_teacher()
    _require_csrf()
    semester = request.form.get("semestre", "")
    number = request.form.get("numero", "")
    if semester not in SEMESTERS:
        abort(404)
    try:
        sheet = student_sheet(semester, number)
    except (OSError, UnicodeError, ValueError):
        current_app.logger.exception("Lecture de la fiche enseignante indisponible")
        return "Fiche momentanément indisponible.", 503
    if sheet is None:
        abort(404)
    listing, student = sheet
    return _render(authenticated=True, listing=listing, selected=student)


@teacher_bp.route("/export/<semester>", methods=["GET"])
def export(semester):
    _require_teacher()
    if semester not in SEMESTERS:
        abort(404)
    try:
        content = csv_export(semester)
    except (OSError, UnicodeError, ValueError):
        current_app.logger.exception("Export enseignant indisponible")
        return "Export momentanément indisponible.", 503
    if content is None:
        abort(404)
    return send_file(
        io.BytesIO(content), mimetype="text/csv; charset=utf-8",
        as_attachment=True,
        download_name=f"progression_{semester}_{os.environ['TAL_ACADEMIC_YEAR']}.csv",
    )




@teacher_bp.route("/dm-s1", methods=["GET"])
def dm_queue():
    _require_teacher()
    from dm_hybrid import queue
    from teacher_progress import cohort
    try:
        students = {s["number"]: s for s in cohort("S1")["students"]}
        rows = queue()
        for row in rows:
            identity = students.get(row["student_number"], {})
            row["student_name"] = (
                identity.get("last_name", "") + " " +
                identity.get("first_name", "")
            ).strip() or "Étudiant"
    except (OSError, ValueError):
        current_app.logger.exception("File de correction DM indisponible")
        return "File de corrections indisponible.", 503
    return render_template("teacher_dm_queue_template.html", csrf=_csrf(), rows=rows)


@teacher_bp.route("/dm-s1/<receipt>", methods=["GET"])
def dm_review(receipt):
    _require_teacher()
    from dm_hybrid import by_receipt, review_evidence
    import json
    record = by_receipt(receipt)
    if record is None or record["state"] == "superseded":
        abort(404)
    try:
        identity, questions, _ = review_evidence(record)
        saved = json.loads(record["review_json"])
    except (ValueError, OSError, UnicodeError):
        current_app.logger.exception("Copie de DM indisponible pour relecture")
        return "Copie indisponible ou altérée.", 503
    return render_template(
        "teacher_dm_review_template.html", csrf=_csrf(),
        record=record, identity=identity, questions=list(questions.values()),
        saved=saved,
    )


@teacher_bp.route("/dm-s1/<receipt>/enregistrer", methods=["POST"])
def dm_save(receipt):
    _require_teacher()
    _require_csrf()
    from dm_hybrid import HUMAN_WEIGHTS, save_review, StaleReview
    try:
        revision = int(request.form.get("revision", "-1"))
        action = request.form.get("action", "")
        if action not in ("draft", "publish"):
            abort(400)
        notes = {
            q: {
                "points": request.form.get(f"points_{q}", ""),
                "appreciation": request.form.get(f"appreciation_{q}", ""),
            }
            for q in HUMAN_WEIGHTS
        }
        save_review(receipt, revision, notes, validate=(action == "publish"))
    except StaleReview:
        return "Cette fiche n'est plus active ou a été modifiée. Rechargez la liste.", 409
    except (ValueError, TypeError):
        flash("Correction incomplète ou note hors barème.", "error")
        return redirect(tal_url_for("teacher.dm_review", receipt=receipt), code=303)
    flash("Correction publiée." if action == "publish" else "Brouillon enregistré.", "info")
    return redirect(tal_url_for("teacher.dm_queue"), code=303)


@teacher_bp.route("/deconnexion", methods=["POST"])
def logout():
    _require_csrf()
    session.clear()
    return _redirect_home()
