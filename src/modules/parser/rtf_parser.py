from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

from striprtf.striprtf import rtf_to_text

from .base import BaseParser
from .models import ParsedDocument
from .utils import normalize_text


class RtfParser(BaseParser):
    """
    Парсер RTF-файлов (.rtf)
    """

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".rtf"

    def parse(self, path: Path) -> ParsedDocument:
        if not path.exists():
            raise FileNotFoundError(path)

        # --- Читаем текст из RTF ---
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            rtf_content = f.read()

        text = rtf_to_text(rtf_content)

        # --- Метаданные ---
        stat = path.stat()
        metadata: Dict[str, str] = {
            "file_name": path.name,
            "absolute_path": str(path.resolve()),
            "size_bytes": str(stat.st_size),
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "content_type": "application/rtf",
            "source_format": "rtf",
        }

        return ParsedDocument(
            id=str(path.resolve()),
            raw_text=normalize_text(text),
            metadata=metadata,
        )
