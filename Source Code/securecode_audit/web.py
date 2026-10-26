"""Simple Flask interface for the local SecureCode-Audit demo."""

import os
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from .database import UserDatabase
from .errors import ConfigurationError, SecureCodeAuditError, UserAlreadyExistsError
from .service import AuthenticationService

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(database_path: str | Path | None = None) -> Flask:
    """Build the Flask application for the secure-demo website."""
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config["SECRET_KEY"] = os.environ.get(
        "SECURECODE_AUDIT_WEB_SECRET",
        "local-demo-web-secret-change-this",
    )
    app.config["DATABASE_PATH"] = str(
        database_path
        or os.environ.get("SECURECODE_AUDIT_DB", str(BASE_DIR / "securecode_audit.sqlite3"))
    )

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.post("/register")
    def register() -> object:
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        try:
            service = AuthenticationService(UserDatabase(app.config["DATABASE_PATH"]))
            service.register(username, password)
        except UserAlreadyExistsError:
            flash("That username already exists.", "error")
        except ConfigurationError as error:
            flash(str(error), "error")
        except SecureCodeAuditError as error:
            flash(str(error), "error")
        except (OSError, sqlite3.Error):
            flash("The local database could not be accessed.", "error")
        else:
            flash("Account created successfully.", "success")
        return redirect(url_for("index"))

    @app.post("/login")
    def login() -> object:
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        try:
            service = AuthenticationService(UserDatabase(app.config["DATABASE_PATH"]))
            if service.authenticate(username, password):
                flash("Authentication successful.", "success")
            else:
                flash("Authentication failed. Check your username and password.", "error")
        except ConfigurationError as error:
            flash(str(error), "error")
        except (OSError, sqlite3.Error):
            flash("The local database could not be accessed.", "error")
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
