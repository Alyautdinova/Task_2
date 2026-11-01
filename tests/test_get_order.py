import allure
import requests

from data.urls import Urls

class TestGetOrder:

    @allure.title('Получение заказов авторизованным пользователем')
    @allure.description('Проверяем, что авторизованный пользователь получает список своих заказов')
    def test_get_orders_with_auth(self, created_order):
        with allure.step('Проверка, что заказы получены и среди них есть созданный'):
            token = created_order["token"]
            headers = {"Authorization": token}

        with allure.step('Получение заказов пользователя'):
            response = requests.get(Urls.ORDER_URL, headers=headers)

        with allure.step('Проверка, что заказы получены и среди них есть созданный'):
            assert response.status_code == 200
            
            orders = response.json().get("orders", [])
            assert len(orders) > 0

            # создаем новый список для номеров заказов, чтобы потом найти в нем нужный номер
            order_numbers = []
            for order in orders:
                number = order.get("number")
                order_numbers.append(number)
                
            assert created_order["order_number"] in order_numbers

    @allure.title('Получение заказов неавторизованным пользователем')
    @allure.description('Проверяем, что без авторизации нельзя получить список заказов')
    def test_get_orders_without_auth(self):
        with allure.step('Получение заказов без токена'):
            response = requests.get(Urls.ORDER_URL)

        with allure.step('Проверка, что вернулась ошибка авторизации'):
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"
        