"""Module with Database class."""

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class PostgreSQL:
    """Class for work with PostgreSQL."""

    def __init__(self, dsn: PostgresDsn) -> None:
        """Init method.

        Args:
            dsn (PostgresDsn): PostgreSQL DSN.
        """
        self._engine = create_async_engine(
            url=str(dsn),
            echo=True,
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        """Get async session maker.

        Returns:
            async_sessionmaker: SQLAlchemy async session maker.
        """
        return self._session_factory
