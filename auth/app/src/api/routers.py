"""Module with API routers."""

from fastapi import FastAPI
from src.api.user.routers import router


def init_routers(app: FastAPI):
    """Include routers to FastAPI app.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    app.include_router(router, prefix='/api/public')
