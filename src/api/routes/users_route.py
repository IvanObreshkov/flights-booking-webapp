# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, request
from flask_expects_json import expects_json

from api.services.users_services import *
from api.database import db
from api.services.jwt_required_decorators import admin_required
from json_schemas import update_users_schema

rud_users_bp = Blueprint("crud_users", __name__)


@rud_users_bp.get("/users")
@admin_required
def get_users_route():
    get_users_service()


@rud_users_bp.get("/users/<uuid:user_uuid>")
@admin_required
def get_user_route(user_uuid):
    return get_user_service(user_uuid)


@rud_users_bp.delete("/users/<uuid:user_uuid>")
@admin_required
def delete_user(user_uuid):
    try:
        user = query_user_by_uuid(user_uuid)
        if user:
            delete_user_from_db(user)
            return {"Message": f"User with uuid {user_uuid} was removed successfully from the DB"}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't delete user with uuid {user_uuid} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@rud_users_bp.put("/users/<uuid:user_uuid>")
@admin_required
@expects_json(update_users_schema, check_formats=True)
def update_user(user_uuid):
    try:
        user = query_user_by_uuid(user_uuid)
        if user:
            json_data = request.json
            edit_user_data(user, json_data)

            return {"Message": f"User with uuid {user_uuid} was updated successfully."}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't update user with uuid {user_uuid}", "Error": str(e)}, 500

    finally:
        db.session.close()
