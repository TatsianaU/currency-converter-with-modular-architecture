# -*- coding: utf-8 -*-
import sys
import io

from storage import save_to_file, read_from_file, is_cache_valid
from api_client import get_currency_rates

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CACHE_PATH = "currency_rate.json"


def get_available_currencies(data: dict) -> list[str]:
    return sorted(data.get("rates", {}).keys())


def convert_currency(amount: float, from_curr: str, to_curr: str, data: dict) -> float | None:
    rates = data.get("rates", {})

    if from_curr not in rates or to_curr not in rates:
        return None

    return amount * rates[to_curr] / rates[from_curr]


def load_or_update(base: str) -> dict | None:
    if is_cache_valid(CACHE_PATH):
        cached = read_from_file(CACHE_PATH)
        if cached and cached.get("base_code") == base:
            print("Используется кэш.")
            return cached

    print("Обновление данных с API...")
    fresh = get_currency_rates(base)
    if fresh:
        save_to_file(fresh, CACHE_PATH)
    return fresh


def main() -> None:
    base = input("Введите базовую валюту (например, USD): ").strip().upper()

    data = load_or_update(base)
    if not data:
        return

    print("\nКурсы для RUB, EUR, GBP:")
    for code in ["RUB", "EUR", "GBP"]:
        rate = data["rates"].get(code)
        if rate:
            print(f"{code}: {rate}")

    while True:
        print("\n1. Конвертировать сумму")
        print("2. Показать все доступные валюты")
        print("3. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "3":
            print("До свидания!")
            break

        if choice == "1":
            amount_str = input("Введите сумму: ").replace(",", ".")
            try:
                amount = float(amount_str)
            except ValueError:
                print("Некорректная сумма.")
                continue

            from_curr = input("Из валюты: ").upper()
            to_curr = input("В валюту: ").upper()

            result = convert_currency(amount, from_curr, to_curr, data)

            if result is None:
                print("Некорректный код валюты.")
            else:
                print(f"Результат: {result:.4f} {to_curr}")

        elif choice == "2":
            currencies = get_available_currencies(data)
            print(", ".join(currencies))

        else:
            print("Неверный выбор.")
