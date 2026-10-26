"""Account operations that combine validation, hashing, and persistence."""

import sqlite3

from .database import UserDatabase
from .errors import UserAlreadyExistsError, ValidationError
from .password import hash_password, load_pepper, verify_password
from .validation import validate_password, validate_username


class AuthenticationService:
    """Register accounts and authenticate them against the local repository."""

    def __init__(self, database: UserDatabase) -> None:
        self.database = database
        self.database.initialize()

    def register(self, username: str, password: str) -> None:
        """Validate and store a newly registered account."""
        validated_username = validate_username(username)
        validated_password = validate_password(password)
        pepper = load_pepper()
        salt, digest = hash_password(validated_password, pepper)
        try:
            self.database.create_user(validated_username, salt, digest)
        except sqlite3.IntegrityError as error:
            raise UserAlreadyExistsError("An account with that username already exists.") from error

    def authenticate(self, username: str, password: str) -> bool:
        """Return whether credentials match; use a generic failure for bad input."""
        try:
            validated_username = validate_username(username)
            validated_password = validate_password(password)
        except ValidationError:
            return False

        pepper = load_pepper()
        record = self.database.get_user(validated_username)
        if record is None:
            return False
        return verify_password(
            validated_password,
            bytes(record["salt"]),
            bytes(record["password_hash"]),
            pepper,
        )
