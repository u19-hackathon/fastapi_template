# внедрение зависимостей, функции провайдеры для этого
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.config import JWT_KEY, JWT_ACCESS_EXPIRATION, JWT_REFRESH_EXPIRATION, JWT_ALGORITHM
from fastapi import Depends
from src.modules.jwt.service import JWTService
from src.core.security import PasswordManager
from sqlalchemy.orm import Session
from src.core.database import session_maker

from src.modules.user.repository import UserRepository
from src.modules.user.services import UserService

_password_manager = PasswordManager()
_jwt_service = JWTService(JWT_KEY, JWT_ACCESS_EXPIRATION, JWT_REFRESH_EXPIRATION, JWT_ALGORITHM)
_oauth2_scheme = HTTPBearer()


def get_password_manager() -> PasswordManager:
    return _password_manager


def get_session() -> Session:
    db = session_maker()
    try:
        return db
    except Exception:
        db.close()
        raise


def get_jwt_service() -> JWTService:
    return _jwt_service


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


def get_authentication_header(credentials: HTTPAuthorizationCredentials = Depends(_oauth2_scheme)) -> str:
    return credentials.credentials
