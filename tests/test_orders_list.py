# test_orders_list.py
import allure
import requests
from urls import BASE_URL, ORDERS

@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Тело ответа возвращает список заказов')
    def test_orders_list_returns_list(self):
        with allure.step("Получение списка заказов"):
            response = requests.get(f'{BASE_URL}{ORDERS}')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
