from flask import Blueprint
from flask_expects_json import expects_json

from api.json_schemas import bookings_schema
from api.services.bookings_services import *
from api.services.jwt_required_decorators import *

crud_bookings_bp = Blueprint("bookings", __name__)


@crud_bookings_bp.post("/bookings")
@require_admin_or_user_to_book_a_flight
@expects_json(bookings_schema, check_formats=True)
def add_booking_route():
    return add_booking_service(request)


@crud_bookings_bp.get("/bookings")
@admin_required
def get_bookings_route():
    return get_bookings_service()


@crud_bookings_bp.get("/bookings/<uuid:booking_id>")
# FIXME fix the decorator
# @admin_or_user_id_required
def get_booking_route(booking_id):
    return get_booking_service(booking_id)


@crud_bookings_bp.get("/users/<uuid:user_id>/bookings")
# @admin_or_user_id_required
def get_user_bookings_route(user_id):
    get_user_bookings_service(user_id)


@crud_bookings_bp.delete("/bookings/<uuid:booking_id>")
@admin_required
def delete_booking_route(booking_id):
    delete_booking_service(booking_id)
