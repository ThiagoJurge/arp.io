from flask import Flask
from routes.main import main_blueprint
from routes.api import api_blueprint
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)
import os

SECRET_KEY = os.environ.get('SECRET_KEY')


def create_app():
    load_dotenv()
    app = Flask(__name__)
    jwt = JWTManager(app)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    return app
