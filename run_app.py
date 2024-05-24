import logging

from flask import Flask
from flask_cors import CORS

from helpers import env
from models import db
from routes import home_bp, reels_bp, storage_bp


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = env.get_env("APP_SECRET_KEY")

    database_url = env.get_env("DATABASE_URL")
    print(f"Connecting to database at {database_url}")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    logging.info("Connecting to database at %s", database_url)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    logging.info("Database connected")

    # login_manager.init_app(app)

    # app.add_url_rule("/", "home", home)
    # app.register_blueprint(auth_bp)

    app.register_blueprint(reels_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(storage_bp)

    return app


app = create_app()
