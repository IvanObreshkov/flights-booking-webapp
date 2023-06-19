import uuid

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import db


class UserBookings(db.Model):
    __tablename__ = "user_bookings"

    booking_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True, default=str(uuid.uuid4()), unique=True)
    flight_number = sqlalchemy.Column(ForeignKey('flights.flight_number'), primary_key=True)
    user_id = sqlalchemy.Column(ForeignKey('users.id'), primary_key=True)

    users = relationship("Users", back_populates="user_bookings")
    flights = relationship("Flights", back_populates="user_bookings")

    # FIXME
    def to_json(self):
        return {
            'id': self.booking_id,
            'flight_number': self.flight_number,
            'user_id': self.user_id
        }
