from flask import Blueprint, jsonify, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.users import UserRepo

routes = Blueprint('users', __name__)

repo = UserRepo(session=db_session)


@routes.get('/')
def get_all():
    entities = repo.get_all()
    users = [schemas.User.from_orm(entity).dict() for entity in entities]
    return jsonify(users), 200


@routes.get('/<int:uid>')
def get_by_id(uid: int):
    entity = repo.get_by_id(uid)
    user = schemas.User.from_orm(entity)
    return user.dict(), 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400

    user = schemas.User(**payload)
    entity = repo.add(name=user.name, uid=user.uid, feed_id=user.feed_id)
    new_user = schemas.User.from_orm(entity)
    return new_user.dict(), 200


@routes.put('/<int:uid>')
def update(uid: int):
    """в том числе добавить rss"""

    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400

    print('вошли в view update ---', payload)
    user = schemas.User(**payload)
    entity = repo.update(uid=user.uid, name=user.name, feed_id=user.feed_id)
    updated_user = schemas.User.from_orm(entity)
    return updated_user.dict(), 200


@routes.delete('/<int:uid>/<int:feed_id>')
def delete_rss(uid, feed_id):
    repo.delete_rss_from_subs(uid, feed_id)
    return f'Удалили {feed_id}', 204


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return {}, 204
