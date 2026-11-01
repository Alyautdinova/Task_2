import pytest
import requests
import allure

from data.urls import Urls

class TestCreateOrder:
    @allure.title('Создание заказа авторизованным и с корректными ингредиентами')
    @allure.description('Проверяем, что авторизованным пользователем можно и с корректными ингредиентами можно создать заказ')
    def test_create_order_with_auth_and_valid_ingredients(self, auth_token, get_valid_ingredients):
        with allure.step('Подготовка данных для создание заказа'):
            headers = {"Authorization": auth_token}
            payload = {"ingredients": get_valid_ingredients}

        with allure.step('Создание заказа авторизованным и с корректными ингредиентами'):
            response = requests.post(Urls.ORDER_URL, json=payload, headers=headers)

        with allure.step('Проверка, что заказ создан'):
            assert response.status_code == 200
            assert "number" in response.json()["order"]

    @allure.title('Создание заказа неавторизованным и с корректными ингредиентами')
    @allure.description('Проверяем, что неавторизованным пользователем можно и с корректными ингредиентами можно создать заказ')
    def test_create_order_without_auth_and_valid_ingredients(self, get_valid_ingredients):
        with allure.step('Подготовка данных для создание заказа'):
            payload = {"ingredients": get_valid_ingredients}

        with allure.step('Создание заказа неавторизованным и с корректными ингредиентами'):
            response = requests.post(Urls.ORDER_URL, json=payload)

        with allure.step('Проверка, что заказ создан'):
            assert response.status_code == 200
            assert "number" in response.json()["order"]

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('Проверяем, что без ингредиентов нельзя создать заказ')
    def test_create_order_without_ingredients(self):
        with allure.step('Подготовка данных для создание заказа'):
            payload = {"ingredients": []}

        with allure.step('Создание заказа без ингредиентов'):
            response = requests.post(Urls.ORDER_URL, json=payload)

        with allure.step('Проверка, что заказ не создан'):
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title('Создание заказа с невалидным ингредиентом')
    @allure.description('Проверяем, что с невалидным ингредиентом нельзя создать заказ')
    def test_create_order_with_invalid_ingredients(self):
        with allure.step('Подготовка данных для создание заказа'):
            payload = {"ingredients": ["invalid_hash_12345"]}

        with allure.step('Создание заказа с невалидным ингредиентом'):
            response = requests.post(Urls.ORDER_URL, json=payload)

        with allure.step('Проверка, что заказ не создан'):
            assert response.status_code == 500
    