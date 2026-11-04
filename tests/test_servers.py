def test_add_server(client, login, add_server):
    login()
    response = add_server("This machine", "127.0.0.1")
    assert response.status_code == 200
    assert b"Server added." in response.data
    assert b"This machine" in response.data
    assert b"127.0.0.1" in response.data


def test_missing_name(client, login, add_server):
    login()
    response = add_server("   ", "127.0.0.1")
    assert b"Name is required." in response.data
    assert b"No servers yet." in response.data


def test_missing_hostname(client, login, add_server):
    login()
    response = add_server("This machine", " ")
    assert b"Hostname is required." in response.data
    assert b"No servers yet." in response.data


def test_duplicate_hostname(client, login, add_server):
    login()
    add_server("This machine", "localhost")
    response = add_server("Again", "LocalHost")
    assert b"That hostname is already in the list." in response.data
    assert response.data.count(b"Again") == 0


def test_rejects_shell_metacharacters(client, login, add_server):
    login()
    response = add_server("Bad", "127.0.0.1; rm -rf /")
    assert b"letters, digits, dots, and hyphens" in response.data
    assert b"rm -rf" not in response.data


def test_anonymous_cannot_add(client):
    response = client.post("/servers", data={"name": "X", "hostname": "127.0.0.1"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
