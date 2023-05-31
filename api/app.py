from flask import Flask

from routes.register_route import register_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(register_bp)

    @app.route("/")
    def hello():
        return "Hello, World!"
    return app
