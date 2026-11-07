"""Accès individuel sans SSO par premier rattachement email confirmé.

Le code remis par email est personnel et réutilisable jusqu'à son
remplacement. Il est conservé uniquement sous forme de dérivé PBKDF2.
Un email différent ne peut jamais remplacer celui du premier rattachement.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import re
import secrets
import smtplib
import sqlite3
import ssl
import time
from email.message import EmailMessage
from pathlib import Path

import outils

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
PENDING_SECONDS = 20 * 60
SESSION_SECONDS = 12 * 60 * 60
NUMBER_RE = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
EMAIL_RE = re.compile(r"[^@\s]{1,64}@[^@\s]{1,185}\.[A-Za-z]{2,}\Z")
GENERIC_ACK = ("Si ce numéro est connu et cette adresse autorisée, "
               "un code individuel a été envoyé. Vérifiez vos messages.")
GENERIC_DENIED = "Informations de connexion ou code non valides."


def normalize(number, email):
    number = (number or "").strip()
    email = (email or "").strip().lower()
    if not NUMBER_RE.fullmatch(number) or len(email) > 254 or not EMAIL_RE.fullmatch(email):
        return None
    return number, email


def _hash(number, code, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", (number + "|" + code.strip().upper()).encode("utf-8"),
        bytes.fromhex(salt), 200_000,
    ).hex()


def _db_path():
    root = Path(outils.BASE_DIR) / "suivi"
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    return root / "acces_etudiants.sqlite3"


def _db():
    path = _db_path()
    conn = sqlite3.connect(path, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 10000")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS accounts (
            number TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            salt TEXT NOT NULL,
            digest TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS pending (
            number TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            salt TEXT NOT NULL,
            digest TEXT NOT NULL,
            expires INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS throttle (
            token TEXT PRIMARY KEY,
            count INTEGER NOT NULL,
            expires INTEGER NOT NULL
        );
    """)
    os.chmod(path, 0o600)
    return conn


def _throttle(conn, key, limit, window, now):
    # Ne pas conserver les adresses IP et numéros en clair dans les clés.
    secret = os.environ.get("FLASK_SECRET_KEY", "")
    tag = hmac.new(secret.encode("utf-8"), key.encode("utf-8"),
                   "sha256").hexdigest()
    entry = conn.execute("SELECT count, expires FROM throttle WHERE token=?",
                         (tag,)).fetchone()
    if entry and entry["expires"] > now and entry["count"] >= limit:
        return False
    if entry and entry["expires"] > now:
        conn.execute("UPDATE throttle SET count=count+1 WHERE token=?", (tag,))
    else:
        conn.execute("INSERT OR REPLACE INTO throttle VALUES (?,1,?)",
                     (tag, now + window))
    return True


def mail_ready():
    return (bool(os.environ.get("TAL_SMTP_HOST"))
            and bool(os.environ.get("TAL_SMTP_FROM"))
            and os.environ.get("TAL_SMTP_SECURITY", "").lower() in {"starttls", "ssl"}
            and bool(os.environ.get("FLASK_SECRET_KEY")))


def _send_code(email, code):
    if not mail_ready():
        raise RuntimeError("Envoi email non configuré")
    message = EmailMessage()
    message["From"] = os.environ["TAL_SMTP_FROM"]
    message["To"] = email
    message["Subject"] = "Votre code personnel — Progression TAL"
    message.set_content(
        "Voici votre code personnel pour consulter votre progression TAL :\n\n"
        + code + "\n\n"
        + "Si vous demandiez votre premier accès, saisissez-le dans les "
        "20 minutes pour confirmer l'association de votre email et de "
        "votre numéro étudiant. Après validation, ce même code reste "
        "réutilisable jusqu'à une nouvelle demande de code confirmée.\n\n"
        + "Si vous n'avez rien demandé, ignorez ce message.\n"
    )
    port = int(os.environ.get("TAL_SMTP_PORT", "465"))
    context = ssl.create_default_context()
    if os.environ["TAL_SMTP_SECURITY"].lower() == "ssl":
        client = smtplib.SMTP_SSL(os.environ["TAL_SMTP_HOST"], port, timeout=8,
                                  context=context)
    else:
        client = smtplib.SMTP(os.environ["TAL_SMTP_HOST"], port, timeout=8)
    with client:
        if os.environ["TAL_SMTP_SECURITY"].lower() == "starttls":
            client.starttls(context=context)
        user = os.environ.get("TAL_SMTP_USER", "")
        if user:
            client.login(user, os.environ.get("TAL_SMTP_PASSWORD", ""))
        client.send_message(message)


