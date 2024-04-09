"""Module with Tokens repositories."""

import uuid

from redis.asyncio.client import Pipeline
from src.infrastructure.interfaces.tokens.entities import IToken
from src.infrastructure.interfaces.tokens.key_schema import KeySchema
from src.use_cases.interfaces.tokens.repo import (
    IAccessTokenRepository,
    IRefreshTokenRepository,
)


class AccessTokenRepository(IAccessTokenRepository):
    """Repository for work with access JWT tokens.

    Args:
        IAccessTokenRepository (class): Abstract Repository.
    """

    def __init__(self, pipeline: Pipeline, key_schema: KeySchema) -> None:
        """Init method.

        Args:
            pipeline (Pipeline): Redis pipeline.
            key_schema (KeySchema): Class with key schemas for redis.
        """
        self._pipeline = pipeline
        self._key_schema = key_schema

    async def insert(
        self,
        uid: uuid.UUID,
        access_token: IToken,
    ) -> None:
        """Insert new access token to the Redis.

        Args:
            uid (uuid.UUID): User UUID.
            access_token (IToken): Access Json Web Token.
        """
        key = self._key_schema.user_access_token(uid, access_token)
        decoded = access_token.get_decoded_token()
        expire = decoded['exp']
        await self._pipeline.set(
            name=key, value=str(expire), exat=int(expire),
        )

    async def exists(self, uid: uuid.UUID, access_token: IToken) -> None:
        """Check that access token exists.

        Args:
            uid (uuid.UUID): User UUID.
            access_token (IToken): Access Json Web Token.
        """
        key = self._key_schema.user_access_token(uid, access_token)
        await self._pipeline.exists(key)


class RefreshTokenRepository(IRefreshTokenRepository):
    """Repository for work with refresh JWT tokens.

    Args:
        IRefreshTokenRepository (class): Abstract Repository.
    """

    def __init__(self, pipeline: Pipeline, key_schema: KeySchema) -> None:
        """Init method.

        Args:
            pipeline (Pipeline): Redis pipeline.
            key_schema (KeySchema): Class with key schemas for redis
        """
        self._pipeline = pipeline
        self._key_schema = key_schema

    async def insert(
        self,
        uid: uuid.UUID,
        refresh_token: IToken,
    ) -> None:
        """Insert new refresh token to the Redis.

        Args:
            uid (uuid.UUID): User UUID.
            refresh_token (IToken): Refresh Json Web Token.
        """
        key = self._key_schema.user_refresh_token(uid, refresh_token)
        decoded = refresh_token.get_decoded_token()
        expire = decoded['exp']
        await self._pipeline.set(
            name=key, value=str(expire), exat=int(expire),
        )

    async def exists(
        self,
        uid: uuid.UUID,
        refresh_token: IToken,
    ) -> None:
        """Retrieve refresh token from storage.

        Args:
            uid (uuid.UUID): User UUID ID.
            refresh_token (IToken): Refresh Json Web Token.
        """
        key = self._key_schema.user_refresh_token(uid, refresh_token)
        await self._pipeline.exists(key)

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
        key = self._key_schema.user_refresh_token(uid, refresh_token)
        await self._pipeline.delete(key)
