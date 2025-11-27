from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from pypdf import PdfReader

from .base import BaseParser
from .models import ParsedDocument
from .utils import normalize_text


class PdfParser(BaseParser):
    """
    Парсер PDF-файлов.
    Работает с текстовыми PDF.
    Для сканов понадобится OCR (потом).
    """

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".pdf"

    def parse(self, path: Path) -> ParsedDocument:
        if not path.exists():
            raise FileNotFoundError(path)

        reader = PdfReader(str(path))
        pages_text: List[str] = []

        for page in reader.pages:
            try:
                extracted = page.extract_text() or ""
            except Exception:
                extracted = ""
            pages_text.append(extracted)

        text = "\n".join(pages_text)

        stat = path.stat()
        metadata: Dict[str, str] = {
            "file_name": path.name,
            "absolute_path": str(path.resolve()),
            "size_bytes": str(stat.st_size),
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "content_type": "application/pdf",
            "pages": str(len(reader.pages)),
        }

        return ParsedDocument(
            id=str(path.resolve()),
            raw_text=normalize_text(text),
            metadata=metadata,
        )
