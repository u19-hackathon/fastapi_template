from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends
from fastapi import Query

from src.core.dependencies import get_jwt_service, get_storage_service, \
    get_authentication_header
from src.modules.jwt.services import JWTService
from src.modules.storage.schemas import FileResponseDTO
from src.modules.storage.services import StorageService

storage_router = APIRouter(prefix="/api/storage")


@storage_router.get("")
async def get_files(
        file_type: Optional[str] = Query(None),
        tags: Optional[list[str]] = Query(None),
        counterparty: Optional[str] = Query(None),
        user_jwt: str = Depends(get_authentication_header),
        jwt_service: JWTService = Depends(get_jwt_service),
        storage_service: StorageService = Depends(get_storage_service)
) -> list[FileResponseDTO]:
    payload = jwt_service.decode_token(token=user_jwt)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not payload.get("type"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    files = storage_service.get_list_of_user_files(int(user_id), file_type, tags, counterparty)
    files_answer_dto = [FileResponseDTO.model_validate(file) for file in files]
    return files_answer_dto


@storage_router.post("/upload")
async def upload_file(
        jwt_service: JWTService = Depends(get_jwt_service),
        user_jwt: str = Depends(get_authentication_header),
        files: list[UploadFile] = File(...),
        storage_service: StorageService = Depends(get_storage_service)
) -> None:
    payload = jwt_service.decode_token(token=user_jwt)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not payload.get("type"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    files_answer = storage_service.create_files(user_id, files)
    # files_answer_dto = [FileResponseDTO.model_validate(file) for file in files_answer]
    return None


@storage_router.delete("/{file_id}")
async def delete_file(
        file_id: int,
        jwt_service: JWTService = Depends(get_jwt_service),
        user_jwt: str = Depends(get_authentication_header),
        storage_service: StorageService = Depends(get_storage_service)
) -> None:
    payload = jwt_service.decode_token(token=user_jwt)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not payload.get("type"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = int(user_id)
    file = storage_service.get_file_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Not found")
    if file.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    storage_service.delete_file(file_id)
    return None
