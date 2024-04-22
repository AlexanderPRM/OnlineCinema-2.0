"""Module with API entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src import api
from src.api.routers import init_routers
from src.config import APISettings, LoggingSettings
from src.containers import Container
from src.logging import get_logging_config


def setup_logging():
    """Set logging configuration."""
    logging_config = LoggingSettings()

    logging.config.dictConfig(get_logging_config())

    if logging_config.use_sentry:
        import sentry_sdk  # noqa: WPS433 (Nested Import)

        sentry_sdk.init(
            dsn=logging_config.sentry_dsn,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan for initialize container.

    Args:
        app (FastAPI): FastAPI application instance.

    Yields:
        None: None. :)
    """
    setup_logging()
    async with Container.lifespan(wireable_packages=[api]):
        yield


config = APISettings()

app = FastAPI(
    lifespan=lifespan,
    title='Auth API.',
    root_path='/auth',
    debug=not config.production,
    default_response_class=ORJSONResponse,
)

init_routers(app)
