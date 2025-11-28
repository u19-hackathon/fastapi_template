from fastapi import APIRouter, UploadFile, File

storage_router = APIRouter(prefix="/api/storage")


@storage_router.get("")
def get_files(
        file_type: str,
        tags: list[str],
        counterparty: str
):
    pass


@storage_router.post("/upload")
def upload_file(files: list[UploadFile] = File(...)):
    pass
