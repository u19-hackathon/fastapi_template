from __future__ import annotations

import re
from typing import Any, Dict, List


DATE_PATTERN = re.compile(
    r"\b(\d{1,2}[.\-]\d{1,2}[.\-]\d{2,4})\b"
)

NUMBER_PATTERN = re.compile(
    r"(?:ДОГОВОР|Договор|Номер договора|№)\s*[:№]?\s*([A-Za-zА-Яа-я0-9/\-]+)"
)

AMOUNT_PATTERN = re.compile(
    r"(?:(?:сумма|итого к оплате|итого|стоимость|сумма договора)\s*[:\-]?\s*)?"
    r"(\d{1,3}(?:[\s ]\d{3})*(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"
)

ORG_PATTERN = re.compile(
    r"\b(ООО|АО|ПАО|ЗАО|ИП)\s*[«\"]?([A-Za-zА-Яа-я0-9\s\.\-]+?)[»\"]?(?=[\s,.]|$)"
)


def _extract_date(text: str) -> str | None:
    match = DATE_PATTERN.search(text)
    if not match:
        return None
    return match.group(1)


def _extract_number(text: str) -> str | None:
    match = NUMBER_PATTERN.search(text)
    if not match:
        return None
    return match.group(1)


def _extract_amount(text: str) -> float | None:
    """
    Пытаемся найти сумму. Сначала ищем суммы рядом со словами "итого", "сумма" и т.п.,
    иначе берём самое крупное число, похожее на сумму.
    """
    candidates: List[float] = []

    for m in AMOUNT_PATTERN.finditer(text):
        raw = m.group(1)
        # убираем пробелы-разделители тысяч
        normalized = raw.replace(" ", "").replace(" ", "")
        # заменяем запятую на точку
        normalized = normalized.replace(",", ".")
        try:
            value = float(normalized)
        except ValueError:
            continue

        # отбрасываем заведомо странные маленькие числа
        if value <= 0:
            continue
        candidates.append(value)

    if not candidates:
        return None

    # берём максимальную найденную сумму - часто это сумма договора / итого
    return max(candidates)


def _extract_organizations(text: str, limit: int = 5) -> List[str]:
    orgs: List[str] = []

    for m in ORG_PATTERN.finditer(text):
        form = m.group(1)
        name = m.group(2).strip()
        full = f"{form} «{name}»"
        if full not in orgs:
            orgs.append(full)
        if len(orgs) >= limit:
            break

    return orgs


def extract_fields_from_text(text: str) -> Dict[str, Any]:
    """
    Извлекает структурированные поля из текста договора:
    - date
    - number
    - total_amount
    - organizations (список)
    """

    fields: Dict[str, Any] = {}

    date = _extract_date(text)
    if date:
        fields["date"] = date

    number = _extract_number(text)
    if number:
        fields["number"] = number

    amount = _extract_amount(text)
    if amount is not None:
        fields["total_amount"] = amount

    orgs = _extract_organizations(text)
    if orgs:
        fields["organizations"] = orgs

    return fields
