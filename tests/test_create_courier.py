# test_create_courier.py
import allure
import pytest
import requests
from data import BASE_URL, generate_random_string

@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно создать (позитивный сценарий)')
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f'{BASE_URL}/courier', data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        # Чистим – удаляем созданного курьера
        auth = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
        if auth.status_code == 200:
            courier_id = auth.json()["id"]
            requests.delete(f'{BASE_URL}/courier/{courier_id}')

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        # Первый запрос – успешный
        resp1 = requests.post(f'{BASE_URL}/courier', data=payload)
        assert resp1.status_code == 201
        # Второй запрос с теми же данными – должен вернуть 409 и сообщение
        resp2 = requests.post(f'{BASE_URL}/courier', data=payload)
        assert resp2.status_code == 409
        assert resp2.json()["message"] == "Этот логин уже используется"
        # Чистим
        auth = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
        if auth.status_code == 200:
            courier_id = auth.json()["id"]
            requests.delete(f'{BASE_URL}/courier/{courier_id}')

    @allure.title('Для создания курьера нужно передать все обязательные поля')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        del payload[missing_field]
        response = requests.post(f'{BASE_URL}/courier', data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title('Запрос возвращает правильный код ответа и ok=true')
    def test_create_courier_returns_ok(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f'{BASE_URL}/courier', data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        # Чистка
        auth = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
        if auth.status_code == 200:
            requests.delete(f'{BASE_URL}/courier/{auth.json()["id"]}')