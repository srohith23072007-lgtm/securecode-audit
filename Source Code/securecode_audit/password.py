"""Password hashing and environment-based secret configuration."""

import hashlib
import hmac
import os
import secrets

from .errors import ConfigurationError

PBKDF2_ITERATIONS = 600_000
SALT_BYTES = 16
HASH_BYTES = 32
PEPPER_ENVIRONMENT_VARIABLE = "SECURECODE_AUDIT_PEPPER"
MIN_PEPPER_LENGTH = 32


def load_pepper() -> bytes:
    """Load the password pepper from the environment or fail explicitly."""
    pepper = os.environ.get(PEPPER_ENVIRONMENT_VARIABLE)
    if pepper is None or len(pepper) < MIN_PEPPER_LENGTH:
        raise ConfigurationError(
            f"Set {PEPPER_ENVIRONMENT_VARIABLE} to a secret of at least "
            f"{MIN_PEPPER_LENGTH} characters."
        )
    return pepper.encode("utf-8")


def hash_password(password: str, pepper: bytes) -> tuple[bytes, bytes]:
    """Return a fresh random salt and PBKDF2-HMAC-SHA-256 digest."""
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8") + pepper,
        salt,
        PBKDF2_ITERATIONS,
        dklen=HASH_BYTES,
    )
    return salt, digest


def verify_password(password: str, salt: bytes, expected_digest: bytes, pepper: bytes) -> bool:
    """Verify a password without leaking digest comparison timing."""
    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8") + pepper,
        salt,
        PBKDF2_ITERATIONS,
        dklen=len(expected_digest),
    )
    return hmac.compare_digest(candidate, expected_digest)
