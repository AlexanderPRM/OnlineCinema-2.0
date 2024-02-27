"""Module with classes for work with Tokens."""

import uuid
from abc import ABC, abstractmethod
from typing import Optional, TypeAlias

JWTToken: TypeAlias = str


class IAccessTokenRepository(ABC):
    """Repository for work with Access Tokens.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(
        self,
        user_id: uuid.UUID,
        access_token: JWTToken,
        exp: int,
    ) -> JWTToken:
        """Insert access token in storage.

        Args:
            user_id (uuid.UUID): User UUID ID.
            access_token (JWTToken): JWT access token.
            exp (int): When Token expire.

        Returns:
            Optional[JWTToken]: Json Web Token.
        """

    @abstractmethod
    async def retrieve(
        self,
        user_id: uuid.UUID,
        access_token: JWTToken,
    ) -> Optional[JWTToken]:
        """Retrieve access token from storage.

        Args:
            user_id (uuid.UUID): User UUID ID.
            access_token (JWTToken): JWT access token.

        Returns:
            Optional[JWTToken]: Json Web Token.
        """


class IRefreshTokenRepository(ABC):
    """Repository for work with Refresh Tokens.

    Args:
        ABC (class): Used to create an abstract class.
    """

    @abstractmethod
    async def insert(
        self,
        user_id: uuid.UUID,
        refresh_token: JWTToken,
        exp: int,
    ) -> JWTToken:
        """Insert refresh token in storage.

        Args:
            user_id (uuid.UUID): User UUID ID.
            refresh_token (JWTToken): JWT refresh token.
            exp (int): When Token expire.

        Returns:
            JWTToken: Json Web Token.
        """

    @abstractmethod
    async def retrieve(
        self,
        user_id: uuid.UUID,
        refresh_token: JWTToken,
    ) -> Optional[JWTToken]:
        """Retrieve refresh token from storage.

        Args:
            user_id (uuid.UUID): User UUID ID.
            refresh_token (JWTToken): JWT refresh token.

        Returns:
            Optional[JWTToken]: Json Web Token.
        """

    @abstractmethod
    async def delete(
        self,
        user_id: uuid.UUID,
        refresh_token: JWTToken,
    ) -> None:
        """Delete refresh token from Storage.

        Args:
            user_id (uuid.UUID): User UUID ID.
            refresh_token (JWTToken): JWT refresh token.
        """
