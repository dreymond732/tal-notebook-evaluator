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
        abort(400)


def _require_teacher():
    if not _enabled() or not _authenticated():
        abort(403)


def _redirect_home():
    """Canonical public redirect; preserve the cookie and proxy prefix."""
    return redirect(tal_url_for("teacher.index"), code=303)

def _render(**kwargs):
    attempted = session.get("teacher_code_requested_at", 0)
    elapsed = time.time() - attempted if type(attempted) in (int, float) else teacher_access.CODE_SECONDS + 1
    auto_send = (not kwargs.get("authenticated", False)
                 and elapsed >= teacher_access.CODE_SECONDS)
    return render_template(
        "teacher_progress_template.html",
        auto_send=auto_send,
        ready=True,
        year=os.environ["TAL_ACADEMIC_YEAR"],
        semesters=SEMESTERS,
        csrf=_csrf(),
        **kwargs,
    )


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


@teacher_bp.route("/demander-code", methods=["POST"])
def request_login_code():
    if not _enabled():
        abort(503)
    _require_csrf()
    # Une demande par ouverture de page au maximum. Les tentatives et l'IP
    # restent aussi limitées dans teacher_access.
    session["teacher_code_requested_at"] = int(time.time())
    try:
        teacher_access.request_code(request.remote_addr or "unknown")
        flash(
            "Si l'envoi est autorisé, un code temporaire a été envoyé "
            "à l'adresse enseignante configurée.", "info",
        )
    except Exception:
        current_app.logger.exception("Envoi du code enseignant indisponible")
        flash("L'envoi du code est momentanément indisponible.", "error")
    return _redirect_home()


@teacher_bp.route("/connexion", methods=["POST"])
def login():
    if not _enabled():
        abort(503)
    _require_csrf()
    try:
        accepted = teacher_access.consume_code(
            request.form.get("code", ""), request.remote_addr or "unknown",
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


@teacher_bp.route("/deconnexion", methods=["POST"])
def logout():
    _require_csrf()
    session.clear()
    return _redirect_home()
