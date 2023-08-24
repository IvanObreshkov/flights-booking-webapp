from unittest.mock import MagicMock, patch

import pytest

from api.db.models.users_model import Users
from api.services.users_services import validate_data, get_users_service, get_user_by_uuid_service, delete_user_service, \
    update_user_service


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
@patch('api.services.users_services.close_db_session')
def test_get_users_service_not_empty(mock_close_db_session, mock_query_all_users, sample_users_list):
    mock_query_all_users.return_value = sample_users_list
    response, status_code = get_users_service()
    assert status_code == 200
    assert "Users" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_all_users')
@patch('api.services.users_services.close_db_session')
def test_get_users_service_empty(mock_close_db_session, mock_query_all_users):
    mock_query_all_users.return_value = []
    response, status_code = get_users_service()
    assert status_code == 404
    assert response == {"Message": "The users table is empty"}
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_all_users')
@patch('api.services.users_services.close_db_session')
def test_get_users_service_exception(mock_close_db_session, mock_query_all_users):
    mock_query_all_users.side_effect = Exception("Test exception")
    response, status_code = get_users_service()
    assert status_code == 500
    assert response == {
        "Message": "Couldn't retrieve users from DB!",
        "Error": "Test exception",
    }
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.close_db_session')
def test_get_user_by_uuid_service_existing(mock_close_db_session, mock_query_user, sample_user):
    mock_query_user.return_value = sample_user
    response, status_code = get_user_by_uuid_service("user1")
    assert status_code == 200
    assert "User" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.close_db_session')
def test_get_user_by_uuid_service_non_existing(mock_close_db_session, mock_query_user):
    mock_query_user.return_value = None
    user_uuid = "Wrong user"
    response, status_code = get_user_by_uuid_service(user_uuid)
    assert status_code == 404
    assert response == {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.close_db_session')
def test_get_user_by_uuid_service_exception(mock_close_db_session, mock_query_user):
    user_uuid = "Wrong user"
    mock_query_user.side_effect = Exception("Test exception")
    response, status_code = get_user_by_uuid_service(user_uuid)
    assert status_code == 500
    assert response == {
        "Message": f"Couldn't retrieve user with uuid {user_uuid} from DB!",
        "Error": "Test exception",
    }
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.delete_user_from_db')
@patch('api.services.users_services.close_db_session')
def test_delete_user_service_existing_user(mock_close_db_session, mock_delete_user, mock_query_user):
    user_uuid = "user1"
    mock_query_user.return_value = sample_user

    response, status_code = delete_user_service(user_uuid)
    assert status_code == 200
    assert response == {"Message": f"User with uuid {user_uuid} was removed successfully from the DB"}
    mock_delete_user.assert_called_once()
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.delete_user_from_db')
@patch('api.services.users_services.close_db_session')
def test_delete_user_service_wrong_user_uuid(mock_close_db_session, mock_delete_user, mock_query_user):
    user_uuid = "Wrong user"
    mock_query_user.return_value = None

    response, status_code = delete_user_service(user_uuid)
    assert status_code == 404
    assert response == {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}
    mock_delete_user.assert_not_called()
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.delete_user_from_db')
@patch('api.services.users_services.close_db_session')
@patch("api.services.users_services.db_rollback")
def test_delete_user_service_exception(mock_db_rollback, mock_close_db_session, mock_delete_user, mock_query_user):
    user_uuid = "user1"
    mock_delete_user.side_effect = Exception("Test exception")
    mock_query_user.side_effect = Exception("Test exception")

    response, status_code = delete_user_service(user_uuid)
    assert status_code == 500
    assert response == {"Message": f"Couldn't delete user with uuid {user_uuid} from DB!",
                        "Error": "Test exception"}
    mock_delete_user.assert_not_called()
    mock_close_db_session.assert_called_once()
    mock_db_rollback.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.edit_user_data')
@patch('api.services.users_services.close_db_session')
def test_update_user_service_existing_user(mock_close_db_session, mock_edit_user_data, mock_query_user):
    user_uuid = "user1"
    mock_query_user.return_value = sample_user
    request = MagicMock()
    request.json = {"first_name": "Gosho"}
    response, status_code = update_user_service(user_uuid, request)
    assert status_code == 200
    assert response == {"Message": f"User with uuid {user_uuid} was updated successfully."}
    mock_edit_user_data.assert_called_once_with(sample_user, request.json)
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.edit_user_data')
@patch('api.services.users_services.close_db_session')
def test_update_user_service_wrong_user_number(mock_close_db_session, mock_edit_user_data, mock_query_user):
    user_uuid = "Wrong user"
    mock_query_user.return_value = None
    request = MagicMock()
    request.json = {"first_name": "Gosho"}
    response, status_code = update_user_service(user_uuid, request)
    assert status_code == 404
    assert response == {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}
    mock_edit_user_data.assert_not_called()
    mock_close_db_session.assert_called_once()


@patch('api.services.users_services.query_user_by_uuid')
@patch('api.services.users_services.edit_user_data')
@patch('api.services.users_services.close_db_session')
@patch("api.services.users_services.db_rollback")
def test_update_user_service_exception(mock_db_rollback, mock_close_db_session, mock_edit_user_data, mock_query_user):
    user_uuid = "user1"
    mock_query_user.side_effect = Exception("Test exception")
    mock_edit_user_data.side_effect = Exception("Test exception")
    request = MagicMock()
    request.json = {"first_name": "Gosho"}
    response, status_code = update_user_service(user_uuid, request)
    assert status_code == 500
    assert response == {"Message": f"Couldn't update user with uuid {user_uuid}",
                        "Error": "Test exception"}
    mock_edit_user_data.assert_not_called()
    mock_close_db_session.assert_called_once()
    mock_db_rollback.assert_called_once()
