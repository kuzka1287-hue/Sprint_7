# test_create_courier.py
import allure
import pytest
import requests
from urls import BASE_URL, COURIER

@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно создать (позитивный сценарий)')
    def test_create_courier_success(self, create_courier):
        resp = create_courier["response"]
        assert resp.status_code == 201
        assert resp.json() == {"ok": True}

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self, create_courier):
        login = create_courier["login"]
        password = create_courier["password"]
        first_name = create_courier["first_name"]
        payload = {"login": login, "password": password, "firstName": first_name}
        with allure.step("Попытка создать курьера с уже существующим логином"):
            response = requests.post(f'{BASE_URL}{COURIER}', data=payload)
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется"

    @allure.title('Для создания курьера нужно передать все обязательные поля')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        login = "test_login"
        password = "test_pass"
        first_name = "test_name"
        payload = {"login": login, "password": password, "firstName": first_name}
        del payload[missing_field]
        with allure.step(f"Запрос без поля {missing_field}"):
            response = requests.post(f'{BASE_URL}{COURIER}', data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title('Запрос возвращает правильный код ответа и ok=true')
    def test_create_courier_returns_ok(self, create_courier):
        resp = create_courier["response"]
        assert resp.status_code == 201
        assert resp.json() == {"ok": True}
