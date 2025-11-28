import hashlib
from fastapi import UploadFile


def get_file_hash(file: UploadFile, algorithm: str = "sha256") -> str:
    """
    Возвращает хэш по метаданным UploadFile:
      - имени файла (filename)
      - MIME-типу (content_type)
      - размеру (size)

    Содержимое файла НЕ учитывается.
    """

    filename = file.filename or ""
    content_type = file.content_type or ""
    size = getattr(file, "size", 0) or 0

    # Собираем строку вида:
    # "contract.pdf|application/pdf|123456"
    meta_string = f"{filename}|{content_type}|{size}"

    hasher = hashlib.new(algorithm)
    hasher.update(meta_string.encode("utf-8"))

    return hasher.hexdigest()
