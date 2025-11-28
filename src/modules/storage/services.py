from src.modules.file_save_service.file_save_service import FileSaveService
from src.modules.parser import ParserRegistry
from src.modules.storage.repository import StorageRepository
from src.modules.storage.schemas import FileUploadDTO, FileResponseDTO


class StorageService:
    def __init__(self,
                 file_repository: StorageRepository,
                 file_save_service: FileSaveService,
                 parser_registry: ParserRegistry,
                 file_analyzer: callable,
                 hasher: callable
                 ):
        self.__file_repository: StorageRepository = file_repository
        self.__file_save_service: FileSaveService = file_save_service
        self.__parser_registry = parser_registry
        self.__file_analyzer = file_analyzer
        self.__hasher = hasher

    def create_file(self, file_upload_dto: FileUploadDTO, user_id: int):
        """
        Функция для создания нового файла. Идея в том, что именно она будет отсеивать дубликаты,
        так же она будет не только принимать параметры и теги от пользователя, но и через анализатор
        находить новые
        """
        pass

    def get_list_of_user_files(self, ) -> list[FileResponseDTO]:
        """
        Функция для получения списка файлов пользователя. Здесь должна быть поддержка фильтров.
        Должна возвращать список dto_response_file
        """
        pass
