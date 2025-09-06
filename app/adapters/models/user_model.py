from sqlalchemy import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.adapters.models.base import Base
from app.domain.enums.user_role import UserRole


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[bytes] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), default=UserRole.USER, nullable=False
    )
