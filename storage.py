# -*- coding: utf-8 -*-
import json
from pathlib import Path

RATES_FILE = Path(__file__).parent / "currency_rates.json"


def load_rates() -> dict | None:
    """Загружает курсы валют из JSON-файла."""
    try:
        with open(RATES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_to_file(data: dict) -> None:
    with open(RATES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
