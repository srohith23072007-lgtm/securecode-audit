"""Tests for bounded username and password validation."""

import pytest

from securecode_audit.errors import ValidationError
from securecode_audit.validation import validate_password, validate_username


@pytest.mark.parametrize("username", ["alice", "Alice_2", "a.user-3"])
def test_accepts_valid_usernames(username):
    assert validate_username(username) == username


@pytest.mark.parametrize(
    "username",
    ["", "ab", "contains space", "bad'name", "x" * 33, "user;DROP TABLE users"],
)
def test_rejects_invalid_usernames(username):
    with pytest.raises(ValidationError):
        validate_username(username)


def test_accepts_password_at_minimum_length():
    password = "a" * 12
    assert validate_password(password) == password


@pytest.mark.parametrize("password", ["short", "x" * 129, "valid-but\x00invalid"])
def test_rejects_invalid_passwords(password):
    with pytest.raises(ValidationError):
        validate_password(password)
