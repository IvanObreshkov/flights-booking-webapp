from flask import Flask, render_template
from flask_migrate import Migrate

from api.config import DevConfig
from api.db.database import db
from api.routes.routes import Routes

migrate = Migrate()


def create_app(config_class=DevConfig):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    Routes.register_blueprints(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)

    @app.route("/")
    def hello():
        return render_template("index.html")

    return app
