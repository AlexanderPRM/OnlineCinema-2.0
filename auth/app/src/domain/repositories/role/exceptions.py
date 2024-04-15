"""Module with custom exceptions."""


class RoleNotFoundError(Exception):
    """Role with this fields not Found."""


class RoleAlreadyExists(Exception):
    """Role with this fields already exists."""


class BaseRoleNotExists(Exception):
    """Base role for not exists."""
