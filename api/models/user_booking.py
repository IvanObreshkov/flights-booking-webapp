import uuid
import sqlalchemy
from sqlalchemy import ForeignKey, String, Column
from sqlalchemy.orm import relationship
from database import db
from users_model import Users
from flights_model import Flights
from base import Base


class UserBookings(db.Model, Base):
    booking_id = sqlalchemy.Column(sqlalchemy.String(10), primary_key=True, default=str(uuid.uuid4), unique=True)
    flight_number = Column(String, ForeignKey('flights.flight_number'), primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'), primary_key=True)

    user = relationship(Users, back_populates='flights')
    flight = relationship(Flights, back_populates='users')


    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

