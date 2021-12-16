from flask import Flask
from my_database import models, db_queries

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    models.db.init_app(app)


    @app.route('/', methods=['GET'])
    def say_hello():
        hello_dict = {"hello": "dict"}
        return hello_dict


    @app.route('/feed', methods=['GET'])
    def get_feeds():
        '''параметр у get_latest_news - количество статей'''
        news = db_queries.get_latest_news(5)
        news = [e.title for e in news] # взяли только заголовки
        return {'main_news': news}


    @app.route('/feed/<int:feed_id>', methods=['GET'])
    def get_feed(feed_id):
        return "This returns one feed by ID"


    @app.route('/feed', methods=['POST'])
    def add_feed(data):
        return "This adds a new feed."


    @app.route('/feed/<int:feed_id>', methods=['PUT', 'PATCH'])
    def edit_feed(feed_id):
        return "This updates a feed by ID."


    @app.route('/feed/<int:feed_id>', methods=['DELETE'])
    def delete_feed(feed_id):
        return "This removes a feed by ID."

    return app

app = create_app()