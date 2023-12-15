from flask import jsonify, make_response

class ApiResponse:
    @staticmethod
    def response(data, status=200):
        return make_response(jsonify(data), status)

    @staticmethod
    def success(data=None, message="Success", status=200):
        return ApiResponse.response({"message": message, "data": data}, status=status)

    @staticmethod
    def no_content():
        return make_response({'data': 'no content'}, 204)

    @staticmethod
    def error(message, status=400):
        return ApiResponse.response({"message": message, "status": status}, status=status)

    @staticmethod
    def not_found(message, status=404):
        return ApiResponse.response({"message": message, "status": status}, status=status)