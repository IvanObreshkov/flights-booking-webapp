from flask import request
from flask import Blueprint

register_bp = Blueprint("register", __name__)


@register_bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == "GET":
        response = {"Message": "OK!"}
        return response
