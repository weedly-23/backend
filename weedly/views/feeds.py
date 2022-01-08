from flask import Blueprint, jsonify, request
from weedly.repos.feeds import FeedRepo
from weedly.db.session import db_session
from weedly import schemas


routes = Blueprint('feeds', __name__)

repo = FeedRepo(db_session)

@routes.get('/')
def get_all():
    feeds = repo.get_all()
    feeds = [schemas.Feed.from_orm(e).dict() for e in feeds]
    return jsonify(feeds), 200


@routes.get('/<int:uid>')
def get_by_id(uid):
    return {}, 200


@routes.get('/<int:uid>/authors/')
def get_authors(uid: int):
    return jsonify([]), 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400
    payload['uid'] = 0
    feed = schemas.Feed(**payload)
    entity = repo.add(name=feed.name, url=feed.url,
                      is_rss=feed.is_rss, category=feed.category)
    new_feed = schemas.Feed.from_orm(entity)
    return new_feed.dict(), 200


@routes.put('/<int:uid>')
def update(uid: int):
    return {}, 200


@routes.delete('/<int:uid>')
def delete(uid: int):
    return {}, 204
