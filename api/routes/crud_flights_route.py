import re
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request
from flask_expects_json import expects_json
from database import db
from models.flights_model import Flights

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

@crud_flights_bp.get("/flights")
def get_flights():
    try:
        all_flights = db.session.query(Flights).all()
        users_list = [flight.to_json() for flight in all_flights]

        return {"Flights": users_list}, 200
    except Exception as e:
        return {"Message": "Couldn't retrieve flights from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()

@crud_flights_bp.route("/flight", methods=['POST'])
@expects_json(flights_schema, check_formats=True)
def add_flight():
    try:
        json_data = request.json
        start_destination = json_data["start_destination"]
        end_destination = json_data["end_destination"]
        takeoff_time = json_data["takeoff_time"]
        landing_time = json_data['landing_time']
        price = json_data['price']

        new_flight = Flights(
            start_destination=start_destination,
            end_destination=end_destination,
            takeoff_time=takeoff_time,
            landing_time=landing_time,
            price=price

        )
        db.session.add(new_flight)
        db.session.commit()

        return {"Message": "New flight added to DB!"}

    except IntegrityError:
        # Handle integrity constraint violation (e.g., duplicate entry)
        return {"Message": "Flight already exists in the database."}, 409
    except Exception as e:
        # Handle any other exceptions or errors
        return {"Message": "Failed to add flight.", "Error": str(e)}, 500
    finally:
        db.session.close()
