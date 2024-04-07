"""Module with Tokens repositories."""

import uuid

from redis.asyncio.client import Pipeline
from src.infrastructure.interfaces.cache.tokens.key_schema import KeySchema
from src.use_cases.interfaces.cache.tokens.repo import (
    IAccessTokenRepository,
    IRefreshTokenRepository,
    JWTToken,
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
        access_token: JWTToken,
        exp: int,
    ) -> None:
        """Insert new access token to the Redis.

        Args:
            uid (uuid.UUID): User UUID.
            access_token (JWTToken): Access Json Web Token.
            exp (int): When token expire in timestamp.
        """
        key = self._key_schema.user_access_token(uid, access_token)
        await self._pipeline.set(name=key, value=exp, exat=exp)

    async def exists(self, uid: uuid.UUID, access_token: JWTToken) -> None:
        """Check that access token exists.

        Args:
            uid (uuid.UUID): User UUID.
            access_token (JWTToken): Access Json Web Token.
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
        refresh_token: JWTToken,
        exp: int,
    ) -> None:
        """Insert new refresh token to the Redis.

        Args:
            uid (uuid.UUID): User UUID.
            refresh_token (JWTToken): Refresh Json Web Token.
            exp (int): When token expire in timestamp.
        """
        key = self._key_schema.user_refresh_token(uid, refresh_token)
        await self._pipeline.set(name=key, value=refresh_token, exat=exp)

    async def exists(
        self,
        uid: uuid.UUID,
        refresh_token: JWTToken,
    ) -> None:
        """Retrieve refresh token from storage.

        Args:
            uid (uuid.UUID): User UUID ID.
            refresh_token (JWTToken): Refresh Json Web Token.
        """
        key = self._key_schema.user_refresh_token(uid, refresh_token)
        await self._pipeline.exists(key)

    async def delete(
        self,
        uid: uuid.UUID,
        refresh_token: JWTToken,
    ) -> None:
        """Delete refresh token from Storage.

        Args:
            uid (uuid.UUID): User UUID ID.
            refresh_token (JWTToken): Refresh Json Web Token.
        """
        key = self._key_schema.user_refresh_token(uid, refresh_token)
        await self._pipeline.delete(key)
