"""Accès enseignant : OTP historique ou code personnel réutilisable optionnel.

Le code réutilisable est un secret à longue durée de vie, révocable depuis
la CLI uniquement. Les sessions web restent à durée limitée.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import smtplib
import sqlite3
import ssl
import time
from email.message import EmailMessage
from pathlib import Path

import outils
from student_access import ALPHABET, EMAIL_RE, mail_ready
from progression import _academic_start

CODE_LENGTH = 12
REUSABLE_CODE_LENGTH = 20
CODE_SECONDS = 10 * 60
SESSION_SECONDS = 2 * 60 * 60


def code_mode():
    """one_time (défaut historique) ou reusable (activation explicite)."""
    return os.getenv("TAL_TEACHER_CODE_MODE", "one_time").strip().lower()


def reusable_mode():
    return code_mode() == "reusable"


def teacher_email():
    return os.getenv("TAL_TEACHER_EMAIL", "").strip().lower()


def configured():
    email = teacher_email()
    year = os.getenv("TAL_ACADEMIC_YEAR", "").strip()
    secret = os.getenv("FLASK_SECRET_KEY", "")
    try:
        valid_year = _academic_start(year) is not None
    except ValueError:
        valid_year = False
    return (
        mail_ready() and bool(EMAIL_RE.fullmatch(email))
        and len(email) <= 254 and valid_year
        and len(secret) >= 24
        and code_mode() in {"one_time", "reusable"}
    )


def _db():
    root = Path(outils.BASE_DIR) / "suivi"
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    path = root / "acces_enseignant.sqlite3"
    db = sqlite3.connect(path, timeout=10, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout = 10000")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS challenge (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            salt TEXT NOT NULL, digest TEXT NOT NULL,
            expires INTEGER NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS limits (
            key TEXT PRIMARY KEY, count INTEGER NOT NULL,
            expires INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reusable_credential (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            owner TEXT NOT NULL,
            salt TEXT NOT NULL,
            digest TEXT NOT NULL,
            created INTEGER NOT NULL
        );
    """)
    os.chmod(path, 0o600)
    return db


def _hash(code, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", code.strip().upper().encode("ascii"),
        bytes.fromhex(salt), 200_000,
    ).hex()


def _key(raw):
    secret = os.environ["FLASK_SECRET_KEY"].encode("utf-8")
    return hmac.new(secret, raw.encode("utf-8"), "sha256").hexdigest()


def _permit(db, label, count, duration, now):
    key = _key(label)
    previous = db.execute(
        "SELECT count, expires FROM limits WHERE key=?", (key,)
    ).fetchone()
    if previous and previous["expires"] > now:
        if previous["count"] >= count:
            return False
        db.execute(
            "UPDATE limits SET count=count+1 WHERE key=?", (key,)
        )
    else:
        db.execute(
            "INSERT OR REPLACE INTO limits(key,count,expires) VALUES (?,1,?)",
            (key, now + duration),
        )
    return True


def _deliver_code(address, code):
    """Envoi transactionnel SMTP, sans log du code ni de l'adresse."""
    message = EmailMessage()
    message["From"] = os.environ["TAL_SMTP_FROM"]
    message["To"] = address
    message["Subject"] = "Code personnel enseignant — Suivi TAL" if reusable_mode() else "Connexion enseignant — Suivi TAL"
    if reusable_mode():
        message.set_content(
            "Voici votre nouveau code personnel pour le suivi TAL :\n\n"
            + code + "\n\n"
            + "Ce code reste utilisable jusqu'à son remplacement ou sa révocation "
            "depuis le serveur. Il remplace immédiatement le précédent.\n"
            + "Conservez-le comme un mot de passe et ne le transmettez pas.\n"
            + "Si vous n'avez pas demandé cette opération, contactez l'administrateur.\n"
        )
    else:
        message.set_content(
            "Voici votre code à usage unique pour consulter les synthèses "
            "de progression TAL :\n\n"
            + code + "\n\n"
            + "Ce code expire après 10 minutes et ne peut servir qu'une fois.\n"
            + "Si vous n'avez pas demandé cet accès, ignorez cet email.\n"
        )
    host = os.environ["TAL_SMTP_HOST"]
    security = os.environ["TAL_SMTP_SECURITY"].lower()
    port = int(os.getenv("TAL_SMTP_PORT", "465"))
    context = ssl.create_default_context()
    if security == "ssl":
        client = smtplib.SMTP_SSL(host, port, timeout=8, context=context)
    else:
        client = smtplib.SMTP(host, port, timeout=8)
    with client:
        if security == "starttls":
            client.starttls(context=context)
        username = os.getenv("TAL_SMTP_USER", "")
        if username:
            client.login(username, os.getenv("TAL_SMTP_PASSWORD", ""))
        client.send_message(message)


def issue_cli_code():
    """Envoi demandé manuellement depuis le conteneur ; aucune route web."""
    if not configured():
        raise RuntimeError("Portail enseignant non configuré")
    if reusable_mode():
        return issue_reusable_code()
    code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
    salt = secrets.token_hex(16)
    digest = _hash(code, salt)
    now = int(time.time())
    db = _db()
    authorized = False
    try:
        db.execute("BEGIN IMMEDIATE")
        by_ip = _permit(db, "send:admin-cli", 4, 3600, now)
        global_limit = _permit(db, "send:global", 8, 3600, now)
        authorized = by_ip and global_limit
        if authorized:
            db.execute(
                "INSERT OR REPLACE INTO challenge"
                "(id,salt,digest,expires,attempts) VALUES (1,?,?,?,0)",
                (salt, digest, now + CODE_SECONDS),
            )
        db.execute("DELETE FROM limits WHERE expires < ?", (now,))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    if not authorized:
        return False
    try:
        _deliver_code(teacher_email(), code)
    except (OSError, ValueError, RuntimeError, smtplib.SMTPException):
        # Ne retirer le défi que si aucun autre envoi concurrent ne l'a
        # remplacé entre-temps.
        db = _db()
        try:
            db.execute(
                "DELETE FROM challenge WHERE id=1 AND salt=?", (salt,)
            )
        finally:
            db.close()
        raise RuntimeError("Envoi SMTP indisponible") from None
    return True


