"""Module with User social account."""

import uuid
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from src.domain.repositories.user_social_account.repo import (
    IUserSocialAccountRepository,
)
from src.domain.user_social_account.dto import UserSocialAccountDTO
from src.domain.user_social_account.entities import UserSocialAccount
from src.domain.user_social_account.exceptions import UserSocialAccountNotFound
from src.infrastructure.models import UserSocialAccount as UserSocialAccountORM


class UserSocialAccountRepository(IUserSocialAccountRepository):
    """Repository with users social accounts objects.

    Args:
        IUserSocialAccountRepository (class): Abstract Repository class.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Init method.

        Args:
            session (AsyncSession): SQLAlchemy session to Database.
        """
        self._session = session

    async def insert(self, entity: UserSocialAccount) -> UserSocialAccount:
        """Add a new social account for user.

        Args:
            entity (UserSocialAccount): entity of UserSocialAccount class.

        Returns:
            UserSocialAccount: entity of UserSocialAccount class with new info.
        """
        dumped_user_social_account = entity.__dict__
        stmt = sa.Insert(UserSocialAccountORM).values(
            social_network_id=dumped_user_social_account['_social_network_id'],
            user_id=dumped_user_social_account['_user_id'],
            social_account_id=dumped_user_social_account['_social_account_id'],
        ).returning(
            UserSocialAccountORM.id,
            UserSocialAccountORM.created_at,
            UserSocialAccountORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one()
        return UserSocialAccount(
            UserSocialAccountDTO(
                id=fetch[0],
                social_network_id=(
                    dumped_user_social_account['_social_network_id']
                ),
                user_id=dumped_user_social_account['_user_id'],
                social_account_id=(
                    dumped_user_social_account['_social_account_id']
                ),
                created_at=fetch[1],
                updated_at=fetch[2],
            ),
        )

    async def delete_by_id(self, user_social_account_id: uuid.UUID) -> None:
        """Delete social account by ID.

        Args:
            user_social_account_id (uuid.UUID): User social account UUID.
        """
        stmt = sa.Delete(UserSocialAccountORM).where(
            UserSocialAccountORM.id == user_social_account_id,
        )
        await self._session.execute(stmt)

    async def delete_by_user_and_social_network(
        self, uid: uuid.UUID, social_network_id: uuid.UUID,
    ) -> None:
        """Delete social account by user ID and social network ID.

        Args:
            uid (uuid.UUID): User UUID.
            social_network_id (uuid.UUID): Social Network UUID.
        """
        stmt = sa.Delete(UserSocialAccountORM).where(
            sa.and_(
                UserSocialAccountORM.user_id == uid,
                UserSocialAccountORM.social_network_id == social_network_id,
            ),
        )
        await self._session.execute(stmt)

    async def retrieve_by_id(
        self, user_social_account_id: uuid.UUID,
    ) -> UserSocialAccount:
        """Retrieve user social account by ID.

        Args:
            user_social_account_id (uuid.UUID): User social account UUID.

        Returns:
            UserSocialAccount: Retrieved record.
        """
        stmt: Select[Any] = sa.Select(UserSocialAccountORM).where(
            UserSocialAccountORM.id == user_social_account_id,
        )
        return await self._retrieve_one(stmt)

    async def retrieve_by_user_id(
        self, uid: uuid.UUID,
    ) -> list[UserSocialAccount]:
        """Retrieve all user social accounts.

        Args:
            uid (uuid.UUID): User UUID.

        Returns:
            list[UserSocialAccount]: Retrieved records.
        """
        stmt: Select[Any] = sa.Select(UserSocialAccountORM).where(
            UserSocialAccountORM.user_id == uid,
        )
        return await self._retrieve_all(stmt)

    async def retrieve_by_social_network_id(
        self, social_network_id: uuid.UUID,
    ) -> list[UserSocialAccount]:
        """Retrieve all social accounts with this social network.

        Args:
            social_network_id (uuid.UUID): Social network ID.

        Returns:
            list[UserSocialAccount]: Retrieved records.
        """
        stmt: Select[Any] = sa.Select(UserSocialAccountORM).where(
            UserSocialAccountORM.social_network_id == social_network_id,
        )
        return await self._retrieve_all(stmt)

    async def _retrieve_one(self, stmt: Select[Any]) -> UserSocialAccount:
        """Retrieve one record by some statement.

        Args:
            stmt (Select[Any]): Select query.

        Raises:
            UserSocialAccountNotFound: If user social account not found.

        Returns:
            UserSocialAccount: Retrieved record.
        """
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserSocialAccountNotFound
        record: UserSocialAccountORM = fetch[0]
        return UserSocialAccount(
            entity=UserSocialAccountDTO(
                **record.__dict__,
            ),
        )

    async def _retrieve_all(
        self, stmt: Select[Any],
    ) -> list[UserSocialAccount]:
        """Retrieve all records by some statement.

        Args:
            stmt (Select[Any]): Select query.

        Raises:
            UserSocialAccountNotFound: If user social account not found.

        Returns:
            list[UserSocialAccount]: Retrieved records.
        """
        res = await self._session.execute(stmt)
        fetch = res.all()
        if not fetch:
            raise UserSocialAccountNotFound

        records: list[UserSocialAccount] = []
        for entry in fetch:
            user_social_account = UserSocialAccount(
                UserSocialAccountDTO(
                    **entry.__dict__,
                ),
            )
            records.append(user_social_account)
        return records
