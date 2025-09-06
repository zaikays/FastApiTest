from app.application.common.ports.flusher import FlusherAsync
from app.application.common.ports.transaction_manager import TransactionManagerAsync
from app.application.common.ports.user_command_gateway import UserCommandGatewayAsync
from app.application.services.user_service import UserService
from app.domain.exceptions.user import EmailAlreadyExistsError
from app.domain.models.value_objects.raw_password.raw_password import RawPassword
from app.domain.models.value_objects.email.email import Email
from app.presentation.dtos.auth import SignUpRequest, SignUpResponse


class SignUpHandler:
    def __init__(
        self,
        user_service: UserService,
        user_command_gateway: UserCommandGatewayAsync,
        flusher: FlusherAsync,
        transaction_manager: TransactionManagerAsync,
    ):
        self._user_command_gateway = user_command_gateway
        self._transaction_manager = transaction_manager
        self._user_service = user_service
        self._flusher = flusher

    async def execute(self, request_data: SignUpRequest) -> SignUpResponse:
        email = Email(request_data.email)
        password = RawPassword(request_data.password)

        user = self._user_service.create_user(email, password)

        await self._user_command_gateway.add(user)
        try:
            await self._flusher.flush()
        except EmailAlreadyExistsError:
            raise
        await self._transaction_manager.commit()
        return SignUpResponse(
            id=user.id,
            email=user.email,
        )
