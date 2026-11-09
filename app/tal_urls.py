"""Canonical relative links for TAL when SWAG omits X-Forwarded-Prefix.

Never infer a new public prefix from an untrusted browser field. The prefix
comes from the server's TAL_SESSION_COOKIE_PATH setting.
"""
from flask import current_app, request, url_for


def tal_url_for(endpoint, **values):
    """Build links under the canonical public cookie path, if configured."""
    target = url_for(endpoint, **values)
    canonical = current_app.config.get("SESSION_COOKIE_PATH", "/").rstrip("/")
    if not canonical:
        return target
    script = request.script_root.rstrip("/")
    if script and target.startswith(script + "/"):
        target = target[len(script):]
    if target.startswith(canonical + "/"):
        return target
    if not target.startswith("/"):
        raise ValueError("URL relative inattendue")
    return canonical + target
