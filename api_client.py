# -*- coding: utf-8 -*-
import requests

from storage import save_to_file

FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]


def get_currency_rate(currency_code: str) -> dict | None:
    response = requests.get(f"https://open.er-api.com/v6/latest/{currency_code}")
    if response.status_code != 200:
        return None
    return response.json()


def update_currency_rates() -> None:
    all_data = {}
    for currency in FAVORITE_CURRENCIES:
        rate = get_currency_rate(currency)
        if rate:
            all_data[currency] = rate
    save_to_file(all_data)
    print("Курсы валют обновлены.")
