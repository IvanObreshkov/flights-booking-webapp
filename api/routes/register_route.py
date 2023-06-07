# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

import re

import sqlalchemy
from flask import Blueprint
from flask import request
from flask_expects_json import expects_json

from database import db
from models.users_model import Users

register_bp = Blueprint("register", __name__)

schema = {
    'type': 'object',
    'properties': {
        'frst_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['first_name', 'last_name', 'email', 'password']
}


@register_bp.route("/register", methods=['POST'])
@expects_json(schema)
def register():
    json_data = request.json
    first_name = json_data["first_name"]
    last_name = json_data["last_name"]
    email = json_data["email"]
    password = json_data["password"]

    # TODO:
    #  - Hash password
    #  - Implement JWT
    #  - Send verification emails

    try:
        new_user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        return {"Message": "New user added to DB!"}

    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        pattern = r"\"(.*?)\""
        matches = re.findall(pattern, str(e))
        if matches:
            return {"Error": f"{matches[0]}"}, 409
        else:
            return {"Error": f"{str(e)}"}, 500
    finally:
        db.session.close()
