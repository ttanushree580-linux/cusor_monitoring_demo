# Server Monitor

Local demo for a read-only view of Linux server usage. This step shows an empty dashboard only.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --host 127.0.0.1 --port 5000
```

Open http://127.0.0.1:5000.

The app listens on this machine only. Debug mode stays off.
