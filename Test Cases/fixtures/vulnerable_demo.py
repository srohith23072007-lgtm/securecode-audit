"""TEST-ONLY deliberately vulnerable patterns for local Bandit demonstrations.

Never run this against a real database or reuse these patterns in an application.
All values below are fake placeholders and the function creates only in-memory data.
"""

import hashlib
import sqlite3

DEMO_PASSWORD = "FAKE-TEST-ONLY-NOT-A-CREDENTIAL"


def find_user_unsafe(username: str) -> list[tuple]:
    """Intentionally concatenate input into SQL to demonstrate injection risk."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (username TEXT)")
    connection.execute("INSERT INTO users VALUES ('demo')")
    query = "SELECT username FROM users WHERE username = '" + username + "'"
    return connection.execute(query).fetchall()


def weak_password_digest(password: str) -> str:
    """Intentionally use a fast hash to demonstrate unsafe password storage."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def ignore_database_error() -> None:
    """Intentionally suppress an exception to demonstrate improper error handling."""
    try:
        raise sqlite3.OperationalError("fake test-only database error")
    except Exception:
        pass
