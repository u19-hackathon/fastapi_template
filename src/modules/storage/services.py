from typing import Type, Optional

from fastapi import UploadFile

from src.core.config import MAX_FILE_SIZE
from src.modules.file_save_service.file_save_service import FileSaveService
from src.modules.storage.models import File, SourceType, Tag
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

    async def create_files(self, user_id: int, files_upload: list[UploadFile], tags: list[str]):
        """
        Функция для создания нового файла. Идея в том, что именно она будет отсеивать дубликаты,
        так же она будет не только принимать параметры и теги от пользователя, но и через анализатор
        находить новые
        """
        for file in files_upload:
            await self.create_file(user_id, file, tags)

    async def create_file(self, user_id, file_upload: UploadFile, tags: list[str]):
        if file_upload.size > MAX_FILE_SIZE:
            return

        file_hash = self.__hasher(file_upload)

        if self.__check_hash_exists_for_user(file_hash, user_id):
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

        # parsed_document: ParsedDocument = await self.__parser_registry(file_upload)
        # analyze_result: AnalysisResult = self.__file_analyzer(FileMetadata(
        #     file_id=file.id,
        #     title=file.title,
        #     category_document_type=file.file_type,
        #     priority_level=PriorityLevel.normal,
        #     confidentiality=ConfidentialityLevel.internal
        # ), parsed_document.raw_text, tags)
        # print(analyze_result)
        self.__add_all_tags_to_file(file.id, tags, user_id)

    def __add_all_tags_to_file(self, file_id: int, tags: list[str], user_id: int):
        if not tags: return
        for tag in tags:
            if not tag: continue
            if not self.__check_tag_exists(tag):
                self.create_tag(tag, "manual", "")
            tag_model: Tag = self.__get_tag_id_by_name(tag)
            if tag_model:
                self.add_tag_to_file(file_id, tag_model.id, user_id)

    def __check_hash_exists_for_user(self, file_hash: str, user_id: int):
        return self.__storage_repository.check_hash_exists_for_user(file_hash, user_id)

    def __get_tag_id_by_name(self, tag_name: str):
        return self.__storage_repository.get_tag_by_name(tag_name)

    def add_tag_to_file(self, file_id: int, tag_id: int, assigned_by: Optional[int]):
        self.__storage_repository.add_tag_to_file(file_id, tag_id, assigned_by=assigned_by)

    def __check_source_id_exists(self, source_id: int):
        return self.__storage_repository.check_source_id_exists(source_id)

    def __check_tag_exists(self, tag_name: str):
        return self.__storage_repository.check_tag_exists(tag_name)

    def create_tag(self, tag_name, tag_type: str, description: str):
        return self.__storage_repository.create_tag(tag_name, tag_type, description)

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
