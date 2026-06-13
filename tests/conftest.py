# conftest.py
import pytest
import requests
import allure
from urls import BASE_URL, COURIER, LOGIN
from data import generate_random_string

@pytest.fixture
def create_courier():
    """Создаёт курьера, возвращает данные и response. После теста удаляет."""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    with allure.step(f"Создание курьера с логином {login}"):
        response = requests.post(f'{BASE_URL}{COURIER}', data=payload)
    yield {
        "login": login,
        "password": password,
        "first_name": first_name,
        "response": response
    }
    # Пост-условие: удаляем курьера, если он создался
    if response.status_code == 201:
        with allure.step(f"Удаление курьера с логином {login}"):
            auth_resp = requests.post(f'{BASE_URL}{LOGIN}', data={"login": login, "password": password})
            if auth_resp.status_code == 200:
                courier_id = auth_resp.json()["id"]
                requests.delete(f'{BASE_URL}{COURIER}/{courier_id}')

@pytest.fixture
def create_order():
    """Фабрика для создания заказа. Принимает список цветов, возвращает track."""
    def _create_order(color_list=None):
        color_list = color_list if color_list is not None else []
        payload = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "address": "Москва",
            "metroStation": 1,
            "phone": "+79998887766",
            "rentTime": 5,
            "deliveryDate": "2025-12-31",
            "comment": "Тест",
            "color": color_list
        }
        with allure.step(f"Создание заказа с цветами {color_list}"):
            response = requests.post(f'{BASE_URL}{ORDERS}', json=payload)
            assert response.status_code == 201, f"Не удалось создать заказ: {response.text}"
        return response.json().get("track")
    return _create_order
