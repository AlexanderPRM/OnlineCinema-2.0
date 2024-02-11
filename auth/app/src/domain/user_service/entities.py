"""Module with User Service class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from domain.base import Base
from domain.role.entities import Role
from domain.user_service.dto import UserServiceDTO


class UserService(Base):
    """Class which represent a User Service.

    Args:
        Base (class): Base representing class.
    """

    def __init__(self, entity: UserServiceDTO, role: Role) -> None:
        """Init method.

        Args:
            entity (UserServiceDTO): Data Transfer Object of User Service.
            role (Role): Entity of Role.
        """
        self.id = entity.id

        self._role_id = entity.role_id
        self._active = entity.active
        self._verified = entity.verified
        self._date_joined = entity.date_joined

        self.role = role

    @classmethod
    def create(
        cls,
        role: Role,
        is_active: bool = True,
        verified: bool = False,
    ) -> UserService:
        """Create User Service class which represent a user service object.

        Args:
            role (Role): Entity of Role.
            is_active (bool): Is the user account active.
            verified (bool): Is the user account verified.

        Returns:
            Role (class): Return created class.
        """
        return cls(
            entity=UserServiceDTO(
                id=uuid.uuid4(),
                role_id=role.id,
                active=is_active,
                verified=verified,
                date_joined=datetime.now(UTC),
            ),
            role=role,
        )

    def change_role(self, role: Role) -> None:
        """Change the User role.

        Args:
            role (Role): Entity of Role.
        """
        self._role_id = role.id
        self.role = role

    def is_verified(self) -> bool:
        """Return the user verification status.

        Returns:
            bool: Is user account verified.
        """
        return self._verified

    def is_active(self) -> bool:
        """Return the user active status.

        Returns:
            bool: Is user account active.
        """
        return self._active
