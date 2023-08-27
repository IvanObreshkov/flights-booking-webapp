import uuid

from sqlalchemy.exc import IntegrityError

from api.db.repositories.flights_repository import *
from utilities.utils import handle_integrity_error


def add_flight_service(request):
    """Returns JSON formatted response containing a success message if the flight was added to the DB
     or an error message along with corresponding status codes"""

    try:
        json_data = request.json
        if check_flight_existence(json_data):
            return {"Message": "Cannot add the certain flight! "
                               "A flight with the same data already exist in the database!"}, 409
        new_flight = create_flight(json_data)
        add_flight_to_db(new_flight)
        return {"Message": "New flight added to DB!"}, 200
    except IntegrityError as e:
        db_rollback()
        handle_integrity_error(e)
    except Exception as e:
        return {"Message": f"Couldn't create a new flight. Please try again later!", "Error": str(e)}, 500
    finally:
        close_db_session()


def create_flight(json_data):
    """Creates a new flight with the data from the request body"""

    flight = Flights(flight_number=str(uuid.uuid4().hex)[:6].upper(),
                     start_destination=json_data["start_destination"],
                     end_destination=json_data["end_destination"],
                     takeoff_time=json_data["takeoff_time"],
                     landing_time=json_data['landing_time'],
                     price=json_data["price"])
    return flight


def get_flights_service():
    """Returns JSON formatted response containing flights data or an error message along with
    corresponding status codes"""

    try:
        all_flights = query_all_flights()
        flights_list = [flight.to_json() for flight in all_flights]
        if all_flights:
            return {"Flights": flights_list}, 200
        return {"Message": "The flights table is empty"}, 404
    except Exception as e:
        return {"Message": "Couldn't retrieve flights from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def get_flight_service(flight_number):
    """Returns JSON formatted response containing flight data or an error message along with
    corresponding status codes"""

    try:
        flight = query_flight_by_flight_number(flight_number)
        if flight:
            return {"Flight": flight.to_json()}, 200

        return {"Message": f"Flight with number {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't retrieve flight with number {flight_number} from DB!", "Error": str(e)}, 500

    finally:
        close_db_session()


def get_flight_passengers_service(flight_number):
    """Returns JSON formatted response containing passengers' infor or an error message along with
    corresponding status codes"""

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
        return {"Message": f"Couldn't retrieve passengers for flight {flight_number} from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def delete_flight_service(flight_number):
    """Returns JSON formatted response containing a success message if the flight was deleted from the DB
     or an error message along with corresponding status codes"""

    try:
        flight = query_flight_by_flight_number(flight_number)
        if flight:
            delete_flight_from_db(flight)
            return {"Message": f"Flight with number: {flight_number} was removed successfully from the DB"}, 200

        return {"Message": f"Flight with number: {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        db_rollback()
        return {"Message": f"Couldn't delete flight with number: {flight_number} from DB!", "Error": str(e)}, 500

    finally:
        close_db_session()


def update_flight_service(flight_number, request):
    """Returns JSON formatted response containing a success message if the flight was altered
    successfully in the DB or an error message along with corresponding status codes"""

    try:
        flight = query_flight_by_flight_number(flight_number)
        if flight:
            json_data = request.json
            edit_flight_data(flight, json_data)

            return {"Message": f"Flight with number: {flight_number} was updated successfully."}, 200

        return {"Message": f"Flight with number: {flight_number} doesn't exist in the DB!"}, 404

    except Exception as e:
        db_rollback()
        return {"Message": f"Couldn't update flight with number: {flight_number}", "Error": str(e)}, 500

    finally:
        close_db_session()
