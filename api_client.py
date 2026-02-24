# -*- coding: utf-8 -*-
import requests


def get_currency_rates(base: str) -> dict | None:
    """
    Делает GET-запрос к open.er-api.com и возвращает dict.
    """
    url = f"https://open.er-api.com/v6/latest/{base}"

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        print("Ошибка сети. Проверьте подключение к интернету.")
        return None

    if response.status_code != 200:
        print(f"Ошибка API: статус {response.status_code}")
        return None

    data = response.json()

    if data.get("result") != "success":
        print("Ошибка API: некорректный ответ сервера.")
        return None

    return data
