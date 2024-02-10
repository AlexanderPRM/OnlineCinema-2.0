"""Module with Login History class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Optional

from domain.base import Base
from domain.login_history.dto import LoginHistoryDTO
from domain.social_network.dto import SocialNetworkDTO


class LoginHistory(Base):
    """Class which represent a Login History.

    Args:
        Base (class): Base representing class.
    """

    def __init__(
        self,
        entity: LoginHistoryDTO,
        social_network_entity: Optional[SocialNetworkDTO] = None,
    ) -> None:
        """Init method.

        Args:
            entity (LoginHistoryDTO):  Data Transfer Object of Login History.
            social_network_entity (SocialNetworkDTO):
            Data Transfer Object of Social Network.
        """
        self._id = entity.id
        self._user_agent = entity.user_agent
        self._social_network_id = entity.social_network_id
        self._login_date = entity.login_date

        self._social_network_entity = social_network_entity

    @classmethod
    def create(
        cls,
        uid: uuid.UUID,
        user_agent: str,
        social_network: Optional[SocialNetworkDTO] = None,
    ) -> LoginHistory:
        """Create Login History class which represent a login history object.

        Args:
            uid (uuid.UUID): User UUID ID.
            user_agent (str): HTTP Header intended to identify User.
            social_network (SocialNetworkDTO): entity of SocialNetworkDTO.

        Returns:
            Role (class): Return created class.
        """
        return cls(
            entity=LoginHistoryDTO(
                id=uuid.uuid4(),
                user_id=uid,
                user_agent=user_agent,
                social_network_id=(
                    social_network.id if social_network else None
                ),
                login_date=datetime.now(UTC),
            ),
            social_network_entity=social_network,
        )
