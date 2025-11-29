from typing import Type

from fastapi import UploadFile

from src.core.config import MAX_FILE_SIZE
from src.modules.analysis import FileMetadata
from src.modules.file_save_service.file_save_service import FileSaveService
from src.modules.parser import ParsedDocument
from src.modules.storage.models import File, PriorityLevel, ConfidentialityLevel, SourceType
from src.modules.storage.repository import StorageRepository


class StorageService:
    def __init__(self,
                 file_repository: StorageRepository,
                 file_save_service: FileSaveService,
                 parser_registry: callable,
                 file_analyzer: callable,
                 hasher: callable
                 ):
        self.__storage_repository: StorageRepository = file_repository
        self.__file_save_service: FileSaveService = file_save_service
        self.__parser_registry = parser_registry
        self.__file_analyzer = file_analyzer
        self.__hasher = hasher

    def create_files(self, user_id: int, files_upload: list[UploadFile]):
        """
        Функция для создания нового файла. Идея в том, что именно она будет отсеивать дубликаты,
        так же она будет не только принимать параметры и теги от пользователя, но и через анализатор
        находить новые
        """
        for file in files_upload:
            self.create_file(user_id, file)

    def create_file(self, user_id, file_upload: UploadFile):
        if file_upload.size > MAX_FILE_SIZE:
            return

        file_hash = self.__hasher(file_upload)

        if self.__storage_repository.check_hash_exists(file_hash):
            return

        # пробую сохранять на диске и в бд
        if not self.__check_category_exists(file_upload.content_type):
            self.create_category(file_upload.content_type, file_upload.content_type)

        if not self.__check_source_id_exists(1):
            self.create_source("base", SourceType.website)

        file_path = self.__file_save_service.save_user_file(file_upload.file, file_upload.filename, user_id)
        file = self.__storage_repository.create_file(file_upload.filename, file_path, file_upload.size,
                                                     file_upload.content_type, file_hash, user_id,
                                                     self.get_category_id_by_name(file_upload.content_type), 1, None)

        parsed_document: ParsedDocument = self.__parser_registry(file_upload)
        analyze_result = self.__file_analyzer(FileMetadata(
            file_id=file.id,
            title=file.title,
            category_document_type=file.file_type,
            priority_level=PriorityLevel.normal,
            confidentiality=ConfidentialityLevel.internal
        ), parsed_document)
        print("Result!!!" + str(analyze_result))

    def __check_hash_exists(self, file_hash: str):
        return self.__storage_repository.check_hash_exists(file_hash)

    def __check_source_id_exists(self, source_id: int):
        return self.__storage_repository.check_source_id_exists(source_id)

    def __check_category_exists(self, file_category: str):
        return self.__storage_repository.check_category_exists(file_category)

    def get_category_id_by_name(self, category_name: str):
        return self.__storage_repository.get_category_id_by_name(category_name)

    def create_category(self, category_name, document_type):
        self.__storage_repository.create_category(category_name, document_type)

    def create_source(self, source_name, source_type: SourceType):
        self.__storage_repository.create_source(source_name, source_type)

    def get_list_of_user_files(self, user_id: int, file_type: str, tags: list[str], counterparty: str) -> list[
        Type[File]]:
        """
        Функция для получения списка файлов пользователя. Здесь должна быть поддержка фильтров.
        Должна возвращать список dto_response_file
        """
        files = self.__storage_repository.get_files_by_filters(user_id, file_type, tags, counterparty)
        return files

    def delete_file(self, file_id: int, file_path: str) -> None:
        self.__file_save_service.delete_file(file_path)
        self.__storage_repository.delete_file(file_id)

    def get_file_by_id(self, file_id: int):
        return self.__storage_repository.get_file_by_id(file_id)

    def get_file_path(self, file_id: int):
        return self.__storage_repository.get_file_path(file_id)

    def get_all_types(self):
        return self.__storage_repository.get_all_types()

    def get_all_tags(self):
        return self.__storage_repository.get_all_tags()

    def get_all_counterparty(self):
        return self.__storage_repository.get_all_counterparty()
