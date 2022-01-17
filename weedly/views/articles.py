from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request
import arrow
from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.articles import ArticleRepo

routes = Blueprint('articles', __name__)

repo = ArticleRepo(db_session)


@routes.get('/')
def get_all():
    entities = repo.get_all()
    articles = [schemas.Article.from_orm(ent).dict() for ent in entities]
    return jsonify(articles), 200


@routes.get('/<string:feed_name>')
def get_all_by_feed_name(feed_name):
    entities = repo.get_by_feed_name(feed_name)[0]
    articles = [schemas.Article.from_orm(ent).dict() for ent in entities]
    return jsonify(articles), 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'payload required')
    payload['uid'] = 0
    payload['published'] = arrow.get(payload['published']).datetime

    article = schemas.Article(**payload)
    entity = repo.add(title=article.title, url=article.url, published=article.published,
                      feed_id=article.feed_id, author_id=article.author_id)
    new_article = schemas.Article.from_orm(entity)
    new_article.published = arrow.get(new_article.published).for_json()

    return new_article.dict(), HTTPStatus.CREATED
