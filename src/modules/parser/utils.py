def normalize_text(text: str) -> str:
    """
    Простейшая нормализация текста:
    - приводим переводы строк к \n
    - убираем пробелы справа
    - удаляем пустые строки в начале/конце
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()
