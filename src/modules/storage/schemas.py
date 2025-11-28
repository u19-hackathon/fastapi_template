from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from src.modules.storage.models import PriorityLevel, ConfidentialityLevel


class FileUploadDTO(BaseModel):
    title: str


class FileResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    file_path: str
    file_type: str
    file_hash: Optional[str] = None
    upload_date: datetime
    first_lines: str
    last_modified: datetime

    # Вложенные объекты
    category: 'CategoryResponseDTO'
    source: 'SourceResponseDTO'
    tags: List['TagResponseDTO'] = []


class CategoryResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category_name: str
    priority_level: str
    confidentiality: str


class SourceResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    source_name: str


class TagResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tag_name: str


class CategoryCreateDTO(BaseModel):
    file_id: int
    priority_level: Optional[PriorityLevel] = None
    confidentiality: Optional[ConfidentialityLevel] = None
    description: str


class TagBase(BaseModel):
    tag_name: str
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int
    tag_type: str
    created_at: datetime

    class Config:
        from_attributes = True
