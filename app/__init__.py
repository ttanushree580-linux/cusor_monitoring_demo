from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = False

    @app.get("/")
    def dashboard():
        cards = [
            {"name": "CPU", "detail": "Usage on the selected server"},
            {"name": "Memory", "detail": "Used and total memory"},
            {"name": "Network", "detail": "Bytes sent and received"},
            {"name": "Ports", "detail": "Listening TCP ports"},
        ]
        return render_template("dashboard.html", cards=cards)

    return app
