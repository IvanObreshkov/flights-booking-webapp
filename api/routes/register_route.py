from flask import Blueprint
from flask import request
from flask_expects_json import expects_json

register_bp = Blueprint("register", __name__)

schema = {
    'type': 'object',
    'properties': {
        'frst_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['first_name', 'last_name', 'email', 'password']
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
        #  - Check if user exists in DB: if true -> return Bad Request, else -> add user to DB
        #  (later add verification email )
        #  - Hash password

        return {"Message": "Ok"}

def check_if_user_exists():
    pass