def issue_reusable_code():
    """Créer ou remplacer le secret réutilisable (transaction atomique avec SMTP).

    En cas d'échec de l'envoi, le code précédent reste valable.
    """
    if not configured() or not reusable_mode():
        raise RuntimeError("Mode enseignant réutilisable non configuré")
    code = "".join(secrets.choice(ALPHABET) for _ in range(REUSABLE_CODE_LENGTH))
    salt = secrets.token_hex(16)
    digest = _hash(code, salt)
    owner = _key("teacher-reusable:" + teacher_email())
    now = int(time.time())
    db = _db()
    try:
        db.execute("BEGIN IMMEDIATE")
        allowed_cli = _permit(db, "send:admin-cli", 4, 3600, now)
        allowed_global = _permit(db, "send:global", 8, 3600, now)
        if not (allowed_cli and allowed_global):
            db.commit()
            return False
        db.execute(
            "INSERT OR REPLACE INTO reusable_credential"
            "(id,owner,salt,digest,created) VALUES (1,?,?,?,?)",
            (owner, salt, digest, now),
        )
        # L'envoi est volontairement dans la transaction pour conserver
        # l'ancien code si le serveur SMTP est indisponible.
        try:
            _deliver_code(teacher_email(), code)
        except (OSError, ValueError, RuntimeError, smtplib.SMTPException):
            raise RuntimeError("Envoi SMTP indisponible") from None
        db.execute("DELETE FROM limits WHERE expires < ?", (now,))
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def revoke_reusable_code():
    """Révoquer le code personnel et toutes les sessions associées (CLI)."""
    db = _db()
    try:
        db.execute("BEGIN IMMEDIATE")
        deleted = db.execute("DELETE FROM reusable_credential WHERE id=1").rowcount
        db.commit()
        return bool(deleted)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def verify_reusable_code(code, ip, email):
    """Vérification à temps constant, limitée par IP et globalement."""
    value = code.strip().upper()
    if len(value) != REUSABLE_CODE_LENGTH or any(c not in ALPHABET for c in value):
        return False
    now = int(time.time())
    db = _db()
    try:
        db.execute("BEGIN IMMEDIATE")
        allowed_ip = _permit(db, "login:ip:" + ip, 10, 15 * 60, now)
        allowed_global = _permit(db, "login:reusable:global", 30, 15 * 60, now)
        row = db.execute(
            "SELECT owner,salt,digest FROM reusable_credential WHERE id=1"
        ).fetchone()
        success = bool(
            allowed_ip and allowed_global and row
            and hmac.compare_digest(email.strip().lower(), teacher_email())
            and hmac.compare_digest(row["owner"], _key("teacher-reusable:" + teacher_email()))
            and hmac.compare_digest(_hash(value, row["salt"]), row["digest"])
        )
        db.execute("DELETE FROM limits WHERE expires < ?", (now,))
        db.commit()
        return success
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def consume_code(code, ip, email):
    """Vérifier le code du mode actif ; jamais de repli entre modes."""
    if (not configured() or not isinstance(code, str)
            or not isinstance(email, str) or len(email) > 254):
        return False
    if reusable_mode():
        return verify_reusable_code(code, ip, email)
    value = code.strip().upper()
    if len(value) != CODE_LENGTH or any(c not in ALPHABET for c in value):
        return False
    now = int(time.time())
    db = _db()
    try:
        db.execute("BEGIN IMMEDIATE")
        allowed = _permit(db, "login:ip:" + ip, 10, 15 * 60, now)
        challenge = db.execute(
            "SELECT salt,digest,expires,attempts FROM challenge WHERE id=1"
        ).fetchone()
        success = False
        valid_email = hmac.compare_digest(email.strip().lower(), teacher_email())
        if allowed and valid_email and challenge and challenge["expires"] >= now and challenge["attempts"] < 5:
            db.execute("UPDATE challenge SET attempts=attempts+1 WHERE id=1")
            success = hmac.compare_digest(
                _hash(value, challenge["salt"]), challenge["digest"]
            )
            if success:
                db.execute("DELETE FROM challenge WHERE id=1")
        db.execute("DELETE FROM limits WHERE expires < ?", (now,))
        db.commit()
        return success
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def session_identity():
    """Empreinte de la session : une rotation révoque les sessions réutilisables."""
    if reusable_mode():
        db = _db()
        try:
            row = db.execute("SELECT salt FROM reusable_credential WHERE id=1").fetchone()
        finally:
            db.close()
        salt = row["salt"] if row else "aucun-code"
        return _key("teacher-session:reusable:" + teacher_email() + ":" + salt)
    return _key("teacher-session:one_time:" + teacher_email())


def session_valid(auth_at, identity):
    if not configured() or type(auth_at) is not int:
        return False
    if not isinstance(identity, str):
        return False
    elapsed = time.time() - auth_at
    return 0 <= elapsed < SESSION_SECONDS and hmac.compare_digest(
        identity, session_identity()
    )
