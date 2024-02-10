"""Module with User Social Account class."""

from __future__ import annotations

import uuid

from domain.base import Base
from domain.social_network.dto import SocialNetworkDTO
from domain.user.dto import UserDTO
from domain.user_social_account.dto import UserSocialAccountDTO


class UserSocialAccount(Base):
    """Class which represent a User Social Account.

    Args:
        Base (class): Base representing class.
    """

    def __init__(
        self,
        entity: UserSocialAccountDTO,
        user_entity: UserDTO,
        social_network: SocialNetworkDTO,
    ) -> None:
        """Init method.

        Args:
            entity (UserSocialAccountDTO):
            Data Transfer Object of User Account Network.
            user_entity (UserDTO): Data Transfer Object of User.
            social_network (SocialNetworkDTO):
            Data Transfer Object of Social Network.
        """
        self._id = entity
        self._social_network_id = entity.social_network_id
        self._user_id = entity.user_id
        self._social_account_id = entity.social_account_id
        self._created_at = entity.created_at

        self._user = UserDTO
        self._social_network = SocialNetworkDTO

    @classmethod
    def create(
        cls,
        social_network_id: uuid.UUID,
        user_id: uuid.UUID,
        social_account_id: str,
    ) -> UserSocialAccount:
        """Create User Social Account class which represent a user social account object. # noqa: E501,D400

        Args:
            social_network_id (uuid.UUID): UUID identifier of social network.
            user_id (uuid.UUID): UUID identifier of user.
            social_account_id (str): identifier of user social account.

        Returns:
            UserSocialAccount (class): Return created class.
        """
        return cls(
            entity=UserSocialAccountDTO(
                id=uuid.uuid4(),
                social_network_id=social_network_id,
                user_id=user_id,
                social_account_id=social_account_id,
            ),
        )
