import secrets

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.auth import credentials_match, ensure_csrf, login_required, validate_csrf
from app.metrics import is_local, metrics_for_host, present_metrics
from app.servers import ServerError, add_server, get_server, load_servers

bp = Blueprint("main", __name__)


@bp.app_context_processor
def inject_template_globals():
    return {
        "csrf_token": ensure_csrf(),
        "current_user": session.get("user"),
        "is_local_host": is_local,
    }


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user") == current_app.config["ADMIN_USERNAME"]:
        return redirect(url_for("main.dashboard"))
    error = None
    if request.method == "POST":
        validate_csrf()
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if credentials_match(username, password):
            session.clear()
            session["user"] = current_app.config["ADMIN_USERNAME"]
            session["csrf_token"] = secrets.token_hex(32)
            return redirect(url_for("main.dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@bp.post("/logout")
def logout():
    validate_csrf()
    session.clear()
    return redirect(url_for("main.login"))


@bp.get("/")
@login_required
def dashboard():
    servers = load_servers(current_app.config["SERVERS_PATH"])
    local = next((server for server in servers if is_local(server["hostname"])), None)
    metrics = present_metrics(metrics_for_host(local["hostname"])) if local else None
    return render_template(
        "dashboard.html",
        servers=servers,
        metrics=metrics,
        local_server=local,
    )


@bp.post("/servers")
@login_required
def add_server_view():
    validate_csrf()
    try:
        add_server(
            current_app.config["SERVERS_PATH"],
            request.form.get("name", ""),
            request.form.get("hostname", ""),
        )
    except ServerError as exc:
        flash(str(exc), "error")
    else:
        flash("Server added.", "ok")
    return redirect(url_for("main.dashboard"))


@bp.get("/servers/<server_id>")
@login_required
def server_detail(server_id):
    server = get_server(current_app.config["SERVERS_PATH"], server_id)
    if server is None:
        abort(404)
    metrics = present_metrics(metrics_for_host(server["hostname"]))
    return render_template("server.html", server=server, metrics=metrics)
