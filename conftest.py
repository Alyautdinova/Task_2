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

    response = requests.post(Urls.REGISTER_URL, json=payload)

    token = response.json().get("accessToken")

    yield {"payload": payload, "token": token}
    
    # удаление юзера
    headers = {"Authorization": token}
    requests.delete(Urls.USER_URL, headers=headers)

# фикстура для получения валидных ID ингредиентов
@pytest.fixture
def get_valid_ingredients():
    response = requests.get(Urls.INGREDIENTS_URL)
    
    ingredients_data = response.json().get("data", [])
    return [ingredients_data[0]["_id"], ingredients_data[1]["_id"]]


# фикстура для создание заказа
@pytest.fixture
def created_order(register_new_user, get_valid_ingredients):
    token = register_new_user["token"]
    headers = {"Authorization": token}
    payload = {"ingredients": get_valid_ingredients}
    
    response = requests.post(Urls.ORDER_URL, json=payload, headers=headers)
    
    return {"order_number": response.json()["order"]["number"], "token": token}
