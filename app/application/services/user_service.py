from app.adapters.models.user_model import UserModel

from app.domain.enums.user_role import UserRole

from app.domain.models.value_objects.email.email import Email
from app.domain.models.value_objects.raw_password.raw_password import RawPassword
from app.domain.services.password_hasher import PasswordHasher


class UserService:
    def __init__(
        self,
        password_hasher: PasswordHasher,
    ):
        self._password_hasher = password_hasher

    def create_user(self, email: Email, password: RawPassword) -> UserModel:
        hashed_password = self._password_hasher.hash(raw_password=password)
        return UserModel(
            email=email.value,
            password_hash=hashed_password,
            is_active=True,
            role=UserRole.USER,
        )
