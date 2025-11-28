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
def get_files(
        file_type: Optional[str] = Query(None),
        tags: Optional[list[str]] = Query(None),
        counterparty: Optional[str] = Query(None),
        user_jwt: str = Depends(get_authentication_header),
        jwt_service: JWTService = Depends(get_jwt_service),
        storage_service: StorageService = Depends(get_storage_service)
):
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
    return files


@storage_router.post("/upload")
def upload_file(
        jwt_service: JWTService = Depends(get_jwt_service),
        user_jwt: str = Depends(get_authentication_header),
        files: list[UploadFile] = File(...),
        storage_service: StorageService = Depends(get_storage_service)
):
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
    files_answer_dto = [FileResponseDTO.model_validate(file) for file in files_answer]
    return files_answer_dto
