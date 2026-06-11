# test_delete_courier.py
import allure
import pytest
import requests
from data import BASE_URL, register_new_courier_and_return_login_password

@allure.feature('Удаление курьера')
class TestDeleteCourier:

    @allure.title('Успешное удаление курьера возвращает {"ok":true}')
    def test_delete_courier_success(self):
        creds = register_new_courier_and_return_login_password()
        if not creds:
            pytest.skip("Не удалось создать курьера")
        login, password, _ = creds
        # Получаем id
        auth = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
        assert auth.status_code == 200
        courier_id = auth.json()["id"]
        response = requests.delete(f'{BASE_URL}/courier/{courier_id}')
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title('Удаление без id возвращает ошибку')
    def test_delete_courier_no_id(self):
        response = requests.delete(f'{BASE_URL}/courier/')
        # Обратите внимание, что ручка требует id в URL, поэтому без него будет 404 или 405
        assert response.status_code in (404, 405)

    @allure.title('Удаление с несуществующим id возвращает ошибку')
    def test_delete_courier_invalid_id(self):
        response = requests.delete(f'{BASE_URL}/courier/999999')
        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет"