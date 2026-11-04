from werkzeug.security import check_password_hash

from app.auth import DEFAULT_ADMIN_PASSWORD_HASH


def test_demo_hash_matches_documented_password():
    assert check_password_hash(DEFAULT_ADMIN_PASSWORD_HASH, "admin123")


def test_valid_login(client, login):
    response = login()
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    page = client.get("/")
    assert page.status_code == 200
    assert b"Server monitor" in page.data


def test_wrong_password(client, login):
    response = login(password="not-the-password")
    assert response.status_code == 200
    assert b"Invalid username or password." in response.data


def test_unknown_user(client, login):
    response = login(username="someone-else")
    assert response.status_code == 200
    assert b"Invalid username or password." in response.data


def test_anonymous_dashboard_redirects(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_logout(client, login):
    login()
    with client.session_transaction() as sess:
        token = sess["csrf_token"]
    response = client.post("/logout", data={"csrf_token": token})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
    follow = client.get("/")
    assert follow.status_code == 302
    assert follow.headers["Location"].endswith("/login")


def test_session_cookie_is_httponly_and_samesite(client, login):
    response = login()
    cookie = response.headers["Set-Cookie"]
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie


def test_login_rejects_missing_csrf(client):
    response = client.post("/login", data={"username": "admin", "password": "admin123"})
    assert response.status_code == 400
