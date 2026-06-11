# test_accept_order.py
import allure
import pytest
import requests
from data import BASE_URL

@allure.feature('Принять заказ')
class TestAcceptOrder:

    @allure.title('Успешный запрос возвращает {"ok":true}')
    def test_accept_order_success(self, create_order, create_courier):
        track = create_order()
        # Получаем order_id по track
        get_order = requests.get(f'{BASE_URL}/orders/track?t={track}')
        assert get_order.status_code == 200
        order_id = get_order.json()["order"]["id"]
        courier_id = create_courier["id"]  # create_courier фикстура должна возвращать id, адаптируйте
        # ВАЖНО: в документации ошибка – параметры передаются как query string
        response = requests.put(f'{BASE_URL}/orders/accept/{order_id}?courierId={courier_id}')
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title('Если не передать id курьера, вернётся ошибка')
    def test_accept_order_no_courier_id(self, create_order):
        track = create_order()
        get_order = requests.get(f'{BASE_URL}/orders/track?t={track}')
        order_id = get_order.json()["order"]["id"]
        response = requests.put(f'{BASE_URL}/orders/accept/{order_id}')
        assert response.status_code == 400
        assert "Недостаточно данных" in response.text

    @allure.title('Если не передать id заказа, вернётся ошибка')
    def test_accept_order_no_order_id(self, create_courier):
        courier_id = create_courier["id"]
        response = requests.put(f'{BASE_URL}/orders/accept/?courierId={courier_id}')
        assert response.status_code == 404  # или 400