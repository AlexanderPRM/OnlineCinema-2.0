"""Module with Database class."""

from typing import Any, AsyncGenerator

from config import PostgreSQLSettings, RedisSettings
from pydantic import PostgresDsn
from redis.asyncio import ConnectionPool
from redis.asyncio import Redis as RedisClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class PostgreSQL:
    """Class for work with PostgreSQL."""

    def __init__(self, config: PostgreSQLSettings) -> None:
        """Init method.

        Args:
            config (PostgreSQLSettings): Settings for PostgreSQL.
        """
        self._config = config

        dsn = PostgresDsn(
            '{driver}://{user}:{password}@{host}:{port}/{name}'.format(
                driver=self._config.db_driver,
                user=self._config.db_user,
                password=self._config.db_password,
                host=self._config.db_host,
                port=self._config.db_port,
                name=self._config.db_name,
            ),
        )

        self._engine = create_async_engine(
            url=str(dsn),
            echo=True,
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        """Get async session maker.

        Returns:
            async_sessionmaker: SQLAlchemy async session maker.
        """
        return self._session_factory


class Redis:
    """Class for work with Redis."""

    def __init__(self, redis: RedisClient) -> None:
        """Init method.

        Args:
            redis (RedisClient): Redis connection client.
        """
        self._redis = redis

    @property
    def client(self) -> RedisClient:
        """Get redis client.

        Returns:
            RedisClient: Redis client instance.
        """
        return self._redis


async def init_redis(
    config: RedisSettings,
) -> AsyncGenerator[RedisClient, Any]:
    """Initialize redis connection pool.

    Args:
        config (RedisSettings): Configuration for redis.

    Yields:
        Iterator[AsyncGenerator[RedisClient, Any]]: Yield redis client.
    """
    connection_pool = ConnectionPool(
        host=config.redis_host,
        port=config.redis_port,
        username=config.redis_user,
        password=config.redis_password,
        max_connections=config.max_connections,
    )
    async with RedisClient(connection_pool=connection_pool) as redis:
        yield redis
