# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

import re

from werkzeug.exceptions import BadRequest

import sqlalchemy
from flask import Blueprint
from flask import request
from flask_bcrypt import Bcrypt
from flask_expects_json import expects_json

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


@register_bp.route("/register", methods=['POST'])
@expects_json(schema, check_formats=True)
def register_user():
    try:
        json_data = request.json
        first_name = json_data["first_name"]
        last_name = json_data["last_name"]
        email = json_data["email"]
        password = json_data["password"]
        hashed_password = Bcrypt.generate_password_hash(password,10).decode("utf-8")

        # TODO:
        #  - Implement JWT
        #  - Send verification emails

        new_user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return {"Message": "New user added to DB!"}

    except Exception as e:
        db.session.rollback()
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, str(e))
        if matches:
            return {"Error": f"{matches[0]}"}, 409
        else:
            return {"Error": f"{str(e)}"}, 500
    except KeyError as e:
        # Handle missing or invalid JSON properties
        raise BadRequest(f'Missing or invalid property: {e}')
    except Exception as e:
        # Handle any other exceptions and errors
        raise BadRequest('Registration failed! Please try again later!')
    finally:
        db.session.close()
