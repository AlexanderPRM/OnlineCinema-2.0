"""Module with Database Unit of Work."""

from __future__ import annotations

from redis.asyncio import Redis
from src.infrastructure.interfaces.tokens.key_schema import KeySchema
from src.infrastructure.interfaces.tokens.repo import (
    AccessTokenRepository,
    RefreshTokenRepository,
)
from src.use_cases.interfaces.cache.unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    """Class for work with tokens repositories.

    Args:
        AbstractUnitOfWork (class): Abstract Unit of Work.
    """

    def __init__(self, redis: Redis, key_schema: KeySchema):
        """Init method.

        Args:
            redis (Redis): Redis client.
            key_schema (KeySchema): Class with key schemas for Redis.
        """
        self._redis = redis
        self._key_schema = key_schema
        self.responses: list[None] = []

    def __call__(self, transaction: bool) -> UnitOfWork:
        """Magic method responsible for the logic when calling class.

        Args:
            transaction (bool): Do request like transaction.

        Returns:
            UnitOfWork: Return itself.
        """
        self.transaction = transaction
        return self

    async def __aenter__(self) -> UnitOfWork:
        """Call when entry in async context manager.

        Returns:
            UnitOfWork: Return themself.
        """
        self._pipeline = self._redis.pipeline(transaction=self.transaction)

        self.access_tokens = AccessTokenRepository(
            self._pipeline, self._key_schema,
        )
        self.refresh_tokens = RefreshTokenRepository(
            self._pipeline, self._key_schema,
        )
        return self

    async def _execute(self) -> None:
        self.responses = await self._pipeline.execute()

    async def _discard(self) -> None:
        await self._pipeline.discard()
