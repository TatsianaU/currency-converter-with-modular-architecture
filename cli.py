# -*- coding: utf-8 -*-
import sys
import io

from storage import load_rates
from api_client import update_currency_rates

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]
BASE_CURRENCIES = FAVORITE_CURRENCIES


def get_available_currencies(rates_data: dict) -> list[str]:
    """Возвращает отсортированный список доступных валют."""
    if not rates_data or "USD" not in rates_data:
        return []
    rates = rates_data["USD"].get("rates", rates_data["USD"])
    return sorted(rates.keys())


def convert_currency(
    amount: float, from_currency: str, to_currency: str, rates_data: dict
) -> float | None:
    """Конвертирует amount из from_currency в to_currency."""
    if from_currency == to_currency:
        return amount

    def get_rate(base: str, target: str) -> float | None:
        if base not in rates_data:
            return None
        rates = rates_data[base].get("rates", rates_data[base])
        return rates.get(target)

    if from_currency in BASE_CURRENCIES:
        rate = get_rate(from_currency, to_currency)
        if rate is not None:
            return amount * rate

    if to_currency in BASE_CURRENCIES:
        rate = get_rate(to_currency, from_currency)
        if rate is not None and rate != 0:
            return amount / rate

    usd_rates = rates_data.get("USD", {}).get("rates", rates_data.get("USD", {}))
    if from_currency in usd_rates and to_currency in usd_rates:
        return amount * usd_rates[to_currency] / usd_rates[from_currency]

    return None


def display_menu() -> None:
    print("\n=== Конвертер валют ===")
    print("1. Конвертировать валюту")
    print("2. Показать доступные валюты")
    print("3. Обновить курсы валют")
    print("4. Выход")


def main() -> None:
    while True:
        display_menu()
        choice = input("Выберите действие (1-4): ").strip()

        if choice == "4":
            print("До свидания!")
            break

        if choice == "1":
            rates_data = load_rates()
            if not rates_data:
                print("Ошибка: не удалось загрузить курсы. Выберите пункт 3 для обновления.")
                continue

            amount_str = input("Введите сумму: ").strip().replace(",", ".")
            try:
                amount = float(amount_str)
            except ValueError:
                print("Ошибка: введите корректную сумму.")
                continue

            currencies = get_available_currencies(rates_data)
            print(f"Доступные валюты: {', '.join(currencies)}")

            from_curr = input("Введите исходную валюту (например, USD): ").strip().upper()
            to_curr = input("Введите целевую валюту (например, EUR): ").strip().upper()

            if from_curr not in currencies or to_curr not in currencies:
                print("Ошибка: валюта не найдена.")
                continue

            result = convert_currency(amount, from_curr, to_curr, rates_data)
            if result is not None:
                print(f"Результат: {result:.4f} {to_curr}")
            else:
                print("Ошибка конвертации.")

        elif choice == "2":
            rates_data = load_rates()
            if not rates_data:
                print("Ошибка: не удалось загрузить курсы. Выберите пункт 3 для обновления.")
                continue
            currencies = get_available_currencies(rates_data)
            print(f"Доступные валюты: {', '.join(currencies)}")

        elif choice == "3":
            update_currency_rates()

        else:
            print("Неверный выбор. Введите число от 1 до 4.")


if __name__ == "__main__":
    main()
