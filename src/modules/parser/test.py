from __future__ import annotations

from pathlib import Path

from .services import parse_file


def test_one(path: Path) -> None:
    print(f"\n=== ТЕСТ ФАЙЛА: {path.name} ===")
    doc = parse_file(path)
    print("ID:", doc.id)
    print("content_type:", doc.metadata.get("content_type"))
    print("size_bytes:", doc.metadata.get("size_bytes"))
    print("----- FIRST 5 LINES -----")
    lines = doc.raw_text.splitlines()
    for line in lines[:5]:
        print(line)


def main() -> None:
    base_dir = Path(__file__).parent
    docs_dir = base_dir / "test_doc"

    print(f"Папка с тестовыми файлами: {docs_dir}")

    candidates = [
        docs_dir / "example.txt",
        docs_dir / "example.docx",
        docs_dir / "example.pdf",
    ]

    for file_path in candidates:
        if file_path.exists():
            test_one(file_path)
        else:
            print(f"\n--- Файл не найден, пропускаем: {file_path.name} ---")


if __name__ == "__main__":
    main()
