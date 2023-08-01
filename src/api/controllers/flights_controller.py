import uuid

from api.database import db
from api.models.flights_model import Flights
from api.models.user_bookings_model import UserBookings
from api.models.users_model import Users


def create_flight(json_data):
    """Creates a new flight with the data from the request body and adds it to the database"""

    new_flight = Flights(flight_number=str(uuid.uuid4().hex)[:6].upper(),
                         start_destination=json_data["start_destination"],
                         end_destination=json_data["end_destination"],
                         takeoff_time=json_data["takeoff_time"],
                         landing_time=json_data['landing_time'],
                         price=json_data["price"])
    db.session.add(new_flight)
    db.session.commit()


def get_all_flights():
    """Retrieve all flights from the database
    Returns:
            list of all flights
    """
    all_flights = db.session.query(Flights).all()
    return all_flights


def get_flight_by_flight_number(flight_number):
    """Retrieves a flight from the database by flight_number (uuid)"""

    flight = db.session.query(Flights).get(flight_number)
    return flight


def get_passengers_on_flight(flight_number):
    """Retrieve all passengers (users) on a given flight
    Returns:
        list of users
    """

    all_passengers = db.session.query(UserBookings). \
        join(UserBookings.users). \
        join(UserBookings.flights). \
        with_entities(UserBookings.booking_id,
                      Users.id,
                      Users.email,
                      Users.first_name,
                      Users.last_name). \
        filter_by(flight_number=flight_number).all()
    return all_passengers


def delete_flight_from_db(flight):
    """Deletes a flight from the database"""

    db.session.delete(flight)
    db.session.commit()


def edit_flight_data(flight, json_data):
    """Updates the user with the provided data in the body of the request

    Parameters:
        flight: The Flight obj
        json_data: The body of the PUT request
    """

    flight.start_destination = json_data.get('start_destination', flight.start_destination)
    flight.end_destination = json_data.get('end_destination', flight.end_destination)
    flight.takeoff_time = json_data.get('takeoff_time', flight.takeoff_time)
    flight.landing_time = json_data.get('landing_time', flight.landing_time)
    flight.price = json_data.get('price', flight.price)
    db.session.commit()


def check_flight_existence(json_data):
    """Checks if a flight with the same start & destination, and takeoff & landing times exist
    Returns:
         True - if such flight exists,
         False - if such flight doesn't exist
    """

    existing_flight = db.session.query(Flights).filter_by(
        start_destination=json_data["start_destination"],
        end_destination=json_data["end_destination"],
        takeoff_time=json_data["takeoff_time"],
        landing_time=json_data['landing_time']).all()

    if existing_flight:
        return True

    return False


