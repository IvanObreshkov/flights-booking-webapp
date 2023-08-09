import uuid

from api.database import db
from api.models.flights_model import Flights
from api.models.user_bookings_model import UserBookings
from api.models.users_model import Users


def add_new_booking(json_data):
    """Creates a new booking with the data from the request body and adds it to the database """

    new_booking = UserBookings(booking_id=uuid.uuid4(), user_id=json_data["user_id"],
                               flight_number=json_data["flight_number"])
    db.session.add(new_booking)
    db.session.commit()


def get_all_bookings():
    """Retrieve all bookings from the database
    Returns:
            list of all bookings
    """

    all_bookings = db.session.query(UserBookings). \
        join(UserBookings.users). \
        join(UserBookings.flights). \
        with_entities(UserBookings.booking_id,
                      Flights.flight_number,
                      Flights.price,
                      Users.email,
                      Users.first_name,
                      Users.last_name).all()
    return all_bookings


def get_booking_by_id(booking_id):
    """Retrieves a booking from the database by uuid"""

    booking = db.session.query(UserBookings).filter_by(booking_id=str(booking_id)).first()
    return booking


def get_bookings_by_user_id(user_id):
    """Retrieve all user bookings by user_id

    Parameters:
        user_id (uuid): the uuid of the user

    Returns:
        list of all bookings of a given user

    """
    all_user_bookings = db.session.query(UserBookings). \
        join(UserBookings.users). \
        join(UserBookings.flights). \
        with_entities(UserBookings.booking_id, Flights.flight_number, Flights.start_destination,
                      Flights.end_destination, Flights.takeoff_time, Flights.takeoff_time, Flights.price,
                      Users.email,
                      Users.first_name,
                      Users.last_name). \
        filter_by(user_id=str(user_id)).all()
    return all_user_bookings


def remove_booking(booking):
    """Deletes a booking from the database"""

    db.session.delete(booking)
    db.session.commit()


def check_booking_existence(json_data):
    """Checks if a user has already booked a given flight
    Returns:
         True - if the user has already booked the flight,
         False - if the user hasn't booked the flight
    """

    existing_booking = db.session.query(UserBookings).filter_by(user_id=json_data["user_id"],
                                                                flight_number=json_data["flight_number"]).all()
    if existing_booking:
        return True

    return False
