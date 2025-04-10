from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")

db = SQLAlchemy()

def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect: Person API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    logger.info(f"DB Config: {app.config['SQLALCHEMY_DATABASE_URI']}")
    try:
        db.init_app(app)
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app

