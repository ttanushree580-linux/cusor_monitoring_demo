import ipaddress
import os
import socket
import urllib.request

import psutil

LOCAL_NAMES = frozenset({"localhost", "127.0.0.1", "::1"})
REMOTE_MESSAGE = "Metrics for remote hosts are not collected in this demo."
_public_ip = {"done": False, "value": ""}


def interface_addresses():
    found = set()
    for addresses in psutil.net_if_addrs().values():
        for address in addresses:
            if address.family not in (socket.AF_INET, socket.AF_INET6):
                continue
            ip = (address.address or "").split("%", 1)[0].strip().lower()
            if ip:
                found.add(ip)
    return found


def detected_public_ip():
    if _public_ip["done"]:
        return _public_ip["value"]
    _public_ip["done"] = True
    override = os.environ.get("MONITOR_PUBLIC_IP", "").strip()
    _public_ip["value"] = override or _fetch_public_ip()
    return _public_ip["value"]


def _fetch_public_ip():
    request = urllib.request.Request(
        "https://ifconfig.me/ip",
        headers={"User-Agent": "server-monitor"},
    )
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            text = response.read().decode().strip()
    except (OSError, TimeoutError, ValueError):
        return ""
    try:
        ipaddress.ip_address(text)
    except ValueError:
        return ""
    return text


def is_local(hostname):
    host = (hostname or "").strip().lower()
    if host in LOCAL_NAMES or host in interface_addresses():
        return True
    public = (detected_public_ip() or "").strip().lower()
    return bool(public) and host == public


def format_bytes(num):
    size = float(num)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(size)} B"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def collect_local_metrics():
    memory = psutil.virtual_memory()
    network = psutil.net_io_counters()
    ports = []
    try:
        connections = psutil.net_connections(kind="tcp")
    except (psutil.AccessDenied, PermissionError, OSError):
        connections = []
    for conn in connections:
        if conn.status != psutil.CONN_LISTEN or not conn.laddr:
            continue
        ports.append({"address": conn.laddr.ip, "port": int(conn.laddr.port)})
    ports.sort(key=lambda item: (item["port"], item["address"]))
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_used": int(memory.used),
        "memory_total": int(memory.total),
        "bytes_sent": int(network.bytes_sent),
        "bytes_recv": int(network.bytes_recv),
        "ports": ports,
    }


def metrics_for_host(hostname, reader=None):
    if not is_local(hostname):
        return {"available": False, "message": REMOTE_MESSAGE}
    data = (reader or collect_local_metrics)()
    ports = [
        {"address": str(item["address"]), "port": int(item["port"])}
        for item in data.get("ports", [])
    ]
    return {
        "available": True,
        "cpu_percent": float(data["cpu_percent"]),
        "memory_used": int(data["memory_used"]),
        "memory_total": int(data["memory_total"]),
        "bytes_sent": int(data["bytes_sent"]),
        "bytes_recv": int(data["bytes_recv"]),
        "ports": ports,
    }


def present_metrics(metrics):
    if not metrics["available"]:
        return metrics
    used = metrics["memory_used"]
    total = metrics["memory_total"]
    percent = (used / total * 100) if total else 0
    return {
        **metrics,
        "cpu_display": f"{metrics['cpu_percent']:.1f}%",
        "memory_display": f"{format_bytes(used)} / {format_bytes(total)} ({percent:.0f}%)",
        "sent_display": format_bytes(metrics["bytes_sent"]),
        "recv_display": format_bytes(metrics["bytes_recv"]),
    }
