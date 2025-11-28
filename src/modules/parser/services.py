from __future__ import annotations

from pathlib import Path
from typing import List, Sequence

from .base import BaseParser
from .models import ParsedDocument
from .txt_parser import TxtParser
from .docx_parser import DocxParser
from .pdf_parser import PdfParser
# from .image_parser import ImageParser
from .rtf_parser import RtfParser  # <-- обязательно импортируем здесь


class ParserRegistry:
    """
    Реестр парсеров. Хранит список всех парсеров и выбирает подходящий под файл.
    """

    def __init__(self, parsers: Sequence[BaseParser] | None = None) -> None:
        if parsers is None:
            parsers = [
                TxtParser(),
                DocxParser(),
                PdfParser(),
                # ImageParser(),
                RtfParser(),
                # Добавляем парсер изображений
            ]
        self._parsers: List[BaseParser] = list(parsers)

    def register(self, parser: BaseParser) -> None:
        """
        Позволяет динамически добавлять новые парсеры.
        """
        self._parsers.append(parser)

    def parse(self, path: Path) -> ParsedDocument:
        """
        Подбирает и вызывает нужный парсер.
        """
        for parser in self._parsers:
            if parser.supports(path):
                return parser.parse(path)

        raise ValueError(f"Нет подходящего парсера для файла: {path}")


# Singleton-экземпляр реестра, используется в parse_file()
_registry = ParserRegistry()


def parse_file(path: str | Path) -> ParsedDocument:
    """
    Главная точка входа: принимает путь к файлу и возвращает ParsedDocument.
    Этот метод будет использоваться модулем анализа.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    return _registry.parse(p)
