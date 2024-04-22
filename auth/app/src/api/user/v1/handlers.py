"""Module with users API handlers."""

from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from src.api.user.exceptions import (
    BASE_ROLE_NOT_FOUND,
    CREDENTIAL_OR_PASSWORD_NOT_CORRECT,
    USER_ALREADY_EXISTS,
)
from src.containers import Container
from src.domain.repositories.role.exceptions import BaseRoleNotFoundError
from src.domain.repositories.user.exceptions import (
    UserAlreadyExists,
    UserNotFoundError,
)
from src.use_cases.exceptions import PasswordNotCorrect
from src.use_cases.user.dto import UserOutDTO, UserSignInDTO, UserSignUpDTO
from src.use_cases.user.signin import SignInUseCase
from src.use_cases.user.signup import SignUpUseCase

router = APIRouter()


@router.post(
    path='/signup/',
    status_code=HTTPStatus.CREATED,
    response_model=UserOutDTO,
    responses={
        HTTPStatus.NOT_FOUND: {
            'content': {
                'application/json': {
                    'example': {'detail': BASE_ROLE_NOT_FOUND.detail},
                },
            },
        },
        HTTPStatus.CONFLICT: {
            'content': {
                'application/json': {
                    'example': {'detail': USER_ALREADY_EXISTS.detail},
                },
            },
        },
    },
)
@inject
async def signup(
    body: UserSignUpDTO,
    use_case: SignUpUseCase = Depends(Provide[Container.signup_use_case]),
) -> UserOutDTO:
    """Signup handler.

    Processes user signup.

    Args:
        body (UserSignUpDTO): Data for signup.
        use_case (SignUpUseCase): Signup use case.

    Raises:
        USER_ALREADY_EXISTS: If that user already exists.
        BASE_ROLE_NOT_FOUND: If base role for user not found.

    Returns:
        UserOutDTO: Output data with new user info.
    """
    try:
        res = await use_case.execute(body)
    except UserAlreadyExists:
        raise USER_ALREADY_EXISTS
    except BaseRoleNotFoundError:
        raise BASE_ROLE_NOT_FOUND
    return res


@router.post(
    path='/signin/',
    status_code=HTTPStatus.OK,
    response_model=UserOutDTO,
    responses={
        HTTPStatus.UNAUTHORIZED: {
            'content': {
                'application/json': {
                    'example': {
                        'detail': CREDENTIAL_OR_PASSWORD_NOT_CORRECT.detail,
                    },
                },
            },
        },
    },
)
@inject
async def signin(
    body: UserSignInDTO,
    use_case: SignInUseCase = Depends(Provide[Container.signin_use_case]),
) -> UserOutDTO:
    """Sign in handler.

    Args:
        body (UserSignInDTO): Data for sign in.
        use_case (SignInUseCase): Sign in Use case.

    Raises:
        CREDENTIAL_OR_PASSWORD_NOT_CORRECT: If credentials not correct.

    Returns:
        UserOutDTO: Output data with new user info.
    """
    try:
        res = await use_case.execute(body)
    except (UserNotFoundError, PasswordNotCorrect):
        raise CREDENTIAL_OR_PASSWORD_NOT_CORRECT
    return res
