import uuid

import sqlalchemy

from database import db


class Flights(db.Model):
    flight_number = sqlalchemy.Column(sqlalchemy.String(6), primary_key=True, default=str(uuid.uuid4().hex)[:6].upper(),
                                      nullable=False, unique=True)
    start_destination = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    end_destination = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    takeoff_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    landing_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
