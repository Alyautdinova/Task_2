import pytest
import requests
import allure

from data.urls import Urls


class TestUpdateUser:

    @allure.title('Изменение данных авторизованным пользователем')
    @allure.description('Проверяем, что авторизованным пользователем можно изменить 3 поля')
    @pytest.mark.parametrize("field", ["email", "name", "password"])
    def test_update_user_with_auth(self, auth_token, generate_user, field):
        with allure.step('Подготовка пользователя и вытаскивание токена'):
            headers = {"Authorization": auth_token}

        with allure.step('Подготовка новых данных для пользователя'):
            new_user_data = generate_user
            new_value = new_user_data[field]
            payload = {field: new_value}

        with allure.step('Изменение данных пользователя'):
            response = requests.patch(Urls.USER_URL, json=payload, headers=headers)

        with allure.step('Проверка что данные изменились'):
            assert response.status_code == 200

            # если поле пароль, то измененное значение не возвращается
            if field != "password":
                user_data = response.json().get("user", {})
                assert user_data.get(field) == new_value

    @allure.title('Изменение данных неавторизованным пользователем')
    @allure.description('Проверяем, что неавторизованным пользователем нельзя изменить значения')
    @pytest.mark.parametrize("field", ["email", "name", "password"])
    def test_update_user_without_auth(self, generate_user, field):

        with allure.step('Подготовка новых данных для пользователя'):
            new_user_data = generate_user
            new_value = new_user_data[field]
            payload = {field: new_value}

        with allure.step('Изменение данных пользователя'):
            response = requests.patch(Urls.USER_URL, json=payload)

        with allure.step('Проверка, что данные можно изменять только авторизованным пользователем'):
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"
