"""Module with Users Service Repository."""

import uuid
from abc import ABC, abstractmethod

from src.domain.role.entities import Role
from src.domain.user_service.entities import UserService


class IUserServiceRepository(ABC):
    """Repository with User Service objects.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(self, user_service: UserService) -> UserService:
        """Add a new user service.

        Args:
            user_service (UserService): Entity of User Service class.

        Returns:
            UserService: New User Service class with new
            created user service object info.
        """

    @abstractmethod
    async def retrieve_by_id(self, uid: uuid.UUID) -> UserService:
        """Get user service by user ID from storage.

        Args:
            uid (uuid.UUID): User UUID ID.

        Returns:
            UserService: Return User Service if exists.
        """

    @abstractmethod
    async def update_active_status(
        self, uid: uuid.UUID, active_status: bool,
    ) -> UserService:
        """Update user account active status (Active | Not Active).

        Args:
            uid (uuid.UUID): User UUID ID.
            active_status (bool): New User active status.

        Returns:
            UserService (class):
            User Service class which represent user service.
        """

    @abstractmethod
    async def update_verification_status(
        self, uid: uuid.UUID, verified_status: bool,
    ) -> UserService:
        """Update user verification account status (Verified | Not Verified).

        Args:
            uid (uuid.UUID): User UUID ID.
            verified_status (bool): New User verified status.

        Returns:
            UserService (class):
            User Service class which represent user service.
        """

    @abstractmethod
    async def update_role(self, uid: uuid.UUID, role: Role) -> UserService:
        """Update user role to new one.

        Args:
            uid (uuid.UUID): User UUID ID.
            role (Role): Entity of class Role which represent Role.

        Returns:
            UserService (class):
            User Service which represent user service.
        """
