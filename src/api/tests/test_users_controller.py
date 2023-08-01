import pytest

from api.controllers.users_controller import validate_data


def test_validate_data_valid():
    # Valid data should not raise any errors
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "secret123",
    }
    assert validate_data(data) is None


def test_validate_data_missing_fields():
    # Missing fields should raise ValueError
    data = {
        "first_name": "John",
        "last_name": "Doe",
        # Missing "email" and "password"
    }
    with pytest.raises(ValueError, match=".* cannot be empty!"):
        validate_data(data)


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
