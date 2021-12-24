import arrow
from flask import Flask, request

from weedly.db import model
from weedly.db.crud import PostgreStorage
from weedly.db.model import News


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    model.db.init_app(app)

    news = PostgreStorage(News)

    @app.route('/api/v1/feeds/', methods=['GET'])
    def get_all():
        get_all_res = news.query_as_json(news.get_all(num_rows=20))
        return get_all_res

    @app.route('/api/v1/feeds/<int:uid>', methods=['GET'])
    def get_one(uid):
        if news._id_in_table(uid):
            get_one_res = news.query_as_json(news.get_one(uid))
            return get_one_res
        else:
            return {"message": f"We don't have index {uid}"}, 404

    @app.route('/api/v1/feeds/', methods=['POST'])
    def add_one():
        payload = request.json
        if "published" in payload:
            try:
                a = arrow.get(payload["published"])
                payload["published"] = a.datetime
            except:
                return {"message": f"Bad 'published' field format {payload['published']}"}, 400
        news.add(payload)
        return payload

    @app.route('/api/v1/feeds/<int:index>', methods=['DELETE'])
    def delete_one(index):
        if news.delete(index):
            return {"message": f"Successfully deleted index {index}"}, 200
        return {"message": f"We were not able to delete index {index}"}, 400

    @app.route('/api/v1/feeds/<int:index>', methods=['PUT'])
    def update_one(index):
        payload = request.json
        try:
            a = arrow.get(payload["published"])
            payload["published"] = a.datetime
        except:
            return {"message": f"Bad 'published' field format {payload['published']}"}, 400
        if news.update(index, payload):
            return {"message": f"Successfully updated {index}"}
        return {"message": f"We were not able to update index {index}"}, 404

    return app

app = create_app()
