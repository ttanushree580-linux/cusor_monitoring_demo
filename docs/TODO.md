# Implementation TODO

Local demo only. Python and Flask, run on this machine. Read-only view of Linux CPU, memory, network, and port usage. One admin user. Password stored as a hash. Servers are added in the app.

Do the steps in order. Finish one step and run the app locally before starting the next.

## 1. Project initialization and basic UI

- [ ] Add `.gitignore` for `.venv/`, `__pycache__/`, `.pytest_cache/`, and `.env`.
- [ ] Add `requirements.txt` with pinned `Flask`.
- [ ] Add a Flask app factory in `app/__init__.py`.
- [ ] Serve one page at `/` with a read-only dashboard shell (title and empty cards for CPU, memory, network, and ports).
- [ ] Add plain CSS so the page is easy to scan. No buttons that change a server.
- [ ] Run it with `flask --app app run --host 127.0.0.1 --port 5000`.

Security:

- [ ] Bind to `127.0.0.1` only.
- [ ] Leave Flask debug off unless you are actively developing.
- [ ] Do not put secrets in the repo.

Documentation:

- [ ] `README.md`: create a virtualenv, install requirements, start the app, open `http://127.0.0.1:5000`.

## 2. Sign-in functionality and unit tests

- [ ] Add `/login` with username and password fields.
- [ ] Accept only username `admin`.
- [ ] Compare the password to a Werkzeug hash, never to a plain-text password.
- [ ] On success, store a server-side session and redirect to `/`.
- [ ] On failure, show one generic message: “Invalid username or password.”
- [ ] Require a session for `/`. Send anonymous users to `/login`.
- [ ] Add `/logout` to clear the session.
- [ ] Add `tests/test_auth.py` for: valid login, wrong password, unknown user, anonymous access to `/`, and logout.
- [ ] Run `python -m pytest`.

Security:

- [ ] Store the demo password only as a hash (environment variable `ADMIN_PASSWORD_HASH`, with a local demo default hash for `admin` / `admin123`).
- [ ] Set the session cookie to `HttpOnly` and `SameSite=Lax`.
- [ ] Set a fixed `SECRET_KEY` from the environment for anything beyond this machine.
- [ ] Do not log the password or the hash.
- [ ] Add a CSRF token on the login form.

Documentation:

- [ ] `README.md`: demo login `admin` / `admin123`, and that the password is checked as a hash.
- [ ] `README.md`: how to run `python -m pytest`.

## 3. CI/CD with GitHub Actions

- [ ] Add `.github/workflows/ci.yml` that runs on push and pull request.
- [ ] The workflow installs `requirements.txt` plus `pytest`, then runs `python -m pytest`.
- [ ] Use one Python version (3.11).
- [ ] Delivery stays local: after the workflow is green, start the app on this machine. No deploy job to another host.

Security:

- [ ] Do not put secrets, the password, or a production `SECRET_KEY` in the workflow file.
- [ ] Let the tests use the demo hash already in the app.

Documentation:

- [ ] `README.md`: CI runs tests on GitHub; the app itself is started locally.

## 4. Add a Linux server

- [ ] After login, show a short form: display name and hostname.
- [ ] Save servers in a local JSON file under the project (for example `data/servers.json`).
- [ ] List saved servers on the dashboard. The list is view-only apart from this add form.
- [ ] Reject an empty name, an empty hostname, and duplicate hostnames.
- [ ] Add unit tests for valid add, missing fields, and duplicates.

Security:

- [ ] Only a signed-in admin can add a server.
- [ ] CSRF token on the add form.
- [ ] Treat the hostname as text. Do not pass it to a shell.
- [ ] Allow only a simple hostname or IP (letters, digits, `.` and `-`).

Documentation:

- [ ] `README.md`: sign in, add a server, see it in the list. Note the JSON file path.

## 5. CPU and memory for this machine

- [ ] Add `psutil` (pinned) and read CPU percent and memory used / total.
- [ ] Show those values on the dashboard for the server that points at this machine (`localhost` or `127.0.0.1`).
- [ ] Refresh the numbers every 15 seconds with a small script, or a manual Refresh link if that is simpler.
- [ ] Add unit tests with a fake metrics reader so tests do not depend on live load.

Security:

- [ ] Read metrics inside the Flask process. Do not shell out.
- [ ] Keep the page read-only: no action that changes the host.

Documentation:

- [ ] `README.md`: add this machine as `127.0.0.1` to see CPU and memory.

## 6. Network and ports

- [ ] Show bytes sent and bytes received since boot.
- [ ] Show listening TCP ports (port number and address).
- [ ] Add unit tests with a fake network and port reader.

Security:

- [ ] Show port and address only. Omit process command lines.
- [ ] Keep collection inside the process (`psutil`), not via shell.

Documentation:

- [ ] `README.md`: what the network and port cards mean.

## 7. Metrics for the selected server

- [ ] Clicking a server in the list opens its read-only metrics page.
- [ ] For `localhost` / `127.0.0.1`, show the live CPU, memory, network, and ports from steps 5 and 6.
- [ ] For any other hostname, show the saved name and host, and the text “Metrics for remote hosts are not collected in this demo.”
- [ ] Add a unit test that local hosts return numbers and other hosts return that message.

Security:

- [ ] Do not open SSH connections and do not run remote commands in this demo.
- [ ] The metrics page stays read-only.

Documentation:

- [ ] `README.md`: this demo collects metrics only for this machine. Other saved hosts are listed and not contacted.

## 8. Local smoke check

- [ ] From a clean virtualenv: install, run tests, start on `127.0.0.1:5000`.
- [ ] Sign in as `admin`, add `127.0.0.1`, and confirm CPU, memory, network, and ports render.
- [ ] Confirm `/` redirects to `/login` when logged out.
- [ ] Confirm a non-local hostname is stored and shows the remote-not-collected message.

Security:

- [ ] Confirm the repo has no `.env`, no plain-text password, and no private keys.

Documentation:

- [ ] `README.md` matches the commands used in this check.
