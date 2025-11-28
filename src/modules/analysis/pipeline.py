from __future__ import annotations

from typing import List, Sequence

from .models import (
    FileMetadata,
    AnalysisResult,
    TagResult,
    TagSource,
)
from .metadata_rules import build_tags_from_metadata
from .content_rules import extract_fields_from_text


def analyze_file(
    meta: FileMetadata,
    text: str,
    manual_tag_names: Sequence[str] | None = None,
) -> AnalysisResult:
    """
    Главная функция анализа: принимает метаданные файла, текст и список ручных тегов.
    Возвращает AnalysisResult.
    """

    if manual_tag_names is None:
        manual_tag_names = []

    # Уберём дубликаты, сохраняя порядок
    manual_tag_names = list(dict.fromkeys(manual_tag_names))

    # Ручные теги
    manual_tags: List[TagResult] = [
        TagResult(name=name, source=TagSource.MANUAL, reason=None)
        for name in manual_tag_names
    ]

    # Авто-теги по метаданным
    auto_meta_tags = build_tags_from_metadata(
        meta,
        existing_manual_tag_names=set(manual_tag_names),
    )

    # Извлечение полей из текста (дата, номер, сумма, организации и т.п.)
    fields = extract_fields_from_text(text)

    all_tags = manual_tags + auto_meta_tags

    return AnalysisResult(
        file_id=meta.file_id,
        doc_type=meta.category_document_type,
        fields=fields,
        tags=all_tags,
    )


def build_metadata_from_db_file(db_file) -> FileMetadata:
    """
    Строит FileMetadata из ORM-объекта File (modules/storage/models.py).
    Не жестко типизировано, чтобы не плодить циклических импортов.
    """

    category = getattr(db_file, "category", None)
    source = getattr(db_file, "source", None)

    # document_type
    doc_type = "unknown"
    if category is not None and getattr(category, "document_type", None):
        doc_type = category.document_type

    # priority_level
    priority = getattr(category, "priority_level", None) if category is not None else None
    if priority is None:
        priority_value = "normal"
    else:
        priority_value = getattr(priority, "value", priority)
    # confidentiality
    confidentiality = getattr(category, "confidentiality", None) if category is not None else None
    if confidentiality is None:
        conf_value = "internal"
    else:
        conf_value = getattr(confidentiality, "value", confidentiality)

    # source_type
    if source is not None:
        st = getattr(source, "source_type", None)
        source_type_value = getattr(st, "value", st)
    else:
        source_type_value = None

    return FileMetadata(
        file_id=db_file.id,
        title=db_file.title,
        category_document_type=doc_type,
        priority_level=priority_value,       # Pydantic сконвертирует в PriorityLevel
        confidentiality=conf_value,          # Pydantic сконвертирует в ConfidentialityLevel
        source_type=source_type_value,
        file_type=getattr(db_file, "file_type", None),
    )


def get_manual_tag_names_from_db_file(db_file) -> list[str]:
    """
    Возвращает список имён ручных тегов, привязанных к файлу через связь file_tags_users.
    """

    tag_names: List[str] = []
    for tag in getattr(db_file, "tags", []):
        tag_type = getattr(tag, "tag_type", None)
        tag_type_value = getattr(tag_type, "value", tag_type)
        if tag_type_value == "manual":
            tag_names.append(tag.tag_name)

    # уберём дубликаты, сохранив порядок
    return list(dict.fromkeys(tag_names))


def analyze_db_file(db_file, parsed_document) -> AnalysisResult:
    """
    Удобная обёртка: принимает ORM-файл и ParsedDocument,
    сам собирает метаданные, ручные теги и вызывает analyze_file().
    """

    meta = build_metadata_from_db_file(db_file)
    manual_tag_names = get_manual_tag_names_from_db_file(db_file)
    text = getattr(parsed_document, "raw_text", str(parsed_document))

    return analyze_file(
        meta=meta,
        text=text,
        manual_tag_names=manual_tag_names,
    )
