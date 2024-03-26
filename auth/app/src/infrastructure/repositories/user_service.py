"""Module with User Service repository."""

import uuid
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select
from src.domain.repositories.user.exceptions import UserNotFoundError
from src.domain.repositories.user_service.repo import IUserServiceRepository
from src.domain.role.dto import RoleDTO
from src.domain.role.entities import Role
from src.domain.user_service.dto import UserServiceDTO
from src.domain.user_service.entities import UserService
from src.infrastructure.models import Role as RoleORM
from src.infrastructure.models import UserService as UserServiceORM


class UserServiceRepository(IUserServiceRepository):
    """Implement Repository with user service objects.

    Args:
        IUserServiceRepository (class): Abstract Repository Interface.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Init method.

        Args:
            session (AsyncSession): SQLAlchemy session to Database.
        """
        self._session = session

    async def insert(self, user_service: UserService) -> UserService:
        """Add a new User Service info.

        Args:
            user_service (UserService): entity of User Service class.

        Returns:
            UserService: Entity of User Service class with created user info.
        """
        dumped_user_service = user_service.__dict__
        stmt = sa.Insert(UserServiceORM).values(
            role_id=dumped_user_service['_role_id'],
            active=dumped_user_service['_active'],
            verified=dumped_user_service['_verified'],
        ).returning(
            UserServiceORM.id,
            UserServiceORM.role_id,
            UserServiceORM.active,
            UserServiceORM.verified,
            UserServiceORM.created_at,
            UserServiceORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one()
        return UserService(
            entity=UserServiceDTO(
                id=fetch[0],
                role_id=fetch[1],
                active=fetch[2],
                verified=fetch[3],
                created_at=fetch[4],
                updated_at=fetch[5],
            ),
            role=user_service.role,
        )

    async def retrieve_by_id(self, uid: uuid.UUID) -> UserService:
        """Retrieve User Service info by user ID.

        Args:
            uid (uuid.UUID): ID of the user to update.

        Returns:
            UserService: Retrieved user service.
        """
        stmt: Select[Any] = sa.Select(UserServiceORM).where(
            UserServiceORM.id == uid,
        )
        return await self._retrieve_one(stmt)

    async def update_active_status(
        self, uid: uuid.UUID, active_status: bool,
    ) -> UserService:
        """Update the active status with that ID.

        Args:
            uid (uuid.UUID): ID of the user to update.
            active_status (bool): The new active status.

        Raises:
            UserNotFoundError: If the user service is not found.

        Returns:
            UserService: Updated user service.
        """
        stmt = sa.Update(UserServiceORM).where(
            UserServiceORM.id == uid,
        ).values(
            active=active_status,
        ).returning(
            UserServiceORM.id,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        select_stmt: Select[Any] = sa.Select(UserServiceORM).where(
            UserServiceORM.id == fetch[0],
        )
        return await self._retrieve_one(select_stmt)

    async def update_verification_status(
        self, uid: uuid.UUID, verified_status: bool,
    ) -> UserService:
        """Update the verification status of a user service.

        Args:
            uid (uuid.UUID): ID of the user to update.
            verified_status (bool): The new verification status.

        Raises:
            UserNotFoundError: If the user service is not found.

        Returns:
            UserService: Updated user service.
        """
        stmt = sa.Update(UserServiceORM).where(
            UserServiceORM.id == uid,
        ).values(
            verified=verified_status,
        ).returning(
            UserServiceORM.id,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        select_stmt: Select[Any] = sa.Select(UserServiceORM).where(
            UserServiceORM.id == fetch[0],
        )
        return await self._retrieve_one(select_stmt)

    async def update_role(self, uid: uuid.UUID, role: Role) -> UserService:
        """Update the role of a user service.

        Args:
            uid (uuid.UUID): ID of the user to update.
            role (Role): New role for update.

        Raises:
            UserNotFoundError: if the user not found.

        Returns:
            UserService: Updated user service.
        """
        stmt = sa.Update(UserServiceORM).where(
            UserServiceORM.id == uid,
        ).values(
            role_id=role.id,
        ).returning(
            UserServiceORM.id,
            UserServiceORM.role_id,
            UserServiceORM.active,
            UserServiceORM.verified,
            UserServiceORM.created_at,
            UserServiceORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        return UserService(
            UserServiceDTO(
                id=fetch[0],
                role_id=fetch[1],
                active=fetch[2],
                verified=fetch[3],
                created_at=fetch[4],
                updated_at=fetch[5],
            ),
            role=role,
        )

    async def _retrieve_one(self, stmt: Select[Any]) -> UserService:
        """Retrieve User Service by some statement.

        Args:
            stmt (Select[Any]): Select Query.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            UserService: Retrieved User Service.
        """
        res = await self._session.execute(
            stmt.options(selectinload(UserServiceORM.role)),
        )
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        user_service_record: UserServiceORM = fetch[0]
        role_record: RoleORM = user_service_record.role
        return UserService(
            UserServiceDTO(
                **user_service_record.__dict__,
            ),
            role=Role(
                entity=RoleDTO(
                    **role_record.__dict__,
                ),
            ),
        )
