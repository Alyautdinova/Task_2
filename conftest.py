import requests
import pytest
from faker import Faker
from data.urls import Urls

# фикстуры для генерации данных пользователя
@pytest.fixture
def generate_user():
    fake = Faker()

    # генерируем почту, пароль и имя пользователя
    name = fake.file_name()
    email = fake.email()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    
    # собираем тело запроса
    payload = {
        "email": email,
        "password": password,
        "name": name
        }

    return payload

# фикстура для создания пользователя
@pytest.fixture
def register_new_user(generate_user):

    payload = generate_user

    requests.post(Urls.REGISTER_URL, json=payload)

    return payload

# фикстура для создания пользователя и возвращения токена
@pytest.fixture
def auth_token(generate_user):
    response = requests.post(Urls.REGISTER_URL, json=generate_user)
   
    return response.json().get("accessToken")

# фикстура для получения валидных ID ингредиентов
@pytest.fixture
def get_valid_ingredients():
    response = requests.get(Urls.INGREDIENTS_URL)
    assert response.status_code == 200
    
    ingredients_data = response.json().get("data", [])
    return [ingredients_data[0]["_id"], ingredients_data[1]["_id"]]
