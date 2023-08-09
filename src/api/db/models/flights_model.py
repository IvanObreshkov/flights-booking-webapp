import sqlalchemy
from sqlalchemy.orm import relationship

from api.db.database import db


class Flights(db.Model):
    __tablename__ = "flights"

    flight_number = sqlalchemy.Column(sqlalchemy.String(6), primary_key=True,
                                      nullable=False, unique=True)
    start_destination = sqlalchemy.Column(sqlalchemy.String(255),
                                          nullable=False)
    end_destination = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    takeoff_time = sqlalchemy.Column(sqlalchemy.String(16), nullable=False)
    landing_time = sqlalchemy.Column(sqlalchemy.String(16), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Double, nullable=False)

    user_bookings = relationship("UserBookings", back_populates="flights",
                                 cascade="all")

    def to_json(self):
        return {
            'flight_number': self.flight_number,
            'start_destination': self.start_destination,
            'end_destination': self.end_destination,
            'takeoff_time': self.takeoff_time,
            'landing_time': self.landing_time,
            'price': self.price
        }
