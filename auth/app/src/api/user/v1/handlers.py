"""Module with users API handlers."""

from http import HTTPStatus

from containers import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from src.api.user.exceptions import BASE_ROLE_NOT_FOUND, USER_ALREADY_EXISTS
from src.domain.repositories.role.exceptions import BaseRoleNotFoundError
from src.domain.repositories.user.exceptions import UserAlreadyExists
from src.use_cases.user.dto import UserSignUpDTO, UserSignUpOutDTO
from src.use_cases.user.signup import SignUpUseCase

router = APIRouter()


@router.post(
    path='/signup/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSignUpOutDTO,
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
) -> UserSignUpOutDTO:
    """Signup handler.

    Processes user signup.

    Args:
        body (UserSignUpDTO): Data for signup.
        use_case (SignUpUseCase): Signup use case.

    Raises:
        USER_ALREADY_EXISTS: If that user already exists.
        BASE_ROLE_NOT_FOUND: If base role for user not found.

    Returns:
        UserSignUpOutDTO: Output data with new user info.
    """
    try:
        res = await use_case.execute(body)
    except UserAlreadyExists:
        raise USER_ALREADY_EXISTS
    except BaseRoleNotFoundError:
        raise BASE_ROLE_NOT_FOUND
    return res
