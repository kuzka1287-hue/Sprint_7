# conftest.py
import pytest
import requests
from data import BASE_URL, register_new_courier_and_return_login_password

@pytest.fixture
def create_courier():
    """Создаёт курьера и возвращает его данные (login, password, first_name). После теста удаляет."""
    creds = register_new_courier_and_return_login_password()
    if creds is None:
        pytest.skip("Не удалось создать курьера для теста")
    login, password, first_name = creds
    yield {"login": login, "password": password, "firstName": first_name}
    # Удаление курьера после теста (нужен id)
    # Сначала получаем id через логин
    auth_resp = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
    if auth_resp.status_code == 200:
        courier_id = auth_resp.json().get("id")
        if courier_id:
            requests.delete(f'{BASE_URL}/courier/{courier_id}')

@pytest.fixture
def create_order():
    """Создаёт заказ с заданными цветами (по умолчанию без цвета) и возвращает track."""
    def _create_order(color_list=None):
        payload = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "address": "Москва",
            "metroStation": 1,
            "phone": "+79998887766",
            "rentTime": 5,
            "deliveryDate": "2025-12-31",
            "comment": "Тест",
            "color": color_list if color_list else []
        }
        response = requests.post(f'{BASE_URL}/orders', json=payload)
        assert response.status_code == 201, f"Не удалось создать заказ: {response.text}"
        return response.json().get("track")
    return _create_order