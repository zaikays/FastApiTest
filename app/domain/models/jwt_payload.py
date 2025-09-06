from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.token_type import TokenType
from app.domain.enums.user_role import UserRole


@dataclass(eq=False, kw_only=True)
class AuthJwtPayload:
    sub: int
    role: UserRole
    expiration: datetime
    type: TokenType = TokenType.ACCESS
