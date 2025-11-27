# внедрение зависимостей, функции провайдеры для этого
from security import PasswordManager
from sqlalchemy.orm import Session
from core.database import session_maker

_password_manager = PasswordManager()


def get_password_manager() -> PasswordManager:
    return _password_manager


def get_session() -> Session:
    db = session_maker()
    try:
        return db
    except Exception:
        db.close()
        raise
