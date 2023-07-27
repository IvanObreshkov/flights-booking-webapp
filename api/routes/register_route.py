# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

import re

from flask import Blueprint, render_template
from flask import request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from controllers.users_controller import create_user, add_user_to_db
from database import db

register_bp = Blueprint("register", __name__)

schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'}
    },
    'required': ['first_name', 'last_name', 'email', 'password'],
    'additionalProperties': False
}


@register_bp.post("/register")
def register_user():
    """Endpoint handling registration of new users"""

    try:
        data = request.form
        new_user = create_user(data)
        add_user_to_db(new_user)

        return render_template('register.html', msg="New user added to DB!")

    except ValueError as e:
        # Handle validation errors.
        return render_template('register.html', msg=str(e)), 400

    except IntegrityError as e:
        db.session.rollback()
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, str(e))
        if matches:
            return render_template('register.html', msg=f"{matches[0]}"), 409

    except Exception as e:
        # Handle any other exceptions and errors
        raise InternalServerError(f'Registration failed! Please try again later!, Error: {str(e)}')

    finally:
        db.session.close()


@register_bp.get("/register")
def get_register_form():
    return render_template("register.html"), 200
