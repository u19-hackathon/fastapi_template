# внедрение зависимостей, функции провайдеры для этого
from core.config import JWT_KEY, JWT_ACCESS_EXPIRATION, JWT_REFRESH_EXPIRATION, JWT_ALGORITHM
from modules.jwt.service import JWTService
from core.security import PasswordManager
from sqlalchemy.orm import Session
from core.database import session_maker

_password_manager = PasswordManager()
_jwt_service = JWTService(JWT_KEY, JWT_ACCESS_EXPIRATION, JWT_REFRESH_EXPIRATION, JWT_ALGORITHM)


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
