from flask import Blueprint
from utils.api_response import ApiResponse

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/<path:path>')
def fallback(path):
    return ApiResponse.not_found("Página não encontrada")