from collections import namedtuple
from unittest.mock import patch, MagicMock

import pytest

from api.db.models.user_bookings_model import UserBookings
from api.services.bookings_services import validate_and_add_booking, add_booking_service, get_bookings_service, \
    get_booking_service, get_user_bookings_service, delete_booking_service


@pytest.fixture
def sample_booking():
    return UserBookings(booking_id='booking_1', user_id="user_1", flight_number="F123")


@patch("api.services.bookings_services.create_booking")
@patch("api.services.bookings_services.add_booking_to_db")
@patch("api.services.bookings_services.check_booking_existence")
def test_validate_and_add_booking(mock_check_booking_existence, mock_add_booking_to_db,
                                  mock_create_booking):
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
def test_validate_and_add_booking_user_does_not_exist(mock_add_booking_to_db):
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
def test_validate_and_add_booking_flight_does_not_exist(mock_add_booking_to_db):
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
@patch("api.services.bookings_services.close_db_session")
def test_add_booking_service_exception(mock_close_db_session, mock_get_user_by_uuid_service,
                                       mock_query_flight_by_flight_number,
                                       mock_validate_and_add_booking):
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
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_all_bookings')
@patch("api.services.bookings_services.close_db_session")
def test_get_bookings_service_not_empty(mock_close_db_session, mock_query_all_bookings):
    BookingsRow = namedtuple('BookingsRow',
                             ['booking_id', 'flight_number', 'price', 'email', 'first_name', 'last_name'])

    bookings_data = [
        BookingsRow(booking_id='70e4c838-a57d-46fc-9050-c94b6ab946e9', flight_number="F123", price=123,
                    email='dani@gmail.com', first_name='Dani', last_name='Ivanov'),
        BookingsRow(booking_id='8c8565cf-4384-4474-a8c7-10a62b27ceed', flight_number="F123", price=345,
                    email='ivan@gmail.com', first_name='Ivan', last_name='Obreshkov')
    ]
    mock_query_all_bookings.return_value = bookings_data
    response, status_code = get_bookings_service()
    assert status_code == 200
    assert "All bookings" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_all_bookings')
@patch("api.services.bookings_services.close_db_session")
def test_get_bookings_service_empty(mock_close_db_session, mock_query_all_bookings):
    mock_query_all_bookings.return_value = []
    response, status_code = get_bookings_service()
    assert status_code == 404
    assert response == {"Message": "The bookings table is empty"}
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_all_bookings')
@patch("api.services.bookings_services.close_db_session")
def test_get_bookings_service_exception(mock_close_db_session, mock_query_all_bookings):
    mock_query_all_bookings.side_effect = Exception("Test exception")
    response, status_code = get_bookings_service()
    assert status_code == 500
    assert response == {
        "Message": "Couldn't retrieve bookings from DB!",
        "Error": "Test exception",
    }
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_booking_by_id')
@patch("api.services.bookings_services.close_db_session")
def test_get_booking_service_existing(mock_close_db_session, mock_query_booking, sample_booking):
    booking_id = 'booking_1'
    mock_query_booking.return_value = sample_booking
    response, status_code = get_booking_service(booking_id)
    assert status_code == 200
    assert "Booking" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_booking_by_id')
