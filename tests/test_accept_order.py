# test_accept_order.py (дополнительное задание)
import allure
import requests
from urls import BASE_URL, ACCEPT_ORDER, TRACK_ORDER, ORDERS

@allure.feature('Принять заказ')
class TestAcceptOrder:

    @allure.title('Успешный запрос возвращает {"ok":true}')
    def test_accept_order_success(self, create_order, create_courier):
        track = create_order()
        with allure.step(f"Получение order_id по треку {track}"):
            get_order = requests.get(f'{BASE_URL}{TRACK_ORDER}', params={"t": track})
            assert get_order.status_code == 200
            order_id = get_order.json()["order"]["id"]
        login = create_courier["login"]
        password = create_courier["password"]
        with allure.step("Получение id курьера"):
            auth = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
            assert auth.status_code == 200
            courier_id = auth.json()["id"]
        with allure.step(f"Принятие заказа {order_id} курьером {courier_id}"):
            response = requests.put(f'{BASE_URL}{ACCEPT_ORDER}/{order_id}', params={"courierId": courier_id})
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title('Если не передать id курьера, вернётся ошибка')
    def test_accept_order_no_courier_id(self, create_order):
        track = create_order()
        with allure.step("Получение order_id"):
            get_order = requests.get(f'{BASE_URL}{TRACK_ORDER}', params={"t": track})
            assert get_order.status_code == 200
            order_id = get_order.json()["order"]["id"]
        with allure.step("Принятие заказа без courierId"):
            response = requests.put(f'{BASE_URL}{ACCEPT_ORDER}/{order_id}')
        assert response.status_code == 400
        assert "Недостаточно данных" in response.text

    @allure.title('Если не передать id заказа, вернётся ошибка')
    def test_accept_order_no_order_id(self, create_courier):
        login = create_courier["login"]
        password = create_courier["password"]
        with allure.step("Получение id курьера"):
            auth = requests.post(f'{BASE_URL}/courier/login', data={"login": login, "password": password})
            assert auth.status_code == 200
            courier_id = auth.json()["id"]
        with allure.step("Запрос на принятие без id заказа"):
            response = requests.put(f'{BASE_URL}{ACCEPT_ORDER}/', params={"courierId": courier_id})
        assert response.status_code == 404  # или 400, зависит от API
