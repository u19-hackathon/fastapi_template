# внедрение зависимостей, функции провайдеры для этого
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.config import JWT_KEY, JWT_ACCESS_EXPIRATION, JWT_REFRESH_EXPIRATION, JWT_ALGORITHM, FILE_SAVE_BASE_PATH
from fastapi import Depends

from src.modules.analysis import analyze_file
from src.modules.file_save_service.file_save_service import FileSaveService
from src.modules.get_hash import get_file_hash
from src.modules.jwt.services import JWTService
from src.core.security import PasswordManager
from sqlalchemy.orm import Session
from src.core.database import session_maker
from src.modules.parser import ParserRegistry
from src.modules.parser.services import parse_upload_file
from src.modules.storage.repository import StorageRepository
from src.modules.storage.services import StorageService

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
    return UserService(user_repository, _password_manager)


def get_authentication_header(credentials: HTTPAuthorizationCredentials = Depends(_oauth2_scheme)) -> str:
    return credentials.credentials


def get_file_save_service():
    return FileSaveService(FILE_SAVE_BASE_PATH)


def get_storage_repository(session: Session = Depends(get_session)) -> StorageRepository:
    return StorageRepository(session)


def get_analyzer():
    return analyze_file


def get_parser_registry():
    return parse_upload_file


def get_hasher():
    return get_file_hash


def get_storage_service(
        storage_repository: StorageRepository = Depends(get_storage_repository),
        file_save_service: FileSaveService = Depends(get_file_save_service),
        parser_registry: callable = Depends(get_parser_registry),
        file_analyzer: callable = Depends(get_analyzer),
        hasher: callable = Depends(get_hasher)
) -> StorageService:
    return StorageService(storage_repository, file_save_service, parser_registry, file_analyzer, hasher)
