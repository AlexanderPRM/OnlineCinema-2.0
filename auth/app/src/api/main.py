"""Module with API entry point."""

from contextlib import asynccontextmanager

from config import APISettings, LoggingSettings
from containers import Container
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src import api
from src.api.routers import init_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan for initialize container.

    Args:
        app (FastAPI): FastAPI application instance.

    Yields:
        None: None. :)
    """
    async with Container.lifespan(wireable_packages=[api]):
        yield


log_config = LoggingSettings()

if log_config.use_sentry:
    import sentry_sdk  # noqa: WPS433 (Nested Import)

    sentry_sdk.init(
        dsn=log_config.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

config = APISettings()

app = FastAPI(
    lifespan=lifespan,
    title='Auth API.',
    root_path='/auth',
    debug=not config.production,
    default_response_class=ORJSONResponse,
)

init_routers(app)
