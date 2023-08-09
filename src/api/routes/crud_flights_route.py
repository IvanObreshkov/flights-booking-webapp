from flask import Blueprint, request
from flask_expects_json import expects_json
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from services.flights_services import *
from api.database import db
from api.services.jwt_required_decorators import admin_required
from api.utils import handle_integrity_error

crud_flights_bp = Blueprint("flights", __name__)

flights_schema = {
    'type': 'object',
    'properties': {
        'start_destination': {'type': 'string'},
        'end_destination': {'type': 'string'},
        'takeoff_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 15:30"]
                         },
        'landing_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 17:15"]
                         },
        'price': {'type': 'number'}
    },
    'required': ['start_destination', 'end_destination', 'takeoff_time', 'landing_time', 'price'],
    'additionalProperties': False
}

update_flight_schema = {
    'type': 'object',
    'properties': {
        'start_destination': {'type': 'string'},
        'end_destination': {'type': 'string'},
        'takeoff_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 15:30"]
                         },
        'landing_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 17:15"]
                         },
        'price': {'type': 'number'}
    },
    'additionalProperties': False
}


@crud_flights_bp.post("/flights")
@admin_required
@expects_json(flights_schema, check_formats=True)
def add_flight():
    try:
        json_data = request.json
        if check_flight_existence(json_data):
            return {"Message": "Cannot add the certain flight! "
                               "A flight with the same data already exist in the database!"}
        new_flight = create_flight(json_data)
        add_flight_to_db(new_flight)
        return {"Message": "New flight added to DB!"}

    except IntegrityError as e:
        db.session.rollback()
        handle_integrity_error(e)
    except Exception as e:
        # Handle any other exceptions and errors
        raise InternalServerError(f"Couldn't create a new flight. Please try again later!, Error: {str(e)}")
    finally:
        db.session.close()


@crud_flights_bp.get("/flights")
@admin_required
def get_flights():
    try:
        all_flights = get_all_flights()
        flights_list = [flight.to_json() for flight in all_flights]
        if flights_list:
            return {"Flights": flights_list}, 200
        return {"Message": "The flights table is empty"}, 404
    except Exception as e:
        return {"Message": "Couldn't retrieve flights from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


@crud_flights_bp.get("/flights/<flight_number>")
@admin_required
def get_flight(flight_number):
    try:
        flight = get_flight_by_flight_number(flight_number)
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
        flight = get_flight_by_flight_number(flight_number)
        if flight:

            all_passengers = get_passengers_on_flight(flight_number)
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
        flight = get_flight_by_flight_number(flight_number)
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
        flight = get_flight_by_flight_number(flight_number)
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
