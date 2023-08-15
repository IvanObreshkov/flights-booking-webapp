from unittest.mock import MagicMock, patch

import pytest

from api.app import create_app
from api.config import TestConfig
from api.db.models.users_model import Users
from api.services.users_services import validate_data


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


def test_validate_data_valid():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "mypassword"
    }
    validate_data(data)


def test_validate_data_missing_field():
    data = {
        "first_name": "John",
        "last_name": "",
        "email": "john@example.com",
        "password": "mypassword"
    }
    with pytest.raises(ValueError):
        validate_data(data)


def test_validate_data_invalid_email():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid_email",
        "password": "mypassword"
    }
    with pytest.raises(ValueError):
        validate_data(data)
