"""Module with Relational Database classes."""

from abc import ABC, abstractmethod

import backoff
from sqlalchemy.exc import (
    DisconnectionError,
    ResourceClosedError,
    TimeoutError,
)
from sqlalchemy.ext.asyncio import (
    AsyncResult,
    async_sessionmaker,
    create_async_engine,
)


class AbstractRelationalDatabase(ABC):
    """Abstract class for Relational DataBases classes.

    Args:
        ABC (class): Makes class abstract.
    """

    @abstractmethod
    async def dispose(self):
        """Close all currently checked in database connection."""

    @abstractmethod
    async def execute_query(self, stmt, **options):
        """Execute a given statement with optional options.

        Args:
            stmt: Query.
            options: Optional options for execute.

        Returns:
            result: Execution result.
        """


class PostgreSQL(AbstractRelationalDatabase):
    """Class for work with PostgreSQL DB.

    Args:
        AbstractRelationalDatabase (class): Abstract class for Relational DB's.
    """

    def __init__(self, postgres_url: str, **options) -> None:
        """Init class.

        Args:
            postgres_url (str): PostgreSQL DSN.
            options: Optional options for create engine.
        """
        self.engine = create_async_engine(postgres_url, **options)
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            TimeoutError,
            ResourceClosedError,
            DisconnectionError,
        ),
        max_time=10,
        max_tries=3,
    )
    async def dispose(self) -> None:
        """Close all currently checked in database connection."""
        await self.engine.dispose()

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            TimeoutError,
            ResourceClosedError,
            DisconnectionError,
        ),
        max_time=5,
        max_tries=3,
    )
    async def execute_query(self, stmt, **options) -> AsyncResult:
        """Execute a given statement with optional options.

        Args:
            stmt: SQLAlchemy Query.
            options: Optional options for execute.

        Returns:
            AsyncResult: Execution result.
        """
        async with self.async_session() as session:
            async with session.begin():
                return await session.execute(stmt, **options)


db: [AbstractRelationalDatabase] = None


async def get_database() -> AbstractRelationalDatabase:
    """Return Relational DataBase Class, for example, for FastAPI Depends.

    Returns:
        AbstractRelationalDatabase: Abstract class for Relational DataBases.
    """
    return db
