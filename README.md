# Server monitor

Local demo for CPU, memory, network, and listening ports on this Linux machine. The pages are read only. Sign-in uses the username `admin` and a hashed password. You can add Linux servers to the list. Metrics are collected when the saved host is this machine: `localhost`, `127.0.0.1`, an address on a local interface, or this machine's public IP. Other saved hosts are listed and not contacted.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest==8.3.5
python -m pytest
flask --app app run --host 127.0.0.1 --port 5000
```

Open http://127.0.0.1:5000

Sign in with `admin` / `admin123`. The app stores a hash of that password and checks the hash at login. The plain password is not kept in the application code.

The app listens on `127.0.0.1`. Flask debug stays off unless you turn it on yourself.

## Use

1. Sign in.
2. Add a server. Display name: `This machine`. Hostname: `127.0.0.1`.
3. The dashboard shows CPU, memory used of total, bytes sent and received since boot, and listening TCP ports.
4. Open the server to see the same read-only metrics.
5. A hostname that is not this machine is saved in the list and is not contacted. The page says: “Metrics for remote hosts are not collected in this demo.” This machine's public IP, such as the address shown by `ifconfig.me`, is treated as this machine.

Servers are stored in `data/servers.json`.

The network card is a counter since boot, not a live rate. The port card lists listening TCP ports as address and port only. Process command lines are not shown.

Numbers reload every 15 seconds. Refresh reloads sooner and does not change the host. Typing in the add-server form pauses the automatic reload.

## Tests and CI

`python -m pytest` runs the unit tests.

GitHub Actions (`.github/workflows/ci.yml`) runs those tests on Python 3.11 for every push and pull request. There is no deploy job. After CI is green, start the app on this machine with the command above.

## Configuration

- `ADMIN_PASSWORD_HASH` overrides the demo password hash.
- `SECRET_KEY` sets the session signing key. The built-in default is for this machine only. Set your own before using the app anywhere else.

The session cookie is `HttpOnly` and `SameSite=Lax`. Do not commit `.env` files or private keys.
