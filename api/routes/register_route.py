# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

import re
import uuid

import flask_bcrypt
from flask import Blueprint, render_template
from flask import request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from database import db
from models.users_model import Users

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
    try:
        data = request.form
        print(data)
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        password = data["password"]
        hashed_password = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8")

        # TODO:
        #  - Implement JWT
        #  - Send verification emails

        new_user = Users(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return render_template('register.html', msg="New user added to DB!")

    except IntegrityError as e:
        db.session.rollback()
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, str(e))
        if matches:
            return render_template('register.html', msg=f"{matches[0]}"), 409
    except Exception as e:
        # Handle any other exceptions and errors
        raise InternalServerError(
            f'Registration failed! Please try again later!, Error: {str(e)}')
    finally:
        db.session.close()


@register_bp.get("/register")
def get_register_form():
    return render_template("register.html"), 200
