"""Module with role value objects."""

import enum


class AccessLevel(enum.Enum):
    """Service access levels.

    Args:
        Enum (class): Parent class to create enumeration type.
    """

    base = 0
    subscriber = 1
    superuser = 2
