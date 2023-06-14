from flask import Blueprint

from database import db
from models.user_bookings_model import UserBookings

crud_bookings_bp = Blueprint("bookings",__name__)

@crud_bookings_bp.get("/bookings")
def get_bookings():
    try:
        all_bookings = db.session.query(UserBookings).all()
        bookings = [booking.to_json for booking in all_bookings]
        return {"All bookings": bookings}, 200
    except Exception as e:
        return {"Message": "Couldn't retrieve bookings from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()

