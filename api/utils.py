import os
from functools import wraps

import jwt
from flask import request


def admin_required(f):
    @wraps(f)
    def admin_token_check(*args, **kwargs):
        token = request.cookies.get("token")
        if token:
            try:
                decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
                if decoded_token.get("admin"):
                    return f(*args, **kwargs)
                else:
                    return {"Message": "Admin privileges required."}, 403
            except jwt.exceptions.ExpiredSignatureError:
                return {"Message": "Auth token expired."}, 498
            except jwt.exceptions.InvalidSignatureError:
                return {"Message": "Invalid token signature."}, 401
            except jwt.exceptions.DecodeError:
                return {"Message": "Invalid or missing auth token."}, 401
        else:
            return {"Message": "No auth token provided."}, 401
    return admin_token_check