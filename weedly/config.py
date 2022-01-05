import os

# SQLALCHEMY_DATABASE_URI = os.environ['DB_URL']
# SQLALCHEMY_TRACK_MODIFICATIONS = False

basedir = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '', 'news.db')


