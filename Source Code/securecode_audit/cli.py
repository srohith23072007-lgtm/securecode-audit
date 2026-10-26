"""Command-line entry point for the local demonstration application."""

import argparse
import getpass
import os
import sqlite3
from pathlib import Path

from .database import UserDatabase
from .errors import (
    ConfigurationError,
    SecureCodeAuditError,
    UserAlreadyExistsError,
)
from .service import AuthenticationService

DEFAULT_DATABASE_PATH = "securecode_audit.sqlite3"
DATABASE_ENVIRONMENT_VARIABLE = "SECURECODE_AUDIT_DB"


def _database_path() -> Path:
    return Path(os.environ.get(DATABASE_ENVIRONMENT_VARIABLE, DEFAULT_DATABASE_PATH))


def main() -> int:
    parser = argparse.ArgumentParser(description="Local SecureCode-Audit authentication demo.")
    parser.add_argument("action", choices=("register", "login"))
    parser.add_argument("username", help="Demo username (not a password).")
    arguments = parser.parse_args()
    password = getpass.getpass("Password: ")

    try:
        service = AuthenticationService(UserDatabase(_database_path()))
        if arguments.action == "register":
            service.register(arguments.username, password)
            print("Account registered.")
            return 0

        if service.authenticate(arguments.username, password):
            print("Authentication successful.")
            return 0
        print("Authentication failed.")
        return 1
    except UserAlreadyExistsError:
        print("Registration failed: an account with that username already exists.")
        return 1
    except ConfigurationError as error:
        print(f"Configuration error: {error}")
        return 2
    except SecureCodeAuditError as error:
        print(f"Request rejected: {error}")
        return 1
    except (OSError, sqlite3.Error):
        print("The local database could not be accessed.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
