"""Input validation rules for account registration and login."""

import re

from .errors import ValidationError

_USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{3,32}$")
MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 128


def validate_username(username: str) -> str:
    """Return a normalized username or raise ValidationError."""
    if not isinstance(username, str) or not _USERNAME_PATTERN.fullmatch(username):
        raise ValidationError(
            "Username must be 3-32 characters using letters, numbers, dot, "
            "underscore, or hyphen."
        )
    return username


def validate_password(password: str) -> str:
    """Return a valid password unchanged or raise ValidationError."""
    if not isinstance(password, str):
        raise ValidationError("Password must be text.")
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password must be between {MIN_PASSWORD_LENGTH} and "
            f"{MAX_PASSWORD_LENGTH} characters."
        )
    if "\x00" in password:
        raise ValidationError("Password contains an unsupported character.")
    return password
