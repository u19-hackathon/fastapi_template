from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from .models import ParsedDocument


class BaseParser(ABC):
    """
    Базовый интерфейс для парсеров документов.
    """

    @abstractmethod
    def supports(self, path: Path) -> bool:
        """
        Возвращает True, если парсер умеет работать с таким файлом.
        Например, по расширению или mime-type.
        """
        raise NotImplementedError

    @abstractmethod
    def parse(self, path: Path) -> ParsedDocument:
        """
        Парсит указанный файл и возвращает ParsedDocument.
        """
        raise NotImplementedError
