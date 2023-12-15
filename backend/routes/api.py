from flask import Blueprint, jsonify, request
from utils.api_response import ApiResponse
from scripts import ExaBGPRestarter
from scripts.database import Database
import subprocess

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
db_trap_handler = Database("trap_handler")
db_mitigation_service = Database("mitigation_service")


@api_blueprint.route("/restart_exabgp")
def restart_exabgp():
    exabgp_manager = ExaBGPRestarter.ExaBGPRestarter()

    if exabgp_manager.check_session_exists():
        exabgp_manager.stop_session()

    if exabgp_manager.start_session():
        exabgp_manager.wait_for_start()
        if exabgp_manager.execute_curl_request():
            return ApiResponse.success(exabgp_manager.success_message)
        else:
            return ApiResponse.error(exabgp_manager.error_message)
    else:
        return ApiResponse.error(exabgp_manager.error_message)


@api_blueprint.route("/if_status", methods=["GET"])
def get_if_status():
    query = "SELECT * FROM if_status"
    data = db_trap_handler.fetch(query)
    formatted_data = [dict(row) for row in data]
    return ApiResponse.success(formatted_data)


@api_blueprint.route("/attacks", methods=["GET"])
def get_attacks():
    return ApiResponse.success(
        db_mitigation_service.fetch("SELECT * FROM AttackMitigation")
    )


@api_blueprint.route("/attacks/<int:id>", methods=["PUT"])
def update_attack(id):
    data = request.json
    action = data.get("action")
    bandwidth = data.get("bandwidth")

    if bandwidth is not None:
        db_mitigation_service.execute(
            "UPDATE AttackMitigation SET action = %s, bandwidth = %s WHERE id = %s",
            (action, bandwidth, id),
        )
    else:
        db_mitigation_service.execute(
            "UPDATE AttackMitigation SET action = %s WHERE id = %s", (action, id)
        )
    return ApiResponse.success("Update sucessful")


@api_blueprint.route("/asns", methods=["GET"])
def get_asns():
    return ApiResponse.success(db_mitigation_service.fetch("SELECT DISTINCT asn FROM AttackMitigation"))


@api_blueprint.route("/api/attacks/search", methods=["GET"])
def search_attacks():
    prefix = request.args.get("prefix")
    return ApiResponse.success(
        db_mitigation_service.fetch(
            "SELECT * FROM AttackMitigation WHERE prefix = %s", (prefix)
        )
    )


@api_blueprint.route("/api/asns/search", methods=["GET"])
def search_asns():
    asn = request.args.get("asn")
    return ApiResponse.success(
        db_mitigation_service.fetch(
            "SELECT * FROM AttackMitigation WHERE asn = %s", (asn)
        )
    )


@api_blueprint.route("/bypass", methods=["POST"])
def execute_curl():
    data = request.json
    curl_command = data.get("curlCommand")
    try:
        subprocess.run(
            curl_command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return jsonify({"message": "cURL command executed successfully"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Internal Server Error"})


# @api_blueprint.route("/", defaults={"path": ""})
# @api_blueprint.route("/<path:path>")
# def serve(path):
#     if path != "" and path != "favicon.ico":
#         return send_from_directory("../frontend/dist", path)
#     else:
#         return send_from_directory("../frontend/dist", "index.html")
