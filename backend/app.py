from flask import Flask
from flask_cors import CORS
from flask_app.flask_app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from utils.loopacks import main


def schedule_jobs():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=main, trigger="interval", minutes=10)
    scheduler.start()


if __name__ == "__main__":
    app = create_app()
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Iniciando o scheduler
    schedule_jobs()

    app.run(host="0.0.0.0", port=81, debug=True, use_reloader=True, threaded=True)
