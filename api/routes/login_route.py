import datetime
import os

import jwt
from dotenv import load_dotenv
from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from flask_expects_json import expects_json
from database import db
from models.users_model import Users

login_bp = Blueprint("login", __name__)
flask_bcrypt = Bcrypt()
load_dotenv()

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

    user = db.session.query(Users).filter_by(email=email).first()
    if user:
        hashed_user_password = user.password

        if flask_bcrypt.check_password_hash(hashed_user_password,
                                            raw_password):
            if os.getenv("ADMIN_EMAIL") == user.email and os.getenv(
                    "ADMIN_PASSWORD") == user.password:
                payload = {"sub": user.id,
                           "name": f"{user.first_name} {user.last_name}",
                           "email": user.email, "admin": True,
                           "exp": datetime.datetime.utcnow() + datetime.timedelta(
                               hours=1)}
            else:
                payload = {"sub": user.id,
                           "name": f"{user.first_name} {user.last_name}",
                           "email": user.email, "admin": False,
                           "exp": datetime.datetime.utcnow() + datetime.timedelta(
                               hours=1)}

            token = jwt.encode(payload, os.getenv("SECRET_KEY"),
                               algorithm="HS256")

            return {"Token": token}

        return {"Message": "Invalid password!"}, 401

    return {"Message": "User doesn't exist in the DB"}, 404
