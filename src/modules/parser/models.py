from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    """
    Результат парсинга файла.
    """

    id: str                                  # уникальный идентификатор (пока путь)
    raw_text: str                            # сырой текст после нормализации
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Метаданные файла (имя, размер, даты и т.п.)",
    )
