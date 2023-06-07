import uuid

import sqlalchemy

from database import db


class Users(db.Model):
    id = sqlalchemy.Column(sqlalchemy.String(36), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
