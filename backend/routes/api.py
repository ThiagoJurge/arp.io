from flask import Blueprint
from utils.api_response import ApiResponse

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/alguma_rota')
def alguma_rota():
    return ApiResponse.error('Bom dia')
