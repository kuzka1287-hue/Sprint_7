# test_login_courier.py
import allure
import pytest
import requests
from data import BASE_URL, generate_random_string

@allure.feature('Логин курьера')
class TestLoginCourier:

    @allure.title('Курьер может авторизоваться')
    def test_courier_login_success(self, create_courier):
        login = create_courier["login"]
        password = create_courier["password"]
        response = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Для авторизации нужно передать все обязательные поля')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, create_courier, missing_field):
        login = create_courier["login"]
        password = create_courier["password"]
        payload = {"login": login, "password": password}
        del payload[missing_field]
        response = requests.post(f'{BASE_URL}/courier/login', data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Ошибка при неправильном логине или пароле')
    def test_login_wrong_credentials(self, create_courier):
        login = create_courier["login"]
        # Неправильный пароль
        response = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": "wrong"})
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
        # Неправильный логин
        response2 = requests.post(f'{BASE_URL}/courier/login', data={"login": "nonexistent", "password": "pass"})
        assert response2.status_code == 404
        assert response2.json()["message"] == "Учетная запись не найдена"

    @allure.title('Авторизация несуществующего пользователя возвращает ошибку')
    def test_login_nonexistent_user(self):
        random_login = generate_random_string(10)
        random_pass = generate_random_string(10)
        response = requests.post(f'{BASE_URL}/courier/login', data={"login": random_login, "password": random_pass})
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Успешный запрос возвращает id курьера')
    def test_login_returns_id(self, create_courier):
        login = create_courier["login"]
        password = create_courier["password"]
        response = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)