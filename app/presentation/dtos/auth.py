from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthUserCredentials:
    email: str
    password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class SignUpRequest(AuthUserCredentials):
    pass


class SignUpResponse(TypedDict):
    id: int
    email: str


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginRequest(AuthUserCredentials):
    pass


class LoginResponse(TypedDict):
    token: str
    refresh_token: str
