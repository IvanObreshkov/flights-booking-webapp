import pytest

from app import create_app
from config import TestConfig
from db.models.users_model import Users


@pytest.fixture
def sample_user():
    return Users(
        id="user_1",
        first_name="Ivan",
        last_name="Obreshkov",
        email="ivan@gmail.com",
        password="test1234"
    )


@pytest.fixture
def sample_users_list():
    return [
        Users(
            id="user_1",
            first_name="Ivan",
            last_name="Obreshkov",
            email="ivan@gmail.com",
            password="test1234"
        ),
        Users(
            id="user_2",
            first_name="Dani",
            last_name="Ivanov",
            email="dani@gmail.com",
            password="dani1234"
        )
    ]


@pytest.fixture()
def empty_users_table():
    return []


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app
