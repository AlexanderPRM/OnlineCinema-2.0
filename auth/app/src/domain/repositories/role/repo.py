"""Module with Roles Repository."""

import uuid
from abc import ABC, abstractmethod

from src.domain.role.entities import Role
from src.domain.role.value_objects import AccessLevel


class IRoleRepository(ABC):
    """Repository with Role objects.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(self, role: Role) -> Role:
        """Add a new role.

        Args:
            role (Role): entity of Role class.

        Returns:
            Role (class): New Role class with new created role object info.
        """

    @abstractmethod
    async def retrieve_by_id(self, role_id: uuid.UUID) -> Role:
        """Retrieve role by role ID from storage.

        Args:
            role_id (uuid.UUID): Role UUID ID.

        Returns:
            Role | None: Return Role if exists.
        """

    @abstractmethod
    async def retrieve_by_name(self, name: str) -> Role:
        """Retrieve role by role name from storage.

        Args:
            name (str): Role name.

        Returns:
            Role | None: Return Role if exists.
        """

    @abstractmethod
    async def update_access_level(
        self, role_id: uuid.UUID, access_level: AccessLevel,
    ) -> Role:
        """Update role access level to new one.

        Args:
            role_id (uuid.UUID): Role UUID ID.
            access_level (AccessLevel): Entity of Access Level enum.

        Returns:
            Role (class): Role class which represent role.
        """

    @abstractmethod
    async def update_description(
        self, role_id: uuid.UUID, description: str,
    ) -> Role:
        """Update role description to new one.

        Args:
            role_id (uuid.UUID): Role UUID ID.
            description (str): New description.

        Returns:
            Role (class): Role class which represent role.
        """
