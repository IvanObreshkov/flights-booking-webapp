from flask import Blueprint

from database import db
from models.flights_model import Flights

crud_flights_bp = Blueprint("flights",__name__)

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

