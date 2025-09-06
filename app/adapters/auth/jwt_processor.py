import logging
import jwt
from dataclasses import dataclass
from typing import Any, Literal, NewType, TypedDict, cast, Optional


from app.domain.enums.token_type import TokenType
from app.presentation.controllers.auth.constants import (
    ACCESS_TOKEN_INVALID_OR_EXPIRED,
    ACCESS_TOKEN_PAYLOAD_MISSING,
    ACCESS_TOKEN_PAYLOAD_OF_INTEREST,
    ACCESS_TOKEN_TYPE_INVALID,
)

from app.domain.models.jwt_payload import AuthJwtPayload

log = logging.getLogger(__name__)

JwtSecret = NewType("JwtSecret", str)
JwtAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]


class JwtPayload(TypedDict):
    sub: str
    role: str
    exp: int
    type: str


@dataclass
class JwtTokenData:
    is_success: bool
    error_msg: Optional[str] = None
    payload: Optional[JwtPayload] = None


class JwtAccessTokenProcessor:
    def __init__(self, secret: JwtSecret, algorithm: JwtAlgorithm):
        self._secret = secret
        self._algorithm = algorithm

    def encode(self, auth_jwt_payload: AuthJwtPayload) -> str:
        payload = JwtPayload(
            sub=str(auth_jwt_payload.sub),
            role=auth_jwt_payload.role,
            exp=int(auth_jwt_payload.expiration.timestamp()),
            type=auth_jwt_payload.type,
        )
        return jwt.encode(
            cast(dict[str, Any], payload),
            key=self._secret,
            algorithm=self._algorithm,
        )

    def decode_auth_token(
        self, token: str, expected_type: TokenType = TokenType.ACCESS
    ) -> JwtTokenData:
        try:
            payload = jwt.decode(
                token,
                key=self._secret,
                algorithms=[self._algorithm],
            )

        except jwt.PyJWTError as error:
            log.debug("%s %s", ACCESS_TOKEN_INVALID_OR_EXPIRED, error)
            return JwtTokenData(
                is_success=False,
                error_msg=ACCESS_TOKEN_INVALID_OR_EXPIRED,
                payload=None,
            )

        token_type = payload.get("type")
        if token_type != expected_type:
            log.debug(
                "%s: expected '%s', got '%s'",
                ACCESS_TOKEN_TYPE_INVALID,
                expected_type,
                token_type,
            )
            return JwtTokenData(
                is_success=False,
                error_msg=ACCESS_TOKEN_TYPE_INVALID,
                payload=None,
            )
        user_id: str | None = payload.get(ACCESS_TOKEN_PAYLOAD_OF_INTEREST)
        if user_id is None:
            log.debug(
                "%s '%s'",
                ACCESS_TOKEN_PAYLOAD_MISSING,
                ACCESS_TOKEN_PAYLOAD_OF_INTEREST,
            )
            return JwtTokenData(
                is_success=False,
                error_msg=ACCESS_TOKEN_PAYLOAD_MISSING,
                payload=None,
            )

        return JwtTokenData(
            is_success=True,
            error_msg=ACCESS_TOKEN_PAYLOAD_MISSING,
            payload=JwtPayload(
                sub=str(user_id),
                role=payload.get("role"),
                exp=int(payload.get("exp")),
                type=payload.get("type"),
            ),
        )
