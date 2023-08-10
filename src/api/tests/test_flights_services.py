import pytest

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
def mock_query_all_flights(mocker):
    return mocker.patch("api.db.repositories.flights_repository.query_all_flights")


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


def test_get_flights_service_not_empty(mock_query_all_flights, sample_flight_list, app):
    mock_query_all_flights.return_value = sample_flight_list
    response, status_code = get_flights_service()
    assert status_code == 200
    assert "Flights" in response
