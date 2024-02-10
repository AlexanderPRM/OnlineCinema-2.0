"""Module with Users Social Accounts Repository."""

import uuid
from abc import ABC, abstractmethod

from domain.user_social_account.entities import UserSocialAccount


class UserSocialAccountRepository(ABC):
    """Repository with User Social Account objects.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(self, entity: UserSocialAccount) -> UserSocialAccount:
        """Add a new User Social Account.

        Args:
            entity (UserSocialAccount): entity of UserSocialAccount.

        Returns:
            UserSocialAccount (class):
            UserSocialAccount class which represent User Social Account.
        """

    @abstractmethod
    async def retrieve_by_id(
        self, user_social_account_id: uuid.UUID,
    ) -> UserSocialAccount:
        """Retrieve User Social Account from storage by id.

        Args:
            user_social_account_id (uuid.UUID): User Social Account UUID ID.

        Returns:
            UserSocialAccount (class):
            UserSocialAccount class which represent User Social Account.
        """
    @abstractmethod
    async def retrieve_by_user_id(
        self, uid: uuid.UUID,
    ) -> list[UserSocialAccount]:
        """Retrieve all Users Social Accounts from storage by user_id.

        Args:
            uid (uuid.UUID): User UUID ID.

        Returns:
            UserSocialAccount (class): list of Users Social Accounts.
        """

    @abstractmethod
    async def retrieve_by_social_network_id(
        self, social_network_id: uuid.UUID,
    ) -> list[UserSocialAccount]:
        """Retrieve all Users which use that Social Network.

        Args:
            social_network_id (uuid.UUID): Social Network UUID ID.

        Returns:
            UserSocialAccount (class): list of Users Social Accounts.
        """
