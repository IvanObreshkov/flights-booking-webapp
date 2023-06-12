import uuid
import sqlalchemy
from sqlalchemy import ForeignKey, String, Column
from sqlalchemy.orm import relationship
from database import db
from users_model import Users
from flights_model import Flights


class UserBookings(db.Model):
    __tablename__ = 'user_bookings'


    booking_id = sqlalchemy.Column(sqlalchemy.String(10), primary_key=True, default=str(uuid.uuid4), unique=True)
    flight_number = Column(String, ForeignKey('flights.flight_number'), primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'), primary_key=True)

    user = relationship(Users, back_populates='flights')
    flight = relationship(Flights, back_populates='users')

    # FIXME
    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'flight_number': self.flight_number,
            'start_destination': self.start_destination,
            'end_destination': self.end_destination,
            'takeoff_time': self.takeoff_time,
            'landing_time': self.landing_time
        }

