from __future__ import annotations

import tempfile
from pathlib import Path
from typing import List, Sequence

from fastapi import UploadFile

from .base import BaseParser
from .docx_parser import DocxParser
from .models import ParsedDocument
from .pdf_parser import PdfParser
# from .image_parser import ImageParser
from .rtf_parser import RtfParser
from .txt_parser import TxtParser


# from .image_parser import ImageParser


class ParserRegistry:
    def __init__(self, parsers: Sequence[BaseParser] | None = None) -> None:
        if parsers is None:
            parsers = [
                TxtParser(),
                DocxParser(),
                PdfParser(),
                # ImageParser(),
                RtfParser(),
            ]
        self._parsers: List[BaseParser] = list(parsers)

    def register(self, parser: BaseParser) -> None:
        self._parsers.append(parser)

    def parse(self, path: Path) -> ParsedDocument:
        for parser in self._parsers:
            if parser.supports(path):
                return parser.parse(path)
        raise ValueError(f"Нет подходящего парсера для файла: {path}")


_registry = ParserRegistry()


# -------------------- parse_file --------------------

def parse_file(path: str | Path) -> ParsedDocument:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    return _registry.parse(p)


# -------------------- parse_upload_file --------------------

async def _copy_upload_to_temp(upload: UploadFile) -> Path:
    suffix = Path(upload.filename).suffix if upload.filename else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            tmp.write(chunk)
        temp_path = Path(tmp.name)
    await upload.seek(0)
    return temp_path


async def parse_upload_file(upload: UploadFile) -> ParsedDocument:
    tmp_path = await _copy_upload_to_temp(upload)

    try:
        doc = _registry.parse(tmp_path)

        if upload.filename:
            doc.metadata.setdefault("original_filename", upload.filename)

        content_type = getattr(upload, "content_type", None)
        if content_type:
            doc.metadata.setdefault("upload_content_type", content_type)

        size = getattr(upload, "size", None)
        if size is not None:
            doc.metadata.setdefault("upload_size_bytes", str(size))

        return doc

    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass
