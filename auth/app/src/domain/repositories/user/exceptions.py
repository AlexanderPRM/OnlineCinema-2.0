"""Module with custom exceptions."""


class UserNotFoundError(Exception):
    """User with this fields not Found."""


class UserAlreadyExists(Exception):
    """User with this fields already exists."""
