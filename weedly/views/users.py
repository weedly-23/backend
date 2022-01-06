from flask import Blueprint, jsonify

routes = Blueprint('users', __name__)


@routes.get('/')
def get_all():
    return jsonify([]), 200


@routes.get('/<int:uid>')
def get_by_id(uid: int):
    return {}, 200


@routes.post('/')
def add():
    return {}, 200


@routes.put('/<int:uid>')
def update(uid: int):
    return {}, 200


@routes.delete('/<int:uid>')
def delete(uid: int):
    return {}, 204
