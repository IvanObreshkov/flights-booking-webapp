from flask import Flask
from flask_migrate import Migrate

from config import DevConfig
from models.extension import db
from routes.register_route import register_bp


def create_app(config_class=DevConfig):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.register_blueprint(register_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db)
    @app.route("/")
    def hello():
        return "Hello, World!"

    return app
