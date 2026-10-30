import requests
import pytest
import allure

from data.urls import Urls

class TestCreateUser:
    @allure.title('Создание нового пользователя')
    @allure.description('Проверяем, что запрос отдает 200 и True при создании пользователя с валидными данными')
    def test_create_uniq_user(self, generate_user):
        with allure.step('Подготовка данных для создании пользователя'):
            payload = generate_user

        with allure.step('Создание пользователя'):
            response = requests.post(Urls.REGISTER_URL, json=payload)

        with allure.step('Проверка, что создали пользователя'):
            assert response.status_code == 200
            assert response.json()["success"] == True

    @allure.title('Создание пользователя с данными существующими в системе')
    @allure.description('Проверяем, что запрос отдает 403 и ошибку при создании пользователя с данными как у существующего пользователя в системе')
    def test_create_two_identical_user(self, register_new_user):
        with allure.step('Создание второго пользователя с такими же данными как первый пользователь'):
            payload = register_new_user
            response = requests.post(Urls.REGISTER_URL, json=payload)

        with allure.step('Проверка, что пользователь с данными, которые уже есть в системе, не создается'):  
            assert response.status_code == 403
            assert response.json()["message"] == 'User already exists'

    @allure.title('Создание пользователя без обязательных параметров')
    @allure.description('Проверяем, что запрос отдает 403 и ошибку при создании пользователя без обязательных параметров')
    @pytest.mark.parametrize("missing_payload",
        [
            ({"password": "123", "name": "Farida"}),
            ({"email": "login", "name": "Farida"}),
            ({"email": "login", "password": "123"}),
            ({},)
        ]
    )
    def test_create_user_missing_required_field_returns_error(self, missing_payload):
        with allure.step('Создание пользователя без обязательных параметров'): 
            response = requests.post(Urls.REGISTER_URL, json=missing_payload)

        with allure.step('Проверка, что пользователь не создался'):
            assert response.status_code == 403
            assert response.json()["message"] == 'Email, password and name are required fields'
