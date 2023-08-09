# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, render_template
from flask import request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from api.services.users_services import create_user, add_user_to_db
from api.database import db
from api.utils import handle_integrity_error

register_bp = Blueprint("register", __name__)


@register_bp.post("/register")
def register_user():
    try:
        data = request.form
        new_user = create_user(data)
        add_user_to_db(new_user)

        return render_template('register.html', msg="New user added to DB!"), 200

    except ValueError as e:
        # Handle validation errors.
        return render_template('register.html', msg=str(e)), 400

    except IntegrityError as e:
        db.session.rollback()
        handle_integrity_error(e)

    except Exception as e:
        # Handle any other exceptions and errors
        raise InternalServerError(f'Registration failed! Please try again later!, Error: {str(e)}')

    finally:
        db.session.close()


@register_bp.get("/register")
def get_register_form():
    return render_template("register.html"), 200
