import os
import re
import time
import uuid

import jwt
from flask import Blueprint, request
from flask_expects_json import expects_json
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from database import db
from models.flights_model import Flights
from models.user_bookings_model import UserBookings
from models.users_model import Users

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
@expects_json(flights_schema, check_formats=True)
def add_flight():
    try:
        json_data = request.json
        start_destination = json_data["start_destination"]
        end_destination = json_data["end_destination"]
        takeoff_time = json_data["takeoff_time"]
        landing_time = json_data['landing_time']
        price = json_data['price']


        existing_flight = db.session.query(Flights).filter_by(start_destination=start_destination, end_destination=end_destination,
                                                              takeoff_time=takeoff_time, landing_time=landing_time).all()
        if not existing_flight:
            new_flight = Flights(
                flight_number=str(uuid.uuid4().hex)[:6].upper(),
                start_destination=start_destination,
                end_destination=end_destination,
                takeoff_time=takeoff_time,
                landing_time=landing_time,
                price=price
            )
            db.session.add(new_flight)
            db.session.commit()

            return {"Message": "New flight added to DB!"}

        return {"Message":"Cannot add the certain flight! A flight with the same data already exist in the database!"}

    except IntegrityError as e:
        db.session.rollback()
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, str(e))
        if matches:
            return {"Error": f"{matches[0]}"}, 409
    except Exception as e:
        # Handle any other exceptions and errors
        raise InternalServerError(f"Couldn't create a new flight. Please try again later!, Error: {str(e)}")
    finally:
        db.session.close()

@crud_flights_bp.get("/flights")
def get_flights():
    token = jwt.decode(request.cookies.get("token"), os.getenv("SECRET_KEY"), algorithms=["HS256"])
    # FIXME:
    #   - PyJWT automatically checks that the token has expired and returns 500 status code
    if int(time.time()) - token["exp"] >= 60:
        return {"Message": "Auth token expired."}, 498
    if token["admin"]:
        try:
            all_flights = db.session.query(Flights).all()
            users_list = [flight.to_json() for flight in all_flights]

            return {"Flights": users_list}, 200
        except Exception as e:
            return {"Message": "Couldn't retrieve flights from DB!", "Error": str(e)}, 500
        finally:
            db.session.close()
    else:
        return {"Message": "You don't have access to this resource"}, 403

@crud_flights_bp.get("/flights/<flight_number>")
def get_flight(flight_number):
    # TODO: Add BEARER TOKEN

    try:
        flight = db.session.query(Flights).get(flight_number)
        if flight:
            return {"Flight": flight.to_json()}, 200

        return {"Message": f"Flight with uuid {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't retrieve flight with number {flight_number} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()

@crud_flights_bp.get("/flights/<string:flight_number>/passengers")
def get_flight_passengers(flight_number):
    # TODO: Add Bearer Token

    try:
        flight = db.session.query(Flights).get(flight_number)
        if flight:
            all_passengers = db.session.query(UserBookings). \
                join(UserBookings.users). \
                join(UserBookings.flights). \
                with_entities(UserBookings.booking_id,
                              Users.id,
                              Users.email,
                              Users.first_name,
                              Users.last_name). \
                filter_by(flight_number=flight_number).all()

            # When querying individual rows the row is a KeyedTuple which has an _asdict method
            passengers = [passenger._asdict() for passenger in all_passengers]

            return {f"Passengers for flight {flight_number}": passengers}, 200

        return {"Message": f"Flight with uuid {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't passengers for flight {flight_number} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()

@crud_flights_bp.delete("/flights/<string:flight_number_uuid>")
def delete_user(flight_number_uuid):
    # TODO: Add BEARER TOKEN

    try:
        user = db.session.query(Flights).get(flight_number_uuid)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"Message": f"Flight with number: {flight_number_uuid} was removed successfully from the DB"}, 200

        return {"Message": f"Flight with number: {flight_number_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't delete flight with number: {flight_number_uuid} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@crud_flights_bp.put("/flights/<string:flight_number_uuid>")
@expects_json(update_flight_schema, check_formats=True)
def update_flight(flight_number_uuid):
    # TODO: Add BEARER TOKEN

    try:
        flight = db.session.query(Flights).get(flight_number_uuid)
        if flight:
            json_data = request.json
            flight.start_destination = json_data.get('start_destination', flight.start_destination)
            flight.end_destination = json_data.get('end_destination', flight.end_destination)
            flight.takeoff_time = json_data.get('takeoff_time', flight.takeoff_time)
            flight.landing_time = json_data.get('landing_time', flight.landing_time)
            flight.price = json_data.get('price', flight.price)
            db.session.commit()
            return {"Message": f"Flight with number: {flight_number_uuid} was updated successfully."}, 200

        return {"Message": f"Flight with number: {flight_number_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't update flight with number: {flight_number_uuid}", "Error": str(e)}, 500

    finally:
        db.session.close()
