from flask import Blueprint, request, Flask
from utils.api_response import ApiResponse
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

app = Flask(__name__)
main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/<path:path>")
def fallback(path):
    return ApiResponse.not_found("Página não encontrada")


@main_blueprint.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return ApiResponse.error({"msg": "Bad username or password"}, 401)

    access_token = create_access_token(identity=username)
    return ApiResponse.success({"token": access_token})


# without a valid JWT present.
@main_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return ApiResponse.success({"user": current_user})


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTgzOTgwMCwianRpIjoiNzBkZjNjMDMtMGMzOC00ZDMzLWEwMzQtNGVhNTY2NmJiZDU0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE3MDE4Mzk4MDAsImV4cCI6MTcwMTg0MDcwMH0.yJhOntmpd_YDwO0lohlGZeGwWDvNNVrxB3VoK8yQC-E
