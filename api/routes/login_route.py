from flask_bcrypt import check_password_hash
from dotenv import load_dotenv
from flask import Blueprint, request, render_template, make_response
from werkzeug.exceptions import InternalServerError

from controllers.users_controller import validate_data, get_user_by_email
from services.jwt_creation import create_jwt

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
    try:
        data = request.form
        validate_data(data)

        email = data["email"]
        raw_password = data["password"]

        user = get_user_by_email(email)
        if user:
            hashed_user_password = user.password

            if check_password_hash(hashed_user_password, raw_password):

                token = create_jwt(user, raw_password)
                resp = make_response(render_template('login.html', msg=str(token)))
                resp.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
                return resp

            return render_template('login.html', msg="Invalid password!"), 401

        return render_template('login.html', msg="User doesn't exist in the DB"), 404

    except ValueError as e:
        return render_template('login.html', msg=str(e)), 400
    except Exception as e:
        raise InternalServerError(f'Login failed! Please try again later!, Error: {str(e)}')

@login_bp.get("/login")
def get_login_form():
    return render_template("login.html"), 200
