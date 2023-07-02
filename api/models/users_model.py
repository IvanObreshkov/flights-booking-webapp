import sqlalchemy
from sqlalchemy.orm import relationship
from database import db


class Users(db.Model):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.String(36), primary_key=True,
                           nullable=False, unique=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=False,
                              unique=True)
    password = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    user_bookings = relationship("UserBookings", back_populates="users",
                                 cascade="all")

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,

        }
