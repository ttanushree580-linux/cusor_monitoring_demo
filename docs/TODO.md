# Implementation TODO

Local demo only. Python and Flask, run on this machine. Read-only view of Linux CPU, memory, network, and port usage. One admin user. Password stored as a hash. Servers are added in the app.

Do the steps in order. Finish one step and run the app locally before starting the next.

## 1. Project initialization and basic UI

- [x] Add `.gitignore` for `.venv/`, `__pycache__/`, `.pytest_cache/`, and `.env`.
- [x] Add `requirements.txt` with pinned `Flask`.
- [x] Add a Flask app factory in `app/__init__.py`.
- [x] Serve one page at `/` with a read-only dashboard shell (title and empty cards for CPU, memory, network, and ports).
- [x] Add plain CSS so the page is easy to scan. No buttons that change a server.
- [x] Run it with `flask --app app run --host 127.0.0.1 --port 5000`.

Security:

- [x] Bind to `127.0.0.1` only.
- [x] Leave Flask debug off unless you are actively developing.
- [x] Do not put secrets in the repo.

Documentation:

- [x] `README.md`: create a virtualenv, install requirements, start the app, open `http://127.0.0.1:5000`.

## 2. Sign-in functionality and unit tests

- [x] Add `/login` with username and password fields.
- [x] Accept only username `admin`.
- [x] Compare the password to a Werkzeug hash, never to a plain-text password.
- [x] On success, store a server-side session and redirect to `/`.
- [x] On failure, show one generic message: “Invalid username or password.”
- [x] Require a session for `/`. Send anonymous users to `/login`.
- [x] Add `/logout` to clear the session.
- [x] Add `tests/test_auth.py` for: valid login, wrong password, unknown user, anonymous access to `/`, and logout.
- [x] Run `python -m pytest`.

Security:

- [x] Store the demo password only as a hash (environment variable `ADMIN_PASSWORD_HASH`, with a local demo default hash for `admin` / `admin123`).
- [x] Set the session cookie to `HttpOnly` and `SameSite=Lax`.
- [x] Set a fixed `SECRET_KEY` from the environment for anything beyond this machine.
- [x] Do not log the password or the hash.
- [x] Add a CSRF token on the login form.

Documentation:

- [x] `README.md`: demo login `admin` / `admin123`, and that the password is checked as a hash.
- [x] `README.md`: how to run `python -m pytest`.

## 3. CI/CD with GitHub Actions

- [x] Add `.github/workflows/ci.yml` that runs on push and pull request.
- [x] The workflow installs `requirements.txt` plus `pytest`, then runs `python -m pytest`.
- [x] Use one Python version (3.11).
- [x] Delivery stays local: after the workflow is green, start the app on this machine. No deploy job to another host.

Security:

- [x] Do not put secrets, the password, or a production `SECRET_KEY` in the workflow file.
- [x] Let the tests use the demo hash already in the app.

Documentation:

- [x] `README.md`: CI runs tests on GitHub; the app itself is started locally.

## 4. Add a Linux server

- [x] After login, show a short form: display name and hostname.
- [x] Save servers in a local JSON file under the project (for example `data/servers.json`).
- [x] List saved servers on the dashboard. The list is view-only apart from this add form.
- [x] Reject an empty name, an empty hostname, and duplicate hostnames.
- [x] Add unit tests for valid add, missing fields, and duplicates.

Security:

- [x] Only a signed-in admin can add a server.
- [x] CSRF token on the add form.
- [x] Treat the hostname as text. Do not pass it to a shell.
- [x] Allow only a simple hostname or IP (letters, digits, `.` and `-`).

Documentation:

- [x] `README.md`: sign in, add a server, see it in the list. Note the JSON file path.

## 5. CPU and memory for this machine

- [x] Add `psutil` (pinned) and read CPU percent and memory used / total.
- [x] Show those values on the dashboard for the server that points at this machine (`localhost` or `127.0.0.1`).
- [x] Refresh the numbers every 15 seconds with a small script, or a manual Refresh link if that is simpler.
- [x] Add unit tests with a fake metrics reader so tests do not depend on live load.

Security:

- [x] Read metrics inside the Flask process. Do not shell out.
- [x] Keep the page read-only: no action that changes the host.

Documentation:

- [x] `README.md`: add this machine as `127.0.0.1` to see CPU and memory.

## 6. Network and ports

- [x] Show bytes sent and bytes received since boot.
- [x] Show listening TCP ports (port number and address).
- [x] Add unit tests with a fake network and port reader.

Security:

- [x] Show port and address only. Omit process command lines.
- [x] Keep collection inside the process (`psutil`), not via shell.

Documentation:

- [x] `README.md`: what the network and port cards mean.

## 7. Metrics for the selected server

- [x] Clicking a server in the list opens its read-only metrics page.
- [x] For `localhost` / `127.0.0.1`, show the live CPU, memory, network, and ports from steps 5 and 6.
- [x] For any other hostname, show the saved name and host, and the text “Metrics for remote hosts are not collected in this demo.”
- [x] Add a unit test that local hosts return numbers and other hosts return that message.

Security:

- [x] Do not open SSH connections and do not run remote commands in this demo.
- [x] The metrics page stays read-only.

Documentation:

- [x] `README.md`: this demo collects metrics only for this machine. Other saved hosts are listed and not contacted.

## 8. Local smoke check

- [x] From a clean virtualenv: install, run tests, start on `127.0.0.1:5000`.
- [x] Sign in as `admin`, add `127.0.0.1`, and confirm CPU, memory, network, and ports render.
- [x] Confirm `/` redirects to `/login` when logged out.
- [x] Confirm a non-local hostname is stored and shows the remote-not-collected message.

Security:

- [x] Confirm the repo has no `.env`, no plain-text password, and no private keys.

Documentation:

- [x] `README.md` matches the commands used in this check.
