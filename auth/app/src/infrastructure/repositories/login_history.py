"""Module with LoginHistoryRepository."""

import logging
import uuid
from typing import Any, Optional

import backoff
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select
from src.domain.login_history.dto import LoginHistoryDTO
from src.domain.login_history.entities import LoginHistory
from src.domain.login_history.exceptions import LoginEntryNotFound
from src.domain.repositories.login_history.repo import ILoginHistoryRepository
from src.domain.social_network.dto import SocialNetworkDTO
from src.domain.social_network.entities import SocialNetwork
from src.infrastructure.models import LoginHistory as LoginHistoryORM
from src.infrastructure.repositories.base import decorate_all_methods

logger = logging.getLogger(__name__)


@decorate_all_methods(
    backoff.on_exception,
    wait_gen=backoff.expo,
    exception=TimeoutError,
    max_time=10,
    max_tries=3,
    logger=logger,
    backoff_log_level=logging.WARNING,
    giveup_log_level=logging.CRITICAL,
)
class LoginHistoryRepository(ILoginHistoryRepository):
    """Repository with login entries objects.

    Args:
        ILoginHistoryRepository (class): Abstract Repository class.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Init method.

        Args:
            session (AsyncSession): SQLAlchemy session to Database.
        """
        self._session = session

    async def insert(self, entity: LoginHistory) -> LoginHistory:
        """Add a new login entry.

        Args:
            entity (LoginHistory): entity of LoginHistory class.

        Returns:
            LoginHistory: entity of LoginHistory class with new info.
        """
        dumped_login_history = entity.__dict__
        stmt = sa.Insert(LoginHistoryORM).values(
            user_id=dumped_login_history['_user_id'],
            user_agent=dumped_login_history['_user_agent'],
            social_network_id=dumped_login_history['_social_network_id'],
        ).returning(
            LoginHistoryORM.id,
            LoginHistoryORM.created_at,
            LoginHistoryORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one()
        return LoginHistory(
            LoginHistoryDTO(
                id=fetch[0],
                user_id=dumped_login_history['_user_id'],
                user_agent=dumped_login_history['_user_agent'],
                social_network_id=dumped_login_history['_social_network_id'],
                created_at=fetch[1],
                updated_at=fetch[2],
            ),
            social_network=entity.social_network,
        )

    async def retrieve_by_id(self, login_entry_id: uuid.UUID) -> LoginHistory:
        """Retrieve login entry by ID.

        Args:
            login_entry_id (uuid.UUID): Login entry UUID.

        Raises:
            LoginEntryNotFound: If login entry not found.

        Returns:
            LoginHistory: Retrieved login entry.
        """
        stmt: Select[Any] = sa.Select(LoginHistoryORM).where(
            LoginHistoryORM.id == login_entry_id,
        ).options(
            selectinload(LoginHistoryORM.social_network),
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise LoginEntryNotFound
        record: LoginHistoryORM = fetch[0]

        social_network_entity: Optional[SocialNetwork] = None
        if record.social_network:
            social_network_entity = SocialNetwork(
                SocialNetworkDTO(
                    **record.social_network.__dict__,
                ),
            )
        return LoginHistory(
            LoginHistoryDTO(
                **record.__dict__,
            ),
            social_network=social_network_entity,
        )

    async def retrieve_by_user_id(self, uid: uuid.UUID) -> list[LoginHistory]:
        """Retrieve all login entries by user id.

        Args:
            uid (uuid.UUID): User UUID.

        Raises:
            LoginEntryNotFound: If no one login entry was found.

        Returns:
            list[LoginHistory]: Retrieved login entries.
        """
        stmt: Select[Any] = sa.Select(LoginHistoryORM).where(
            LoginHistoryORM.user_id == uid,
        ).options(
            selectinload(LoginHistoryORM.social_network),
        )
        res = await self._session.execute(stmt)
        fetch = res.fetchall()
        if not fetch:
            raise LoginEntryNotFound

        records: list[LoginHistory] = []
        for entry in fetch[0]:
            social_network_entity: Optional[SocialNetwork] = None
            if entry.social_network:
                social_network_entity = SocialNetwork(
                    SocialNetworkDTO(
                        **entry.social_network.__dict__,
                    ),
                )
            entity = LoginHistory(
                LoginHistoryDTO(
                    **entry.__dict__,
                ),
                social_network=social_network_entity,
            )
            records.append(entity)
        return records
