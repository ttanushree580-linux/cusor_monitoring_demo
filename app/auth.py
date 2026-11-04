import os
import secrets
from functools import wraps

from flask import abort, current_app, redirect, request, session, url_for
from werkzeug.security import check_password_hash

# Hash of the local demo password. The plain password is not stored.
DEFAULT_ADMIN_PASSWORD_HASH = (
    "scrypt:32768:8:1$QayI3tKb365y3kKZ$"
    "1cf122d5b125c3f3f7757d518c768e63a9c21a22c14d033d5308bc5a956853c3"
    "af74f88c7907b3633031d41831da309646c1a6f03f185ddc24f0a15a0c625b46"
)


def admin_password_hash():
    return os.environ.get("ADMIN_PASSWORD_HASH", DEFAULT_ADMIN_PASSWORD_HASH)


def ensure_csrf():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_hex(32)
        session["csrf_token"] = token
    return token


def validate_csrf():
    sent = request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")
    if not sent or not expected or not secrets.compare_digest(sent, expected):
        abort(400)


def credentials_match(username, password):
    password_hash = current_app.config["ADMIN_PASSWORD_HASH"]
    hash_ok = check_password_hash(password_hash, password)
    return username == current_app.config["ADMIN_USERNAME"] and hash_ok


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("user") != current_app.config["ADMIN_USERNAME"]:
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped
