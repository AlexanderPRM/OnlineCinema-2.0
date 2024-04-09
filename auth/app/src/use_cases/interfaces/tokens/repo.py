"""Module with classes for work with Tokens."""

import uuid
from abc import ABC, abstractmethod

from src.use_cases.interfaces.tokens.entities import IToken


class IAccessTokenRepository(ABC):
    """Repository for work with Access Tokens.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(
        self,
        user_id: uuid.UUID,
        access_token: IToken,
    ) -> None:
        """Insert access token in storage.

        Args:
            user_id (uuid.UUID): User UUID ID.
            access_token (IToken): JWT access token.
        """

    @abstractmethod
    async def exists(
        self,
        user_id: uuid.UUID,
        access_token: IToken,
    ) -> None:
        """Retrieve access token from storage.

        Args:
            user_id (uuid.UUID): User UUID ID.
            access_token (IToken): Json web token.
        """


class IRefreshTokenRepository(ABC):
    """Repository for work with Refresh Tokens.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(
        self,
        uid: uuid.UUID,
        refresh_token: IToken,
    ) -> None:
        """Insert refresh token in storage.

        Args:
            uid (uuid.UUID): User UUID ID.
            refresh_token (IToken): JWT refresh token.
        """

    @abstractmethod
    async def exists(
        self,
        uid: uuid.UUID,
        refresh_token: IToken,
    ) -> None:
        """Check exists that Refresh Token in storage.

        Args:
            uid (uuid.UUID): User UUID ID.
            refresh_token (IToken): Refresh Json Web Token.
        """

    @abstractmethod
    async def delete(
        self,
        uid: uuid.UUID,
        refresh_token: IToken,
    ) -> None:
        """Delete refresh token from Storage.

        Args:
            uid (uuid.UUID): User UUID ID.
            refresh_token (IToken): Refresh Json Web Token.
        """
