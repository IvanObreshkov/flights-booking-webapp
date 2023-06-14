from flask import Flask
from flask_migrate import Migrate

from config import DevConfig
from database import db
from routes.crud_bookings_route import crud_bookings_bp
from routes.crud_flights_route import crud_flights_bp
from routes.rud_users_route import rud_users_bp
from routes.register_route import register_bp

migrate = Migrate()


def create_app(config_class=DevConfig):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.register_blueprint(register_bp)
    app.register_blueprint(rud_users_bp)
    app.register_blueprint(crud_flights_bp)
    app.register_blueprint(crud_bookings_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)

    @app.route("/")
    def hello():
        return "Hello, World!"

    return app
