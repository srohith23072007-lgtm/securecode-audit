"""Tests for the Flask-based SecureCode-Audit website."""

from securecode_audit.web import create_app


def test_homepage_renders(monkeypatch, tmp_path):
    database_path = tmp_path / "web_demo.sqlite3"
    monkeypatch.setenv("SECURECODE_AUDIT_DB", str(database_path))
    monkeypatch.setenv("SECURECODE_AUDIT_PEPPER", "local-demo-pepper-change-this-32-chars")

    app = create_app(database_path)
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"SecureCode-Audit" in response.data


def test_registration_and_login_flow(monkeypatch, tmp_path):
    database_path = tmp_path / "web_demo.sqlite3"
    monkeypatch.setenv("SECURECODE_AUDIT_DB", str(database_path))
    monkeypatch.setenv("SECURECODE_AUDIT_PEPPER", "local-demo-pepper-change-this-32-chars")

    app = create_app(database_path)
    client = app.test_client()

    register_response = client.post(
        "/register",
        data={"username": "demo_user", "password": "StrongPassword123!"},
        follow_redirects=True,
    )
    assert register_response.status_code == 200
    assert b"Account created successfully." in register_response.data

    login_response = client.post(
        "/login",
        data={"username": "demo_user", "password": "StrongPassword123!"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200
    assert b"Authentication successful." in login_response.data
