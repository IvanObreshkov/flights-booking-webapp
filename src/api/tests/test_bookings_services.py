import pytest

from app import create_app
from config import TestConfig
from db.models.user_bookings_model import UserBookings


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
