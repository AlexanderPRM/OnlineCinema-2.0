"""Module with Users Repository."""

import uuid
from abc import ABC, abstractmethod

from src.domain.user.entities import User
from src.domain.user.value_objects import UserAdditionalFields


class IUserRepository(ABC):  # noqa: WPS214
    """Repository with User objects.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(self, user: User) -> User:
        """Add a new user.

        Args:
            user (User): Entity of User class.

        Returns:
            User (class): New User class with new created user object info.
        """

    @abstractmethod
    async def retrieve_by_id(self, uid: uuid.UUID) -> User:
        """Get user by user ID from storage.

        Args:
            uid (uuid.UUID): User UUID ID.

        Returns:
            User: Retrieved User.
        """

    @abstractmethod
    async def retrieve_by_email(self, email: str) -> User:
        """Retrieve user by email from storage.

        Args:
            email (str): User electronic mail address.

        Returns:
            User: Retrieved User.
        """

    @abstractmethod
    async def retrieve_by_login(self, login: str) -> User:
        """Retrieve user by login from storage.

        Args:
            login (str): User login.

        Returns:
            User: Retrieved User.
        """

    @abstractmethod
    async def change_email(
        self, uid: uuid.UUID, email: str,
    ) -> User:
        """Change email of a user with this ID.

        Args:
            uid (uuid.UUID): User UUID ID.
            email (str): New user electronic mail address.

        Returns:
            User (class): User class which represent user.
        """

    @abstractmethod
    async def change_login(
        self, uid: uuid.UUID, login: str,
    ) -> User:
        """Change login of a user with this ID.

        Args:
            uid (uuid.UUID): User UUID ID.
            login (str): New user login.

        Returns:
            User (class): User class which represent user.
        """

    @abstractmethod
    async def change_password(
        self, uid: uuid.UUID, password: str,
    ) -> User:
        """Change password of a user with this ID.

        Args:
            uid (uuid.UUID): User UUID ID.
            password (str): New user password.

        Returns:
            User (class): User class which represent user.
        """

    @abstractmethod
    async def update_additional_info(
        self, uid: uuid.UUID, user_additional_fields: UserAdditionalFields,
    ) -> User:
        """Change additional fields of a user with this ID.

            Additional fields like:
                - full_name
                - phone_number
                - bio
                - birthday

        Args:
            uid (uuid.UUID): User UUID ID.
            user_additional_fields (UserAdditionalFields):
            Additional fields to change.

        Returns:
            User (class): User class which represent user.
        """
