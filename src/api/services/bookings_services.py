from sqlalchemy.exc import IntegrityError

from api.services.flights_services import query_flight_by_flight_number
from api.services.users_services import get_user_by_uuid_service
from api.utilities.utils import handle_integrity_error
from api.db.repositories.user_bookings_repository import *


def add_booking_service(request):
    """Returns JSON formatted response containing a success message if the new booking was added to the DB
     or an error message along with corresponding status codes"""

    try:
        json_data = request.json

        user = get_user_by_uuid_service(json_data['user_id'])
        flight = query_flight_by_flight_number(json_data["flight_number"])

        return validate_and_add_booking(user, flight, json_data)

    except IntegrityError as e:
        db_rollback()
        return handle_integrity_error(e)
    except Exception as e:
        return {"Message": f"Couldn't create a new booking. Please try again later!", "Error": str(e)}, 500
    finally:
        close_db_session()


def create_booking(json_data):
    """Creates a new booking with the data from the request body"""

    new_booking = UserBookings(booking_id=uuid.uuid4(), user_id=json_data["user_id"],
                               flight_number=json_data["flight_number"])
    return new_booking


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
    if user is None:
        return {"Message": f"User with uuid {json_data['user_id']} doesn't exist in the DB!"}, 404

    if flight is None:
        return {"Message": f"Flight with number: {json_data['flight_number']} doesn't exist in the DB!"}, 404

    if check_booking_existence(json_data):
        return {
            "Message": f"User with uuid {json_data['user_id']} has already booked flight {flight.flight_number}!"}, 409

    new_booking = create_booking(json_data)
    add_booking_to_db(new_booking)
    return {"Message": "New booking added to DB!"}, 200


def get_bookings_service():
    """Returns JSON formatted response containing bookings data or an error message along with
    corresponding status codes"""

    try:
        all_bookings = query_all_bookings()

        if all_bookings:
            # When querying individual rows the row is a KeyedTuple which has an _asdict method
            bookings = [booking._asdict() for booking in all_bookings]
            return {"All bookings": bookings}, 200

        return {"Message": "The bookings table is empty"}, 404

    except Exception as e:
        return {"Message": "Couldn't retrieve bookings from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def get_booking_service(booking_id):
    """Returns JSON formatted response containing booking data or an error message along with
    corresponding status codes"""

    try:
        booking = query_booking_by_id(booking_id)
        if booking:
            return {"Booking": booking.to_json()}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404
    except Exception as e:
        return {"Message": f"Couldn't retrieve Booking with uuid {booking_id} from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def get_user_bookings_service(user_id):
    """Returns JSON formatted response containing the bookings of a given user or an error message along with
    corresponding status codes"""

    try:
        user = get_user_by_uuid_service(user_id)
        if user:
            all_user_bookings = query_bookings_by_user_id(user_id)
            if all_user_bookings:
                # When querying individual rows the row is a KeyedTuple which has an _asdict method
                user_bookings = [booking._asdict() for booking in all_user_bookings]
                return {"User's Bookings": user_bookings}, 200

            return {"Message": f"User with uuid {user_id} has not booked any flights!"}, 404

        return {"Message": f"User with uuid {user_id} doesn't exist in the DB!"}, 404
    except Exception as e:
        return {"Message": "Couldn't retrieve user's bookings from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def delete_booking_service(booking_id):
    """Returns JSON formatted response containing a success message if the booking was deleted from the DB
     or an error message along with corresponding status codes"""

    try:
        booking = query_booking_by_id(booking_id)
        if booking:
            delete_booking_from_db(booking)
            return {"Message": f"User with uuid {booking_id} was removed successfully from the DB"}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        db_rollback()
        return {"Message": f"Couldn't delete booking with uuid {booking_id} from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()

# We don't have an update_service as in the other files,
# because we decided that the booking would be immutable,
# as the user shouldn't be able to change which flight they have booked
