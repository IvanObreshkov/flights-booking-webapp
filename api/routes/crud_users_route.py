# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, request

from database import db
from models.users_model import Users

crud_users_bp = Blueprint("curd_users", __name__)


@crud_users_bp.route("/users", methods=["GET"])
def users_handler():
    if request.method == "GET":
        try:
            return get_users()
        except Exception as e:
            return {"Message": "Couldn't retrieve users from DB!", "Error": str(e)}, 500
        finally:
            db.session.close()


def get_users():
    all_users = db.session.query(Users).all()
    users_list = [user.to_json() for user in all_users]
    response = {"Users": users_list}
    return response
