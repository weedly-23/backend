from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.videos import VideoRepo

routes = Blueprint('videos', __name__)

repo = VideoRepo(db_session)


@routes.get('/')
def get_all():
    entities = repo.get_all()
    videos = [schemas.Video.from_orm(entity).dict() for entity in entities]

    return jsonify(videos)


@routes.get('/<int:uid>')
def get_by_uid(uid):
    video = repo.get_by_id(uid)
    data = schemas.Video.from_orm(video).json()

    return data, 200


@routes.get('/video-id/<string:video_id>')
def get_by_video_id(video_id):
    video = repo.get_by_video_id(video_id)
    data = schemas.Video.from_orm(video).json()

    return data, 200


@routes.get('/channel-id/<string:channel_id>')
def get_videos_by_channel_id(channel_id):
    entities = repo.get_by_channel_id(channel_id)
    data = [schemas.Video.from_orm(entity).dict() for entity in entities]

    return jsonify(data), 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'payload required')
    payload['uid'] = 0
    video = schemas.Video(**payload)
    entity = repo.add(
        video_id=video.video_id,
        title=video.title,
        channel_id=video.channel_id,
        duration=video.duration,
    )
    new_video = schemas.Video.from_orm(entity)
    return new_video.json(), HTTPStatus.CREATED


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return '', 204