@patch("api.services.bookings_services.close_db_session")
def test_get_booking_service_non_existing(mock_close_db_session, mock_query_booking):
    booking_id = 'Wrong booking'
    mock_query_booking.return_value = None
    response, status_code = get_booking_service("Wrong booking")
    assert status_code == 404
    assert response == {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_booking_by_id')
@patch("api.services.bookings_services.close_db_session")
def test_get_booking_service_exception(mock_close_db_session, mock_query_booking):
    booking_id = 'booking_1'
    mock_query_booking.side_effect = Exception("Test exception")
    response, status_code = get_booking_service(booking_id)
    assert status_code == 500
    assert response == {
        "Message": f"Couldn't retrieve Booking with uuid {booking_id} from DB!",
        "Error": "Test exception",
    }
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.get_user_by_uuid_service')
@patch('api.services.bookings_services.query_bookings_by_user_id')
@patch("api.services.bookings_services.close_db_session")
def test_get_user_bookings_service_existing_user(mock_close_db_session, mock_query_bookings_by_user_id,
                                                 mock_get_user_by_uuid_service):
    user_id = "user_1"
    UsersBookingsRow = namedtuple('BookingsRow',
                                  ['booking_id', 'flight_number', 'start_destination', 'end_destination',
                                   'takeoff_time', 'landing_time', 'price', 'email', 'first_name', 'last_name'])

    users_bookings_data = [
        UsersBookingsRow(booking_id='70e4c838-a57d-46fc-9050-c94b6ab946e9', flight_number="F123",
                         start_destination="City C", end_destination="City D",
                         takeoff_time="2023-08-10 14:00", landing_time="2023-08-10 16:00", price=123,
                         email='dani@gmail.com', first_name='Dani', last_name='Ivanov'),
        UsersBookingsRow(booking_id='8c8565cf-4384-4474-a8c7-10a62b27ceed', flight_number="F123",
                         start_destination="City C", end_destination="City D",
                         takeoff_time="2023-08-10 14:00", landing_time="2023-08-10 16:00", price=123,
                         email='ivan@gmail.com', first_name='Ivan', last_name='Obreshkov')
    ]
    mock_get_user_by_uuid_service.return_value = MagicMock()
    mock_query_bookings_by_user_id.return_value = users_bookings_data
    response, status_code = get_user_bookings_service(user_id)
    assert status_code == 200
    assert "User's Bookings" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.get_user_by_uuid_service')
@patch('api.services.bookings_services.query_bookings_by_user_id')
@patch("api.services.bookings_services.close_db_session")
def test_get_user_bookings_service_not_existing_bookings(mock_close_db_session, mock_query_bookings_by_user_id,
                                                         mock_get_user_by_uuid_service):
    user_id = "user_1"

    mock_get_user_by_uuid_service.return_value = MagicMock()
    mock_query_bookings_by_user_id.return_value = []
    response, status_code = get_user_bookings_service(user_id)
    assert status_code == 404
    assert response == {"Message": f"User with uuid {user_id} has not booked any flights!"}
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.get_user_by_uuid_service')
@patch("api.services.bookings_services.close_db_session")
def test_get_user_bookings_service_non_existing_user(mock_close_db_session, mock_get_user_by_uuid_service):
    user_id = "Wrong user"

    mock_get_user_by_uuid_service.return_value = None
    response, status_code = get_user_bookings_service(user_id)
    assert status_code == 404
    assert response == {"Message": f"User with uuid {user_id} doesn't exist in the DB!"}
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.get_user_by_uuid_service')
@patch('api.services.bookings_services.query_bookings_by_user_id')
@patch("api.services.bookings_services.close_db_session")
def test_get_user_bookings_service_exception(mock_close_db_session, mock_query_bookings_by_user_id,
                                             mock_get_user_by_uuid_service):
    user_id = "user_1"

    mock_get_user_by_uuid_service.side_effect = Exception("Test exception")
    mock_query_bookings_by_user_id.side_effect = Exception("Test exception")
    response, status_code = get_user_bookings_service(user_id)
    assert status_code == 500
    assert response == {"Message": "Couldn't retrieve user's bookings from DB!",
                        "Error": "Test exception"}
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_booking_by_id')
@patch('api.services.bookings_services.delete_booking_from_db')
@patch("api.services.bookings_services.close_db_session")
def test_delete_booking_service_existing_booking(mock_close_db_session, mock_remove_booking, mock_query_booking_by_id):
    booking_id = 'booking_1'
    mock_query_booking_by_id.return_value = sample_booking
    response, status_code = delete_booking_service(booking_id)
    assert status_code == 200
    assert response == {"Message": f"User with uuid {booking_id} was removed successfully from the DB"}
    mock_remove_booking.assert_called_once_with(sample_booking)
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_booking_by_id')
@patch('api.services.bookings_services.delete_booking_from_db')
@patch("api.services.bookings_services.close_db_session")
def test_delete_booking_service_non_existing_booking(mock_close_db_session, mock_remove_booking,
                                                     mock_query_booking_by_id):
    booking_id = 'Wrong booking'
    mock_query_booking_by_id.return_value = None
    response, status_code = delete_booking_service(booking_id)
    assert status_code == 404
    assert response == {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}
    mock_remove_booking.assert_not_called()
    mock_close_db_session.assert_called_once()


@patch('api.services.bookings_services.query_booking_by_id')
@patch('api.services.bookings_services.delete_booking_from_db')
@patch("api.services.bookings_services.close_db_session")
@patch("api.services.bookings_services.db_rollback")
def test_delete_booking_service_non_existing_booking(mock_db_rollback, mock_close_db_session, mock_remove_booking,
                                                     mock_query_booking_by_id):
    booking_id = 'booking_1'
    mock_query_booking_by_id.side_effect = Exception("Test exception")
    mock_remove_booking.side_effect = Exception("Test exception")
    response, status_code = delete_booking_service(booking_id)
    assert status_code == 500
    assert response == {"Message": f"Couldn't delete booking with uuid {booking_id} from DB!",
                        "Error": "Test exception"}
    mock_remove_booking.assert_not_called()
    mock_close_db_session.assert_called_once()
    mock_db_rollback.assert_called_once()
