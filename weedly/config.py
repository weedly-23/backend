import os

# db settings
SQLALCHEMY_DATABASE_URI = os.environ['DB_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False


# server settings
DEBUG = bool(os.getenv('DEBUG', 'False'))
APP_PORT = int(os.getenv('APP_PORT', '5000'))
APP_HOST = os.getenv('APP_HOST', '0.0.0.0')


import logging
my_log_format = f'%(asctime)s %(name)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.WARN, format=my_log_format)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

