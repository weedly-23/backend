from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.authors import AuthorRepo

routes = Blueprint('authors', __name__)

repo = AuthorRepo(db_session)


@routes.get('/')
def get_all():
    return jsonify([]), 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'payload required')

    payload['uid'] = 0

    author = schemas.Author(**payload)
    entity = repo.add(name=author.name, feed_id=author.feed_id)
    new_author = schemas.Author.from_orm(entity)
    return new_author.dict(), 200
