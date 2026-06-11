# test_get_order_by_track.py
import allure
import pytest
import requests
from data import BASE_URL

@allure.feature('Получение заказа по номеру')
class TestGetOrderByTrack:

    @allure.title('Успешный запрос возвращает объект с заказом')
    def test_get_order_by_track_success(self, create_order):
        track = create_order()
        response = requests.get(f'{BASE_URL}/orders/track?t={track}')
        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == track

    @allure.title('Запрос без номера заказа возвращает ошибку')
    def test_get_order_no_track(self):
        response = requests.get(f'{BASE_URL}/orders/track')
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title('Запрос с несуществующим заказом возвращает ошибку')
    def test_get_order_invalid_track(self):
        response = requests.get(f'{BASE_URL}/orders/track?t=999999999')
        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"