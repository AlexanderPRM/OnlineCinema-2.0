"""Entrypoint module to API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.config import api_settings, database_settings
from src.db import relational


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan for FastAPI app.

    Args:
        app (FastAPI): main app for FastAPI.

    Yields:
        Before yield when app is running.
        After yield when app is stop.

    """
    postgres_dsn = 'postgres+asyncpg://{0}:{1}@{2}:{3}/{4}'.format(
        database_settings.postgres_user,
        database_settings.postgres_password,
        database_settings.postgres_host,
        database_settings.postgres_port,
        database_settings.postgres_db,
    )
    relational.db = relational.PostgreSQL(postgres_dsn)
    yield
    relational.db.dispose()


app = FastAPI(
    title=api_settings.api_title,
    version=api_settings.api_version,
    summary=api_settings.api_summary,
    description=api_settings.api_description,
    docs_url='/api/openapi/',
    openapi_url='/api/openapi.json',
    license_info={
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    },
    default_response_class=ORJSONResponse,
)
