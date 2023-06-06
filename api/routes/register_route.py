from flask import Blueprint
from flask import request
from flask_expects_json import expects_json
from sqlalchemy import text

from models.extension import db
from models.users_model import Users

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
            result = db.session.execute(text("Select * From users"))
            rows = result.all()
            for row in rows:
                print(row)
            db.session.close()
            return response
        except Exception as e:
            return {"Message": "Couldn't load register form", "Error": str(e)}, 500
    else:
        json_data = request.json
        # TODO:
        #  - Check if user exists in DB: if true -> return Bad Request, else -> add user to DB
        #  (later add verification email )
        #  - Hash password
        user = Users(
            first_name="Toni",
            last_name="Montana",
            email="misho1234@abv.bg",
            password="pass1234"
        )
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return {"Message": "Ok"}

def check_if_user_exists():
    pass