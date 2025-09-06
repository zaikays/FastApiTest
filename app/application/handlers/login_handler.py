import logging

from app.adapters.auth.jwt_processor import JwtAccessTokenProcessor
from app.adapters.auth.utils.auth_token_timer import UtcAuthTokenTimer
from app.adapters.constants.auth import (
    AUTH_NOT_AUTHENTICATED,
    AUTH_INVALID_PASSWORD,
    AUTH_ACCOUNT_INACTIVE,
)
from app.adapters.exceptions.auth import AuthenticationError
from app.adapters.models.user_model import UserModel
from app.application.common.ports.user_command_gateway import UserCommandGatewayAsync

from app.domain.enums.token_type import TokenType
from app.domain.enums.user_role import UserRole
from app.domain.models.jwt_payload import AuthJwtPayload

from app.domain.models.value_objects.raw_password.raw_password import RawPassword
from app.domain.models.value_objects.email.email import Email
from app.domain.services.password_hasher import PasswordHasher
from app.presentation.dtos.auth import LoginRequest, LoginResponse

log = logging.getLogger(__name__)


class LoginHandler:
    def __init__(
        self,
        user_command_gateway: UserCommandGatewayAsync,
        password_hasher: PasswordHasher,
        token_timer: UtcAuthTokenTimer,
        access_token_processor: JwtAccessTokenProcessor,
    ):
        self._user_command_gateway = user_command_gateway
        self._password_hasher = password_hasher
        self._access_token_processor = access_token_processor
        self._token_timer = token_timer

    async def execute(self, request_data: LoginRequest) -> LoginResponse:

        email = Email(request_data.email)
        password = RawPassword(request_data.password)

        user: UserModel | None = await self._user_command_gateway.read_by_email(email)
        if user is None:
            raise AuthenticationError(AUTH_NOT_AUTHENTICATED)

        if not user.is_active:
            raise AuthenticationError(AUTH_ACCOUNT_INACTIVE)

        if not self._password_hasher.verify(
            raw_password=password, hashed_password=user.password_hash
        ):
            raise AuthenticationError(AUTH_INVALID_PASSWORD)

        return LoginResponse(
            token=self._access_token_processor.encode(
                AuthJwtPayload(
                    sub=user.id,
                    expiration=self._token_timer.auth_access_token_expiration,
                    role=UserRole(user.role),
                    type=TokenType.ACCESS,
                )
            ),
            refresh_token=self._access_token_processor.encode(
                AuthJwtPayload(
                    sub=user.id,
                    expiration=self._token_timer.auth_refresh_token_expiration,
                    role=UserRole(user.role),
                    type=TokenType.REFRESH,
                )
            ),
        )
