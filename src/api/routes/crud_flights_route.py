from flask import Blueprint, request
from flask_expects_json import expects_json
from api.services.flights_services import *
from api.services.jwt_required_decorators import admin_required
from api.json_schemas import flights_schema, update_flight_schema

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
def get_flight(flight_number):
    try:
        flight = query_flight_by_flight_number(flight_number)
        if flight:
            return {"Flight": flight.to_json()}, 200

        return {"Message": f"Flight with number {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't retrieve flight with number {flight_number} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_flights_bp.get("/flights/<string:flight_number>/passengers")
@admin_required
def get_flight_passengers(flight_number):
    try:
        flight = query_flight_by_flight_number(flight_number)
        if flight:

            all_passengers = query_passengers_on_flight(flight_number)
            if all_passengers:
                # When querying individual rows the row is a KeyedTuple which has an _asdict method
                passengers = [passenger._asdict() for passenger in all_passengers]
                return {f"Passengers for flight {flight_number}": passengers}, 200

            return {"Message": f"Flight with number {flight_number} is empty!"}, 404

        return {"Message": f"Flight with number {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't passengers for flight {flight_number} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_flights_bp.delete("/flights/<string:flight_number>")
@admin_required
def delete_flight(flight_number):
    try:
        flight = query_flight_by_flight_number(flight_number)
        if flight:
            delete_flight_from_db(flight)
            return {"Message": f"Flight with number: {flight_number} was removed successfully from the DB"}, 200

        return {"Message": f"Flight with number: {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't delete flight with number: {flight_number} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_flights_bp.put("/flights/<string:flight_number_uuid>")
@admin_required
@expects_json(update_flight_schema, check_formats=True)
def update_flight(flight_number):
    try:
        flight = query_flight_by_flight_number(flight_number)
        if flight:
            json_data = request.json
            edit_flight_data(flight, json_data)

            return {"Message": f"Flight with number: {flight_number} was updated successfully."}, 200

        return {"Message": f"Flight with number: {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't update flight with number: {flight_number}", "Error": str(e)}, 500

    finally:
        db.session.close()
