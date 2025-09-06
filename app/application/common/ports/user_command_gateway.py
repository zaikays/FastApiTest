from abc import abstractmethod
from typing import Protocol

from app.adapters.models.user_model import UserModel
from app.domain.models.value_objects.email.email import Email


class UserCommandGatewayAsync(Protocol):
    @abstractmethod
    async def add(self, user: UserModel) -> None: ...

    @abstractmethod
    async def read_by_id(self, user_id: int) -> UserModel | None: ...

    @abstractmethod
    async def read_by_email(
        self,
        email: Email,
        for_update: bool = False,
    ) -> UserModel | None: ...
