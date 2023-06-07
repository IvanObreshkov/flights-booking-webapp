# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, request

from database import db
from models.users_model import Users

rud_users_bp = Blueprint("crud_users", __name__)


@rud_users_bp.get("/users")
def get_users():
    # TODO: Add BEARER TOKEN

    if request.method == "GET":
        try:
            all_users = db.session.query(Users).all()
            users_list = [user.to_json() for user in all_users]

            return {"Users": users_list}, 200
        except Exception as e:
            return {"Message": "Couldn't retrieve users from DB!", "Error": str(e)}, 500
        finally:
            db.session.close()


@rud_users_bp.get("/users/<uuid:user_uuid>")
def get_user(user_uuid):
    # TODO: Add BEARER TOKEN

    try:
        user = db.session.query(Users).get(user_uuid)
        if user:
            return user.to_json(), 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404
    except Exception as e:
        return {"Message": "Couldn't retrieve user from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()


@rud_users_bp.delete("/users/<uuid:user_uuid>")
def delete_user(user_uuid):
    try:
        user = db.session.query(Users).get(user_uuid)
        if user:
            db.session.delete(user)
            raise Exception("Mama vi")
            return {"Message": f"User with uuid {user_uuid} was removed successfully from the DB"}, 200
        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404
    except Exception as e:
        db.session.rollback()
        return {"Message": "Couldn't retrieve user from DB!", "Error": str(e)}, 500
    finally:
        db.session.commit()
        db.session.close()

# TODO: Add PUT method