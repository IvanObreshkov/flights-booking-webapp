from flask_bcrypt import check_password_hash
from dotenv import load_dotenv
from flask import Blueprint, request, render_template, make_response
from werkzeug.exceptions import InternalServerError

from api.services.users_services import validate_data, get_user_by_email
from api.services.jwt_creation import create_jwt

login_bp = Blueprint("login", __name__)
load_dotenv()


@login_bp.post("/login")
def login_users():
    try:
        data = request.form
        validate_data(data)

        email = data["email"]
        raw_password = data["password"]

        user = get_user_by_email(email)
        return validate_user(raw_password, user), 200

    except ValueError as e:
        return render_template('login.html', msg=str(e)), 400
    except Exception as e:
        raise InternalServerError(f'Login failed! Please try again later!, Error: {str(e)}')


def validate_user(raw_password, user):
    """Checks if user exists and check if they entered a valid password
    Parameters:
        raw_password: password from login form
        user: retrieved user obj from the database
    Returns:
        200 status code, jwt token and login form if user is valid
        401 status code if password is Invalid,
        404 status code if user doesn't exist
    """

    if user:
        hashed_user_password = user.password

        if check_password_hash(hashed_user_password, raw_password):
            token = create_jwt(user, raw_password)
            resp = make_response(render_template('login.html', msg=str(token)))
            resp.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
            return resp

        return render_template('login.html', msg="Invalid password!"), 401
    return render_template('login.html', msg="User doesn't exist in the DB"), 404


@login_bp.get("/login")
def get_login_form():
    return render_template("login.html"), 200
