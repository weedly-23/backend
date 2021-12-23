import os

basedir = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '', '../weedly.db')
DOCKER_DB_URI = 'postgresql://example:example@127.0.0.1:5432/mydatabase'
