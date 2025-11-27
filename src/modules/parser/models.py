from typing import Dict

from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):

    id: str
    raw_text: str
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Метаданные файла (имя, размер, даты и т.п.)",
    )
