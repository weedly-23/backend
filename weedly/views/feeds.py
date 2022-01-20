from http import HTTPStatus

from flask import Blueprint, jsonify, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.feeds import FeedRepo

routes = Blueprint('feeds', __name__)

repo = FeedRepo(db_session)


@routes.get('/')
def get_all():
    args = request.args
    if args['rss-only'] == '1':
        entities = repo.get_all_rss()
        feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]
        return jsonify(feeds), 200
    elif args['rss-only'] == '0':
        entities = repo.get_all()
        feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]
        return jsonify(feeds), 200


@routes.get('/<int:uid>')
def get_by_id(uid):
    feed = repo.get_by_id(uid)
    feed = schemas.Feed.from_orm(feed).json()
    return feed, 200


@routes.get('/source-name/<string:name>')
def get_by_source_name(name):
    entities = repo.get_authors_by_name(name)
    authors = [schemas.Author.from_orm(entity).dict() for entity in entities]
    return jsonify(authors)


@routes.get('/<int:uid>/authors/')
def get_authors(uid: int):
    entities = repo.get_authors_by_id(uid)
    authors = [schemas.Author.from_orm(entity).dict() for entity in entities]
    return jsonify(authors), 200


@routes.get('/<int:uid>/articles/')
def get_articles(uid):
    entities = repo.get_articles(uid)
    articles = [schemas.Article.from_orm(article).dict() for article in entities]
    return jsonify(articles), 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400
    payload['uid'] = 0
    feed = schemas.Feed(**payload)
    entity = repo.add(
        name=feed.name,
        url=feed.url,
        is_rss=feed.is_rss,
        category=feed.category,
    )
    new_feed = schemas.Feed.from_orm(entity)
    return new_feed.dict(), HTTPStatus.CREATED


@routes.put('/')
def update():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400
    feed = schemas.Feed(**payload).dict()
    entity = repo.update(**feed)
    updated_feed = schemas.Feed.from_orm(entity).dict()

    return jsonify(updated_feed), 200


@routes.put('/get-by-url/')
def get_by_url():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400

    url = payload['url']
    entity = repo.get_by_url(url)
    feed = schemas.Feed.from_orm(entity).dict()

    return jsonify(feed), 200


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return '', 204