def request_code(number, email, ip, student_known):
    """Réponse générique contre l'énumération ; inscription après preuve email.

    Enregistrement provisoire non bloquant : aucun email ne devient titulaire
    d'un numéro avant que son code soit utilisé. En cas d'échec d'envoi,
    le code provisoire est annulé.
    """
    if not mail_ready():
        raise RuntimeError("SMTP indisponible")
    identity = normalize(number, email)
    if not identity:
        return GENERIC_ACK
    number, email = identity
    now = int(time.time())
    code = "".join(secrets.choice(ALPHABET) for _ in range(18))
    salt = secrets.token_hex(16)
    digest = _hash(number, code, salt)
    conn = _db()
    permitted = False
    try:
        conn.execute("BEGIN IMMEDIATE")
        per_number = _throttle(conn, "req:n:" + number, 6, 3600, now)
        per_ip = _throttle(conn, "req:ip:" + ip, 25, 3600, now)
        account = conn.execute("SELECT email FROM accounts WHERE number=?",
                               (number,)).fetchone()
        pending = conn.execute("SELECT email, expires FROM pending WHERE number=?",
                               (number,)).fetchone()
        permitted = (per_number and per_ip and student_known
                     and (account is None or hmac.compare_digest(account["email"], email))
                     and (pending is None or pending["expires"] < now
                          or hmac.compare_digest(pending["email"], email)))
        if permitted:
            conn.execute("INSERT OR REPLACE INTO pending VALUES (?,?,?,?,?)",
                         (number, email, salt, digest, now + PENDING_SECONDS))
        conn.execute("DELETE FROM throttle WHERE expires < ?", (now,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    if permitted:
        try:
            _send_code(email, code)
        except (OSError, RuntimeError, ValueError, smtplib.SMTPException):
            conn = _db()
            try:
                conn.execute("DELETE FROM pending WHERE number=? AND salt=?",
                             (number, salt))
            finally:
                conn.close()
            raise RuntimeError("Envoi email indisponible") from None
    return GENERIC_ACK


def authenticate(number, email, code, ip):
    identity = normalize(number, email)
    if not identity or not isinstance(code, str) or not 1 <= len(code.strip()) <= 64:
        return None
    number, email = identity
    now = int(time.time())
    conn = _db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        n = _throttle(conn, "login:n:" + number, 12, 3600, now)
        p = _throttle(conn, "login:ip:" + ip, 80, 3600, now)
        account = conn.execute("SELECT * FROM accounts WHERE number=?", (number,)).fetchone()
        pending = conn.execute("SELECT * FROM pending WHERE number=?", (number,)).fetchone()
        version = None
        if n and p and pending and pending["expires"] >= now and hmac.compare_digest(pending["email"], email):
            if hmac.compare_digest(_hash(number, code, pending["salt"]), pending["digest"]):
                if account is None or hmac.compare_digest(account["email"], email):
                    version = (account["version"] + 1) if account else 1
                    conn.execute(
                        "INSERT OR REPLACE INTO accounts(number,email,salt,digest,version) "
                        "VALUES (?,?,?,?,?)",
                        (number, email, pending["salt"], pending["digest"], version),
                    )
                    conn.execute("DELETE FROM pending WHERE number=?", (number,))
        if version is None and n and p and account and hmac.compare_digest(account["email"], email):
            if hmac.compare_digest(_hash(number, code, account["salt"]), account["digest"]):
                version = account["version"]
        conn.execute("DELETE FROM pending WHERE expires < ?", (now,))
        conn.commit()
        return (number, version) if version is not None else None
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def session_valid(number, version):
    if not isinstance(number, str) or type(version) is not int:
        return False
    conn = _db()
    try:
        row = conn.execute("SELECT version FROM accounts WHERE number=?", (number,)).fetchone()
        return bool(row and row["version"] == version)
    finally:
        conn.close()
