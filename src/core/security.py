
from __future__ import annotations

import re
from typing import Sequence

from passlib.context import CryptContext


class PasswordManager:
    """
    Класс-утилита для работы с паролями.

    Отвечает за:
    * безопасное хеширование паролей (bcrypt через passlib);
    * проверку пароля по сохранённому хэшу;
    * базовую проверку "силы" пароля.
    """

    def __init__(
        self,
        schemes: Sequence[str] | None = None,
        deprecated: str = "auto",
        bcrypt_rounds: int = 12,
    ) -> None:

        if schemes is None:
            schemes = ["bcrypt"]

        self._context = CryptContext(
            schemes=list(schemes),
            deprecated=deprecated,
            bcrypt__rounds=bcrypt_rounds,
        )

    def hash_password(self, password: str) -> str:
        """
        Хеширует пароль для безопасного хранения в базе данных.

        Перед хешированием пароль проходит проверку сложности.
        Возвращаемая строка уже содержит алгоритм, соль и сам хэш.

        :param password: исходный пароль в виде строки.
        :return: строка-хэш, которую можно безопасно хранить в БД.
        :raises ValueError: если пароль не соответствует требованиям.
        """
        self.validate_strength(password)
        return self._context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, соответствует ли введённый пароль сохранённому хэшу.

        :param plain_password: пароль, который ввёл пользователь.
        :param hashed_password: хэш пароля из базы данных.
        :return: True, если пароль верный, иначе False.
        """
        if not hashed_password:
            return False

        return self._context.verify(plain_password, hashed_password)

    def validate_strength(self, password: str) -> None:
        """
        Проверяет базовую "силу" пароля.

        Требования:
        * минимум 8 символов;
        * максимум 50 символов (чтобы не упереться в ограничение bcrypt по 72 байтам);
        * хотя бы одна буква (латиница или кириллица);
        * хотя бы одна цифра;
        * итоговая длина в байтах (UTF-8) не больше 72.

        :param password: проверяемый пароль.
        :raises ValueError: если пароль не соответствует требованиям.
        """

        if len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов.")

        if len(password) > 50:
            raise ValueError("Пароль не должен превышать 50 символов.")

        if not re.search(r"[A-Za-zА-Яа-я]", password):
            raise ValueError("Пароль должен содержать хотя бы одну букву.")

        if not re.search(r"[0-9]", password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")

        if len(password.encode("utf-8")) > 72:
            raise ValueError(
                "Пароль слишком длинный для безопасного хеширования. "
                "Используйте не больше ~50 обычных символов без большого "
                "количества редких символов/эмодзи."
            )
