from fastapi import UploadFile

from src.modules.file_save_service.file_save_service import FileSaveService
from src.modules.parser import ParserRegistry
from src.modules.storage.models import File
from src.modules.storage.repository import StorageRepository


class StorageService:
    def __init__(self,
                 file_repository: StorageRepository,
                 file_save_service: FileSaveService,
                 parser_registry: ParserRegistry,
                 file_analyzer: callable,
                 hasher: callable
                 ):
        self.__storage_repository: StorageRepository = file_repository
        self.__file_save_service: FileSaveService = file_save_service
        self.__parser_registry = parser_registry
        self.__file_analyzer = file_analyzer
        self.__hasher = hasher

    def create_files(self, user_id: int, file_upload: list[UploadFile]):
        """
        Функция для создания нового файла. Идея в том, что именно она будет отсеивать дубликаты,
        так же она будет не только принимать параметры и теги от пользователя, но и через анализатор
        находить новые
        """
        # self.__parser_registry(file_upload)

    def get_list_of_user_files(self, user_id: int, file_type: str, tags: list[str], counterparty: str) -> list[
        File]:
        """
        Функция для получения списка файлов пользователя. Здесь должна быть поддержка фильтров.
        Должна возвращать список dto_response_file
        """
        files = self.__storage_repository.get_files_by_filters(user_id, file_type, tags, counterparty)
        return files

    def delete_file(self, file_id: int) -> None:
        self.__storage_repository.delete_file(file_id)

    def get_file_by_id(self, file_id: int):
        return self.__storage_repository.get_file_by_id(file_id)

    def get_all_types(self):
        return self.__storage_repository.get_all_types()

    def get_all_tags(self):
        return self.__storage_repository.get_all_tags()

    def get_all_counterparty(self):
        return self.__storage_repository.get_all_counterparty()
