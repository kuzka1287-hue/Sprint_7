# test_orders_list.py
import allure
import requests
from data import BASE_URL

@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Тело ответа возвращает список заказов')
    def test_orders_list_returns_list(self):
        response = requests.get(f'{BASE_URL}/orders')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)