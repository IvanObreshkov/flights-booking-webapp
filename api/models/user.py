import sqlalchemy

from models.extension import db


class User(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, unique=True)
