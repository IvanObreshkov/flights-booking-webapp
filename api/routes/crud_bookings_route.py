import re

from flask import Blueprint, request
from flask_expects_json import expects_json
from sqlalchemy.exc import IntegrityError

from database import db
from models.flights_model import Flights
from models.user_bookings_model import UserBookings
from models.users_model import Users

crud_bookings_bp = Blueprint("bookings", __name__)

bookings_schema = {
    'type': 'object',
    'properties': {
        'flight_number': {'type': 'string'},
        'user_id': {'type': 'string'},
    },
    'required': ['flight_number', 'user_id'],
    'additionalProperties': False
}

@crud_bookings_bp.get("/bookings")
def get_bookings():
    # TODO: Add Bearer Token

    try:
        all_bookings = db.session.query(UserBookings). \
            join(UserBookings.users). \
            join(UserBookings.flights). \
            with_entities(UserBookings.booking_id, Flights.flight_number, Flights.price ,Users.email, Users.first_name,
                          Users.last_name). \
            all()

        # When querying individual rows the row is a KeyedTuple which has an _asdict method
        bookings = [booking._asdict() for booking in all_bookings]

        return {"All bookings": bookings}, 200

    except Exception as e:
        return {"Message": "Couldn't retrieve bookings from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


@crud_bookings_bp.get("/bookings/<uuid:booking_id>")
def get_booking(booking_id):
    # TODO: Add Bearer Token

    try:
        booking = db.session.query(UserBookings).get(booking_id)
        if booking:
            return {"Booking": booking.to_json()}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't retrieve booking with uuid {booking_id} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_bookings_bp.get("/bookings/<uuid:user_id>")
def get_user_bookings(user_id):
    # TODO: Add Bearer Token

    try:
        user = db.session.query(Users).get(user_id)
        if user:
            user_bookings = db.session.query(UserBookings).filter_by(UserBookings.user_id == user_id).all()

            # TODO: Show all info for flights
            bookings = [booking.to_json for booking in user_bookings]
            return {f"All bookings for user with uuid {user_id}": bookings}, 200

        return {"Message": f"User with uuid {user_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": "Couldn't retrieve user's bookings from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_bookings_bp.delete("/bookings/<uuid:booking_id>")
def delete_user(booking_id):
    # TODO: Add BEARER TOKEN

    try:
        booking = db.session.query(UserBookings).get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return {"Message": f"User with uuid {booking_id} was removed successfully from the DB"}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't delete booking with uuid {booking_id} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_bookings_bp.post("/bookings")
@expects_json(bookings_schema, check_formats=True)
def add_booking():
    try:
        json_data = request.json
        user_id = json_data["user_id"]
        flight_number = json_data["flight_number"]

        new_booking = UserBookings(user_id=user_id, flight_number=flight_number)

        db.session.add(new_booking)
        db.session.commit()

        return {"Message": "New booking added to DB!"}

    except IntegrityError as e:
        db.session.rollback()
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, str(e))
        if matches:
            return {"Error": f"{matches[0]}"}, 409
    except Exception as e:
        return {"Message": f"Couldn't create a new booking. Please try again later!", "Error": str(e)}, 500
    finally:
        db.session.close()
