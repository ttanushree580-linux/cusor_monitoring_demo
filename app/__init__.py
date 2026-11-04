import os
from pathlib import Path

from flask import Flask

from app.auth import DEFAULT_ADMIN_PASSWORD_HASH, admin_password_hash
from app.views import bp


def create_app(test_config=None):
    app = Flask(__name__)
    data_path = Path(app.root_path).resolve().parent / "data" / "servers.json"
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "demo-local-only-change-me"),
        ADMIN_USERNAME="admin",
        ADMIN_PASSWORD_HASH=admin_password_hash() or DEFAULT_ADMIN_PASSWORD_HASH,
        SERVERS_PATH=str(data_path),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        DEBUG=False,
    )
    if test_config:
        app.config.update(test_config)
    app.register_blueprint(bp)
    return app
