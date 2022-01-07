from flask import Flask

from weedly.db import models
from weedly.errors import AppError
from weedly.views import feeds, users


def handle_app_error(error: AppError):
    return {'error': str(error)}, error.status


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    models.db.init_app(app)

    app.register_blueprint(feeds.routes, url_prefix='/api/v1/feeds/')
    app.register_blueprint(users.routes, url_prefix='/api/v1/users/')
    app.register_error_handler(AppError, handle_app_error)

    return app


app = create_app()
