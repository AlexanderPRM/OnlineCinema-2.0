"""Module with SQLAlchemy Mixins."""

import uuid
from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class IDMixin:
    """Mixin with UUID Primary key."""

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )


class TimestampMixin:
    """Mixin with Timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(True),
        default=datetime.now(UTC),
        server_default=sa.func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(True),
        default=datetime.now(UTC),
        server_default=sa.func.now(),
        onupdate=datetime.now(UTC),
        server_onupdate=sa.FetchedValue(),
    )
