"""Module with User Repository."""

import uuid
from pathlib import Path
from typing import Any

import backoff
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.selectable import Select
from src.domain.repositories.user.exceptions import UserNotFoundError
from src.domain.repositories.user.repo import IUserRepository
from src.domain.role.dto import RoleDTO
from src.domain.role.entities import Role
from src.domain.user.dto import UserDTO
from src.domain.user.entities import User
from src.domain.user.value_objects import UserAdditionalFields
from src.domain.user_service.dto import UserServiceDTO
from src.domain.user_service.entities import UserService
from src.infrastructure.models import User as UserORM
from src.infrastructure.models import UserService as UserServiceORM


class UserRepository(IUserRepository):  # noqa: WPS214 (Too many methods.)
    """Implement Repository with User objects."""

    def __init__(self, session: AsyncSession) -> None:
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
    async def insert(self, user: User) -> User:
        """Add a new user.

        Args:
            user (User): entity of User class.

        Returns:
            User (class): Entity of User class with new added info.
        """
        dumped_user = user.__dict__
        stmt = sa.Insert(UserORM).values(
            id=dumped_user['id'],
            email=dumped_user['_email'],
            login=dumped_user['_login'],
            password=dumped_user['_password'],
            user_service_id=dumped_user['_user_service_id'],
            full_name=dumped_user['_full_name'],
            profile_picture=dumped_user['_profile_picture'],
            birthday=dumped_user['_birthday'],
            phone_number=dumped_user['_phone_number'],
            bio=dumped_user['_bio'],
        ).returning(
            UserORM.id,
            UserORM.email,
            UserORM.login,
            UserORM.password,
            UserORM.user_service_id,
            UserORM.full_name,
            UserORM.profile_picture,
            UserORM.birthday,
            UserORM.phone_number,
            UserORM.bio,
            UserORM.created_at,
            UserORM.updated_at,
        )
        res = await self._session.execute(stmt)
        fetch = res.one()
        return User(
            UserDTO(
                id=fetch[0],
                email=fetch[1],
                login=fetch[2],
                password=fetch[3],
                user_service_id=fetch[4],
                full_name=fetch[5],
                profile_picture=fetch[6],
                birthday=fetch[7],
                phone_number=fetch[8],
                bio=fetch[9],
                created_at=fetch[10],
                updated_at=fetch[11],  # noqa: WPS432 (Magic Number.)
            ),
            user_service=user.user_service,
        )

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def retrieve_by_id(self, uid: uuid.UUID) -> User:
        """Retrieve User by that ID.

        Args:
            uid (uuid.UUID): User UUID.

        Returns:
            User: Retrieved User.
        """
        stmt: Select[Any] = sa.Select(UserORM).where(
            UserORM.id == uid,
        )
        return await self._retrieve_data(stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def retrieve_by_email(self, email: str) -> User:
        """Retrieve User by that email.

        Args:
            email (str): Electronic mail.

        Returns:
            User: Retrieved User.
        """
        stmt: Select[Any] = sa.Select(UserORM).where(
            UserORM.email == email,
        )
        return await self._retrieve_data(stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def retrieve_by_login(self, login: str) -> User:
        """Retrieve User by that login.

        Args:
            login (str): Unique user login.

        Returns:
            User: Retrieved User.
        """
        stmt: Select[Any] = sa.Select(UserORM).where(
            UserORM.login == login,
        )
        return await self._retrieve_data(stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def retrieve_by_email_or_login(self, email: str, login: str) -> User:
        """Retrieve User by login or email.

        Args:
            email (str): Electronic mail.
            login (str): Unique login.

        Returns:
            User: Retrieved user.
        """
        stmt: Select[Any] = sa.Select(UserORM).where(
            sa.or_(UserORM.email == email, UserORM.login == login),
        )
        return await self._retrieve_data(stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def change_email(self, uid: uuid.UUID, email: str) -> User:
        """Change the email of user with that ID.

        Args:
            uid (uuid.UUID): User UUID.
            email (str): Electronic mail.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: Updated User.
        """
        stmt = sa.Update(UserORM).where(
            UserORM.id == uid,
        ).values(
            email=email,
        ).returning(
            UserORM.id,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        retrieve_stmt: Select[Any] = Select(UserORM).where(
            UserORM.id == fetch[0],
        )
        return await self._retrieve_data(retrieve_stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def change_login(self, uid: uuid.UUID, login: str) -> User:
        """Change the login of user with that ID.

        Args:
            uid (uuid.UUID): User UUID.
            login (str): Unique User login.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: Updated User.
        """
        stmt = sa.Update(UserORM).where(
            UserORM.id == uid,
        ).values(
            login=login,
        ).returning(
            UserORM.id,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        retrieve_stmt: Select[Any] = Select(UserORM).where(
            UserORM.id == fetch[0],
        )
        return await self._retrieve_data(retrieve_stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def change_password(self, uid: uuid.UUID, password: str) -> User:
        """Change the password of user with that ID.

        Args:
            uid (uuid.UUID): User UUID.
            password (str): New password.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: Updated User.
        """
        stmt = sa.Update(UserORM).where(
            UserORM.id == uid,
        ).values(
            password=password,
        ).returning(
            UserORM.id,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        retrieve_stmt: Select[Any] = Select(UserORM).where(
            UserORM.id == fetch[0],
        )
        return await self._retrieve_data(retrieve_stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def update_additional_info(  # noqa: WPS210 (Too many variables.)
        self, uid: uuid.UUID, user_additional_fields: UserAdditionalFields,
    ) -> User:
        """Update additional fields of user with that ID.

        Args:
            uid (uuid.UUID): User UUID.
            user_additional_fields (UserAdditionalFields):
            Pydantic model with new Additional fields.

        Raises:
            UserNotFoundError: If user not found.

        Returns:
            User: Updated User.
        """
        fields = {}
        additional_fields_dump = user_additional_fields.model_dump()
        for field, new_value in additional_fields_dump.items():
            if not new_value:
                continue

            if isinstance(new_value, Path):
                new_value = new_value.as_posix()
            fields[field] = new_value
        stmt = sa.Update(UserORM).where(
            UserORM.id == uid,
        ).values(
            **fields,
        ).returning(
            UserORM.id,
        )
        res = await self._session.execute(stmt)
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError

        retrieve_stmt: Select[Any] = Select(UserORM).where(
            UserORM.id == fetch[0],
        )
        return await self._retrieve_data(retrieve_stmt)

    @backoff.on_exception(
        backoff.expo,
        exception=TimeoutError,
        max_time=10,
        max_tries=3,
    )
    async def _retrieve_data(self, stmt: Select[Any]) -> User:
        """Retrieve User by some statement.

        Args:
            stmt (Select[Any]): Select Query.

        Raises:
            UserNotFoundError: If user not found

        Returns:
            User: Retrieved User.
        """
        res = await self._session.execute(
            stmt.options(
                selectinload(UserORM.user_service),
            ),
        )
        fetch = res.one_or_none()
        if not fetch:
            raise UserNotFoundError
        user_record: UserORM = fetch[0]
        user_service_record: UserServiceORM = user_record.user_service
        return User(
            entity=UserDTO(
                **user_record.__dict__,
            ),
            user_service=UserService(
                UserServiceDTO(
                    **user_service_record.__dict__,
                ),
                role=Role(
                    RoleDTO(
                        **user_service_record.role.__dict__,
                    ),
                ),
            ),
        )
