import os
from flask import Blueprint, request, Flask, send_from_directory
from flask_cors import CORS
from utils.api_response import ApiResponse
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

main_blueprint = Blueprint("main", __name__, static_folder="../../frontend/dist", static_url_path="/")

@main_blueprint.route("/", defaults={"path": ""})
@main_blueprint.route("/<path:path>")
def serve(path):
    print(path)
    if path != "" and os.path.exists(main_blueprint.static_folder + "/" + path):
        return send_from_directory("../../frontend/dist", path)
    else:
        return send_from_directory("../../frontend/dist", "index.html")


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
    # Access the identity of the current user witwh get_jwt_identity
    current_user = get_jwt_identity()
    return ApiResponse.success({"user": current_user})
