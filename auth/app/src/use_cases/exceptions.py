"""Module with Use Case Exceptions."""


class UserAlreadyExists(Exception):
    """User with this credentials already exists.

    Args:
        Exception (class): In-build Base exception class.
    """


class BaseRoleNotExists(Exception):
    """Base role for new user not exists.

    Args:
        Exception (class): In-build Base exception class.
    """
