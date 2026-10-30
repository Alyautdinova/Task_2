import requests
from faker import Faker
import allure

from data.urls import Urls

class TestLoginUser:

    @allure.title('Вход под существующим в системе пользователем')
    @allure.description('Проверяем, что запрос отдает 200 и accessToken пользователя при входе под существующим в системе пользователем')
    def test_login_success(self, register_new_user):
        with allure.step('Подготовка данных для входа пользователя'):
            user_data = register_new_user

            login_payload = {
                "email": user_data[0],
                "password": user_data[1]
            }

        with allure.step('Логин пользователем'):
            response = requests.post(Urls.LOGIN_URL, json=login_payload)

        with allure.step('Проверка, что вошли под пользователем'):
            assert response.status_code == 200
            assert "accessToken" in response.json()

    @allure.title('Вход без существующего логина в системе')
    @allure.description('Проверяем, что запрос отдает 401 и ошибку при попытке входа с несуществующим логином')
    def test_login_with_not_exist_login(self):
        
        with allure.step('Данные для входа пользователя'):
            fake = Faker()
            email = fake.email()
            password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
            
            login_payload = {
                "email": email,
                "password": password
            }

        with allure.step('Логин пользователя'):
            response = requests.post(Urls.LOGIN_URL, json=login_payload)

        with allure.step('Проверка, что не вошли под пользователем'):
            assert response.status_code == 401
            assert response.json()["message"] == 'email or password are incorrect'

    @allure.title('Вход без существующего пароля в системе')
    @allure.description('Проверяем, что запрос отдает 401 и ошибку при попытке входа с несуществующим паролем')
    def test_login_with_not_exist_password(self, register_new_user):

        with allure.step('Подготовка данных для входа пользователя'):
            user_data = register_new_user
        
            login_payload = {
                "email": user_data[0],
                "password": "test45678"
            }

        with allure.step('Логин пользователя'):
            response = requests.post(Urls.LOGIN_URL, json=login_payload)

        with allure.step('Проверка, что не вошли под пользователем'):
            assert response.status_code == 401
            assert response.json()["message"] == 'email or password are incorrect'
    