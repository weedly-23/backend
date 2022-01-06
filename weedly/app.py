from flask import Flask, jsonify

from weedly.db import models


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    models.db.init_app(app)

    @app.route('/api/v1/feeds/<feed_name>/authors/', methods=['GET'])
    def get_feed_authors(feed_name: str):
        return jsonify([])

    return app


app = create_app()
