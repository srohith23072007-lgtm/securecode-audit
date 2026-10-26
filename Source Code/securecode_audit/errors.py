"""Application-specific errors exposed by the service layer."""


class SecureCodeAuditError(Exception):
    """Base class for expected application errors."""


class ValidationError(SecureCodeAuditError):
    """Raised when user-supplied data fails validation."""


class UserAlreadyExistsError(SecureCodeAuditError):
    """Raised when attempting to register a duplicate username."""


class ConfigurationError(SecureCodeAuditError):
    """Raised when required application configuration is missing or unsafe."""
