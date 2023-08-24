import re
import uuid

import flask_bcrypt

from api.db.repositories.users_repository import *


def create_user_service(data):
    """
    Creates a new user object with the provided data.

    Parameters:
        data (dict): A dictionary containing user data:
                     - "first_name" (str).
                     - "last_name" (str).
                     - "email" (str).
                     - "password" (str).

    Return:
        The created User object
    """

    validate_data(data)

    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["password"]

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
        data (dict): A dictionary containing user data:

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


def get_users_service():
    """Returns JSON formatted response containing users data or an error message along with
    corresponding status codes"""

    try:
        all_users = query_all_users()
        users_list = [user.to_json() for user in all_users]
        if users_list:
            return {"Users": users_list}, 200
        return {"Message": "The users table is empty"}, 404
    except Exception as e:
        return {"Message": "Couldn't retrieve users from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def get_user_by_uuid_service(user_uuid):
    """Returns JSON formatted response containing flight data or an error message along with
        corresponding status codes"""

    try:
        user = query_user_by_uuid(user_uuid)
        if user:
            return {"User": user.to_json()}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404
    except Exception as e:
        return {"Message": f"Couldn't retrieve user with uuid {user_uuid} from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def delete_user_service(user_uuid):
    """Returns JSON formatted response containing a success message if the user was deleted from the DB
     or an error message along with corresponding status codes"""

    try:
        user = query_user_by_uuid(user_uuid)
        if user:
            delete_user_from_db(user)
            return {"Message": f"User with uuid {user_uuid} was removed successfully from the DB"}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404
    except Exception as e:
        db_rollback()
        return {"Message": f"Couldn't delete user with uuid {user_uuid} from DB!", "Error": str(e)}, 500
    finally:
        close_db_session()


def update_user_service(user_uuid, request):
    """Returns JSON formatted response containing a success message if the user was altered
        successfully in the DB or an error message along with corresponding status codes"""

    try:
        user = query_user_by_uuid(user_uuid)
        if user:
            json_data = request.json
            edit_user_data(user, json_data)

            return {"Message": f"User with uuid {user_uuid} was updated successfully."}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404
    except Exception as e:
        db_rollback()
        return {"Message": f"Couldn't update user with uuid {user_uuid}", "Error": str(e)}, 500
    finally:
        close_db_session()
