from typing import List

from flask import Flask, Blueprint

from api.routes.bookings_route import crud_bookings_bp
from api.routes.flights_route import crud_flights_bp
from api.routes.login_route import login_bp
from api.routes.register_route import register_bp
from api.routes.users_route import rud_users_bp
from api.routes.verification_routes import verification_bp


class Routes:
    _blueprints: List[Blueprint] = [
        register_bp,
        rud_users_bp,
        crud_flights_bp,
        crud_bookings_bp,
        login_bp,
        verification_bp
    ]

    @classmethod
    def register_blueprints(cls, app: Flask) -> None:
        for blueprint in cls._blueprints:
            app.register_blueprint(blueprint)
