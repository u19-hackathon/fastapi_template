from datetime import datetime, timezone, timedelta
from typing import Any

from jose import JWTError, jwt

from modules.jwt.util import TokenType


class JWTService:
    def __init__(self, key, access_expiration, refresh_expiration, algorithm):
        self.__key = key
        self.__expiration = {
            TokenType.ACCESS: access_expiration,
            TokenType.REFRESH: refresh_expiration
        }
        self.__algorithm = algorithm

    def create_token(self, user_id: int, role: str, token_type: TokenType):
        payload = {
            "type": token_type.value,
            "sub": str(user_id),
            "role": role,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.__expiration[token_type]),
            "iat": datetime.now(timezone.utc),
        }
        encoded_jwt = jwt.encode(payload, self.__key, algorithm=self.__algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict[str, Any] | None:
        try:
            payload = jwt.decode(token, self.__key, algorithms=[self.__algorithm])
            return payload
        except JWTError:
            return None

    def get_credential(self, token, credential_name: str) -> Any | None:
        payload = self.decode_token(token)
        if not payload:
            return None
        return payload.get(credential_name)
