"""Module with users API routers."""

from fastapi import APIRouter
from src.api.user.v1 import handlers

router = APIRouter()
router.include_router(
    handlers.router,
    prefix='/v1/user',
)
