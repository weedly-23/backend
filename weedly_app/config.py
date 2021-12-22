import os

basedir = os.path.dirname(__file__)
basedir = os.path.join(basedir, '', 'db')

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '', 'weedly.db') # локальная sqlite

SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL', 'sqlite:///' + os.path.join(basedir, '', 'weedly.db')) # DB_URL прописан в docker-compose
#'postgresql://example:example@127.0.0.1:5432/mydatabase'
