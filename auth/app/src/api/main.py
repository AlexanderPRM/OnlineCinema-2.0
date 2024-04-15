"""Module with API entry point."""

from contextlib import asynccontextmanager

from containers import Container
from fastapi import FastAPI
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


app = FastAPI(lifespan=lifespan)
init_routers(app)
