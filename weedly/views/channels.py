from http import HTTPStatus

from flask import Blueprint, jsonify, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.channels import ChannelRepo

routes = Blueprint('channels', __name__)

repo = ChannelRepo(db_session)


@routes.get('/')
def get_all():
    entities = repo.get_all()
    channels = [schemas.Channel.from_orm(entity).dict() for entity in entities]

    return jsonify(channels), 200


@routes.get('/<int:uid>')
def get_by_uid(uid):
    channel = repo.get_by_uid(uid)
    data = schemas.Channel.from_orm(channel).json()

    return data, 200


@routes.get('/channel-id/<string:channel_id>')
def get_by_channel_id(channel_id):
    channel = repo.get_by_channel_id(channel_id)
    data = schemas.Channel.from_orm(channel).json()

    return data, 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, 400
    payload['uid'] = 0
    channel = schemas.Channel(**payload)
    entity = repo.add(
        title=channel.title,
        channel_id=channel.channel_id,
    )
    new_channel = schemas.Channel.from_orm(entity)
    return new_channel.dict(), HTTPStatus.CREATED


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return '', 204


@routes.delete('/channel-id/<string:channel_id>')
def delete_by_channel_id(channel_id: str):
    repo.delete_by_channel_id(channel_id)
    return '', 204
