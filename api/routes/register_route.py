import json
from flask import request
from flask import Blueprint
from flask_expects_json import expects_json

register_bp = Blueprint("register", __name__)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']
}


@register_bp.route("/register", methods=('GET', 'POST'))
@expects_json(schema, ignore_for=['GET'])
def register():
    if request.method == "GET":
        response = {"Message": "Welcome!"}
        try:
            # TODO: Load register form
            return response
        except Exception as e:
            return {"Message": "Couldn't load register form", "Error": str(e)}, 500
    else:
        json_data = request.json
        # TODO:
        #  - Hash password
        #  - Check if user exists in DB: if true -> return Bad Request, else -> add user to DB
        #  (later add verification email )
        return {"Message": "Ok"}
