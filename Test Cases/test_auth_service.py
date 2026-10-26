"""Tests for account storage and credential verification."""

import pytest

from securecode_audit.errors import ConfigurationError, UserAlreadyExistsError
from securecode_audit.service import AuthenticationService


def test_registration_and_authentication_succeed(service):
    service.register("student_1", "a-long-demo-password")

    assert service.authenticate("student_1", "a-long-demo-password") is True


def test_wrong_password_fails(service):
    service.register("student_2", "another-long-password")

    assert service.authenticate("student_2", "incorrect-password") is False


def test_unknown_user_fails_without_revealing_account_status(service):
    assert service.authenticate("unknown_user", "long-enough-password") is False


def test_sql_injection_shaped_username_is_rejected(service):
    assert service.authenticate("' OR 1=1 --", "long-enough-password") is False


def test_duplicate_registration_is_rejected(service):
    service.register("same_user", "first-long-password")

    with pytest.raises(UserAlreadyExistsError):
        service.register("same_user", "second-long-password")


def test_registration_requires_environment_pepper(service, monkeypatch):
    monkeypatch.delenv("SECURECODE_AUDIT_PEPPER")

    with pytest.raises(ConfigurationError):
        service.register("no_pepper", "long-enough-password")
