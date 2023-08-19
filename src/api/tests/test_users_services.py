from unittest.mock import MagicMock, patch

import pytest

from api.app import create_app
from api.config import TestConfig
from api.db.models.users_model import Users
from api.services.users_services import validate_data, get_users_service, get_user_by_uuid_service


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


@patch('api.services.users_services.query_all_users')
def test_get_users_service_not_empty(mock_query_all_users, sample_users_list, app):
    mock_query_all_users.return_value = sample_users_list
    response, status_code = get_users_service()
    assert status_code == 200
    assert "Users" in response


@patch('api.services.users_services.query_all_users')
def test_get_users_service_empty(mock_query_all_users, app):
    mock_query_all_users.return_value = []
    response, status_code = get_users_service()
    assert status_code == 404
    assert response == {"Message": "The users table is empty"}


@patch('api.services.users_services.query_all_users')
def test_get_users_service_exception(mock_query_all_users, app):
    mock_query_all_users.side_effect = Exception("Test exception")
    response, status_code = get_users_service()
    assert status_code == 500
    assert response == {
        "Message": "Couldn't retrieve users from DB!",
        "Error": "Test exception",
    }


@patch('api.services.users_services.query_user_by_uuid')
def test_get_user_by_uuid_service_existing(mock_query_user, sample_user, app):
    mock_query_user.return_value = sample_user
    response, status_code = get_user_by_uuid_service("user1")
    assert status_code == 200
    assert "User" in response


@patch('api.services.users_services.query_user_by_uuid')
def test_get_user_by_uuid_service_non_existing(mock_query_user, app):
    mock_query_user.return_value = None
    user_uuid = "Wrong user"
    response, status_code = get_user_by_uuid_service(user_uuid)
    assert status_code == 404
    assert response == {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}


@patch('api.services.users_services.query_user_by_uuid')
def test_get_user_by_uuid_service_exception(mock_query_user, app):
    user_uuid = "Wrong user"
    mock_query_user.side_effect = Exception("Test exception")
    response, status_code = get_user_by_uuid_service(user_uuid)
    assert status_code == 500
    assert response == {
        "Message": f"Couldn't retrieve user with uuid {user_uuid} from DB!",
        "Error": "Test exception",
    }
