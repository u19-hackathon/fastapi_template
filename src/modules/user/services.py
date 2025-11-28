from src.core.security import PasswordManager
from src.modules.user.models import User
from src.modules.user.repository import UserRepository
from src.modules.user.schemas import UserRegisterDTO, UserBaseDTO


class UserService:
    def __init__(self, user_repository: UserRepository, password_manager: PasswordManager):
        self.__user_repository: UserRepository = user_repository
        self.__password_manager = password_manager

    def get_user_by_id(self, user_id: int):
        return self.__user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str):
        return self.__user_repository.get_user_by_email(email)

    def create_user(self, user_dto: UserRegisterDTO):
        # может выбросить ValueException из-за того, что пароль кодируется
        if self.__user_repository.check_email_exists(user_dto.email):
            return None
        user_dto.password = self.__encode_password(user_dto.password)
        return self.__user_repository.create_user(
            full_name=user_dto.full_name,
            email=user_dto.email,
            password=user_dto.password,
            organization_name=user_dto.organization_name,
            position=user_dto.position,
            department=user_dto.department
        )

    def update_user(self, user_dto: UserBaseDTO) -> User | None:
        if not user_dto.id or not self.__user_repository.check_id_user_exists(user_dto.id):
            return None
        return self.__user_repository.update_user(
            user_id=user_dto.id,
            full_name=user_dto.full_name,
            email=user_dto.email,
            password=user_dto.password,
            organization_name=user_dto.organization_name,
            position=user_dto.position,
            department=user_dto.department
        )

    def validate_password(self, plain_password: str, hashed_password: str):
        self.__password_manager.verify_password(plain_password=plain_password, hashed_password=hashed_password)

    def delete_user(self, user_id) -> None:
        self.__user_repository.delete_user(user_id)

    def __encode_password(self, password: str):
        return self.__password_manager.hash_password(password)
