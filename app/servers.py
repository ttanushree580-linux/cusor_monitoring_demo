import json
import re
import uuid
from pathlib import Path

HOST_RE = re.compile(
    r"^(?=.{1,253}$)"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)


class ServerError(ValueError):
    pass


def load_servers(path):
    file_path = Path(path)
    if not file_path.exists():
        return []
    raw = file_path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ServerError("Server list is invalid.")
    return data


def save_servers(path, servers):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(servers, indent=2) + "\n", encoding="utf-8")


def add_server(path, name, hostname):
    clean_name = (name or "").strip()
    clean_host = (hostname or "").strip()
    if not clean_name:
        raise ServerError("Name is required.")
    if len(clean_name) > 64 or any(ord(char) < 32 for char in clean_name):
        raise ServerError("Name is invalid.")
    if not clean_host:
        raise ServerError("Hostname is required.")
    if not HOST_RE.match(clean_host):
        raise ServerError(
            "Enter a hostname or IP using only letters, digits, dots, and hyphens."
        )
    servers = load_servers(path)
    if any(server["hostname"].lower() == clean_host.lower() for server in servers):
        raise ServerError("That hostname is already in the list.")
    server = {"id": uuid.uuid4().hex, "name": clean_name, "hostname": clean_host}
    servers.append(server)
    save_servers(path, servers)
    return server


def get_server(path, server_id):
    for server in load_servers(path):
        if server.get("id") == server_id:
            return server
    return None
