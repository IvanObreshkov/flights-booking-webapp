from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from flask_expects_json import expects_json

from database import db
from models.users_model import Users

login_bp = Blueprint("login", __name__)
flask_bcrypt = Bcrypt()
login_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password'],
    'additionalProperties': False
}


@login_bp.post("/login")
@expects_json(login_schema, check_formats=True)
def login_users():
    json_data = request.json
    email = json_data["email"]
    raw_password = json_data["password"]

    check_user = db.session.query(Users).filter_by(email=email).first()
    if check_user:
        hashed_user_password = check_user.password

        if flask_bcrypt.check_password_hash(hashed_user_password,
                                            raw_password):
            print()

        return {"Message": "Invalid password!"}, 401

    return {"Message": "User doesn't exist in the DB"}, 404q
