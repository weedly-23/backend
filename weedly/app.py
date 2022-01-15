import logging

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from weedly.db import models
from weedly.errors import AppError
from weedly.views import authors, feeds, users, articles

logger = logging.getLogger(__name__)


def handle_app_error(error: AppError):
    logger.warning(error.reason)
    return {'error': str(error)}, error.status


def handle_http_error(error: HTTPException):
    logger.warning(error.description)
    return {'error': error.description}, error.code


def handle_validation_error(error: ValidationError):
    return error.json(indent=2), 400


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    models.db.init_app(app)

    app.register_blueprint(feeds.routes, url_prefix='/api/v1/feeds/')
    app.register_blueprint(users.routes, url_prefix='/api/v1/users/')
    app.register_blueprint(authors.routes, url_prefix='/api/v1/authors/')
    app.register_blueprint(articles.routes, url_prefix='/api/v1/articles/')

    app.register_error_handler(HTTPException, handle_http_error)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    return app


app = create_app()
