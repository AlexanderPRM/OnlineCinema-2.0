"""Module with User Social Account class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Optional

from src.domain.base import Base
from src.domain.social_network.entities import SocialNetwork
from src.domain.user.entities import User
from src.domain.user_social_account.dto import UserSocialAccountDTO


class UserSocialAccount(Base):
    """Class which represent a User Social Account.

    Args:
        Base (class): Base representing class.
    """

    def __init__(
        self,
        entity: UserSocialAccountDTO,
        user: Optional[User] = None,
        social_network: Optional[SocialNetwork] = None,
    ) -> None:
        """Init method.

        Args:
            entity (UserSocialAccountDTO):
            Data Transfer Object of User Account Network.
            user (User): Entity of User.
            social_network (SocialNetwork): Entity of Social Network.
        """
        self.id = entity

        self._social_network_id = entity.social_network_id
        self._user_id = entity.user_id
        self._social_account_id = entity.social_account_id
        self._created_at = entity.created_at
        self._updated_at = entity.updated_at

        self.user = user
        self.social = social_network

    @classmethod
    def create(
        cls,
        user: User,
        social_network: SocialNetwork,
        social_account_id: str,
    ) -> UserSocialAccount:
        """Create User Social Account class which represent a user social account object. # noqa: E501,D400

        Args:
            user (User): Entity of User.
            social_network (SocialNetwork): Entity of SocialNetwork.
            social_account_id (str): identifier of user social account.

        Returns:
            UserSocialAccount (class): Return created class.
        """
        return cls(
            entity=UserSocialAccountDTO(
                id=uuid.uuid4(),
                social_network_id=social_network.id,
                user_id=user.id,
                social_account_id=social_account_id,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            ),
            user=user,
            social_network=social_network,
        )
