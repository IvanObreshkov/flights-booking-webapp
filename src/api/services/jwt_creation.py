from datetime import datetime, timedelta
import os

import jwt


def create_jwt(user, raw_password):
    """Create JWT tokens for admin and users

    Parameters:
        user: The retrieved User obj from the db
        raw_password: The password from the input filed in the html

    Returns:
        The JWT token
    """

    if os.getenv("ADMIN_EMAIL") == user.email and os.getenv(
            "ADMIN_PASSWORD") == raw_password:

        payload = {"sub": user.id,
                   "name": f"{user.first_name} {user.last_name}",
                   "email": user.email, "admin": True,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    else:
        payload = {"sub": user.id,
                   "name": f"{user.first_name} {user.last_name}",
                   "email": user.email, "admin": False,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")

    return token
