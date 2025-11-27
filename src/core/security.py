from __future__ import annotations

import re
from typing import Final

import bcrypt


class PasswordManager:
    """
    Класс-утилита для безопасной работы с паролями.

    Отвечает за:
    * хеширование паролей (bcrypt с солью);
    * проверку пароля по сохранённому хэшу;
    * базовую проверку "силы" пароля.
    """

    _MAX_BYTES: Final[int] = 72

    def __init__(self, rounds: int = 12) -> None:
        if rounds < 4 or rounds > 31:
            raise ValueError("Параметр 'rounds' для bcrypt должен быть в диапазоне 4..31.")
        self._rounds: int = rounds


    def hash_password(self, password: str) -> str:
        """
        Хеширует пароль для безопасного хранения в базе данных.

        Перед хешированием:
        * выполняется проверка сложности пароля;
        * проверяется ограничение bcrypt по длине (72 байта).

        Возвращаемая строка уже содержит:
        * алгоритм;
        * соль;
        * сам хэш.

        :param password: исходный пароль в виде строки.
        :return: строка-хэш, которую можно безопасно хранить в БД.
        :raises ValueError: если пароль не соответствует требованиям.
        """
        self.validate_strength(password)

        # bcrypt работает с bytes
        password_bytes = password.encode("utf-8")

        if len(password_bytes) > self._MAX_BYTES:
            # Теоретически сюда не дойдём из-за validate_strength,
            # но дополнительная защита не повредит.
            raise ValueError(
                "Пароль слишком длинный для безопасного хеширования (bcrypt > 72 байт)."
            )

        salt = bcrypt.gensalt(rounds=self._rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, соответствует ли введённый пароль сохранённому хэшу.

        :param plain_password: пароль, который ввёл пользователь.
        :param hashed_password: хэш пароля из базы данных
                                (то, что вернул hash_password()).
        :return: True, если пароль верный, иначе False.
        """
        if not hashed_password:
            return False

        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                hashed_password.encode("utf-8"),
            )
        except ValueError:
            # Если строка в БД не похожа на корректный bcrypt-хэш
            return False

    def validate_strength(self, password: str) -> None:
        """
        Проверяет пароль.

        Требования:
        * минимум 8 символов;
        * максимум ~50 символов (чтобы не упереться в ограничение bcrypt по 72 байтам);
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

        if len(password.encode("utf-8")) > self._MAX_BYTES:
            raise ValueError(
                "Пароль слишком длинный для безопасного хеширования (bcrypt ограничен 72 байтами). "
                "Используйте не больше ~50 обычных символов и избегайте большого количества эмодзи."
            )
