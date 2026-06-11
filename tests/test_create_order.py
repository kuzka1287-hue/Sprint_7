# test_create_order.py
import allure
import pytest
import requests
from data import BASE_URL

@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Можно указать цвет BLACK')
    def test_create_order_black_color(self, create_order):
        track = create_order(["BLACK"])
        assert track is not None

    @allure.title('Можно указать цвет GREY')
    def test_create_order_grey_color(self, create_order):
        track = create_order(["GREY"])
        assert track is not None

    @allure.title('Можно указать оба цвета BLACK и GREY')
    def test_create_order_both_colors(self, create_order):
        track = create_order(["BLACK", "GREY"])
        assert track is not None

    @allure.title('Можно не указывать цвет')
    def test_create_order_no_color(self, create_order):
        track = create_order([])
        assert track is not None

    @allure.title('Тело ответа содержит track')
    def test_create_order_response_has_track(self, create_order):
        # используем прямой запрос, чтобы проверить поле track
        payload = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "address": "Москва",
            "metroStation": 1,
            "phone": "+79998887766",
            "rentTime": 5,
            "deliveryDate": "2025-12-31",
            "comment": "Тест",
            "color": []
        }
        response = requests.post(f'{BASE_URL}/orders', json=payload)
        assert response.status_code == 201
        assert "track" in response.json()