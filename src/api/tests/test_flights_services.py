import pytest
from unittest.mock import patch
from api.services.flights_services import *
from api.app import create_app
from api.config import TestConfig


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
