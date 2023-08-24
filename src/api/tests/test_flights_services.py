from collections import namedtuple
from unittest.mock import patch, MagicMock

import pytest

from api.app import create_app
from api.config import TestConfig
from api.services.flights_services import *


@pytest.fixture
def sample_flight():
    return Flights(
        flight_number="F123",
        start_destination="City A",
        end_destination="City B",
        takeoff_time="2023-08-10 10:00",
        landing_time="2023-08-10 12:00",
        price=200.0
    )


@pytest.fixture
def sample_flight_list():
    return [
        Flights(
            flight_number="F123",
            start_destination="City A",
            end_destination="City B",
            takeoff_time="2023-08-10 10:00",
            landing_time="2023-08-10 12:00",
            price=200.0
        ),
        Flights(
            flight_number="F456",
            start_destination="City C",
            end_destination="City D",
            takeoff_time="2023-08-10 14:00",
            landing_time="2023-08-10 16:00",
            price=250.0
        ),
    ]


@pytest.fixture()
def empty_flights_table():
    return []


@patch('api.services.flights_services.check_flight_existence')
@patch('api.services.flights_services.add_flight_to_db')
@patch('api.services.flights_services.create_flight')
@patch('api.services.flights_services.close_db_session')
def test_add_flight_service(mock_close_db_session, mock_create_flight, mock_add_flight_to_db,
                            mock_check_flight_existence):
    mock_request = MagicMock()
    mock_request.json = {"data": "flight_data"}
    mock_check_flight_existence.return_value = False
    mock_create_flight.return_value = sample_flight
    response, status_code = add_flight_service(mock_request)
    assert status_code == 200
    assert response == {"Message": "New flight added to DB!"}
    mock_add_flight_to_db.called_once_with(sample_flight)
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.check_flight_existence')
@patch('api.services.flights_services.add_flight_to_db')
@patch('api.services.flights_services.close_db_session')
def test_add_flight_service_existing_flight(mock_close_db_session, mock_add_flight_to_db, mock_check_flight_existence):
    mock_request = MagicMock()
    mock_request.json = {"data": "existing_flight"}
    mock_check_flight_existence.return_value = True
    response, status_code = add_flight_service(mock_request)
    assert status_code == 409
    assert response == {
        'Message': 'Cannot add the certain flight! A flight with the same data already exist in the database!'}
    mock_add_flight_to_db.assert_not_called()
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.check_flight_existence')
@patch('api.services.flights_services.add_flight_to_db')
@patch('api.services.flights_services.create_flight')
@patch('api.services.flights_services.close_db_session')
def test_add_flight_service_exception(mock_close_db_session, mock_create_flight, mock_add_flight_to_db,
                                      mock_check_flight_existence):
    mock_request = MagicMock()
    mock_request.json = {"data": "existing_flight"}
    mock_check_flight_existence.return_value = False
    mock_create_flight.return_value = sample_flight
    mock_add_flight_to_db.side_effect = Exception("Test exception")
    response, status_code = add_flight_service(mock_request)
    assert status_code == 500
    assert response == {"Message": f"Couldn't create a new flight. Please try again later!",
                        "Error": "Test exception"}
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_all_flights')
@patch('api.services.flights_services.close_db_session')
def test_get_flights_service_not_empty(mock_close_db_session, mock_query_all_flights, sample_flight_list):
    mock_query_all_flights.return_value = sample_flight_list
    response, status_code = get_flights_service()
    assert status_code == 200
    assert "Flights" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_all_flights')
@patch('api.services.flights_services.close_db_session')
def test_get_flights_service_empty(mock_close_db_session, mock_query_all_flights):
    mock_query_all_flights.return_value = []
    response, status_code = get_flights_service()
    assert status_code == 404
    assert response == {"Message": "The flights table is empty"}
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_all_flights')
@patch('api.services.flights_services.close_db_session')
def test_get_flights_service_exception(mock_close_db_session, mock_query_all_flights):
    mock_query_all_flights.side_effect = Exception("Test exception")
    response, status_code = get_flights_service()
    assert status_code == 500
    assert response == {
        "Message": "Couldn't retrieve flights from DB!",
        "Error": "Test exception",
    }
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.close_db_session')
def test_get_flight_service_existing(mock_close_db_session, mock_query_flight, sample_flight):
    mock_query_flight.return_value = sample_flight
    response, status_code = get_flight_service("F123")
    assert status_code == 200
    assert "Flight" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.close_db_session')
