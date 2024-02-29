"""Module with Login History class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Optional

from src.domain.base import Base
from src.domain.login_history.dto import LoginHistoryDTO
from src.domain.social_network.entities import SocialNetwork


class LoginHistory(Base):
    """Class which represent a Login History.

    Args:
        Base (class): Base representing class.
    """

    def __init__(
        self,
        entity: LoginHistoryDTO,
        social_network: Optional[SocialNetwork] = None,
    ) -> None:
        """Init method.

        Args:
            entity (LoginHistoryDTO):  Data Transfer Object of Login History.
            social_network (SocialNetwork): Entity of Social Network.
        """
        self.id = entity.id

        self._user_agent = entity.user_agent
        self._social_network_id = entity.social_network_id
        self._created_at = entity.created_at
        self._updated_at = entity.updated_at

        self.social_network = social_network

    @classmethod
    def create(
        cls,
        uid: uuid.UUID,
        user_agent: str,
        social_network: Optional[SocialNetwork] = None,
    ) -> LoginHistory:
        """Create Login History class which represent a login history object.

        Args:
            uid (uuid.UUID): User UUID ID.
            user_agent (str): HTTP Header intended to identify User.
            social_network (SocialNetwork): entity of SocialNetwork.

        Returns:
            LoginHistory (class): Return created class.
        """
        return cls(
            entity=LoginHistoryDTO(
                id=uuid.uuid4(),
                user_id=uid,
                user_agent=user_agent,
                social_network_id=(
                    social_network.id if social_network else None
                ),
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            ),
            social_network=social_network,
        )
