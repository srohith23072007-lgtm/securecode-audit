"""Shared fixtures for the authentication tests."""

import sys
from pathlib import Path

import pytest

SOURCE_DIRECTORY = Path(__file__).resolve().parents[1] / "Source Code"
sys.path.insert(0, str(SOURCE_DIRECTORY))

from securecode_audit.database import UserDatabase
from securecode_audit.service import AuthenticationService


@pytest.fixture
def service(tmp_path, monkeypatch):
    monkeypatch.setenv("SECURECODE_AUDIT_PEPPER", "test-only-pepper-value-long-enough-123")
    database = UserDatabase(tmp_path / "users.sqlite3")
    return AuthenticationService(database)
