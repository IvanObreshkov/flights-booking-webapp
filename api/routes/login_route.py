import datetime
import os
import re

import flask_bcrypt
import jwt
from dotenv import load_dotenv
from flask import Blueprint, request, render_template, make_response

from database import db
from models.users_model import Users

login_bp = Blueprint("login", __name__)
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
def login_users():
    email = request.form["email"]
    raw_password = request.form["password"]

    for key in request.form:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if request.form[key].strip() == '':
            key_to_text_list = key.split('_')
            key_to_text = ' '.join(key_to_text_list)
            new_key = key_to_text.capitalize()
            return render_template('login.html', msg=f'{new_key} cannot be empty!')

        if key == 'email':
            if not re.match(email_pattern, request.form[key]):
                key_to_text_list = key.split('_')
                key_to_text = ' '.join(key_to_text_list)
                new_key = key_to_text.capitalize()
                return render_template('login.html', msg=f'{new_key} is not in a valid format!')

    user = db.session.query(Users).filter_by(email=email).first()
    if user:
        hashed_user_password = user.password

        if flask_bcrypt.check_password_hash(hashed_user_password,
                                            raw_password):
            if os.getenv("ADMIN_EMAIL") == user.email and os.getenv(
                    "ADMIN_PASSWORD") == raw_password:
                # TODO:
                #   - Add refresh token logic

                # FIXME:
                #   - Change exp time to what in the industry standard for access_tokens

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
            resp = make_response(render_template('login.html', msg=str(token)))
            resp.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
            return resp

        return render_template('login.html', msg="Invalid password!"), 401

    return render_template('login.html', msg="User doesn't exist in the DB"), 404


@login_bp.get("/login")
def get_login_form():
    return render_template("login.html"), 200
