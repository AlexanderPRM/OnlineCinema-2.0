"""Module with Social Network repository."""

import uuid
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from src.domain.repositories.social_network.repo import (
    ISocialNetworkRepository,
)
from src.domain.social_network.dto import SocialNetworkDTO
from src.domain.social_network.entities import SocialNetwork
from src.domain.social_network.exceptions import SocialNetworkNotFound
from src.infrastructure.models import SocialNetwork as SocialNetworkORM


class SocialNetworkRepository(ISocialNetworkRepository):
    """Repository with social network objects.

    Args:
        ISocialNetworkRepository (class): Abstract Repository Interface.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Init method.

        Args:
            session (AsyncSession): SQLAlchemy session to Database.
        """
        self._session = session

    async def insert(self, entity: SocialNetwork) -> SocialNetwork:
        """Add a new social network.

        Args:
            entity (SocialNetwork): entity of SocialNetwork class.

        Returns:
            SocialNetwork:
            Entity of SocialNetwork class with new info.
        """
        dumped_social_network = entity.__dict__
        picture_file_path = dumped_social_network['_picture']
        if isinstance(picture_file_path, Path):
            picture_file_path = picture_file_path.as_posix()

        stmt = sa.Insert(SocialNetworkORM).values(
            picture=picture_file_path,
            name=dumped_social_network['_name'],
        ).returning(
            SocialNetworkORM.id,
            SocialNetworkORM.created_at,
            SocialNetworkORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one()
        return SocialNetwork(
            SocialNetworkDTO(
                id=fetch[0],
                picture=dumped_social_network['_picture'],
                name=dumped_social_network['_name'],
                created_at=fetch[1],
                updated_at=fetch[2],
            ),
        )

    async def retrieve_by_id(
        self,
        social_network_id: uuid.UUID,
    ) -> SocialNetwork:
        """Retrieve social network by ID.

        Args:
            social_network_id (uuid.UUID): Social network UUID.

        Returns:
            SocialNetwork: Retrieved social network.
        """
        stmt: Select[Any] = sa.Select(SocialNetworkORM).where(
            SocialNetworkORM.id == social_network_id,
        )
        return await self._retrieve_data(stmt)

    async def retrieve_by_name(
        self,
        name: str,
    ) -> SocialNetwork:
        """Retrieve social network by name.

        Args:
            name (str): Social network name.

        Returns:
            SocialNetwork: Retrieved social network.
        """
        stmt: Select[Any] = sa.Select(SocialNetworkORM).where(
            SocialNetworkORM.name == name,
        )
        return await self._retrieve_data(stmt)

    async def change_picture(
        self, social_network_id: uuid.UUID, picture_file_path: Path,
    ) -> SocialNetwork:
        """Change the social network picture with that ID.

        Args:
            social_network_id (uuid.UUID): Social etwork UUID.
            picture_file_path (Path): New file path to picture.

        Raises:
            SocialNetworkNotFound: If social network not found.

        Returns:
            SocialNetwork: Updated social network.
        """
        stmt = sa.Update(SocialNetworkORM).where(
            SocialNetworkORM.id == social_network_id,
        ).values(
            picture=picture_file_path,
        ).returning(
            SocialNetworkORM.id,
            SocialNetworkORM.picture,
            SocialNetworkORM.name,
            SocialNetworkORM.created_at,
            SocialNetworkORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise SocialNetworkNotFound
        return SocialNetwork(
            SocialNetworkDTO(
                id=fetch[0],
                picture=fetch[1],
                name=fetch[2],
                created_at=fetch[3],
                updated_at=fetch[4],
            ),
        )

    async def _retrieve_data(
        self, stmt: Select[Any],
    ) -> SocialNetwork:
        """Retrieve social network by some statement.

        Args:
            stmt (Select[Any]): Select Query.

        Raises:
            SocialNetworkNotFound: If social network not found.

        Returns:
            SocialNetwork: Retrieved social network.
        """
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise SocialNetworkNotFound
        record: SocialNetworkORM = fetch[0]
        return SocialNetwork(
            SocialNetworkDTO(
                **record.__dict__,
            ),
        )
