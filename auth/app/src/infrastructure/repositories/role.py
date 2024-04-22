"""Module with Role Repository."""

import uuid
from typing import Any

import backoff
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, TimeoutError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from src.config import UserSettings
from src.domain.repositories.role.exceptions import (
    BaseRoleNotFoundError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)
from src.domain.repositories.role.repo import IRoleRepository
from src.domain.role.dto import RoleDTO
from src.domain.role.entities import Role
from src.domain.role.value_objects import AccessLevel
from src.infrastructure.models import Role as RoleORM


class RoleRepository(IRoleRepository):
    """Implemented repository with Role objects.

    Args:
        IRoleRepository (class): Abstract Role Repository.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Init method.

        Args:
            session (AsyncSession): SQLAlchemy session to Database.
        """
        self._session = session

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def insert(self, role: Role) -> Role:
        """Add a new role.

        Args:
            role (Role): entity of Role class.

        Raises:
            RoleAlreadyExistsError: If role with that name already exists.

        Returns:
            Role (class): New Role class with new created role object info.
        """
        dumped_role = role.__dict__
        stmt = sa.insert(RoleORM).values(
            name=dumped_role['_name'],
            description=dumped_role['_description'],
            access_level=dumped_role['_access_level'],
        ).returning(
            RoleORM.id,
            RoleORM.name,
            RoleORM.description,
            RoleORM.access_level,
            RoleORM.created_at,
            RoleORM.updated_at,
        )

        try:
            res = await self._session.execute(stmt)
        except IntegrityError as exc:
            raise RoleAlreadyExistsError from exc

        fetch = res.one()
        return Role(
            RoleDTO(
                id=fetch[0],
                name=fetch[1],
                description=fetch[2],
                access_level=fetch[3],
                created_at=fetch[4],
                updated_at=fetch[5],
            ),
        )

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def retrieve_by_id(self, role_id: uuid.UUID) -> Role:
        """Retrieve role by role ID from storage.

        Args:
            role_id (uuid.UUID): Role UUID ID.

        Raises:
            RoleNotFoundError: if role not found, throw this error.

        Returns:
            Role: Entity of Role.
        """
        stmt: Select[Any] = sa.Select(RoleORM).where(
            RoleORM.id == role_id,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise RoleNotFoundError
        record: RoleORM = fetch[0]
        return Role(
            RoleDTO(**record.__dict__),
        )

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def retrieve_by_name(self, name: str) -> Role:
        """Retrieve role by role name from storage.

        Args:
            name (str): Role name.

        Raises:
            RoleNotFoundError: if role not found, throw this error.

        Returns:
            Role: Entity of Role.
        """
        stmt: Select[Any] = sa.Select(RoleORM).where(
            RoleORM.name == name,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise RoleNotFoundError
        record: RoleORM = fetch[0]
        return Role(
            RoleDTO(**record.__dict__),
        )

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def retrieve_base_role(self) -> Role:
        """Retrieve base role by name from storage.

        Raises:
            BaseRoleNotFoundError: If role not found, throw this error.

        Returns:
            Role: Entity of Role.
        """
        user_config = UserSettings()
        stmt: Select[Any] = sa.Select(RoleORM).where(
            RoleORM.name == user_config.default_user_role,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise BaseRoleNotFoundError
        record: RoleORM = fetch[0]
        return Role(
            RoleDTO(**record.__dict__),
        )

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def update_access_level(
        self, role_id: uuid.UUID, access_level: AccessLevel,
    ) -> Role:
        """Update the access level for role with that ID.

        Args:
            role_id (uuid.UUID): UUID Identifier.
            access_level (AccessLevel): Instance of enum Access Class.

        Raises:
            RoleNotFoundError: if role not found, throw this error.

        Returns:
            Role: Entity of Role.
        """
        stmt = sa.Update(RoleORM).where(
            RoleORM.id == role_id,
        ).values(access_level=access_level).returning(
            RoleORM.id,
            RoleORM.name,
            RoleORM.description,
            RoleORM.access_level,
            RoleORM.created_at,
            RoleORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise RoleNotFoundError
        return Role(
            RoleDTO(
                id=fetch[0],
                name=fetch[1],
                description=fetch[2],
                access_level=fetch[3],
                created_at=fetch[4],
                updated_at=fetch[5],
            ),
        )

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def update_description(
        self,
        role_id: uuid.UUID,
        description: str,
    ) -> Role:
        """Update the description for role with that ID.

        Args:
            role_id (uuid.UUID): UUID Identifier.
            description (str): New description for role.

        Raises:
            RoleNotFoundError: if role not found, throw this error.

        Returns:
            Role: Entity of Role.
        """
        stmt = sa.Update(RoleORM).where(
            RoleORM.id == role_id,
        ).values(description=description).returning(
            RoleORM.id,
            RoleORM.name,
            RoleORM.description,
            RoleORM.access_level,
            RoleORM.created_at,
            RoleORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise RoleNotFoundError
        return Role(
            RoleDTO(
                id=fetch[0],
                name=fetch[1],
                description=fetch[2],
                access_level=fetch[3],
                created_at=fetch[4],
                updated_at=fetch[5],
            ),
        )
