"""Module with User Register use case."""

from src.domain.user.entities import User
from src.domain.user_service.entities import UserService
from src.use_cases.exceptions import BaseRoleNotExists, UserAlreadyExists
from src.use_cases.interfaces.cache.unit_of_work import (
    AbstractUnitOfWork as TokensUoW,
)
from src.use_cases.interfaces.database.unit_of_work import (
    AbstractUnitOfWork as DatabaseUoW,
)
from src.use_cases.user.dto import UserSignUpDTO


class RegisterUseCase:
    """User Register Use Case."""

    def __init__(
        self,
        tokens_uow: TokensUoW,
        database_uow: DatabaseUoW,
    ) -> None:
        """Init method.

        Args:
            tokens_uow (TokensUoW): Unit Work with Tokens.
            database_uow (DatabaseUoW): _description_
        """
        self.tokens_uow = tokens_uow
        self.database_uow = database_uow

    async def execute(self, dto: UserSignUpDTO) -> User:
        """Register User.

        Args:
            dto (UserSignUpDTO): DTO with info for user register.

        Raises:
            UserAlreadyExists: User Already Exists Exception.
            BaseRoleNotExists: Base Role for New users not exists.

        Returns:
            User: Created User.
        """
        already_exists = self.check_user_exists(dto.email, dto.login)
        if already_exists:
            raise UserAlreadyExists

        async with self.database_uow(autocommit=True):
            role = await self.database_uow.role.retrieve_by_name('base')

        if not role:
            raise BaseRoleNotExists

        async with self.database_uow(autocommit=True):
            user_service = await self.database_uow.user_service.insert(
                UserService.create(role=role),
            )
            created_user = await self.database_uow.user.insert(
                User.create(
                    email=dto.email,
                    login=dto.login,
                    password=dto.password,
                    user_service=user_service,
                ),
            )
        return created_user

    async def check_user_exists(self, email: str, login: str) -> bool:
        """Check if user already exists or not.

        Args:
            email (str): Electronic mail address.
            login (str): User Login.

        Returns:
            bool: Exists or Not.
        """
        async with self.database_uow(autocommit=True):
            user = await self.database_uow.user.retrieve_by_email_or_login(
                email,
                login,
            )
        return user is not None
