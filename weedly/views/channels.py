from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.channels import ChannelRepo

routes = Blueprint('channels', __name__)

repo = ChannelRepo(db_session)

@routes.post('/')
def add():
    ...
