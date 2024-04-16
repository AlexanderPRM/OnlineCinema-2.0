"""Module with API exceptions."""

from http import HTTPStatus

from fastapi import HTTPException

USER_ALREADY_EXISTS = HTTPException(
    status_code=HTTPStatus.CONFLICT,
    detail='That user already exists.',
)
BASE_ROLE_NOT_FOUND = HTTPException(
    status_code=HTTPStatus.NOT_FOUND,
    detail='Base role for users not found.',
)
