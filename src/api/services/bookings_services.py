import uuid

from sqlalchemy.exc import IntegrityError

from api.database import db
from api.models.flights_model import Flights
from api.models.user_bookings_model import UserBookings
from api.models.users_model import Users
from api.services.flights_services import query_flight_by_flight_number
from api.services.users_services import get_user_service
from api.utils import handle_integrity_error


def add_booking_service(request):
    """Returns JSON formatted response containing a success message if the new booking was added to the DB
     or an error message along with corresponding status codes"""

    try:
        json_data = request.json

        user = get_user_service(json_data['user_id'])
        flight = query_flight_by_flight_number(json_data["flight_number"])

        return validate_and_add_booking(user, flight, json_data)

    except IntegrityError as e:
        db.session.rollback()
        return handle_integrity_error(e)
    except Exception as e:
        return {"Message": f"Couldn't create a new booking. Please try again later!", "Error": str(e)}, 500
    finally:
        db.session.close()


def validate_and_add_booking(user, flight, json_data):
    """Checks if user, flight and booking exist
    Args:
        flight: retrieved flight obj from the database
        user: retrieved user obj from the database
        json_data: body of the post request
    Returns:
        - 200 status code, if booking is created
        - 409 status code if user has already booked that flight
        - 404 status code if user or flight doesn't exist
    """

    if user and flight:
        if check_booking_existence(json_data):
            return {"Message": f"User with uuid {user.id} has already booked flight {flight.flight_number}!"}, 409

        add_new_booking(json_data)
        return {"Message": "New booking added to DB!"}, 200

    elif not user:
        return {"Message": f"User with uuid {user.id} doesn't exist in the DB!"}, 404

    elif not flight:
        return {"Message": f"Flight with number: {flight.flight_number} doesn't exist in the DB!"}, 404


def add_new_booking(json_data):
    """Creates a new booking with the data from the request body and adds it to the database """

    new_booking = UserBookings(booking_id=uuid.uuid4(), user_id=json_data["user_id"],
                               flight_number=json_data["flight_number"])
    db.session.add(new_booking)
    db.session.commit()


def get_bookings_service():
    """Returns JSON formatted response containing bookings data or an error message along with
    corresponding status codes"""

    try:
        all_bookings = get_all_bookings()

        if all_bookings:
            # When querying individual rows the row is a KeyedTuple which has an _asdict method
            bookings = [booking._asdict() for booking in all_bookings]
            return {"All bookings": bookings}, 200

        return {"Message": "The bookings table is empty"}, 404

    except Exception as e:
        return {"Message": "Couldn't retrieve bookings from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


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


def get_booking_service(booking_id):
    """Returns JSON formatted response containing booking data or an error message along with
    corresponding status codes"""

    try:
        booking = get_booking_by_id(booking_id)
        if booking:
            return {"Booking": booking.to_json()}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404
    except Exception as e:
        return {"Message": f"Couldn't retrieve Booking with uuid {booking_id} from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


def get_booking_by_id(booking_id):
    """Retrieves a booking from the database by uuid"""

    booking = db.session.query(UserBookings).filter_by(booking_id=str(booking_id)).first()
    return booking


def get_user_bookings_service(user_id):
    """Returns JSON formatted response containing the bookings of a given user or an error message along with
    corresponding status codes"""

    try:
        user = get_user_service(user_id)
        if user:
            all_user_bookings = get_bookings_by_user_id(user_id)
            if all_user_bookings:
                # When querying individual rows the row is a KeyedTuple which has an _asdict method
                user_bookings = [booking._asdict() for booking in all_user_bookings]
                return {"User's Bookings": user_bookings}, 200

            return {"Message": f"User with uuid {user_id} has not booked any flights!"}, 404

        return {"Message": f"User with uuid {user_id} doesn't exist in the DB!"}, 404
    except Exception as e:
        return {"Message": "Couldn't retrieve user's bookings from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


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


def delete_booking_service(booking_id):
    """Returns JSON formatted response containing a success message if the booking was deleted from the DB
     or an error message along with corresponding status codes"""

    try:
        booking = get_booking_by_id(booking_id)
        if booking:
            remove_booking(booking)
            return {"Message": f"User with uuid {booking_id} was removed successfully from the DB"}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't delete booking with uuid {booking_id} from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


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
