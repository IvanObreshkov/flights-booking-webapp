from unittest.mock import patch, MagicMock

import pytest

from api.app import create_app
from api.config import TestConfig
from api.db.models.user_bookings_model import UserBookings
from api.services.bookings_services import validate_and_add_booking, add_booking_service


@pytest.fixture
def sample_booking():
    return UserBookings(booking_id='booking_1', user_id="user_1", flight_number="F123")


@pytest.fixture
def sample_bookings_list():
    return [
        UserBookings(booking_id='booking_1', user_id="user_1", flight_number="F123"),
        UserBookings(booking_id='booking_2', user_id="user_2", flight_number="F456")
    ]


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@patch("api.services.bookings_services.create_booking")
@patch("api.services.bookings_services.add_booking_to_db")
@patch("api.services.bookings_services.check_booking_existence")
def test_validate_and_add_booking(mock_check_booking_existence, mock_add_booking_to_db, mock_create_booking, app):
    mock_user = MagicMock()
    mock_flight = MagicMock()
    mock_json_data = {
        "user_id": "user_uuid",
        "flight_number": "F123",
    }

    mock_check_booking_existence.return_value = False
    mock_create_booking.return_value = sample_booking
    response, status_code = validate_and_add_booking(mock_user, mock_flight, mock_json_data)
    assert response == {"Message": "New booking added to DB!"}
    assert status_code == 200
    mock_add_booking_to_db.assert_called_once_with(sample_booking)


@patch("api.services.bookings_services.add_booking_to_db")
def test_validate_and_add_booking_user_does_not_exist(mock_add_booking_to_db, app):
    mock_user = None
    mock_flight = MagicMock()
    mock_json_data = {
        "user_id": "user_uuid",
        "flight_number": "F123",
    }

    response, status_code = validate_and_add_booking(mock_user, mock_flight, mock_json_data)
    assert response == {"Message": f"User with uuid {mock_json_data['user_id']} doesn't exist in the DB!"}
    assert status_code == 404
    mock_add_booking_to_db.assert_not_called()


@patch("api.services.bookings_services.add_booking_to_db")
def test_validate_and_add_booking_flight_does_not_exist(mock_add_booking_to_db, app):
    mock_user = MagicMock()
    mock_flight = None
    mock_json_data = {
        "user_id": "user_uuid",
        "flight_number": "F123",
    }

    response, status_code = validate_and_add_booking(mock_user, mock_flight, mock_json_data)
    assert response == {"Message": f"Flight with number: {mock_json_data['flight_number']} doesn't exist in the DB!"}
    assert status_code == 404
    mock_add_booking_to_db.assert_not_called()


@patch("api.services.bookings_services.validate_and_add_booking")
@patch("api.services.bookings_services.query_flight_by_flight_number")
@patch("api.services.bookings_services.get_user_by_uuid_service")
def test_add_booking_service_exception(mock_get_user_by_uuid_service, mock_query_flight_by_flight_number,
                                       mock_validate_and_add_booking, app):
    mock_request = MagicMock()

    mock_request.json = {
        "user_id": "user_uuid",
        "flight_number": "F123",
    }
    mock_get_user_by_uuid_service.side_effect = Exception("Test exception")
    mock_query_flight_by_flight_number.side_effect = Exception("Test exception")

    response, status_code = add_booking_service(mock_request)
    assert response == {"Message": f"Couldn't create a new booking. Please try again later!",
                        "Error": "Test exception"}
    assert status_code == 500
    mock_validate_and_add_booking.assert_not_called()
