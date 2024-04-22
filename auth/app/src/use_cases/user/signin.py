"""Module with Singin Use case."""

import logging

from src.domain.user.entities import User
from src.use_cases.exceptions import PasswordNotCorrect
from src.use_cases.interfaces.cache.unit_of_work import (
    AbstractUnitOfWork as AbstractCacheUnitOfWork,
)
from src.use_cases.interfaces.database.unit_of_work import (
    AbstractUnitOfWork as AbstractDatabaseUnitOfWork,
)
from src.use_cases.interfaces.tokens.entities import ITokenCreator
from src.use_cases.user.dto import UserOutDTO, UserSignInDTO, pwd_context

logger = logging.getLogger(__name__)


class SignInUseCase:
    """User login Use case."""

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

    async def execute(self, dto: UserSignInDTO) -> UserOutDTO:
        """User signin use case.

        Args:
            dto (UserSignInDTO): DTO with info for user login.

        Raises:
            PasswordNotCorrect: If password not correct, throw this.

        Returns:
            UserOutDTO: Output info of that use case.
        """
        user = await self.get_by_credential(
            dto.credential,
            dto.credential_is_email,
        )
        user_as_dto = user.as_dto()
        if not pwd_context.verify(dto.password, user_as_dto.password):
            raise PasswordNotCorrect

        access_token = self.tokens.create_access_token(user_as_dto.id)
        refresh_token = self.tokens.create_refresh_token(user_as_dto.id)

        async with self.cache_uow(False):
            await self.cache_uow.refresh_tokens.insert(
                user_as_dto.id,
                refresh_token,
            )
            logger.debug('Insert tokens to Redis for user ({uid})'.format(
                uid=user_as_dto.id,
                ),
            )

        logger.info('User {uid} logged in account.'.format(uid=user_as_dto.id))

        return UserOutDTO(
            user=user_as_dto,
            access_token=access_token.get_encoded_token(),
            refresh_token=refresh_token.get_encoded_token(),
        )

    async def get_by_credential(  # type: ignore[return]
        self, credential: str, credential_is_email: bool,
    ) -> User:
        """Retrieve user by his credential.

        Args:
            credential (str): User credential.
            credential_is_email (bool): Credential email or not.

        Returns:
            User: Retrieved user.
        """
        async with self.database_uow(autocommit=True):
            if credential_is_email:
                return await self.database_uow.user.retrieve_by_email(
                    credential,
                )
            return await self.database_uow.user.retrieve_by_login(credential)
