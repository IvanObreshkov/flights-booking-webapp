import os
from typing import Dict, Tuple

import jwt

from db.repositories.users_repository import change_verified_status, query_user_by_uuid


class Verification:
    @classmethod
    def verify_user(cls, token) -> Tuple[Dict[str, str], int]:
        response, status_code = cls.verify_token(token)
        if status_code != 200:
            return response, status_code

        user = query_user_by_uuid(response.get("user_id"))
        if not user:
            return {"Message": f"User with uuid {response.get('user_id')} doesn't exist in the DB!"}, 404

        change_verified_status(user)
        return {"Message": "Your account has been verified"}, 200

    @classmethod
    def verify_token(cls, token) -> Tuple[Dict[str, str], int]:
        if not token:
            return {"Message": "No verification token provided."}, 401
        try:
            decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"Message": "Verification link expired."}, 498
        except jwt.exceptions.InvalidSignatureError:
            return {"Message": "Invalid verification token signature."}, 401
        except jwt.exceptions.DecodeError:
            return {"Message": "Invalid or missing verification token."}, 401

        user_id = decoded_token.get("sub", None)
        if not user_id:
            return {"Message": "No user_id provided"}, 403

        return {"user_id": user_id}, 200
