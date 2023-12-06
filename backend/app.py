from dotenv import load_dotenv
import os
from flask_app.flask_app import create_app

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

if __name__ == '__main__':
    app = create_app()
    app.config['SECRET_KEY'] = SECRET_KEY
    app.run(debug=True)