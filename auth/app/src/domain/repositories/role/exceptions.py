"""Module with custom exceptions."""


class RoleAlreadyExistsError(Exception):
    """Role with this fields already exists."""


class RoleNotFoundError(Exception):
    """Role with this fields not Found."""


class BaseRoleNotFoundError(Exception):
    """Base role for not exists."""
