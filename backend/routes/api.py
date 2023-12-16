from flask import Blueprint, jsonify, request
from utils.api_response import ApiResponse
from scripts import ExaBGPRestarter
from scripts.database import Database
import subprocess, json, os

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
    # Determinar o diretório do script atual
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construir o caminho absoluto para o arquivo de mapeamento
    json_path = os.path.join(dir_path, '../../hostnames.json')

    # Carregar o mapeamento de IP para hostname
    with open(json_path, 'r') as file:
        ip_hostname_mapping = json.load(file)

    # Buscar os dados do banco de dados
    data = db_trap_handler.fetch("SELECT * FROM if_status")

    # Substituir o sender_ip pelo hostname correspondente
    for item in data:
        sender_ip = item.get('sender_ip')
        hostname = next((entry['hostname'] for entry in ip_hostname_mapping if entry['ip'] == sender_ip), None)
        if hostname:
            item['sender_ip'] = hostname

    return ApiResponse.success(data)


@api_blueprint.route("/attacks", methods=["GET"])
def get_attacks():
    return ApiResponse.success(
        db_mitigation_service.fetch("SELECT * FROM AttackMitigation")
    )


@api_blueprint.route("/attacks/<int:id>", methods=["POST"])
def update_attack(id):
    action = request.json.get("action")
    bandwidth = request.json.get("bandwidth")

    if (bandwidth is not None) and (action is not None):
        query = f"UPDATE AttackMitigation SET action = '{action}', bandwidth = '{bandwidth}' WHERE id = {id}"
        db_mitigation_service.execute(query)
        return ApiResponse.success("Regra alterada com sucesso")
    elif bandwidth is not None:
        query = f"UPDATE AttackMitigation SET bandwidth = '{bandwidth}' WHERE id = {id}"
        db_mitigation_service.execute(query)
        return ApiResponse.success("Regra alterada com sucesso")
    else:
        query = f"UPDATE AttackMitigation SET action = '{action}' WHERE id = {id}"
        db_mitigation_service.execute(query)
        return ApiResponse.success("Regra alterada com sucesso")


@api_blueprint.route("/asns", methods=["GET"])
def get_asns():
    return ApiResponse.success(
        db_mitigation_service.fetch("SELECT DISTINCT asn FROM AttackMitigation")
    )


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
