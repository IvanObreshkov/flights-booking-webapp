from collections import namedtuple
from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy import Row

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


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@patch('api.services.flights_services.query_all_flights')
def test_get_flights_service_not_empty(mock_query_all_flights, sample_flight_list, app):
    mock_query_all_flights.return_value = sample_flight_list
    response, status_code = get_flights_service()
    assert status_code == 200
    assert "Flights" in response


@patch('api.services.flights_services.query_all_flights')
def test_get_flights_service_empty(mock_query_all_flights, app):
    mock_query_all_flights.return_value = []
    response, status_code = get_flights_service()
    assert status_code == 404
    assert response == {"Message": "The flights table is empty"}


@patch('api.services.flights_services.query_all_flights')
def test_get_flights_service_exception(mock_query_all_flights, app):
    mock_query_all_flights.side_effect = Exception("Test exception")
    response, status_code = get_flights_service()
    assert status_code == 500
    assert response == {
        "Message": "Couldn't retrieve flights from DB!",
        "Error": "Test exception",
    }


@patch('api.services.flights_services.query_flight_by_flight_number')
def test_get_flight_service_existing(mock_query_flight, sample_flight, app):
    mock_query_flight.return_value = sample_flight
    response, status_code = get_flight_service("F123")
    assert status_code == 200
    assert "Flight" in response


@patch('api.services.flights_services.query_flight_by_flight_number')
def test_get_flight_service_non_existing(mock_query_flight, app):
    mock_query_flight.return_value = None
    response, status_code = get_flight_service("Wrong FN")
    assert status_code == 404
    assert response == {"Message": "Flight with number Wrong FN doesn't exist in the DB!"}


@patch('api.services.flights_services.query_flight_by_flight_number')
def test_get_flight_service_exception(mock_query_flight, app):
    mock_query_flight.side_effect = Exception("Test exception")
    response, status_code = get_flight_service("F123")
    assert status_code == 500
    assert response == {
        "Message": "Couldn't retrieve flight with number F123 from DB!",
        "Error": "Test exception",
    }


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.query_passengers_on_flight')
def test_get_flight_passengers_service_full_flight(mock_query_passengers, mock_query_flight, app):
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


@patch('api.services.flights_services.query_flight_by_flight_number')
def test_get_flight_passengers_service_wrong_flight_number(mock_query_flight, app):
    flight_number = "Wrong number"
    mock_query_flight.return_value = None

    response, status_code = get_flight_passengers_service(flight_number)
    assert status_code == 404
    assert response == {"Message": f"Flight with number {flight_number} doesn't exist in the DB!"}


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.query_passengers_on_flight')
def test_get_flight_passengers_service_empty_flight(mock_query_passengers, mock_query_flight, app):
    flight_number = "F123"
    mock_query_flight.return_value = sample_flight
    mock_query_passengers.return_value = []

    response, status_code = get_flight_passengers_service(flight_number)
    assert status_code == 404
    assert response == {"Message": f"Flight with number {flight_number} is empty!"}


@patch('api.services.flights_services.query_flight_by_flight_number')
@patch('api.services.flights_services.query_passengers_on_flight')
def test_get_flight_passengers_service_exception(mock_query_passengers, mock_query_flight, app):
    flight_number = "F123"
    mock_query_flight.side_effect = Exception("Test exception")
    mock_query_passengers.side_effect = Exception("Test exception")

    response, status_code = get_flight_passengers_service(flight_number)
    assert status_code == 500
    assert response == {
        "Message": f"Couldn't retrieve passengers for flight {flight_number} from DB!",
        "Error": "Test exception",
    }
