import base64
import hashlib
import hmac
from typing import NewType

import bcrypt

from app.domain.models.value_objects.raw_password.raw_password import RawPassword
from app.domain.services.password_hasher import PasswordHasher

PasswordPepper = NewType("PasswordPepper", str)


class BcryptHasher(PasswordHasher):

    def __init__(self, pepper: PasswordPepper):
        self._pepper = pepper

    def hash(self, raw_password: RawPassword) -> bytes:
        base64_hmac_password: bytes = self._add_pepper(raw_password, self._pepper)
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(base64_hmac_password, salt)

    @staticmethod
    def _add_pepper(raw_password: RawPassword, pepper: PasswordPepper) -> bytes:
        hmac_password: bytes = hmac.new(
            key=pepper.encode(),
            msg=raw_password.value.encode(),
            digestmod=hashlib.sha256,
        ).digest()
        return base64.b64encode(hmac_password)

    def verify(self, *, raw_password: RawPassword, hashed_password: bytes) -> bool:
        base64_hmac_password: bytes = self._add_pepper(raw_password, self._pepper)
        return bcrypt.checkpw(base64_hmac_password, hashed_password)
