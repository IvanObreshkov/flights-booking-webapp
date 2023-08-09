# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, request
from flask_expects_json import expects_json

from services.users_services import *
from api.database import db
from api.services.jwt_required_decorators import admin_required

rud_users_bp = Blueprint("crud_users", __name__)

schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'}
    },
    'additionalProperties': False
}


@rud_users_bp.get("/users")
@admin_required
def get_users():
    try:
        all_users = get_all_users()
        users_list = [user.to_json() for user in all_users]
        if users_list:
            return {"Users": users_list}, 200
        return {"Message": "The users table is empty"}, 404
    except Exception as e:
        return {"Message": "Couldn't retrieve users from DB!", "Error": str(e)}, 500
    finally:
        db.session.close()

@rud_users_bp.get("/users/<uuid:user_uuid>")
@admin_required
def get_user(user_uuid):
    try:
        user = get_user_by_uuid(user_uuid)
        if user:
            return {"User": user.to_json()}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't retrieve user with uuid {user_uuid} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@rud_users_bp.delete("/users/<uuid:user_uuid>")
@admin_required
def delete_user(user_uuid):
    try:
        user = get_user_by_uuid(user_uuid)
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
@expects_json(schema, check_formats=True)
def update_user(user_uuid):
    try:
        user = get_user_by_uuid(user_uuid)
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
