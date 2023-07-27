import re

from flask import Blueprint, request
from flask_expects_json import expects_json
from sqlalchemy.exc import IntegrityError

from controllers.bookings_controller import *
from controllers.flights_controller import get_flight_by_flight_number
from controllers.users_controller import get_user_by_uuid
from database import db
from services.jwt_required_decorators import admin_required, admin_or_user_id_required, \
    require_admin_or_user_to_book_a_flight

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


@crud_bookings_bp.post("/bookings")
@require_admin_or_user_to_book_a_flight
@expects_json(bookings_schema, check_formats=True)
def add_booking():
    try:
        json_data = request.json
        user_id = json_data['user_id']
        flight_number = json_data["flight_number"]

        user = get_user_by_uuid(user_id)
        flight = get_flight_by_flight_number(flight_number)

        if user and flight:
            if check_booking_existence(json_data):
                return {"Message": f"User with uuid {user_id} has already booked flight {flight_number}!"}, 409

            add_new_booking(json_data)
            return {"Message": "New booking added to DB!"}, 200

        elif not user:
            return {"Message": f"User with uuid {user_id} doesn't exist in the DB!"}, 404

        elif not flight:
            return {"Message": f"Flight with number: {flight_number} doesn't exist in the DB!"}, 404

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


@crud_bookings_bp.get("/bookings")
@admin_required
def get_bookings():
    try:
        all_bookings = get_all_bookings()

        if all_bookings:
            # When querying individual rows the row is a KeyedTuple which has an _asdict method
            bookings = [booking._asdict() for booking in all_bookings]
            return {"All bookings": bookings}, 200

        return {"Message": "The bookings database is empty"}, 404

    except Exception as e:
        return {"Message": "Couldn't retrieve bookings from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


@crud_bookings_bp.get("/bookings/<uuid:booking_id>")
@admin_or_user_id_required
def get_booking(booking_id):
    try:
        booking = get_booking_by_id(booking_id)
        if booking:
            return {"Booking": booking.to_json()}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't retrieve Booking with uuid {booking_id} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_bookings_bp.get("users/<uuid:user_id>/bookings")
@admin_or_user_id_required
def get_user_bookings(user_id):
    try:
        user = get_user_by_uuid(user_id)
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


@crud_bookings_bp.delete("/bookings/<uuid:booking_id>")
@admin_required
def delete_booking(booking_id):
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
