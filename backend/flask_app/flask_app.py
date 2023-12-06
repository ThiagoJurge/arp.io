from flask import Flask
from routes.main import main_blueprint
from routes.api import api_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    return app
