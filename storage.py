# -*- coding: utf-8 -*-
import json
import time
from pathlib import Path

DEFAULT_PATH = Path(__file__).parent / "currency_rate.json"


def save_to_file(data: dict, path=DEFAULT_PATH) -> None:
    """Сохраняет данные в JSON-файл."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_from_file(path=DEFAULT_PATH) -> dict | None:
    """Читает данные из JSON-файла."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def is_cache_valid(path=DEFAULT_PATH, max_age_hours: int = 24) -> bool:
    """Проверяет, моложе ли файл указанного количества часов."""
    if not Path(path).exists():
        return False

    file_age_seconds = time.time() - Path(path).stat().st_mtime
    return file_age_seconds < max_age_hours * 3600
