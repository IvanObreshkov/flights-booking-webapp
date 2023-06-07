import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, create_database

from models.flights_model import Flights
from models.users_model import Users

load_dotenv()

# Create the database engine
db_uri = os.getenv("MYSQL_DATABASE_URI")
engine = create_engine(db_uri)

if not database_exists(engine.url):
    create_database(engine.url)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
Flights.metadata.create_all(engine)
Users.metadata.create_all(engine)

# Seed data for Flights
flights_data = [
    {"start_destination": "London", "end_destination": "Sofia", "takeoff_time": 1352177617,
     "landing_time": 1007873885},
    {"start_destination": "Varna", "end_destination": "Plovidv", "takeoff_time": 1868917941,
     "landing_time": 1322466274},
    {"start_destination": "Frankfurt", "end_destination": "New York", "takeoff_time": 1408940875,
     "landing_time": 1755671246},
]

for flight in flights_data:
    new_flight = Flights(
        flight_number=str(uuid.uuid4().hex)[:6].upper(),
        start_destination=flight["start_destination"],
        end_destination=flight["end_destination"],
        takeoff_time=flight["takeoff_time"],
        landing_time=flight["landing_time"]
    )
    session.add(new_flight)

# Seed data for Users
users_data = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "password123"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "password": "password456"
    },
]

for user in users_data:
    new_user = Users(
        id=str(uuid.uuid4()),
        first_name=user["first_name"],
        last_name=user["last_name"],
        email=user["email"],
        password=user["password"]
    )
    session.add(new_user)

# Commit the changes
session.commit()

print("Data seeded...")
