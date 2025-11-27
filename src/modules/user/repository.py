from src.modules.user.models import User


class UserRepository:
    def __init__(self, session):
        self.__session = session

    def check_email_exists(self, email: str) -> bool:
        pass

    def get_user_by_id(self, user_id: int) -> User:
        pass

    def get_user_by_email(self, email: str) -> User:
        pass

    def get_user_by_fullname(self, full_name: str) -> User:
        pass

    def create_user(
            self,
            full_name: str,
            email: str,
            password: str,
            organization_name: str,
            position: str,
            department: str
    ) -> User:
        # Пароль уже зашифрован. Думаю делать шифрование в контроллере или в service
        pass

    def update_user(
            self,
            user_id: int,
            full_name: str,
            email: str,
            password: str,
            organization_name: str,
            position: str,
            department: str,
    ) -> User:
        pass

    def delete_user(self, user_id) -> None:
        pass
