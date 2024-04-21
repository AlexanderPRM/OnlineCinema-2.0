"""Module with containers for dependency injections."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from config import ProjectSettings
from dependency_injector import containers, providers
from src.infrastructure.databases import PostgreSQL, Redis, init_redis
from src.infrastructure.interfaces.cache.unit_of_work import (
    UnitOfWork as RedisUnifOfWork,
)
from src.infrastructure.interfaces.database.unit_of_work import (
    UnitOfWork as PostgreSQLUnitOfWork,
)
from src.infrastructure.interfaces.tokens.entities import TokenCreator
from src.infrastructure.interfaces.tokens.key_schema import KeySchema
from src.use_cases.user.signin import SignInUseCase
from src.use_cases.user.signup import SignUpUseCase


class PostgreSQLContainer(containers.DeclarativeContainer):
    """Container with PostgreSQL resources and classes."""

    config = providers.Dependency(instance_of=ProjectSettings)
    postgresql = providers.Singleton(
        PostgreSQL,
        config=config.provided.postgresql_settings,
        )
    uow = providers.Factory(
        PostgreSQLUnitOfWork,
        session_factory=postgresql.provided.sessionmaker,
    )


class RedisContainer(containers.DeclarativeContainer):
    """Container with Redis resources and classes."""

    config = providers.Dependency(instance_of=ProjectSettings)
    key_schema = providers.Singleton(KeySchema)
    redis_client = providers.Resource(
        init_redis,
        config=config.provided.redis_settings,
    )
    redis = providers.Singleton(
        Redis,
        redis=redis_client,
    )
    uow = providers.Factory(
        RedisUnifOfWork,
        redis=redis.provided.client,
        key_schema=key_schema.provided,
    )


class Container(containers.DeclarativeContainer):
    """Main container."""

    config = ProjectSettings()

    postgresql = providers.Container(PostgreSQLContainer, config=config)
    redis = providers.Container(RedisContainer, config=config)
    token_creator = providers.Singleton(
        TokenCreator,
        config=config.tokens_settings,
    )

    signup_use_case = providers.Factory(
        SignUpUseCase,
        cache_uow=redis.container.uow,
        database_uow=postgresql.container.uow,
        tokens=token_creator.provided,
    )

    signin_use_case = providers.Factory(
        SignInUseCase,
        cache_uow=redis.container.uow,
        database_uow=postgresql.container.uow,
        tokens=token_creator.provided,
    )

    @classmethod
    @asynccontextmanager
    async def lifespan(
        cls, wireable_packages: list,
    ) -> AsyncGenerator[Container, Any]:
        """Container lifespan.

        Args:
            wireable_packages (list): Names of packages for wire.


        Yields:
            class: Yield themself.
        """
        container = cls()
        container.wire(packages=wireable_packages)

        await container.init_resources()
        yield container
        await container.shutdown_resources()
