import logging
import traceback

from flask import Flask, json, Response
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound

from app.models import Actor
from app.configs import AppConfig, DBConfig
from app.extensions import db
from app.controllers.v1 import v1_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})

    configure_db(app)
    configure_blueprints(app)
    configure_error_handlers(app)

    return app


def configure_db(app: Flask):
    conn_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        DBConfig.USER,
        DBConfig.PASSWORD,
        DBConfig.HOST,
        DBConfig.PORT,
        DBConfig.DATABASE
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = conn_str

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


def configure_blueprints(app: Flask):
    app.register_blueprint(v1_blueprint)


def configure_error_handlers(app: Flask):
    error_logger = logging.getLogger('error')

    @app.errorhandler(Exception)
    def unhandled_exception(e: Exception):
        error_logger.error(traceback.format_exc())
        if AppConfig.DEBUG:
            raise e

        if isinstance(e, (BadRequest, NotFound)):
            response = e.get_response()
            response.data = json.dumps({
                "code": e.code,
                "name": e.name,
                "description": e.description,
            })
            response.content_type = "application/json"
            return response
        if isinstance(e, BaseException):
            response = Response()
            response.data = json.dumps({
                "code": 400,
                "name": e.__class__.__name__,
                "description": str(e)
            })
            response.content_type = "application/json"
            response.status_code = 400
            return response
        return str(e), 500
