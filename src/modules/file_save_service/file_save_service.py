import shutil
from datetime import datetime
from pathlib import Path
from typing import BinaryIO


class FileSaveService:
    def __init__(self, base_storage_path: str = "./files_saved_storage"):
        self.base_storage_path = Path(base_storage_path)
        self.base_storage_path.mkdir(parents=True, exist_ok=True)

    def save_user_file(self, file: BinaryIO, original_filename: str, user_id: int) -> str:
        """Сохраняет файл пользователя на диск в папку user_id
            Возвращает путь к сохраненному файлу для сохранения в БД"""

        # Создаем папку пользователя
        user_folder: Path = self.base_storage_path / str(user_id)
        user_folder.mkdir(exist_ok=True)

        # Получаем расширение файла
        file_extension = Path(original_filename).suffix.lower()

        # Генерируем уникальное имя
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        unique_filename = f"file_{timestamp}{file_extension}"

        # Полный путь к файлу
        file_path = user_folder / unique_filename

        # Копируем файловый объект напрямую на диск
        file.seek(0)
        with open(file_path, 'wb') as destination_file:
            shutil.copyfileobj(file, destination_file)

        return str(file_path)

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Удаляет файл по полному пути"""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
            return False
        except OSError:
            return False
