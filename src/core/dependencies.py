# внедрение зависимостей, функции провайдеры для этого
from security import PasswordManager

_password_manager = PasswordManager()

def get_password_manager() -> PasswordManager:
    return _password_manager
