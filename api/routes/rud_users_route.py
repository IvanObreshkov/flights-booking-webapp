# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, request

from database import db
from models.users_model import Users

crud_users_bp = Blueprint("crud_users", __name__)


@crud_users_bp.route("/users", methods=["GET"])
def get_users():
    if request.method == "GET":
        try:
            all_users = db.session.query(Users).all()
            users_list = [user.to_json() for user in all_users]
            return {"Users": users_list}
        except Exception as e:
            return {"Message": "Couldn't retrieve users from DB!", "Error": str(e)}, 500
        finally:
            db.session.close()

@crud_users_bp.route("/users/<uuid:user_uuid>",methods=["GET","PUT","DELETE"])
def gud_user(user_uuid):
    if request.method == "GET":
        try:
            user = db.session.query(Users).get(user_uuid)
            if user:
                return user.to_json()
            return {"Message": f"The user with {user_uuid}doesn't exist in the DB!"}, 404
        except Exception as e:
            return {"Message": "Couldn't retrieve user from DB!", "Error": str(e)}, 500
        finally:
            db.session.close()

