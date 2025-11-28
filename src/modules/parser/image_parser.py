# from __future__ import annotations
#
# from datetime import datetime
# from pathlib import Path
# from typing import Dict
#
# from PIL import Image
# import easyocr
#
# from .base import BaseParser
# from .models import ParsedDocument
# from .utils import normalize_text
#
#
# class ImageParser(BaseParser):
#     """
#     Парсер изображений: JPG, PNG, BMP.
#     Выполняет OCR напрямую с изображения без создания PDF.
#     """
#
#     SUPPORTED = {".jpg", ".jpeg", ".png", ".bmp"}
#
#     def __init__(self):
#         self.reader = easyocr.Reader(["en", "ru"])
#
#     def supports(self, path: Path) -> bool:
#         return path.suffix.lower() in self.SUPPORTED
#
#     def parse(self, path: Path) -> ParsedDocument:
#         if not path.exists():
#             raise FileNotFoundError(path)
#
#         # --- 1) OCR напрямую с картинки ---
#         ocr_result = self.reader.readtext(str(path), detail=0)
#         text = "\n".join(ocr_result)
#
#         # --- 2) Метаданные изображения ---
#         stat = path.stat()
#         image = Image.open(path)
#
#         metadata: Dict[str, str] = {
#             "file_name": path.name,
#             "absolute_path": str(path.resolve()),
#             "size_bytes": str(stat.st_size),
#             "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
#             "content_type": "image/" + path.suffix.lower().replace(".", ""),  # image/png
#             "width": str(image.width),
#             "height": str(image.height),
#             "source_format": "image",
#         }
#
#         return ParsedDocument(
#             id=str(path.resolve()),
#             raw_text=normalize_text(text),
#             metadata=metadata,
#         )
