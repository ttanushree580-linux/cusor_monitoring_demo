from app.metrics import collect_local_metrics, metrics_for_host

FAKE = {
    "cpu_percent": 12.5,
    "memory_used": 1048576,
    "memory_total": 4194304,
    "bytes_sent": 1048576,
    "bytes_recv": 2097152,
    "ports": [
        {
            "address": "127.0.0.1",
            "port": 5000,
            "command": "secret-process --password",
        }
    ],
}


def test_local_host_returns_numbers_without_command_line():
    result = metrics_for_host("127.0.0.1", reader=lambda: FAKE)
    assert result["available"] is True
    assert result["cpu_percent"] == 12.5
    assert result["bytes_sent"] == 1048576
    assert result["bytes_recv"] == 2097152
    assert result["ports"] == [{"address": "127.0.0.1", "port": 5000}]


def test_this_machine_public_ip_returns_local_metrics(monkeypatch):
    monkeypatch.setattr("app.metrics.detected_public_ip", lambda: "20.235.34.15")
    monkeypatch.setattr("app.metrics.interface_addresses", lambda: {"127.0.0.1"})
    result = metrics_for_host("20.235.34.15", reader=lambda: FAKE)
    assert result["available"] is True
    assert result["cpu_percent"] == 12.5


def test_interface_address_returns_local_metrics(monkeypatch):
    monkeypatch.setattr("app.metrics.interface_addresses", lambda: {"10.0.8.39"})
    result = metrics_for_host("10.0.8.39", reader=lambda: FAKE)
    assert result["available"] is True


def test_remote_host_is_not_read():
    def boom():
        raise AssertionError("reader should not run")

    result = metrics_for_host("db.internal", reader=boom)
    assert result["available"] is False
    assert result["message"] == "Metrics for remote hosts are not collected in this demo."


def test_dashboard_uses_fake_reader(client, login, add_server, monkeypatch):
    monkeypatch.setattr("app.metrics.collect_local_metrics", lambda: FAKE)
    login()
    page = add_server("This machine", "127.0.0.1")
    assert b"12.5%" in page.data
    assert b"1.0 MB" in page.data
    assert b"2.0 MB" in page.data
    assert b"5000" in page.data
    assert b"secret-process" not in page.data


def test_detail_page_for_local_and_remote(client, login, add_server, monkeypatch):
    monkeypatch.setattr("app.metrics.collect_local_metrics", lambda: FAKE)
    login()
    add_server("This machine", "localhost")
    add_server("Other", "db.example.com")
    listing = client.get("/")
    assert b"This machine" in listing.data
    local_id = listing.data.split(b"/servers/")[1].split(b'"')[0].decode()
    local_page = client.get(f"/servers/{local_id}")
    assert b"12.5%" in local_page.data
    remote_id = listing.data.split(b"/servers/")[2].split(b'"')[0].decode()
    remote_page = client.get(f"/servers/{remote_id}")
    assert b"Metrics for remote hosts are not collected in this demo." in remote_page.data
    assert b"12.5%" not in remote_page.data


def test_collect_local_metrics_shape():
    data = collect_local_metrics()
    assert 0 <= data["cpu_percent"] <= 100
    assert data["memory_total"] > 0
    assert data["memory_used"] >= 0
    assert data["bytes_sent"] >= 0
    assert data["bytes_recv"] >= 0
    assert isinstance(data["ports"], list)
    for port in data["ports"]:
        assert set(port) == {"address", "port"}
