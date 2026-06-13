# test_login_courier.py
import allure
import pytest
import requests
from urls import BASE_URL, LOGIN

@allure.feature('Логин курьера')
class TestLoginCourier:

    @allure.title('Курьер может авторизоваться')
    def test_courier_login_success(self, create_courier):
        login = create_courier["login"]
        password = create_courier["password"]
        with allure.step("Авторизация с корректными данными"):
            response = requests.post(f'{BASE_URL}{LOGIN}', data={"login": login, "password": password})
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Для авторизации нужно передать все обязательные поля')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, create_courier, missing_field):
        login = create_courier["login"]
        password = create_courier["password"]
        payload = {"login": login, "password": password}
        del payload[missing_field]
        with allure.step(f"Авторизация без поля {missing_field}"):
            response = requests.post(f'{BASE_URL}{LOGIN}', data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Ошибка при неправильном пароле')
    def test_login_wrong_password(self, create_courier):
        login = create_courier["login"]
        with allure.step("Авторизация с неправильным паролем"):
            response = requests.post(f'{BASE_URL}{LOGIN}', data={"login": login, "password": "wrong"})
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Ошибка при неправильном логине')
    def test_login_wrong_login(self, create_courier):
        password = create_courier["password"]
        with allure.step("Авторизация с неправильным логином"):
            response = requests.post(f'{BASE_URL}{LOGIN}', data={"login": "nonexistent", "password": password})
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Авторизация несуществующего пользователя возвращает ошибку')
    def test_login_nonexistent_user(self):
        with allure.step("Авторизация с несуществующими данными"):
            response = requests.post(f'{BASE_URL}{LOGIN}', data={"login": "no", "password": "body"})
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Успешный запрос возвращает id курьера')
    def test_login_returns_id(self, create_courier):
        login = create_courier["login"]
        password = create_courier["password"]
        with allure.step("Авторизация для получения id"):
            response = requests.post(f'{BASE_URL}{LOGIN}', data={"login": login, "password": password})
        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)
