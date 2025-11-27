from typing import List, Optional

from src.modules.user.models import User
from sqlalchemy import select

class UserRepository:
    def __init__(self, session):
        self.__session = session

    def check_email_exists(self, email: str) -> bool:
        """Проверить на существование email в БД"""
        stmt = select(User).where(User.email == email)
        result = self.__session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def check_id_user_exists(self, user_id: int) -> bool:
        """Проверить на существование id в БД"""
        stmt = select(User).where(User.id == user_id)
        result = self.__session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Забрать из БД по айди"""
        user: User = self.__session.get(User, user_id)
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Забрать из БД по email"""
        stmt = select(User).where(User.email == email)
        result = self.__session.execute(stmt)
        user: User = result.scalar_one_or_none()
        return user

    def create_user(
            self,
            full_name: str,
            email: str,
            password: str,
            organization_name: str,
            position: str,
            department: str
    ) -> User:
        """Создаем пользователя в БД"""

        # Пароль уже зашифрован. Думаю делать шифрование в контроллере или в service
        if self.check_email_exists(email):
            raise ValueError(f"Email{email} уже занят")

        user = User(full_name=full_name, email=email, password=password, organization_name=organization_name,
                    position=position, department=department)

        self.__session.add(user)
        self.__session.commit()
        self.__session.refresh(user)

        return user

    def update_user(
            self,
            user_id: int,
            full_name: str | None = None,
            email: str | None = None,
            password: str | None = None,
            organization_name: str | None = None,
            position: str | None = None,
            department: str | None = None,
    ) -> User:
        """Обновляем пользователя в БД"""

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError(f"Пользователя с таким ID {user_id} не существует")

        if email and user.email != email:
            if self.check_email_exists(email):
                raise ValueError(f"Email {email} уже занят")
        else:
            user.email = email

        user.full_name = full_name if full_name and user.full_name != full_name else user.full_name
        user.password = password if password and user.password != password else user.password
        user.organization_name = organization_name if organization_name and user.organization_name != organization_name else user.organization_name
        user.position = position if position and user.position != position else user.position
        user.department = department if department and user.department != department else user.department

        self.__session.commit()
        self.__session.refresh(user)
        return user

    def delete_user(self, user_id) -> None:
        """Удаляем пользователя из БД"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователя с таким ID {user_id} не существует")

        self.__session.delete(user)
        self.__session.commit()


    def get_users_paginated(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Получаем список всех пользователей с пагинацией (skip с какого начать, limit до какого)"""
        stmt = select(User).offset(skip).limit(limit)
        result = self.__session.execute(stmt)
        return result.scalars().all()

    def get_all_users(self) -> List[User]:
        """Получаем список всех пользователей"""
        stmt = select(User)
        result = self.__session.execute(stmt)
        return result.scalars().all()

    def get_all_users_by_organization_name(self, organization_name : str) -> List[User]:
        """Получаем список всех пользователей из одной организации"""
        stmt = select(User).where(User.organization_name == organization_name)
        result = self.__session.execute(stmt)
        return result.scalars().all()

    def get_all_users_by_organization_name_paginated(self, organization_name : str, skip: int = 0, limit: int = 100) -> List[User]:
        """Получаем список всех пользователей из одной организации с пагинацией (skip с какого начать, limit до какого)"""
        stmt = select(User).where(User.organization_name == organization_name).offset(skip).limit(limit)
        result = self.__session.execute(stmt)
        return result.scalars().all()

    def get_all_users_by_position(self, position: str) -> List[User]:
        """Получаем список всех пользователей c одной должностью"""
        stmt = select(User).where(User.position == position)
        result = self.__session.execute(stmt)
        return result.scalars().all()

    def get_all_users_by_position_paginated(self, position: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Получаем список всех пользователей с одной должностью с пагинацией (skip с какого начать, limit до какого)"""
        stmt = select(User).where(User.position == position).offset(skip).limit(limit)
        result = self.__session.execute(stmt)
        return result.scalars().all()


    def get_all_users_by_department(self, department: str) -> List[User]:
        """Получаем список всех пользователей из одного отдела"""
        stmt = select(User).where(User.department == department)
        result = self.__session.execute(stmt)
        return result.scalars().all()

    def get_all_users_by_position_department(self, department: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Получаем список всех пользователей из одного отдела с пагинацией (skip с какого начать, limit до какого)"""
        stmt = select(User).where(User.department == department).offset(skip).limit(limit)
        result = self.__session.execute(stmt)
        return result.scalars().all()



