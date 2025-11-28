from __future__ import annotations

from typing import Iterable, List

from .models import (
    FileMetadata,
    TagResult,
    TagSource,
    PriorityLevel,
    ConfidentialityLevel,
)


def build_tags_from_metadata(
        meta: FileMetadata,
        existing_manual_tag_names: Iterable[str] | None = None,
) -> List[TagResult]:
    """
    Строит список авто-тегов на основе метаданных файла
    (тип документа, приоритет, конфиденциальность).
    """

    existing = {name.lower() for name in (existing_manual_tag_names or [])}
    tags: List[TagResult] = []

    def add_tag(name: str, reason: str) -> None:
        if name.lower() in existing:
            return
        tags.append(
            TagResult(
                name=name,
                source=TagSource.AUTO_METADATA,
                reason=reason,
            )
        )

    doc_type = (meta.category_document_type or "").lower()
    if "договор" in doc_type:
        add_tag("договор", f"Тип документа: {meta.category_document_type}")

    # 2) Приоритет → "срочный"
    if meta.priority_level in {PriorityLevel.HIGH, PriorityLevel.CRITICAL}:
        add_tag("срочный", f"Приоритет: {meta.priority_level.value}")

    # 3) Конфиденциальность → "конфиденциально"
    if meta.confidentiality in {
        ConfidentialityLevel.CONFIDENTIAL,
        ConfidentialityLevel.STRICTLY_CONFIDENTIAL,
    }:
        add_tag(
            "конфиденциально",
            f"Конфиденциальность: {meta.confidentiality.value}",
        )

    return tags
