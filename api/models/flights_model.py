import uuid

import sqlalchemy
from sqlalchemy.orm import relationship

from database import db
from user_booking import UserBookings


class Flights(db.Model):
    __tablename__ = 'flights'

    flight_number = sqlalchemy.Column(sqlalchemy.String(6), primary_key=True, default=str(uuid.uuid4().hex)[:6].upper(),
                                      nullable=False, unique=True)
    start_destination = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    end_destination = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    takeoff_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    landing_time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    users_bookings = relationship(UserBookings, back_populates='flights')

    def to_json(self):
        return {
            'flight_number': self.flight_number,
            'start_destination': self.start_destination,
            'end_destination': self.end_destination,
            'takeoff_time': self.takeoff_time,
            'landing_time': self.landing_time
        }
