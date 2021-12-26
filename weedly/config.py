import os

DOCKER_DB_URI = os.environ['DB_URI']
SQLALCHEMY_DATABASE_URI = os.environ['DB_URI']
# SQLALCHEMY_DATABASE_URI = "postgresql://weedly:weedly-pass@db:5432/weedly"
SQLALCHEMY_TRACK_MODIFICATIONS = False
