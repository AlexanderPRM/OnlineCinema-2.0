"""Module with Role class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Optional

from domain.base import Base
from domain.role.dto import RoleDTO
from domain.role.value_objects import AccessLevel


class Role(Base):
    """Class which represent a Role.

    Args:
        Base (class): Base representing class.
    """

    def __init__(self, entity: RoleDTO) -> None:
        """Init method.

        Args:
            entity (RoleDTO): Data Transfer Object of Role.
        """
        self.id = entity.id

        self._name = entity.name
        self._description = entity.description
        self._access_level = entity.access_level
        self._created_at = entity.created_at
        self._updated_at = entity.updated_at

    @classmethod
    def create(
        cls,
        name: str,
        access_level: AccessLevel,
        description: Optional[str] = '',
    ) -> Role:
        """Create Role class which represent a role object.

        Args:
            name (str): Role name.
            access_level (AccessLevel): Role Access level.
            description (str): Role description.

        Returns:
            Role (class): Return created class.
        """
        return cls(
            entity=RoleDTO(
                id=uuid.uuid4(),
                name=name,
                description=description,
                access_level=access_level,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            ),
        )

    def change_access_level(self, access_level: AccessLevel) -> None:
        """Change access level to new one.

        Args:
            access_level (AccessLevel): Entity of Access Level enum.
        """
        self._access_level = access_level

    def change_description(self, description: str) -> None:
        """Change description to new one.

        Args:
            description (str): New description.
        """
        self._description = description

    def check_access(self, access_level: AccessLevel) -> bool:
        """Check whether the role has access to the level.

        Args:
            access_level (AccessLevel): Entity of Access Level enum.

        Returns:
            has_access (bool): Return does the role have access.
        """
        return self._access_level.value >= access_level.value
