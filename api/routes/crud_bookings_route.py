from flask import Blueprint

from database import db
from models.user_bookings_model import UserBookings

crud_bookings_bp = Blueprint("bookings", __name__)


@crud_bookings_bp.get("/bookings")
def get_bookings():
    # TODO: Add Bearer Token

    try:
        all_bookings = db.session.query(UserBookings).all()
        bookings = [booking.to_json for booking in all_bookings]
        return {"All bookings": bookings}, 200
    except Exception as e:
        return {"Message": "Couldn't retrieve bookings from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()

@crud_bookings_bp.get("/bookings/<uuid:booking_id>")
def get_booking(booking_id):
    try:
        booking = db.session.query(UserBookings).get(booking_id)
        if booking:
            return {"Booking": booking.to_json()}, 200

        return {"Message": f"Booking with uuid {booking_id} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": "Couldn't retrieve booking from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()

