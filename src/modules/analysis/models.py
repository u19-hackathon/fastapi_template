from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PriorityLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class ConfidentialityLevel(str, Enum):
    OPEN = "open"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    STRICTLY_CONFIDENTIAL = "strictly_confidential"


class TagSource(str, Enum):
    MANUAL = "manual"
    AUTO_METADATA = "auto_metadata"
    AUTO_CONTENT = "auto_content"


class TagResult(BaseModel):
    """
    Один тег в результате анализа.
    """

    name: str
    source: TagSource
    reason: Optional[str] = None


class FileMetadata(BaseModel):
    """
    Метаданные файла, которые приходят не из текста, а из БД
    (files + categories + source).
    """

    file_id: int
    title: str
    category_document_type: str
    priority_level: PriorityLevel
    confidentiality: ConfidentialityLevel
    source_type: Optional[str] = None
    file_type: Optional[str] = None


class AnalysisResult(BaseModel):
    """
    Итог анализа файла: ключевые поля + теги.
    """

    file_id: int
    doc_type: str
    fields: Dict[str, Any]
    tags: List[TagResult]
