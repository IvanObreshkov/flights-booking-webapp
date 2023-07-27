import re
import uuid

from flask import Blueprint, request
from flask_expects_json import expects_json
from sqlalchemy.exc import IntegrityError

from database import db
from models.flights_model import Flights
from models.user_bookings_model import UserBookings
from models.users_model import Users
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
        user_id = json_data["user_id"]
        flight_number = json_data["flight_number"]

        user = db.session.query(Users).get(user_id)
        flight = db.session.query(Flights).get(flight_number)

        if user and flight:

            existing_booking = db.session.query(UserBookings).filter_by(user_id=user_id, flight_number=flight_number).all()
            if not existing_booking:
                new_booking = UserBookings(booking_id=uuid.uuid4(), user_id=user_id, flight_number=flight_number)
                db.session.add(new_booking)
                db.session.commit()

                return {"Message": "New booking added to DB!"}, 200

            return {"Message": f"User with uuid {user_id} has already booked flight {flight_number}!"}, 409

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
        all_bookings = db.session.query(UserBookings). \
            join(UserBookings.users). \
            join(UserBookings.flights). \
            with_entities(UserBookings.booking_id, Flights.flight_number, Flights.price, Users.email, Users.first_name,
                          Users.last_name). \
            all()

        # When querying individual rows the row is a KeyedTuple which has an _asdict method
        bookings = [booking._asdict() for booking in all_bookings]

        return {"All bookings": bookings}, 200

    except Exception as e:
        return {"Message": "Couldn't retrieve bookings from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()

@crud_bookings_bp.get("/bookings/<uuid:user_id>")
@admin_or_user_id_required
def get_user_bookings(user_id):
    try:
        user = db.session.query(Users).get(user_id)
        if user:
            all_user_bookings = db.session.query(UserBookings). \
                join(UserBookings.users). \
                join(UserBookings.flights). \
                with_entities(UserBookings.booking_id, Flights.flight_number, Flights.start_destination,
                              Flights.end_destination, Flights.takeoff_time, Flights.takeoff_time, Flights.price,
                              Users.email,
                              Users.first_name,
                              Users.last_name). \
                filter_by(user_id=str(user_id)).all()

            # When querying individual rows the row is a KeyedTuple which has an _asdict method
            bookings = [booking._asdict() for booking in all_user_bookings]

            return {"User's Bookings": bookings}, 200

        return {"Message": f"User with uuid {user_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": "Couldn't retrieve user's bookings from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_bookings_bp.delete("/bookings/<uuid:booking_id>")
@admin_required
def delete_booking(booking_id):
    try:
        booking = db.session.query(UserBookings).filter_by(booking_id=str(booking_id)).first()
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


