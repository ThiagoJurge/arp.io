import sys
sys.path.insert(0, '/var/www/arp.io/backend/')

from flask_app.flask_app import create_app
application = create_app()

# Inclua esta linha se estiver usando CORS
from flask_cors import CORS
CORS(application, resources={r"/*": {"origins": "*"}})