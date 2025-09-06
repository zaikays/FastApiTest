from fastapi.security import HTTPAuthorizationCredentials

from app.adapters.auth.jwt_processor import JwtAccessTokenProcessor, JwtTokenData
from app.adapters.constants.auth import AUTH_NOT_AUTHENTICATED
from app.adapters.exceptions.auth import AuthenticationError
from app.adapters.models.user_model import UserModel
from app.application.common.ports.user_command_gateway import UserCommandGatewayAsync


class CurrentUserService:
    def __init__(
        self,
        user_command_gateway: UserCommandGatewayAsync,
        http_bearer: HTTPAuthorizationCredentials,
        token_processor: JwtAccessTokenProcessor,
    ):
        self._user_command_gateway = user_command_gateway
        self._cached_current_user: UserModel | None = None
        self._http_bearer = http_bearer
        self._token_processor = token_processor

    async def get_current_user(self) -> UserModel:

        token_data: JwtTokenData = self._token_processor.decode_auth_token(
            self._http_bearer.credentials
        )
        if not token_data.is_success:
            raise AuthenticationError(
                token_data.error_msg,
            )

        if self._cached_current_user is not None:
            return self._cached_current_user

        user: UserModel | None = await self._user_command_gateway.read_by_id(
            int(token_data.payload.get("sub", 0))
        )
        if user is None:
            raise AuthenticationError(AUTH_NOT_AUTHENTICATED)
        self._cached_current_user = user
        return user
