from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from api.db.database import db


class Users(db.Model):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True,
                nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False,
                   unique=True)
    verified = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)

    user_bookings = relationship("UserBookings", back_populates="users",
                                 cascade="all")

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'verified': self.verified
        }
