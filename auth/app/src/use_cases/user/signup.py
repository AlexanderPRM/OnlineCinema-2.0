"""Module with User Register use case."""

from src.domain.repositories.user.exceptions import (
    UserAlreadyExists,
    UserNotFoundError,
)
from src.domain.role.entities import Role
from src.domain.user.entities import User
from src.domain.user_service.entities import UserService
from src.use_cases.interfaces.cache.unit_of_work import (
    AbstractUnitOfWork as AbstractCacheUnitOfWork,
)
from src.use_cases.interfaces.database.unit_of_work import (
    AbstractUnitOfWork as AbstractDatabaseUnitOfWork,
)
from src.use_cases.interfaces.tokens.entities import ITokenCreator
from src.use_cases.user.dto import UserOutDTO, UserSignUpDTO


class SignUpUseCase:
    """User Register Use Case."""

    def __init__(
        self,
        cache_uow: AbstractCacheUnitOfWork,
        database_uow: AbstractDatabaseUnitOfWork,
        tokens: ITokenCreator,
    ) -> None:
        """Init method.

        Args:
            cache_uow (AbstractCacheUnitOfWork): Unit of Work with Cache.
            database_uow (AbstractDatabaseUnitOfWork):
            Unit of Work with main Database.
            tokens (ITokenCreator): Fabric for create Tokens.
        """
        self.cache_uow = cache_uow
        self.database_uow = database_uow
        self.tokens = tokens

    async def execute(self, dto: UserSignUpDTO) -> UserOutDTO:
        """Register User.

        Args:
            dto (UserSignUpDTO): DTO with info for user register.

        Raises:
            UserAlreadyExists: User Already Exists Exception.

        Returns:
            UserOutDTO: Output info of that use case.
        """
        exists = await self._check_user_exists(dto.email, dto.login)
        if exists:
            raise UserAlreadyExists

        async with self.database_uow(autocommit=True):
            role = await self.database_uow.role.retrieve_base_role()

        created_user = await self._insert_user(
            role, dto.email, dto.login, dto.password,
        )
        access_token = self.tokens.create_access_token(created_user.id)
        refresh_token = self.tokens.create_refresh_token(created_user.id)

        async with self.cache_uow(False):
            await self.cache_uow.refresh_tokens.insert(
                created_user.id, refresh_token,
            )

        return UserOutDTO(
            user=created_user.as_dto(),
            access_token=access_token.get_encoded_token(),
            refresh_token=refresh_token.get_encoded_token(),
        )

    async def _check_user_exists(self, email: str, login: str) -> bool:
        """Check if user already exists or not.

        Args:
            email (str): Electronic mail address.
            login (str): User Login.

        Returns:
            bool: Exists or Not.
        """
        async with self.database_uow(autocommit=False):
            try:
                await self.database_uow.user.retrieve_by_email_or_login(
                    email,
                    login,
                )
            except UserNotFoundError:
                return False
        return True

    async def _insert_user(
        self, role: Role, email: str, login: str, password: str,
    ) -> User:
        """Add user to database.

        Args:
            role (Role): Entity of Role.
            email (str): User electronic mail.
            login (str): User unique login.
            password (str): User password.

        Returns:
            user (User): Entity of created user.
        """
        async with self.database_uow(autocommit=True):
            user_service = await self.database_uow.user_service.insert(
                UserService.create(role=role),
            )
            user = await self.database_uow.user.insert(
                User.create(
                    email=email,
                    login=login,
                    password=password,
                    user_service=user_service,
                ),
            )
        return user
