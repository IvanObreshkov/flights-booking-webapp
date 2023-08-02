import pytest

from api.controllers.users_controller import validate_data, get_all_users, get_user_by_uuid, get_user_by_email
from api.models.users_model import Users
from api.models.flights_model import Flights
from api.models.user_bookings_model import UserBookings


def test_validate_data_valid():
    # Valid data should not raise any errors
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "secret123",
    }
    assert validate_data(data) is None


def test_validate_data_empty_fields():
    # Empty fields should raise ValueError
    data = {
        "first_name": "",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "secret123",
    }
    with pytest.raises(ValueError, match="First name cannot be empty!"):
        validate_data(data)


def test_validate_data_invalid_email():
    # Invalid email should raise ValueError
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email",
        "password": "secret123",
    }
    with pytest.raises(ValueError, match="Email is not in a valid format!"):
        validate_data(data)


def create_mock_user(id, first_name, last_name, email, password):
    return Users(id=id, first_name=first_name, last_name=last_name, email=email, password=password)


def test_get_all_users(mocker):
    mock_users = [create_mock_user("1", "Ivan", "Obreshkov", "ivan@test.com", "test1234"),
                  create_mock_user("2", "Toni", "Montana", "toni@toni.bg", "birabira")]

    mock_query = mocker.patch('api.database.db.session.query')
    mock_query.return_value.all.return_value = mock_users

    result = get_all_users()
    assert len(result) == 2
    assert result[0].id == '1'
    assert result[0].first_name == 'Ivan'
    assert result[0].last_name == 'Obreshkov'
    assert result[0].email == 'ivan@test.com'

    assert result[1].id == '2'
    assert result[1].first_name == 'Toni'
    assert result[1].last_name == 'Montana'
    assert result[1].email == 'toni@toni.bg'

def test_get_user_by_uuid(mocker):
    mock_user = create_mock_user("1", "Ivan", "Obreshkov", "ivan@test.com", "test1234")
    mock_query = mocker.patch("api.database.db.session.query")

    mock_query.return_value.get.return_value = mock_user
    result = get_user_by_uuid("1")
    assert result == mock_user

    mock_query.return_value.get.return_value = None
    result = get_user_by_uuid("invalid_uuid")
    assert result is None

def test_get_user_by_email(mocker):
    mock_user = create_mock_user("1", "Ivan", "Obreshkov", "ivan@test.com", "test1234")
    mock_query = mocker.patch("api.database.db.session.query")

    mock_query.return_value.filter_by.return_value.first.return_value = mock_user

    result = get_user_by_email("ivan@test.com")
    assert result == mock_user

    mock_query.return_value.filter_by.return_value.first.return_value = None
    result = get_user_by_email("invalid_email")
    assert result is None