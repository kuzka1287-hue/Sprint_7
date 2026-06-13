# test_get_order_by_track.py (дополнительное задание)
import allure
import requests
from urls import BASE_URL, TRACK_ORDER

@allure.feature('Получение заказа по номеру')
class TestGetOrderByTrack:

    @allure.title('Успешный запрос возвращает объект с заказом')
    def test_get_order_by_track_success(self, create_order):
        track = create_order()
        with allure.step(f"Получение заказа по треку {track}"):
            response = requests.get(f'{BASE_URL}{TRACK_ORDER}', params={"t": track})
        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == track

    @allure.title('Запрос без номера заказа возвращает ошибку')
    def test_get_order_no_track(self):
        with allure.step("Запрос без параметра t"):
            response = requests.get(f'{BASE_URL}{TRACK_ORDER}')
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title('Запрос с несуществующим заказом возвращает ошибку')
    def test_get_order_invalid_track(self):
        with allure.step("Запрос с несуществующим треком"):
            response = requests.get(f'{BASE_URL}{TRACK_ORDER}', params={"t": 999999999})
        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"
