# test_delete_courier.py (дополнительное задание)
import allure
import requests
from urls import BASE_URL, COURIER, LOGIN

@allure.feature('Удаление курьера')
class TestDeleteCourier:

    @allure.title('Успешное удаление курьера возвращает {"ok":true}')
    def test_delete_courier_success(self, create_courier):
        login = create_courier["login"]
        password = create_courier["password"]
        with allure.step("Получение id курьера"):
            auth = requests.post(f'{BASE_URL}{LOGIN}', data={"login": login, "password": password})
            assert auth.status_code == 200
            courier_id = auth.json()["id"]
        with allure.step(f"Удаление курьера с id {courier_id}"):
            response = requests.delete(f'{BASE_URL}{COURIER}/{courier_id}')
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title('Удаление без id возвращает ошибку')
    def test_delete_courier_no_id(self):
        with allure.step("Запрос на удаление без указания id"):
            response = requests.delete(f'{BASE_URL}{COURIER}/')
        # В зависимости от реализации сервера может быть 404 или 405
        assert response.status_code in (404, 405)

    @allure.title('Удаление с несуществующим id возвращает ошибку')
    def test_delete_courier_invalid_id(self):
        with allure.step("Удаление несуществующего курьера"):
            response = requests.delete(f'{BASE_URL}{COURIER}/999999')
        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет"
