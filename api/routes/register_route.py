import sqlalchemy
from flask import Blueprint
from flask import request
from flask_expects_json import expects_json
from sqlalchemy import text

from database import db
from models import Users

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


@register_bp.route("/register", methods=['POST'])
@expects_json(schema)
def register():
    json_data = request.json
    first_name = json_data["first_name"]
    last_name = json_data["last_name"]
    email = json_data["email"]
    password = json_data["password"]

    # TODO:
    #  - Hash password
    #  - Implement JWT
    #  - Send verification emails

    try:
        new_user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return {"Message": "New user added to DB!"}

    except sqlalchemy.exc.IntegrityError as e:
        return {"Error": f"Email address {email} exist in the DB!"}, 409


@register_bp.route("/users", methods=['GET'])
def get_users():
    try:
        result = db.session.execute(text("Select * From users"))
        rows = result.all()

        # JSON serializing of Row objects
        users = serialize_rows(result, rows)
        response = {"Users": users}

        db.session.close()
        return response

    except Exception as e:
        return {"Message": "Couldn't load register form", "Error": str(e)}, 500


def serialize_rows(result, rows):
    """Serializes Row objects to JSON so that they could be returned as a response from the API"""

    column_names = result.keys()
    users = []
    for row in rows:
        user = {}
        for column, value in zip(column_names, row):
            user[column] = value
        users.append(user)
    return users
