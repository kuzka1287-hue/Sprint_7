# test_create_order.py
import allure
import pytest
from urls import BASE_URL, ORDERS

@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа с разными вариантами цвета')
    @pytest.mark.parametrize("color_list", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_colors(self, create_order, color_list):
        track = create_order(color_list)
        assert track is not None, "Трек заказа не должен быть None"

    @allure.title('Тело ответа содержит track')
    def test_create_order_response_has_track(self):
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
        with allure.step("Создание заказа без указания цвета"):
            response = requests.post(f'{BASE_URL}{ORDERS}', json=payload)
        assert response.status_code == 201
        assert "track" in response.json()
