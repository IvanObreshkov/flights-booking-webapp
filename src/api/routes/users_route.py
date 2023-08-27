# Here we use the concept of Blueprints in Flask
# learn more about it in the docs: https://flask.palletsprojects.com/en/2.3.x/blueprints/,
# https://flask.palletsprojects.com/en/2.3.x/tutorial/views/

from flask import Blueprint, request
from flask_expects_json import expects_json

from api.utilities.jwt_required_decorators import admin_required
from api.services.users_services import *
from api.utilities.json_schemas import update_users_schema

rud_users_bp = Blueprint("crud_users", __name__)


@rud_users_bp.get("/users")
@admin_required
def get_users_route():
    return get_users_service()


@rud_users_bp.get("/users/<uuid:user_uuid>")
@admin_required
def get_user_route(user_uuid):
    return get_user_by_uuid_service(user_uuid)


@rud_users_bp.delete("/users/<uuid:user_uuid>")
@admin_required
def delete_user_route(user_uuid):
    delete_user_service(user_uuid)


@rud_users_bp.put("/users/<uuid:user_uuid>")
@admin_required
@expects_json(update_users_schema, check_formats=True)
def update_user_route(user_uuid):
    update_user_service(user_uuid, request)
