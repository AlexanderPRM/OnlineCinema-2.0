"""Table models described using ORM."""

import uuid
from datetime import date, datetime
from enum import Enum
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm as so
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func


class AccessLevel(Enum):
    """Service access levels.

    Args:
        Enum (class): Parent class to create enumeration type.
    """

    base = 0
    subscriber = 1
    superuser = 2


class Base(so.DeclarativeBase):
    """Declarative base models class.

    Args:
        so.DeclarativeBase (class): required SQLAlchemy base Declarative class.
    """

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        postgresql.UUID,
        primary_key=True,
        default=uuid.uuid4,
    )


class Role(Base):
    """Role ORM model.

    Args:
        Base (DeclarativeBase): Declarative Base with common fields.
    """

    __tablename__ = 'role'

    name: so.Mapped[str] = so.mapped_column(sa.String(24))
    description: so.Mapped[str] = so.mapped_column(
        sa.String(100),
        nullable=True,
    )
    access_level: so.Mapped['AccessLevel']
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_onupdate=func.now(),
    )

    users_service: so.Mapped[List['UserService']] = so.relationship(
        back_populates='role',
    )

    def __str__(self) -> str:
        """Human Readable representation magic method.

        Returns:
            str: A human-readable string representation of the object.
        """
        return 'Role "{0}" with access level - {1}'.format(
            self.name,
            self.access_level.value,
        )

    def __repr__(self) -> str:
        """Formal representation magic method.

        Returns:
            str: A string as a representation of the object.
        """
        return '<Role(id={0}, name={1}, access_level={2})'.format(
            self.id,
            self.name,
            self.access_level,
        )


class User(Base):
    """User ORM model.

    Args:
        Base (DeclarativeBase): Declarative Base with common fields.
    """

    __tablename__ = 'user'

    # Ignore WPS432 (Magic Number) because max email length is 254 char.
    email: so.Mapped[str] = so.mapped_column(sa.String(254))  # noqa: WPS432
    login: so.Mapped[str] = so.mapped_column(sa.String(60))
    password: so.Mapped[str] = so.mapped_column(sa.String(100))
    user_service_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user_service.id'),
    )
    profile_picture: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(60), nullable=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(60), nullable=True)
    birthday: so.Mapped[date] = so.mapped_column(nullable=True)
    phone_number: so.Mapped[str] = so.mapped_column(
        sa.String(24),
        nullable=True,
    )
    bio: so.Mapped[str] = so.mapped_column(sa.String(1000), nullable=True)
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_onupdate=func.now(),
    )

    user_service: so.Mapped['UserService'] = so.relationship(
        back_populates='user',
    )
    login_history: so.Mapped[List['LoginHistory']] = so.relationship(
        back_populates='user',
    )

    def __str__(self) -> str:
        """Human Readable representation magic method.

        Returns:
            str: A human-readable string representation of the object.
        """
        return 'User {0}. First name - {1}, Last name - {2}'.format(
            self.email,
            self.first_name,
            self.last_name,
        )

    def __repr__(self) -> str:
        """Formal representation magic method.

        Returns:
            str: A string as a representation of the object.
        """
        return '<User(id={0}, first_name={1}, bio={2})'.format(
            self.id,
            self.first_name,
            self.bio,
        )


class UserService(Base):
    """UserService ORM Model.

    Args:
        Base (DeclarativeBase): Declarative Base with common fields.
    """

    __tablename__ = 'user_service'

    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('role.id'))
    is_active: so.Mapped[bool] = so.mapped_column(default=True)
    verified: so.Mapped[bool] = so.mapped_column(default=False)
    date_joined: so.Mapped[date] = so.mapped_column(
        server_default=func.current_date(),
    )

    role: so.Mapped['Role'] = so.relationship(back_populates='users_service')
    user: so.Mapped['User'] = so.relationship(back_populates='user_service')

    def __str__(self) -> str:
        """Human Readable representation magic method.

        Returns:
            str: A human-readable string representation of the object.
        """
        return 'User "{0}" service info. User role - {1}'.format(
            self.user.email,
            self.role.name,
        )

    def __repr__(self) -> str:
        """Formal representation magic method.

        Returns:
            str: A string as a representation of the object.
        """
        return '<UserService(id={0}, role_id={1}, date_joined={2})'.format(
            self.id,
            self.role_id,
            self.date_joined,
        )


class LoginHistory(Base):
    """Login History ORM model.

    Args:
        Base (DeclarativeBase): Declarative Base with common fields.
    """

    __tablename__ = 'login_history'

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    user_agent: so.Mapped[str] = so.mapped_column(sa.Text)
    login_date: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
    )

    user: so.Mapped['User'] = so.relationship(back_populates='login_history')

    def __str__(self) -> str:
        """Human Readable representation magic method.

        Returns:
            str: A human-readable string representation of the object.
        """
        return 'User Login with user-agent {0} and login date {1}'.format(
            self.user_agent,
            self.login_date,
        )

    def __repr__(self) -> str:
        """Formal representation magic method.

        Returns:
            str: A string as a representation of the object.
        """
        return '<LoginHistory(id={0}, user_id={1}, user_agent={2})'.format(
            self.id,
            self.user_id,
            self.user_agent,
        )
