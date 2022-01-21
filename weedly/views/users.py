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
    entity = repo.add(name=user.name, uid=user.uid)
    new_user = schemas.User.from_orm(entity)
    return new_user.dict(), 200


@routes.post('/<int:uid>/feeds/')
def add_rss_to_user(uid: int):

    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400

    feed_id = payload['feed_id']

    updated_feeds = repo.add_rss_to_user(uid=uid, feed_id=feed_id)
    return {"updated_feeds": updated_feeds}, 200


@routes.delete('/<int:uid>/feeds/<int:feed_id>')
def delete_rss(uid, feed_id):
    repo.delete_rss_from_subs(uid, feed_id)
    return f'Удалили {feed_id}', 204


@routes.get('/<int:uid>/feeds')
def get_user_feeds(uid: int):
    entities = repo.get_user_rss(uid)

    if entities:
        feeds = [schemas.Feed.from_orm(e).dict() for e in entities]
        return jsonify(feeds), 200

    return 'No feeds', 204


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return {}, 204
