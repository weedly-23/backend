from flask import Blueprint, jsonify, request
from weedly.repos.authors import AuthorRepo
from weedly.db.session import db_session
from weedly import schemas


routes = Blueprint('authors', __name__)

repo = AuthorRepo(db_session)

@routes.get('/')
def get_all():
    pass

@routes.put('/')
def add_author():
    payload = request.json
    if not payload:
        return {"error":"payload required"}, 404
    payload['uid'] = -1

    author = schemas.Author(**payload)
    entity = repo.add(name=author.name, feed_id=author.feed_id)
    new_author = schemas.Author.from_orm(entity)
    return new_author.dict(), 200

