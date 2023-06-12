import uuid

import sqlalchemy
from sqlalchemy.orm import relationship

from database import db
from base import Base

class Flights(db.Model, Base):
    __tablename__ = 'flights'

    flight_number = sqlalchemy.Column(sqlalchemy.String(6), primary_key=True, default=str(uuid.uuid4().hex)[:6].upper(),
                                      nullable=False, unique=True)
    start_destination = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    end_destination = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    takeoff_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    landing_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    users_bookings = relationship('UserBookings', back_populates='flights')
