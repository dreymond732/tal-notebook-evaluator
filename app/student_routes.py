"""Interface de consultation personnelle, sans exposition des CSV privés."""
import hmac
import os
import secrets
import time
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, session, url_for)

import student_access
from student_progress import individual_progress, student_exists

student_bp = Blueprint("student", __name__)


def _csrf():
    if "student_csrf" not in session:
        session["student_csrf"] = secrets.token_urlsafe(24)
    return session["student_csrf"]


def _verify_csrf():
    supplied = request.form.get("csrf", "")
    expected = session.get("student_csrf", "")
    if not expected or not hmac.compare_digest(supplied, expected):
        abort(400)


def _ready():
    return (student_access.mail_ready()
            and bool(os.environ.get("TAL_ACADEMIC_YEAR", "").strip()))


@student_bp.after_request
def private_headers(response):
    response.headers["Cache-Control"] = "no-store, private"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@student_bp.route("/ma-progression", methods=["GET"])
def individual():
    if not _ready():
        return render_template("student_progress_template.html", ready=False), 503
    number = session.get("student_number")
    version = session.get("student_version")
    issued = session.get("student_authenticated_at", 0)
    profile = None
    if (number and type(issued) in (int, float)
            and time.time() - issued <= student_access.SESSION_SECONDS
            and student_access.session_valid(number, version)):
        profile = individual_progress(number)
    return render_template(
        "student_progress_template.html", ready=True,
        csrf=_csrf(), profile=profile,
        year=os.environ["TAL_ACADEMIC_YEAR"],
    )


@student_bp.route("/ma-progression/demander-code", methods=["POST"])
def ask_code():
    if not _ready():
        abort(503)
    _verify_csrf()
    number = request.form.get("numero", "")
    email = request.form.get("email", "")
    try:
        student_access.request_code(
            number, email, request.remote_addr or "unknown",
            student_exists(number.strip()),
        )
        flash(student_access.GENERIC_ACK, "info")
    except Exception:
        current_app.logger.exception("Service d'envoi des codes indisponible")
        flash("L'envoi du code est momentanément indisponible.", "error")
    return redirect(url_for("student.individual"), code=303)


@student_bp.route("/ma-progression/connexion", methods=["POST"])
def login():
    if not _ready():
        abort(503)
    _verify_csrf()
    try:
        result = student_access.authenticate(
            request.form.get("numero", ""), request.form.get("email", ""),
            request.form.get("code", ""), request.remote_addr or "unknown",
        )
    except Exception:
        current_app.logger.exception("Service d'accès individuel indisponible")
        result = None
    if result:
        session.clear()
        session.permanent = True
        session["student_number"], session["student_version"] = result
        session["student_authenticated_at"] = int(time.time())
    else:
        flash(student_access.GENERIC_DENIED, "error")
    return redirect(url_for("student.individual"), code=303)


@student_bp.route("/ma-progression/deconnexion", methods=["POST"])
def logout():
    _verify_csrf()
    session.clear()
    return redirect(url_for("student.individual"), code=303)
