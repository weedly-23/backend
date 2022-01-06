from flask import Flask, jsonify

from weedly.db import models
from weedly.views import feeds, users


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    models.db.init_app(app)

    app.register_blueprint(feeds.routes, url_prefix='/api/v1/feeds/')
    app.register_blueprint(users.routes, url_prefix='/api/v1/users/')

    return app


app = create_app()
