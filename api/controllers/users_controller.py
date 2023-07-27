import re
import uuid

import flask_bcrypt

from database import db
from models.users_model import Users


def create_user(data):
    """
    Create a new user object with the provided data.

    Parameters:
        data (dict): A dictionary containing user data with the following keys:
                     - "first_name" (str).
                     - "last_name" (str).
                     - "email" (str).
                     - "password" (str).

    Raises:
        ValueError: If any of the required fields (first_name, last_name, email, password)
                    are missing or empty, or if the email is not in a valid format.
    """

    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["password"]

    validate_data(data)

    hashed_password = flask_bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = Users(
        id=str(uuid.uuid4()),
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )

    return new_user


def validate_data(data):
    """
    Checks if the provided data is in valid format

    Parameters:
        data (dict): A dictionary containing user data with the following keys:
                     - "first_name" (str).
                     - "last_name" (str).
                     - "email" (str).
                     - "password" (str).

    Raises:
        ValueError: If any of the required fields (first_name, last_name, email, password)
                    are missing or empty, or if the email is not in a valid format.
    """

    for key in data:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if data[key].strip() == '':
            key_to_text_list = key.split('_')
            key_to_text = ' '.join(key_to_text_list)
            new_key = key_to_text.capitalize()
            raise ValueError(f'{new_key} cannot be empty!')

        if key == 'email':
            if not re.match(email_pattern, data[key]):
                key_to_text_list = key.split('_')
                key_to_text = ' '.join(key_to_text_list)
                new_key = key_to_text.capitalize()
                raise ValueError(f'{new_key} is not in a valid format!')


def add_user_to_db(user):
    """Adds the created user object to the database"""

    db.session.add(user)
    db.session.commit()
