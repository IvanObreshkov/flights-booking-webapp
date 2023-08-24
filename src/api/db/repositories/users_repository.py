from api.db.database import db
from api.db.models.users_model import Users


def query_all_users():
    """Retrieves all users from the db.
    Returns:
         list of all users
    """

    all_users = db.session.query(Users).all()
    return all_users


def query_user_by_uuid(user_uuid):
    """Retrieves the user from the db by UUID.

    Returns:
        User obj
    """

    user = db.session.query(Users).get(user_uuid)
    return user


def query_user_by_email(email):
    """Retrieves the user from the db by email.

    Returns:
        User obj
    """

    user = db.session.query(Users).filter_by(email=email).first()
    return user


def add_user_to_db(user):
    """Adds the created user object to the database"""

    db.session.add(user)
    db.session.commit()


def delete_user_from_db(user):
    """Deletes the user from the database"""

    db.session.delete(user)
    db.session.commit()


def edit_user_data(user, json_data):
    """Updates the user with the provided data in the body of the request

    Parameters:
        user: The User obj
        json_data: The body of the PUT request
    """

    user.first_name = json_data.get('first_name', user.first_name)
    user.last_name = json_data.get('last_name', user.last_name)
    user.email = json_data.get('email', user.email)
    user.password = json_data.get('password', user.password)
    db.session.commit()


def close_db_session():
    db.session.close()


def db_rollback():
    db.session.rollback()
