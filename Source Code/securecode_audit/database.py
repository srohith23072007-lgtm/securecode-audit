"""SQLite persistence with bound parameters for every user-controlled value."""

import sqlite3
from pathlib import Path


class UserDatabase:
    """Small SQLite repository for the local authentication demonstration."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=5.0)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        """Create the account table if it does not already exist."""
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    salt BLOB NOT NULL,
                    password_hash BLOB NOT NULL
                )
                """
            )

    def create_user(self, username: str, salt: bytes, password_hash: bytes) -> None:
        """Persist an account using parameter binding, never SQL interpolation."""
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                (username, salt, password_hash),
            )

    def get_user(self, username: str) -> sqlite3.Row | None:
        """Fetch one account using a bound username parameter."""
        with self._connect() as connection:
            return connection.execute(
                "SELECT username, salt, password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()
