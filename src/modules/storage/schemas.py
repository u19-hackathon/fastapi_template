from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from modules.storage.models import PriorityLevel, ConfidentialityLevel


class FileUpload(BaseModel):
    title: str


class FileResponse(BaseModel):
    id: int
    title: str
    file_path: str
    file_type: str
    upload_date: datetime
    first_lines: str
    last_modified: datetime
    category_name: str
    source_name: str
    priority_level: PriorityLevel
    confidentiality: ConfidentialityLevel
    tags: List['TagResponse'] = []

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
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