import pytest

from app import create_app
from app.auth import DEFAULT_ADMIN_PASSWORD_HASH


@pytest.fixture(autouse=True)
def no_public_ip_lookup(monkeypatch):
    monkeypatch.setattr("app.metrics.detected_public_ip", lambda: "")


@pytest.fixture
def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SERVERS_PATH": str(tmp_path / "servers.json"),
            "ADMIN_PASSWORD_HASH": DEFAULT_ADMIN_PASSWORD_HASH,
        }
    )


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def login(client):
    def _login(username="admin", password="admin123"):
        client.get("/login")
        with client.session_transaction() as sess:
            token = sess["csrf_token"]
        return client.post(
            "/login",
            data={"username": username, "password": password, "csrf_token": token},
        )

    return _login


@pytest.fixture
def add_server(client):
    def _add(name, hostname):
        with client.session_transaction() as sess:
            token = sess["csrf_token"]
        return client.post(
            "/servers",
            data={"name": name, "hostname": hostname, "csrf_token": token},
            follow_redirects=True,
        )

    return _add
