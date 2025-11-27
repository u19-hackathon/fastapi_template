from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

from .base import BaseParser
from .models import ParsedDocument
from .utils import normalize_text


class TxtParser(BaseParser):
    """
    Парсер обычных текстовых файлов (.txt).
    """

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".txt"

    def parse(self, path: Path) -> ParsedDocument:
        if not path.exists():
            raise FileNotFoundError(path)

        text = path.read_text(encoding="utf-8", errors="ignore")

        stat = path.stat()
        metadata: Dict[str, str] = {
            "file_name": path.name,
            "absolute_path": str(path.resolve()),
            "size_bytes": str(stat.st_size),
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "content_type": "text/plain",
        }

        return ParsedDocument(
            id=str(path.resolve()),
            raw_text=normalize_text(text),
            metadata=metadata,
        )
