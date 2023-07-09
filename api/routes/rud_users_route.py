# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, request
from flask_expects_json import expects_json

from database import db
from models.users_model import Users

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
def get_users():
    # TODO:
    #  - require admin jwt

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
    # TODO:
    #  - require admin jwt

    try:
        user = db.session.query(Users).get(user_uuid)
        if user:
            return {"User": user.to_json()}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        return {"Message": f"Couldn't retrieve user with uuid {user_uuid} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@rud_users_bp.delete("/users/<uuid:user_uuid>")
def delete_user(user_uuid):
    # TODO:
    #  - require admin jwt

    try:
        user = db.session.query(Users).get(user_uuid)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"Message": f"User with uuid {user_uuid} was removed successfully from the DB"}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't delete user with uuid {user_uuid} from DB!", "Error": str(e)}, 500

    finally:
        db.session.close()


@rud_users_bp.put("/users/<uuid:user_uuid>")
@expects_json(schema, check_formats=True)
def update_user(user_uuid):
    # TODO:
    #  - require admin jwt

    try:
        user = db.session.query(Users).get(user_uuid)
        if user:
            json_data = request.json
            user.first_name = json_data.get('first_name', user.first_name)
            user.last_name = json_data.get('last_name', user.last_name)
            user.email = json_data.get('email', user.email)
            user.password = json_data.get('password', user.password)
            db.session.commit()
            return {"Message": f"User with uuid {user_uuid} was updated successfully."}, 200

        return {"Message": f"User with uuid {user_uuid} doesn't exist in the DB!"}, 404

    except Exception as e:
        db.session.rollback()
        return {"Message": f"Couldn't update user with uuid {user_uuid}", "Error": str(e)}, 500

    finally:
        db.session.close()
