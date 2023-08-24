import uuid

from api.db.database import db
from api.db.models.flights_model import Flights
from api.db.models.user_bookings_model import UserBookings
from api.db.models.users_model import Users


def query_all_bookings():
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


def query_booking_by_id(booking_id):
    """Retrieves a booking from the database by uuid"""

    booking = db.session.query(UserBookings).filter_by(booking_id=str(booking_id)).first()
    return booking


def query_bookings_by_user_id(user_id):
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
                      Flights.end_destination, Flights.takeoff_time, Flights.landing_time, Flights.price,
                      Users.email,
                      Users.first_name,
                      Users.last_name). \
        filter_by(user_id=str(user_id)).all()
    return all_user_bookings


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


def delete_booking_from_db(booking):
    """Deletes a booking from the database"""

    db.session.delete(booking)
    db.session.commit()


def add_booking_to_db(new_booking):
    """Creates a new booking with the data from the request body and adds it to the database """

    db.session.add(new_booking)
    db.session.commit()


def close_db_session():
    db.session.close()


def db_rollback():
    db.session.rollback()
