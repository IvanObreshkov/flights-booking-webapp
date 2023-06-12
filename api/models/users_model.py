import uuid
import sqlalchemy
from sqlalchemy.orm import relationship
from database import db
from base import Base

class Users(db.Model, Base):
    __tablename__ = 'users'

    user_id = sqlalchemy.Column(sqlalchemy.String(36), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    user_bookings = relationship('UserBookings', back_populates='users')

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }