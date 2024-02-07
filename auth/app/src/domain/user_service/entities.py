"""Module with User Service class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from src.domain.base import Base
from src.domain.user_service.dto import UserServiceDTO


class UserService(Base):
    """Class which represent a User Service.

    Args:
        Base (class): Base representing class.
    """

    def __init__(self, entity: UserServiceDTO) -> None:
        """Init method.

        Args:
            entity (UserServiceDTO): Data Transfer Object of User Service.
        """
        self._id = entity.id
        self._role_id = entity.role_id
        self._active = entity.active
        self._verified = entity.verified
        self._date_joined = entity.date_joined

    @classmethod
    def create(
        cls,
        role_id: uuid.UUID,
        is_active: bool = True,
        verified: bool = False,
    ) -> UserService:
        """Create User Service class which represent a user service object.

        Args:
            role_id (UUID): Role UUID.
            is_active (bool): Is the user account active.
            verified (bool): Is the user account verified.

        Returns:
            Role (class): Return created class.
        """
        return cls(
            entity=UserServiceDTO(
                id=uuid.uuid4(),
                role_id=role_id,
                is_active=is_active,
                verified=verified,
                date_joined=datetime.now(UTC),
            ),
        )

    def change_role(self, role_id: uuid.UUID) -> None:
        """Change the User role.

        Args:
            role_id (uuid.UUID): UUID identifier to Role.
        """
        self._role_id = role_id

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
