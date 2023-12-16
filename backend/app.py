from flask_cors import CORS
from flask_app.flask_app import create_app

if __name__ == "__main__":
    app = create_app()
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(host="0.0.0.0", port=81, debug=True, use_reloader=True, threaded=True)