import os
import uuid

import flask_bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from api.db.models.flights_model import Flights
from api.db.models.user_bookings_model import UserBookings
from api.db.models.users_model import Users

load_dotenv()

# FIXME or remove, there is a problem with the imports

# Create the database engine
db_uri = os.getenv("MYSQL_TEST_DATABASE_URI")
engine = create_engine(db_uri)

if not database_exists(engine.url):
    create_database(engine.url)

# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Create tables if they don't exist
# Flights.metadata.create_all(engine)
# Users.metadata.create_all(engine)
# UserBookings.metadata.create_all(engine)

# # Seed data for Flights
# flights_data = [
#     {"start_destination": "London", "end_destination": "Sofia", "takeoff_time": "2023-07-30 06:45",
#      "landing_time": "2023-07-30 09:15", "price": 235.70, "flight_number": str(uuid.uuid4().hex)[:6].upper()},
#     {"start_destination": "Paris", "end_destination": "Rome", "takeoff_time": "2023-08-03 11:35",
#      "landing_time": "2023-08-03 13:10", "price": 273.40, "flight_number": str(uuid.uuid4().hex)[:6].upper()},
#     {"start_destination": "Berlin", "end_destination": "Skopje", "takeoff_time": "2023-07-17 16:00",
#      "landing_time": "2023-07-17 18:20", "price": 179.90, "flight_number": str(uuid.uuid4().hex)[:6].upper()},
# ]

# for flight in flights_data:
#     new_flight = Flights(
#         flight_number=flight["flight_number"],
#         start_destination=flight["start_destination"],
#         end_destination=flight["end_destination"],
#         takeoff_time=flight["takeoff_time"],
#         landing_time=flight["landing_time"],
#         price=flight["price"]
#     )
#     session.add(new_flight)
#     session.commit()

# # Seed data for Users
# users_data = [
#     {
#         "id": str(uuid.uuid4()),
#         "first_name": "Jermain",
#         "last_name": "Defoe",
#         "email": "jermaind@gmail.com",
#         "password": "password123"
#     },
#     {
#         "id": str(uuid.uuid4()),
#         "first_name": "Jane",
#         "last_name": "Smith",
#         "email": "janesm@gmail.com",
#         "password": "password456"
#     },
#     {
#         "id": str(uuid.uuid4()),
#         "first_name": "Borislav",
#         "last_name": "Angelov",
#         "email": "boroangelov@gmail.com",
#         "password": "password789"
#     }
# ]

# for user in users_data:
#     hashed_password = flask_bcrypt.generate_password_hash(user["password"]).decode("utf-8")
#     new_user = Users(
#         id=user["id"],
#         first_name=user["first_name"],
#         last_name=user["last_name"],
#         email=user["email"],
#         password=hashed_password
#     )
#     session.add(new_user)
#     session.commit()

# bookings_data = [
#     {
#         "user_id": users_data[2]["id"],
#         "flight_number": flights_data[1]["flight_number"],
#         "booking_id": uuid.uuid4()
#     },
#     {
#         "user_id": users_data[1]["id"],
#         "flight_number": flights_data[0]["flight_number"],
#         "booking_id": uuid.uuid4()
#     },
#     {
#         "user_id": users_data[0]["id"],
#         "flight_number": flights_data[2]["flight_number"],
#         "booking_id": uuid.uuid4()
#     }
# ]

# for booking in bookings_data:
#     user_id = booking["user_id"],
#     flight_number = booking["flight_number"],
#     booking_id = booking["booking_id"]

#     user = session.get(Users, user_id)
#     flight = session.get(Flights, flight_number)
#     existing_booking = session.query(UserBookings).filter_by(user_id=user_id,
#                                                                 flight_number=flight_number).all()
#     if not existing_booking:
#         new_booking = UserBookings(booking_id=booking_id, user_id=user_id, flight_number=flight_number)
#         session.add(new_booking)
#         session.commit()
# # Commit the changes
# session.commit()
# session.close()
# print("Data seeded...")
