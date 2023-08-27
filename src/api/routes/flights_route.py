from flask import Blueprint, request
from flask_expects_json import expects_json
from api.services.flights_services import *
from utilities.jwt_required_decorators import admin_required
from utilities.json_schemas import flights_schema, update_flight_schema

crud_flights_bp = Blueprint("flights", __name__)


@crud_flights_bp.post("/flights")
@admin_required
@expects_json(flights_schema, check_formats=True)
def add_flight_route():
    return add_flight_service(request)


@crud_flights_bp.get("/flights")
@admin_required
def get_flights_route():
    return get_flights_service()


@crud_flights_bp.get("/flights/<flight_number>")
@admin_required
def get_flight_route(flight_number):
    return get_flight_service(flight_number)


@crud_flights_bp.get("/flights/<string:flight_number>/passengers")
@admin_required
def get_flight_passengers_route(flight_number):
    return get_flight_passengers_service(flight_number)


@crud_flights_bp.delete("/flights/<string:flight_number>")
@admin_required
def delete_flight_route(flight_number):
    return delete_flight_service(flight_number)


@crud_flights_bp.put("/flights/<string:flight_number_uuid>")
@admin_required
@expects_json(update_flight_schema, check_formats=True)
def update_flight_route(flight_number):
    return update_flight_service(flight_number, request)
