from flask import Flask, request

from weedly.db import models
from weedly.db.db_funs import DataGetter

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    models.db.init_app(app)

    getter = DataGetter()

    @app.route('/api/v2/feeds/<string:feed_name>/authors/', methods=['GET'])
    def get_all_authors_of_a_feed(feed_name):
        '''получить все статьи по названию фида (meduza, wired, vc)'''

        return {'result' : getter.get_articles_of_a_feed(feed_name)}


    return app

app = create_app()
