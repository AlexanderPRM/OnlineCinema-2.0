"""Module with SQLAlchemy models."""

import uuid
from datetime import date

import sqlalchemy as sa
from config import database_config
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from src.domain.role.value_objects import AccessLevel
from src.infrastructure.mixins import IDMixin, TimestampMixin

metadata = sa.MetaData(schema=database_config.db_schema)


class Base(DeclarativeBase):
    """Base Declarative class for SQLAlchemy models."""

    metadata = metadata


class Role(IDMixin, TimestampMixin, Base):
    """Role model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.
    """

    __tablename__ = 'role'

    name: Mapped[str] = mapped_column(sa.String(24), unique=True)
    description: Mapped[str] = mapped_column(sa.String(100), nullable=True)
    access_level: Mapped[AccessLevel] = mapped_column(sa.Enum(AccessLevel))

    user_services: Mapped[list['UserService']] = relationship(
        back_populates='role',
    )


class UserService(IDMixin, TimestampMixin, Base):
    """User Service model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.
    """

    __tablename__ = 'user_service'

    role_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('role.id', ondelete='SET NULL'),
    )
    active: Mapped[bool] = mapped_column(default=True)
    verified: Mapped[bool] = mapped_column(default=False)

    role: Mapped['Role'] = relationship(back_populates='user_services')
    user: Mapped['User'] = relationship(back_populates='user_service')


class User(IDMixin, TimestampMixin, Base):
    """User model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.
    """

    __tablename__ = 'user'

    email: Mapped[str] = mapped_column(
        sa.String(254), unique=True,  # noqa: WPS432
    )
    login: Mapped[str] = mapped_column(sa.String(60), unique=True)
    password: Mapped[str] = mapped_column(sa.String(100))
    user_service_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('user_service.id', ondelete='CASCADE'),
    )
    full_name: Mapped[str] = mapped_column(sa.String(60), nullable=True)
    profile_picture: Mapped[str] = mapped_column(sa.Text, nullable=True)
    birthday: Mapped[date] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(sa.String(24), nullable=True)
    bio: Mapped[str] = mapped_column(sa.String(1000), nullable=True)

    user_service: Mapped['UserService'] = relationship(back_populates='user')
    login_history: Mapped[list['LoginHistory']] = relationship(
        back_populates='user',
    )
    social_accounts: Mapped[list['UserSocialAccount']] = relationship(
        back_populates='user',
    )


class SocialNetwork(IDMixin, TimestampMixin, Base):
    """Social Network model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.
    """

    __tablename__ = 'social_network'

    picture: Mapped[str] = mapped_column(sa.Text, nullable=True)
    name: Mapped[str] = mapped_column(sa.String(24))

    login_history: Mapped[list['LoginHistory']] = relationship(
        back_populates='social_network',
    )
    social_accounts: Mapped[list['UserSocialAccount']] = relationship(
        back_populates='social_network',
    )


class UserSocialAccount(IDMixin, TimestampMixin, Base):
    """User Social Account model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.
    """

    __tablename__ = 'user_social_account'

    social_network_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('social_network.id', ondelete='CASCADE'),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('user.id', ondelete='CASCADE'),
    )
    social_account_id: Mapped[str]

    social_network: Mapped['SocialNetwork'] = relationship(
        back_populates='social_accounts',
    )
    user: Mapped['User'] = relationship(back_populates='social_accounts')


class LoginHistory(IDMixin, TimestampMixin, Base):
    """Login History model.

    Args:
        IDMixin (class): UUID ID Mixin.
        TimestampMixin (class): TimeStamp Mixin.
        Base (class): Base Declarative class.
    """

    __tablename__ = 'login_history'

    user_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('user.id', ondelete='CASCADE'),
    )
    user_agent: Mapped[str]
    social_network_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('social_network.id', ondelete='SET NULL'), nullable=True,
    )

    user: Mapped['User'] = relationship(back_populates='login_history')
    social_network: Mapped['SocialNetwork'] = relationship(
        back_populates='login_history',
    )