def test_get_flight_service_non_existing(mock_close_db_session, mock_query_flight):
    mock_query_flight.return_value = None
    response, status_code = get_flight_service("Wrong FN")
    assert status_code == 404
    assert response == {"Message": "Flight with number Wrong FN doesn't exist in the DB!"}
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.close_db_session')
def test_get_flight_service_exception(mock_close_db_session, mock_query_flight):
    mock_query_flight.side_effect = Exception("Test exception")
    response, status_code = get_flight_service("F123")
    assert status_code == 500
    assert response == {
        "Message": "Couldn't retrieve flight with number F123 from DB!",
        "Error": "Test exception",
    }
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.query_passengers_on_flight')
@patch('api.services.flights_services.close_db_session')
def test_get_flight_passengers_service_full_flight(mock_close_db_session, mock_query_passengers, mock_query_flight):
    flight_number = "F123"
    mock_query_flight.return_value = sample_flight
    PassengerRow = namedtuple('PassengerRow', ['booking_id', 'uuid', 'email', 'first_name', 'last_name'])

    passengers_data = [
        PassengerRow(booking_id='70e4c838-a57d-46fc-9050-c94b6ab946e9', uuid='cd3348a0-5164-46c0-8ae1-30787c6cb6ea',
                     email='dani@gmail.com', first_name='Dani', last_name='Ivanov'),
        PassengerRow(booking_id='8c8565cf-4384-4474-a8c7-10a62b27ceed', uuid='46916341-3133-4fe0-8520-cc630a185c9f',
                     email='ivan@gmail.com', first_name='Ivan', last_name='Obreshkov')
    ]
    mock_query_passengers.return_value = passengers_data

    response, status_code = get_flight_passengers_service(flight_number)
    assert status_code == 200
    assert f"Passengers for flight {flight_number}" in response
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.close_db_session')
def test_get_flight_passengers_service_wrong_flight_number(mock_close_db_session, mock_query_flight):
    flight_number = "Wrong number"
    mock_query_flight.return_value = None

    response, status_code = get_flight_passengers_service(flight_number)
    assert status_code == 404
    assert response == {"Message": f"Flight with number {flight_number} doesn't exist in the DB!"}
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.query_passengers_on_flight')
@patch('api.services.flights_services.close_db_session')
def test_get_flight_passengers_service_empty_flight(mock_close_db_session, mock_query_passengers, mock_query_flight):
    flight_number = "F123"
    mock_query_flight.return_value = sample_flight
    mock_query_passengers.return_value = []

    response, status_code = get_flight_passengers_service(flight_number)
    assert status_code == 404
    assert response == {"Message": f"Flight with number {flight_number} is empty!"}
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.query_passengers_on_flight')
@patch('api.services.flights_services.close_db_session')
def test_get_flight_passengers_service_exception(mock_close_db_session, mock_query_passengers, mock_query_flight):
    flight_number = "F123"
    mock_query_flight.side_effect = Exception("Test exception")
    mock_query_passengers.side_effect = Exception("Test exception")

    response, status_code = get_flight_passengers_service(flight_number)
    assert status_code == 500
    assert response == {
        "Message": f"Couldn't retrieve passengers for flight {flight_number} from DB!",
        "Error": "Test exception",
    }
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.delete_flight_from_db')
@patch('api.services.flights_services.close_db_session')
def test_delete_flight_service_existing_flight(mock_close_db_session, mock_delete_flight, mock_query_flight):
    flight_number = "F123"
    mock_query_flight.return_value = sample_flight

    response, status_code = delete_flight_service(flight_number)
    assert status_code == 200
    assert response == {"Message": f"Flight with number: {flight_number} was removed successfully from the DB"}
    mock_delete_flight.assert_called_once()
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.delete_flight_from_db')
@patch('api.services.flights_services.close_db_session')
def test_delete_flight_service_wrong_flight_number(mock_close_db_session, mock_delete_flight, mock_query_flight):
    flight_number = "Wrong number"
    mock_query_flight.return_value = None

    response, status_code = delete_flight_service(flight_number)
    assert status_code == 404
    assert response == {"Message": f"Flight with number: {flight_number} doesn't exist in the DB!"}
    mock_delete_flight.assert_not_called()
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.delete_flight_from_db')
@patch('api.services.flights_services.close_db_session')
@patch("api.services.flights_services.db_rollback")
def test_delete_flight_service_exception(mock_db_rollback, mock_close_db_session, mock_delete_flight,
                                         mock_query_flight):
    flight_number = "F123"
    mock_delete_flight.side_effect = Exception("Test exception")
    mock_query_flight.side_effect = Exception("Test exception")

    response, status_code = delete_flight_service(flight_number)
    assert status_code == 500
    assert response == {"Message": f"Couldn't delete flight with number: {flight_number} from DB!",
                        "Error": "Test exception"}
    mock_delete_flight.assert_not_called()
    mock_close_db_session.assert_called_once()
    mock_db_rollback.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.edit_flight_data')
@patch('api.services.flights_services.close_db_session')
def test_update_flight_service_existing_flight(mock_close_db_session, mock_edit_flight_data, mock_query_flight):
    flight_number = "F123"
    mock_query_flight.return_value = sample_flight
    request = MagicMock()
    request.json = {"price": 400}
    response, status_code = update_flight_service(flight_number, request)
    assert status_code == 200
    assert response == {"Message": f"Flight with number: {flight_number} was updated successfully."}
    mock_edit_flight_data.assert_called_once_with(sample_flight, request.json)
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.edit_flight_data')
@patch('api.services.flights_services.close_db_session')
def test_update_flight_service_wrong_flight_number(mock_close_db_session, mock_edit_flight_data, mock_query_flight):
    flight_number = "Wrong number"
    mock_query_flight.return_value = None
    request = MagicMock()
    request.json = {"price": 400}
    response, status_code = update_flight_service(flight_number, request)
    assert status_code == 404
    assert response == {"Message": f"Flight with number: {flight_number} doesn't exist in the DB!"}
    mock_edit_flight_data.assert_not_called()
    mock_close_db_session.assert_called_once()


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.edit_flight_data')
@patch('api.services.flights_services.close_db_session')
@patch("api.services.flights_services.db_rollback")
def test_update_flight_service_exception(mock_db_rollback, mock_close_db_session, mock_edit_flight_data,
                                         mock_query_flight):
    flight_number = "F123"
    mock_query_flight.side_effect = Exception("Test exception")
    mock_edit_flight_data.side_effect = Exception("Test exception")
    request = MagicMock()
    request.json = {"price": 400}
    response, status_code = update_flight_service(flight_number, request)
    assert status_code == 500
    assert response == {'Message': "Couldn't update flight with number: F123",
                        "Error": "Test exception"}
    mock_edit_flight_data.assert_not_called()
    mock_close_db_session.assert_called_once()
    mock_db_rollback.assert_called_once()
